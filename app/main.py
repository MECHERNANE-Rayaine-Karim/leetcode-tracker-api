from fastapi import FastAPI
from app.routers import user


app = FastAPI()
app.include_router(user.router, tags=["user"])




@app.get("/")
def read_root():
    return {"message":"LeetCode Tracker API is running"}