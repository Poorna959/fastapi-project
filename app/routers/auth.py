from fastapi import APIRouter,HTTPException,status,Depends,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..schemas import Userlogin,Token
from ..database import cursor
from ..utils import verify
from ..oauth import create_access_token

router = APIRouter(tags=['Authentication'])


@router.post("/login",response_model=Token)
def login(user: OAuth2PasswordRequestForm = Depends()):
    cursor.execute(
        "SELECT * FROM users WHERE email = %s", 
        (user.username,)
    )
    data = cursor.fetchone()
    
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
        
    if not verify(user.password, data.get('password')):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
        
    
    access_token = create_access_token(data={'user_id': data.get('id')})
    
    
    return {
    "access_token": access_token,
    "token_type": "bearer"
    }


