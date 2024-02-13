from firebase_admin import storage, initialize_app,firestore

initialize_app(options={'storageBucket': 'medical-practice-408309.appspot.com'})

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