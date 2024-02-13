from app.services.transcription_service import process_transcription
from app.lib.firebase import append_to_firestore_document

def handle_transcription(text: str,recordingId:str):
    good_text =  process_transcription(text,recordingId)
    append_to_firestore_document("recordings",recordingId,"cleanedText",good_text)
    return good_text