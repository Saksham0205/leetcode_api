import pandas as pd
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_FOLDER = "data"


def get_all_companies():
    companies = [f.replace(".csv", "") for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]
    logger.info(f"Found companies: {companies}")
    return companies


def load_questions(company):
    path = os.path.join(DATA_FOLDER, f"{company}.csv")
    if not os.path.exists(path):
        logger.error(f"CSV file not found: {path}")
        return []

    try:
        logger.info(f"Loading questions from: {path}")
        df = pd.read_csv(path)
        df = df.dropna()

        # Print the actual columns in the CSV for debugging
        logger.info(f"CSV columns: {df.columns.tolist()}")

        # Create a mapping of CSV column names to model field names
        column_mapping = {
            'Difficulty': 'difficulty',
            'Title': 'title',
            'Frequency': 'frequency',
            'Acceptance Rate': 'acceptance_rate',
            'Link': 'link',
            'Topics': 'topics'
        }

        # Rename columns to match the model fields
        df = df.rename(columns=column_mapping)

        # Verify all required columns are present
        required_fields = ['difficulty', 'title', 'frequency', 'acceptance_rate', 'link', 'topics']
        for field in required_fields:
            if field not in df.columns:
                logger.error(f"Missing required field in CSV: {field}")

        # Convert to records - list of dictionaries
        records = df.to_dict(orient="records")

        logger.info(f"Loaded {len(records)} questions for {company}")
        return records
    except Exception as e:
        logger.error(f"Error loading questions for {company}: {str(e)}")
        return []


def filter_by_difficulty(questions, difficulty):
    if not difficulty:
        return questions
    filtered = [q for q in questions if q['difficulty'].lower() == difficulty.lower()]
    logger.info(f"Filtered {len(questions)} questions to {len(filtered)} by difficulty: {difficulty}")
    return filtered