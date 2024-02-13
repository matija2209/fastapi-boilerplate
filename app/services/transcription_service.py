from app.lib.vertexai import generate

def process_transcription(text: str,recordingId:str):
    prompt = "Slovnično popravi naslednji tekst."
    fixed = generate(prompt,text)
    return fixed