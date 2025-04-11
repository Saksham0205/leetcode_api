from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from app.utils import get_all_companies, load_questions, filter_by_difficulty
from app.models import Question
import logging

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/companies", tags=["Companies"])
def list_companies():
    companies = get_all_companies()
    logger.info(f"Returning {len(companies)} companies")
    return {"companies": companies}


@router.get("/questions", response_model=List[Question], tags=["Questions"])
async def get_questions(company: str, difficulty: Optional[str] = None):
    logger.info(f"Fetching questions for company: {company}, difficulty: {difficulty}")

    if company not in get_all_companies():
        logger.error(f"Company not found: {company}")
        raise HTTPException(status_code=404, detail=f"Company '{company}' not found")

    all_questions = load_questions(company)

    if not all_questions:
        logger.warning(f"No questions found for company: {company}")
        return []

    filtered = filter_by_difficulty(all_questions, difficulty)

    logger.info(f"Returning {len(filtered)} questions")
    return filtered


@router.get("/questions/all", response_model=List[Question], tags=["Questions"])
async def get_all_questions():
    logger.info("Fetching all questions")
    all_data = []
    for company in get_all_companies():
        company_questions = load_questions(company)
        all_data.extend(company_questions)
        logger.info(f"Added {len(company_questions)} questions from {company}")

    logger.info(f"Returning {len(all_data)} total questions")
    return all_data