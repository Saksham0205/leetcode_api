import pandas as pd
import os

DATA_FOLDER = "data"

def get_all_companies():
    return [f.replace(".csv", "") for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]

def load_questions(company):
    path = os.path.join(DATA_FOLDER, f"{company}.csv")
    if not os.path.exists(path):
        return []
    df = pd.read_csv(path)
    df = df.dropna()
    return df.to_dict(orient="records")

def filter_by_difficulty(questions, difficulty):
    if not difficulty:
        return questions
    return [q for q in questions if q['Difficulty'].lower() == difficulty.lower()]
