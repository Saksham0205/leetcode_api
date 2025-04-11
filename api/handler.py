from fastapi import FastAPI
from app.routes import router

# Initialize FastAPI app
app = FastAPI(
    title="DSA Interview API",
    description="Fetch DSA questions by company and difficulty",
    version="1.0"
)

# Include routes
app.include_router(router)