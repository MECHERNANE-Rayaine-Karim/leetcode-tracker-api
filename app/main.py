from fastapi import FastAPI
from app.routers import user, problem

app = FastAPI()
app.include_router(user.router, tags=["user"])
app.include_router(problem.router, tags=["problem"])



@app.get("/")
def read_root():
    return {"message":"LeetCode Tracker API is running"}