
from fastapi import Response,status,HTTPException,APIRouter,Depends
from ..schemas import Post,PostCreate
from ..database import conn,cursor
from typing import Optional
from .. import oauth
router = APIRouter(prefix="/posts",tags=['Posts'])



# @router.get("/", response_model=list[Post])
@router.get("/")
def get_posts(
    current_user=Depends(oauth.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    # cursor.execute(
    #     """
    #     SELECT * FROM posts
    #     WHERE title ILIKE %s
    #     ORDER BY id
    #     LIMIT %s
    #     OFFSET %s
    #     """,
    #     (f"%{search}%", limit, skip)
    # )
    cursor.execute("""SELECT posts.*, users.email, COUNT(votes.post_id) AS votes
FROM posts
JOIN users
    ON posts.user_id = users.id
LEFT JOIN votes
    ON posts.id = votes.post_id
WHERE posts.title ILIKE %s
GROUP BY posts.id, users.id
ORDER BY posts.id
LIMIT %s
OFFSET %s;""", (f"%{search}%", limit, skip))
    posts = cursor.fetchall()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=PostCreate)
def create_post(payload: PostCreate,current_user=Depends(oauth.get_current_user)):
    cursor.execute(""" INSERT INTO POSTS (title,content,published,user_id) VALUES (%s,%s,%s,%s) RETURNING  * """,(payload.title,payload.content,payload.published,str(current_user['id'])))
    new_posts=cursor.fetchone()
    conn.commit()
    return new_posts

# @router.get("/{id}",response_model=Post)
@router.get("/{id}")
def get_post(id: int,current_user=Depends(oauth.get_current_user)):
    cursor.execute( """
        SELECT posts.*, COUNT(votes.post_id) AS votes
        FROM posts
        LEFT JOIN votes
            ON posts.id = votes.post_id
        WHERE posts.id = %s
        GROUP BY posts.id
        """,
        (id,))
    post=cursor.fetchone()
    if  not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT,)
def delete_post(id: int,current_user=Depends(oauth.get_current_user)):
    cursor.execute( """
        SELECT posts.*, COUNT(votes.post_id) AS votes
        FROM posts
        LEFT JOIN votes
            ON posts.id = votes.post_id
        WHERE posts.id = %s
        GROUP BY posts.id
        """,
        (id,))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    if post['user_id']!=current_user['id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised to performe the action")
    cursor.execute(""" DELETE FROM posts WHERE id=%s """,(str(id),))
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}",response_model=Post)     
def update_posts(id:int,post:PostCreate,current_user=Depends(oauth.get_current_user)):
    cursor.execute(f""" SELECT * FROM posts WHERE id= %s  """,(str(id),))
    user_data=cursor.fetchone()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    if user_data['user_id']!=current_user['id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised to performe the action")

    cursor.execute("""UPDATE posts SET title = %s,content=%s,published = %s RETURNING * """,(post.title,post.content,post.published,))
    updated_post=cursor.fetchone()
    conn.commit()
    return updated_post