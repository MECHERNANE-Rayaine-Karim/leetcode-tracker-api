from pydantic import BaseModel
from app.models.problem import Difficulty
from app.models.attempt import Status, Language


class StatsResponse(BaseModel):
    total_problems_solved: int
    problems_by_difficulty: dict[Difficulty, int]
    total_attempts: int
    attempts_by_status: dict[Status, int]
    attempts_by_language: dict[Language, int]
    current_streak: int
    longest_streak: int