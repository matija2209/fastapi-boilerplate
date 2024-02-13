# Audio Transcription Service

## Overview
This project is an audio transcription service built using FastAPI. It integrates Google Cloud Logging and Firestore for logging and data storage. The service allows users to post audio recordings and transcriptions, which are then processed and stored.

## Features
- FastAPI for efficient asynchronous handling of requests.
- Google Cloud Logging for detailed logging of requests and errors.
- Firestore for storing transcribed and processed text.
- Endpoints for posting audio recordings and transcriptions.

## Installation
To set up the project, follow these steps:

1. Clone the repository:
2. Install dependencies:
3. Set up Google Cloud credentials:
- Ensure you have a Google Cloud account and access to Firestore and Logging.
- Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to your Google Cloud credentials JSON file.
- Use gcloud init to authenticate with your Google Cloud account.


## Usage
Start the FastAPI server:

The service will be available at `http://127.0.0.1:8000`.

## API Endpoints
### Test Route
- `GET /test`: Check if the service is alive.

### Recording Routes
- `POST /recording`: Post an audio recording.
   - Body: `{ "url": "audio_url", "recordingId": "id" }`
- `POST /transcription`: Post a transcription.
   - Body: `{ "text": "transcribed_text", "recordingId": "id" }`

## Error Handling
Custom exception handlers are implemented for HTTP and generic exceptions, ensuring informative error messages are logged and returned to the user.

## Logging
All incoming requests and errors are logged using Google Cloud Logging for monitoring and debugging purposes.

# Useful commands
pip freeze > requirements.txt

## Craete files quickly
`touch app/__init__.py app/main.py app/routes/recording_route.py app/controllers/recording_controller.py app/services/recording_service.py`

`touch app/__init__.py app/main.py app/routes/transcription_route.py app/controllers/transcription_controller.py app/services/transcrip`tion_service.py`

`uvicorn main:app --reload`

## Virtual Env

### Create VENV
- `python3 -m virtualenv venv`
- `source venv/bin/activate`

## Docker stuff
### Mac OS
- `pip freeze > requirements.txt`
- `pip install -r requirements.txt`

### Windows 
- `pip freeze > requirements.txt`
- `pip install -r requirements.txt`
- `python -m venv venv`
- `venv\Scripts\activate`


### Upload account
`scp /Users/ziberna/ServiceAccounts/serviceAccount.json  matija@xx.xx.xx.xxx:/home/matija/serviceAccounts`

## Docker

- Build image `sudo docker-compose build --no-cache`
- OR `docker build --platform linux/amd64 -t audio-transcriber-service .`
- Push to Hub `sudo docker-compose push`
— `sudo docker-compose build && sudo docker-compose push`
- Docker pull
  `sudo docker pull matija2209/dockerized-service`
- Run container `sudo docker run -v /home/matija/serviceAccounts/serviceAccount.json:/app/key.json -e GOOGLE_APPLICATION_CREDENTIALS=/app/key.json -d -p 4853:80 matija2209/dockerized-service`

_Make sure to create env file to include all variables needed for this microservice to run._

_ENVs_:

## Host

Server should run on `https://audio-transcriber-service.we-hate-copy-pasting.com/`

Nging config file:

```
server {
        server_name audio-transcriber-service.we-hate-copy-pasting.com;
        location / {
            proxy_pass         http://localhost:6543/;
            proxy_redirect     off;

            proxy_set_header   Host             $host;
            proxy_set_header   X-Real-IP        $remote_addr;
            proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
        }


    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/audio-transcriber-service.we-hate-copy-pasting.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/audio-transcriber-service.we-hate-copy-pasting.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}
```

Generated cert with:
`sudo certbot --nginx -d audio-transcriber-service.we-hate-copy-pasting.com`
