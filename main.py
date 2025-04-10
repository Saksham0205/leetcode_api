from fastapi import FastAPI
from app.routes import router
import os

app = FastAPI(
    title="DSA Interview API",
    description="Fetch DSA questions by company and difficulty",
    version="1.0"
)

app.include_router(router)

# For Vercel serverless function
# The handler function will be called when your serverless function is invoked
# This exports the FastAPI app as a handler that Vercel can use