from fastapi import FastAPI
from app.routers import user, problem, attempt, topic, stats, note
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user.router, tags=["user"])
app.include_router(problem.router, tags=["problem"])
app.include_router(attempt.router, tags=["attempt"])
app.include_router(topic.router, tags=["topic"])
app.include_router(stats.router, tags=["stats"])
app.include_router(note.router, tags=["note"])

@app.get("/")
def read_root():
    return {"message":"LeetCode Tracker API is running"}