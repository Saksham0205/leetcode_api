from pydantic import BaseModel
from typing import List

class Question(BaseModel):
    title: str
    difficulty: str
    frequency: float
    acceptance_rate: float
    link: str
    topics: str