from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from .. import models, oauth
from ..database import get_db
from ..schemas import Post, PostCreate

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)
@router.get("/")
def get_posts(
    current_user=Depends(oauth.get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):

    posts = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes")
        )
        .join(models.User, models.Post.user_id == models.User.id)
        .outerjoin(models.Vote, models.Post.id == models.Vote.post_id)
        .filter(models.Post.title.ilike(f"%{search}%"))
        .group_by(models.Post.id, models.User.id)
        .limit(limit)
        .offset(skip)
        .all()
    )

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(
    payload: PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth.get_current_user)
):

    new_post = models.Post(
        user_id=current_user.id,
        **payload.model_dump()
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}")
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth.get_current_user)
):

    post = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes")
        )
        .outerjoin(models.Vote, models.Post.id == models.Vote.post_id)
        .filter(models.Post.id == id)
        .group_by(models.Post.id)
        .first()
    )

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )

    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth.get_current_user)
):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist"
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )

    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=Post)
def update_post(
    id: int,
    payload: PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth.get_current_user)
):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist"
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )

    post_query.update(payload.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()