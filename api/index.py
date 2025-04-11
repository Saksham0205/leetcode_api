# api/index.py
import os
import sys
import logging
from fastapi import FastAPI
from mangum import Mangum

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import routes
try:
    from app.routes import router
    logger.info("Successfully imported app.routes")
except ImportError as e:
    logger.error(f"Failed to import app.routes: {str(e)}")
    raise

# Initialize FastAPI app
app = FastAPI(
    title="DSA Interview API",
    description="Fetch DSA questions by company and difficulty",
    version="1.0"
)

# Include routes
app.include_router(router)
logger.info("Routes included in FastAPI app")

# Initialize Mangum handler
try:
    mangum_handler = Mangum(app, lifespan="auto")
    logger.info("Mangum handler initialized")
except Exception as e:
    logger.error(f"Failed to initialize Mangum handler: {str(e)}")
    raise

# Explicit Lambda handler
def handler(event, context):
    logger.info(f"Lambda handler invoked with event: {event}")
    try:
        response = mangum_handler(event, context)
        logger.info(f"Lambda handler response: {response}")
        return response
    except Exception as e:
        logger.error(f"Lambda handler error: {str(e)}")
        return {
            "statusCode": 500,
            "body": f"Internal server error: {str(e)}",
            "headers": {
                "Content-Type": "text/plain",
                "Access-Control-Allow-Origin": "*"
            }
        }