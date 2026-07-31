from fastapi import FastAPI
from .routers import posts,users,auth,votes
app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def root():
    return {"message": "Hello poorna"}







