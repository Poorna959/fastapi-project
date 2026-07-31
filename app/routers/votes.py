from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, oauth
from ..database import get_db
from ..schemas import Vote

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def voter(
    vote_data: Vote,
    db: Session = Depends(get_db),
    current_user=Depends(oauth.get_current_user)
):

    # Check if the post exists
    post = db.query(models.Post).filter(
        models.Post.id == vote_data.post_id
    ).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote_data.post_id} does not exist"
        )

    # Check if the vote already exists
    found_vote = db.query(models.Vote).filter(
        models.Vote.post_id == vote_data.post_id,
        models.Vote.user_id == current_user.id
    ).first()

    if vote_data.dir == 1:

        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} has already voted on post {vote_data.post_id}"
            )

        new_vote = models.Vote(
            post_id=vote_data.post_id,
            user_id=current_user.id
        )

        db.add(new_vote)
        db.commit()

        return {"message": "Successfully added vote"}

    else:

        if found_vote is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist"
            )

        db.delete(found_vote)
        db.commit()

        return {"message": "Successfully deleted vote"}