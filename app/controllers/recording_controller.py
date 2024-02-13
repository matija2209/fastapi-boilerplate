from app.services import recording_service
from app.lib.firebase import append_to_firestore_document

def handle_recording(url: str,recordingId:str):
    """
    It downloads the audio file from the URL, transcribes it, and returns the transcribed text
In the mean time it converts and save transribed text to firestore
    :param url: The URL of the audio file to be transcribed
    :type url: str
    :param recordingId: The id of the recording
    :type recordingId: str
    """
    # Implement logic to handle the URL and interact with the service
    transcribedText = recording_service.transcribe(url,recordingId)
    append_to_firestore_document("recordings",recordingId,"transcribedText",transcribedText)
    return transcribedText
