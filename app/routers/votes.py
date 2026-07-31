from fastapi import FastAPI,Depends,HTTPException,status,APIRouter
from ..database import cursor,conn
from ..schemas import Vote
from .. import oauth

router = APIRouter(prefix="/vote",tags=['Vote'])

@router.post("/",status_code=status.HTTP_201_CREATED)
def voter(vote_data:Vote,current_user=Depends(oauth.get_current_user)):
    
    cursor.execute(""" SELECT * FROM posts WHERE id= %s """,(str(vote_data.post_id),))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {vote_data.post_id} does not exist")
    
    cursor.execute("""SELECT * FROM votes WHERE post_id= %s AND user_id= %s """,(str(vote_data.post_id),str(current_user['id'])))
    found_vote = cursor.fetchone()
    if vote_data.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user['id']} has alerdy voted on post {vote_data.post_id}")
        cursor.execute(""" INSERT INTO votes (post_id,user_id) VALUES (%s,%s)""",(str(vote_data.post_id),str(current_user['id'])))
        conn.commit()
        return {"message":"successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exist")
        cursor.execute("""DELETE FROM votes WHERE post_id=%s AND user_id=%s""",(str(vote_data.post_id),str(current_user['id'])))
        conn.commit()
        return {"message":"successfully deleted vote"}

        
