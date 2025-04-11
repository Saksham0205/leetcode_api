from api.handler import app
from mangum import Mangum

# Create handler for AWS Lambda / Vercel
handler = Mangum(app)