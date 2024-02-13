from fastapi import APIRouter
from app.controllers import recording_controller
from pydantic import BaseModel

router = APIRouter()

class RecordingRequest(BaseModel):
    url: str
    recordingId:str

@router.post("/recording")
async def post_recording(request: RecordingRequest):
    return recording_controller.handle_recording(request.url,request.recordingId)