import pandas as pd
import os

DATA_FOLDER = "data"


def get_all_companies():
    return [f.replace(".csv", "") for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]


def load_questions(company):
    path = os.path.join(DATA_FOLDER, f"{company}.csv")
    if not os.path.exists(path):
        return []

    try:
        df = pd.read_csv(path)
        df = df.dropna()

        # Create a mapping of CSV column names to model field names
        column_mapping = {
            'Difficulty': 'difficulty',
            'Title': 'title',
            'Frequency': 'frequency',
            'Acceptance Rate': 'acceptance_rate',
            # This is the key fix - mapping "Acceptance Rate" to "acceptance_rate"
            'Link': 'link',
            'Topics': 'topics'
        }

        # Rename columns to match the model fields
        df = df.rename(columns=column_mapping)

        # Convert to records - list of dictionaries
        records = df.to_dict(orient="records")

        return records
    except Exception as e:
        print(f"Error loading questions for {company}: {str(e)}")
        return []


def filter_by_difficulty(questions, difficulty):
    if not difficulty:
        return questions
    return [q for q in questions if q['difficulty'].lower() == difficulty.lower()]