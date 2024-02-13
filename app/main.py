# Standard library imports
import os

# Related third party imports
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from google.cloud import logging as google_cloud_logging
from starlette.exceptions import HTTPException as StarletteHTTPException

# Local application/library specific imports
from app.routes import recording_route, transcription_route

project_id = os.getenv('GCP_PROJECT_ID')
log_name = os.getenv('LOG_NAME')

# Set up Google Cloud Logging
client = google_cloud_logging.Client(project=project_id)
logger = client.logger(log_name)  # Replace 'your-log-name' with your log name

app = FastAPI()

# Custom exception handler for HTTPException
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.log_text(f"HTTP error occurred: {exc.detail}", severity="ERROR")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"HTTP error occurred: {exc.detail}"}
    )

# Custom exception handler for generic exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.log_text(f"Generic error occurred: {str(exc)}", severity="ERROR")
    return JSONResponse(
        status_code=500,
        content={"message": "An error occurred on the server"}
    )

@app.middleware("http")
async def log_requests_responses(request: Request, call_next):
    # Log incoming request
    logger.log_text(f"Incoming request: {request.method} {request.url}", severity="INFO")
    response = await call_next(request)
    # Optionally, you can also log the response details
    return response

# Add a test route
@app.get("/test")
async def test_route():
    return {"message": "Service is alive"}

app.include_router(recording_route.router)
app.include_router(transcription_route.router)
