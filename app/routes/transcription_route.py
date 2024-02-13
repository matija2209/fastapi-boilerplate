from fastapi import APIRouter
from app.controllers import transcription_controller
from pydantic import BaseModel

router = APIRouter()

class recordingRequest(BaseModel):
    text: str
    recordingId:str

@router.post("/transcription")
async def post_transcription(request: recordingRequest):
    return transcription_controller.handle_transcription(request.text,request.recordingId)