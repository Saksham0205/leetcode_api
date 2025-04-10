from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="DSA Interview API",
    description="Fetch DSA questions by company and difficulty",
    version="1.0"
)

app.include_router(router)
