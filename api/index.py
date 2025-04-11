# api/index.py
from fastapi import FastAPI
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import your modules
from app.routes import router

app = FastAPI(
    title="DSA Interview API",
    description="Fetch DSA questions by company and difficulty",
    version="1.0"
)

app.include_router(router)

# This is how Vercel expects the handler
def handler(request, context):
    return app(request, context)