from .. import models,utils
from fastapi import Response,status,HTTPException,Depends,APIRouter
from ..schemas import UsersCreate,UsersOut,Users

from psycopg2.extras import RealDictCursor
from ..database import conn,cursor

router = APIRouter(prefix="/users",tags=['Users']) 

# get a users data
@router.get("/",response_model=list[Users])
def get_posts():
    cursor.execute("""SELECT * FROM users""")
    users = cursor.fetchall()
    return users

# get a single user data
@router.get("/{id}",response_model=Users)
def get_post(id: int):
    cursor.execute(f""" SELECT * FROM users WHERE id= %s """,(str(id),))
    user=cursor.fetchone()
    if  not user:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
    return user

# create a user
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=UsersOut)
def create_user(user:UsersCreate):
    hash_password=utils.hash(user.password)
    
    cursor.execute("""INSERT INTO USERS (email,password) VALUES (%s,%s) RETURNING  * """,(user.email,hash_password))
    new_user=cursor.fetchone()
    conn.commit()
    return new_user

# delete a user
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(f""" DELETE FROM users WHERE id= {id} RETURNING * """)
    deleted_user=cursor.fetchone()
    conn.commit()

    if not deleted_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update the user data
@router.put("/{id}",response_model=Users)     
def update_posts(id:int,user:Users):
    cursor.execute(f"""UPDATE users SET email=%s,password=%s WHERE id={id} RETURNING * """,(user.email,user.password))
    updated_user=cursor.fetchone()
    conn.commit()
    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    
    return updated_user