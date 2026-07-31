from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, utils
from ..database import get_db
from ..schemas import UsersCreate, UsersOut

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
@router.get("/", response_model=list[UsersOut])
def get_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return users

@router.get("/{id}", response_model=UsersOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} was not found"
        )

    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UsersOut)
def create_user(
    user: UsersCreate,
    db: Session = Depends(get_db)
):

    hashed_password = utils.hash(user.password)

    user.password = hashed_password

    new_user = models.User(**user.model_dump())

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: int,
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(models.User.id == id)

    found_user = user.first()

    if found_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist"
        )

    user.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=UsersOut)
def update_user(
    id: int,
    user: UsersCreate,
    db: Session = Depends(get_db)
):

    user_query = db.query(models.User).filter(models.User.id == id)

    db_user = user_query.first()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist"
        )

    user.password = utils.hash(user.password)

    user_query.update(user.model_dump(), synchronize_session=False)

    db.commit()

    return user_query.first()