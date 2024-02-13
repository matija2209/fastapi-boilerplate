# This is where you will integrate Google's Chirp: Universal Speech Model
from google.api_core.client_options import ClientOptions
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
import requests
import io,os
from google.cloud.speech_v2.types import ExplicitDecodingConfig
import subprocess
from app.lib.firebase import upload_to_firebase_storage

region = "europe-west4"
def transcribe(url: str,recordingId:str):
    # Implement recording logic
    project_id = "medical-practice-408309"
    response = transcribe_chirp(project_id, url,recordingId)
    return response

def transcribe_chirp(
    project_id: str,
    audio_url: str,
    recordingId:str,
) -> cloud_speech.RecognizeResponse:
    """Transcribe an audio file from URL using Chirp. navigate to https://console.cloud.google.com/apis/api/speech.googleapis.com/overview?project=medical-practice-408309"""
    # Instantiates a client
    client = SpeechClient(
        client_options=ClientOptions(
            api_endpoint=f"{region}-speech.googleapis.com",
        )
    )

    input_file = download_file(audio_url,recordingId)
    output_file = convert_audio(input_file,recordingId) # This is only path to the file

    storage_uri = upload_to_firebase_storage(output_file,recordingId)

    # with io.open(output_file, "rb") as audio_file:
    #     content = audio_file.read()
    
    #  ffmpeg -i inputfile.mp3 -acodec pcm_s16le -ac 1 -ar 16000 outputfile.wav

    file_metadata = cloud_speech.BatchRecognizeFileMetadata(uri=storage_uri)

    explicit_decoding_config = ExplicitDecodingConfig(
        encoding="LINEAR16",  # The audio file is now in LINEAR16 encoding
        sample_rate_hertz=16000,  # The sample rate has been set to 16000 Hz
        audio_channel_count=1  # The audio file has been converted to mono
    )

    config = cloud_speech.RecognitionConfig(
        explicit_decoding_config=explicit_decoding_config,
        language_codes=["sl-SI"],
        model="chirp",

    )

    request = cloud_speech.BatchRecognizeRequest(
        recognizer=f"projects/{project_id}/locations/{region}/recognizers/_",
        config=config,
        files=[file_metadata],
        recognition_output_config=cloud_speech.RecognitionOutputConfig(
            inline_response_config=cloud_speech.InlineOutputConfig(),
        ),
    )

    # Transcribes the audio into text
    operation = client.batch_recognize(request=request)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=120)
    copy = []
    for result in response.results[storage_uri].transcript.results:
        copy.append(result.alternatives[0].transcript)
    full_transcript = ' '.join(copy)
    return full_transcript




def download_file(url: str,recordingId: str):
    response = requests.get(url)
    if response.status_code == 200:
        content_type = response.headers['Content-Type']
        ext = 'mp3' if 'mpeg' in content_type else 'm4a'
        file_path = f"recordings/temp-{recordingId}.{ext}"
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return file_path
    else:
        raise Exception("Failed to download file")

def convert_audio(input_path: str,recordingId: str):
    output_path = f"recordings/converted-{recordingId}.wav"
    command = [
        'ffmpeg',
        '-y',  # overwrite output file if it exists
        '-i', input_path, 
        '-acodec', 'pcm_s16le', 
        '-ac', '1', 
        '-ar', '16000', 
        output_path
    ]
    subprocess.run(command, check=True)
    os.remove(input_path)  # Remove the temporary file
    return output_path
