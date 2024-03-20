import asyncio
import base64
import os
import uuid
from typing import Optional, Union

from dotenv import load_dotenv
from firebase_admin import firestore, initialize_app, storage

from app.schemas.site import PageScrape, Sitemap

load_dotenv()

if os.environ.get("ENVIRONMENT") == "development":
    print("Running in development mode. Using Firebase Emulators")
    os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
    #  IT DOESNT WORK ON PYTHON https://stackoverflow.com/questions/68088046/python-firebase-storage-emulator
    os.environ["STORAGE_EMULATOR_HOST"] = "http://127.0.0.1:9199"
    # os.environ["FIREBASE_STORAGE_EMULATOR_HOST"] = "localhost:9199"
else:
    print("Running in production mode. Using Firebase Cloud Functions")

if os.environ.get("GCP_PROJECT_ID") is None:
    raise ValueError("GCP_PROJECT_ID is not set")

if os.environ.get("GCP_STORAGE_BUCKET") is None:
    raise ValueError("GCP_STORAGE_BUCKET is not set")


app = initialize_app(options={'storageBucket': os.environ.get("GCP_STORAGE_BUCKET"),'projectId': os.environ.get("GCP_PROJECT_ID")})


def create_firestore_document(
    collection_name: str,data: Union[Sitemap, PageScrape],document_id = None) -> str:
    """
    Creates a new Firestore document in the specified collection.

    Args:
        collection_name (str): Name of the collection.
        document_id (str): The document ID for the new document.
        data (dict): The data to store in the document.

    Returns:
        str: The ID of the created document.
    """
    db = firestore.client()
    if document_id is None:
        doc_ref = db.collection(collection_name).document()
        document_id = doc_ref.id
    else:
        doc_ref = db.collection(collection_name).document(document_id)

    doc_ref.set(data)
    return document_id

def update_firestore_document(
    collection_name: str, 
    data: Union[Sitemap, PageScrape], 
    document_id: str) -> None:
    """
    Updates an existing Firestore document in the specified collection.
    If the document does not exist, it creates a new document with the provided data.

    Args:
        collection_name (str): Name of the collection.
        document_id (str): The document ID of the document to be updated.
        data (dict): The data to update in the document.

    Returns:
        None
    """
    db = firestore.client()
    doc_ref = db.collection(collection_name).document(document_id)

    # The update method will only modify the fields that are provided in 'data'.
    # If the document does not exist, it will be created with the provided data.
    doc_ref.set(data, merge=True)


def update_firestore_document_by_key(
    collection_name: str, document_id: str, key: str, value: Union[str, int, float, bool, dict, list]
) -> None:
    """
    Updates a specific key or nested key with the provided value in a Firestore document.

    For nested keys, separate each level with a dot ('.'). For example, to update the 'city' key
    inside an address object, use 'address.city' as the key.

    Args:
        collection_name (str): Name of the collection.
        document_id (str): The document ID of the document to update.
        key (str): The key or nested key to update.
        value (Union[str, int, float, bool, dict, list]): The value to set for the key.
    """
    db = firestore.Client()
    doc_ref = db.collection(collection_name).document(document_id)
    
    # Use dot notation for nested keys
    update_data = {key: value}
    doc_ref.update(update_data)

async def async_update_firestore_document_by_key(
    collection_name: str, document_id: str, key: str, value: Union[str, int, float, bool, dict, list]
):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(
        None,  # Default executor
        update_firestore_document_by_key,
        collection_name, document_id, key, value
    )

def upload_to_firebase_storage(local_file_path, recording_id):
    """
    Uploads a file to Firebase Storage.
    Args:
    - local_file_path: The path to the file on the local system.
    - recording_id: The unique identifier for the recording.
    Returns:
    - Storage URI of the uploaded file.
    """
    try:
        bucket = storage.bucket()
        remote_file_path = f"converted_recordings/{recording_id}.wav"
        blob = bucket.blob(remote_file_path)
        blob.upload_from_filename(local_file_path)

        # Make the blob publicly viewable (optional, remove if not needed)
        blob.make_public()

        # Return the public URL
        # return blob.public_url
        gcs_uri = f"gs://{bucket.name}/{blob.name}"
        return gcs_uri
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None


def append_to_firestore_document(collection_name, document_id, key, value):
    """
    Append a new key-value pair to an existing Firestore document.
    
    Args:
    - collection_name: The name of the Firestore collection.
    - document_id: The ID of the document to append data to.
    - key: The key of the new data to append.
    - value: The value of the new data to append.
    
    Returns:
    - A confirmation message or an error message.
    """
    try:
        # Get a reference to the Firestore database
        db = firestore.client()

        # Create a reference to the specific document
        doc_ref = db.collection(collection_name).document(document_id)

        # Update the document
        doc_ref.update({key: value})
        
        return f"Document {document_id} in collection {collection_name} updated successfully."
    except Exception as e:
        return f"Error updating document: {e}"

def upload_base64_to_firebase_storage(base64_image, folder_name):
    """
    Uploads a base64 encoded image to Firebase Storage in a specified folder and returns the file size along with the storage URI.
    
    Args:
    - base64_image: The base64 encoded image string.
    - folder_name: The name of the folder where the image will be stored.

    Returns:
    - A tuple containing the Storage URI of the uploaded file and the file size in bytes.
    """
    try:
        # Decode the base64 string
        encoded_image = base64_image["data_uri"].split(',')[1]

        # Adjust base64 padding if necessary
        missing_padding = len(encoded_image) % 4
        if missing_padding:
            encoded_image += '=' * (4 - missing_padding)

        # Decode the base64 string
        image_data = base64.b64decode(encoded_image)

        # Initialize Firebase Storage
        bucket = storage.bucket()

        # Generate a unique file name
        file_name = f"{uuid.uuid4()}.jpeg"  # Assuming the image is in jpeg format

        # Set the path in the storage bucket
        remote_file_path = f"{folder_name}/{file_name}"

        # Create a blob and upload the image data
        blob = bucket.blob(remote_file_path)
        blob.upload_from_string(image_data, content_type='image/jpeg')
        # Make the blob publicly viewable (optional, remove if not needed)
        blob.make_public()

        # Fetch the size of the blob/file after uploading
        blob.reload()  # Make sure to reload the blob to get the latest metadata, including size
        file_size = blob.size  # This will get the size of the file in bytes

        # Return the download URL and file size
        download_url = blob.public_url
        return download_url, file_size
    except Exception as e:
        print(f"Failed to upload to Firebase Storage: {e}")
        return None, None
