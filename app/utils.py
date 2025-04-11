import pandas as pd
import os
import logging
from functools import lru_cache

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define data folder relative to current file
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "data")

@lru_cache(maxsize=100)
def get_all_companies():
    try:
        logger.debug(f"Accessing DATA_FOLDER: {DATA_FOLDER}")
        if not os.path.exists(DATA_FOLDER):
            logger.error(f"Data folder not found: {DATA_FOLDER}")
            return []
        files = os.listdir(DATA_FOLDER)
        companies = [f.replace(".csv", "") for f in files if f.endswith(".csv")]
        logger.debug(f"Found companies: {companies}")
        return companies
    except Exception as e:
        logger.error(f"Error listing companies: {str(e)}")
        return []

@lru_cache(maxsize=100)
def load_questions(company):
    try:
        path = os.path.join(DATA_FOLDER, f"{company}.csv")
        logger.debug(f"Loading CSV from: {path}")
        if not os.path.exists(path):
            logger.error(f"CSV file not found: {path}")
            return []

        df = pd.read_csv(path)
        df = df.dropna()

        # Define expected columns
        required_columns = ['Difficulty', 'Title', 'Frequency', 'Acceptance Rate', 'Link', 'Topics']
        if not all(col in df.columns for col in required_columns):
            missing = [col for col in required_columns if col not in df.columns]
            logger.error(f"Missing columns in {path}: {missing}")
            return []

        # Map CSV columns to model fields
        column_mapping = {
            'Difficulty': 'difficulty',
            'Title': 'title',
            'Frequency': 'frequency',
            'Acceptance Rate': 'acceptance_rate',
            'Link': 'link',
            'Topics': 'topics'
        }
        df = df.rename(columns=column_mapping)
        records = df.to_dict(orient="records")
        logger.info(f"Loaded {len(records)} questions for {company}")
        return records
    except Exception as e:
        logger.error(f"Error loading questions for {company}: {str(e)}")
        return []

def filter_by_difficulty(questions, difficulty):
    try:
        if not difficulty:
            return questions
        filtered = [q for q in questions if q['difficulty'].lower() == difficulty.lower()]
        logger.info(f"Filtered {len(questions)} questions to {len(filtered)} by difficulty: {difficulty}")
        return filtered
    except Exception as e:
        logger.error(f"Error filtering questions: {str(e)}")
        return []