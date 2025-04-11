from api.handler import app
from mangum import Mangum

# Create handler for AWS Lambda / Vercel
handler = Mangum(app, lifespan="off")

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)