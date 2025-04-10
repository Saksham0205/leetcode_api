from fastapi import APIRouter, Query
from typing import Optional
from app.utils import get_all_companies, load_questions, filter_by_difficulty
from app.models import Question

router = APIRouter()

@router.get("/companies", tags=["Companies"])
def list_companies():
    return {"companies": get_all_companies()}

@router.get("/questions", response_model=list[Question], tags=["Questions"])
def get_questions(company: str, difficulty: Optional[str] = Query(None)):
    all_questions = load_questions(company)
    filtered = filter_by_difficulty(all_questions, difficulty)
    return filtered

@router.get("/questions/all", response_model=list[Question], tags=["Questions"])
def get_all_questions():
    all_data = []
    for company in get_all_companies():
        all_data.extend(load_questions(company))
    return all_data
