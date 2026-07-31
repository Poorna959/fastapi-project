from jose import JWTError,jwt
from datetime import datetime,timedelta
from fastapi import HTTPException,status,Depends
from .schemas import TokenData
from typing import Dict
from fastapi.security import OAuth2PasswordBearer
from .database import cursor

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')
def create_access_token(data: dict):
    to_encode = data.copy()

    expire= datetime.utcnow()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp":expire
    })
    encoded_jwt= jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credential_exeptions):
    try:
        pay_load =  jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id =pay_load.get('user_id')
        if id is None:
            raise credential_exeptions
        token_data= TokenData(id=id)
    except JWTError:
        raise credential_exeptions
    return token_data

def get_current_user(token:str=Depends(oauth2_scheme)):
    credential_exeptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"})
    curr_token = verify_access_token(token,credential_exeptions=credential_exeptions)
    cursor.execute("""SELECT * FROM users WHERE id=%s""",(str(curr_token.id),))
    user = cursor.fetchone()
    return user


  