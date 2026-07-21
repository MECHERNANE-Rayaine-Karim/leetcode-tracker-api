from fastapi import FastAPI
from app.routers import user, problem, attempt, topic

app = FastAPI()
app.include_router(user.router, tags=["user"])
app.include_router(problem.router, tags=["problem"])
app.include_router(attempt.router, tags=["attempt"])
app.include_router(topic.router, tags=["topic"])


@app.get("/")
def read_root():
    return {"message":"LeetCode Tracker API is running"}