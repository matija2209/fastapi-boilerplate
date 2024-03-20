import os

# import vertexai
# from google.cloud import aiplatform
# from vertexai.generative_models import GenerativeModel, Part
from vertexai.preview.generative_models import GenerativeModel

GCP_PROJECT_ID=os.environ.get("GCP_PROJECT_ID")
GCP_LOCATION=os.environ.get("GCP_LOCATION")

# https://cloud.google.com/vertex-ai/docs/generative-ai/start/quickstarts/quickstart-multimodal
# https://gemini.google.com/app/91688c92f95b27d5
def generate_with_bard(prompt:str, text=None,tokens=256)->str:
    try:
        # vertexai.init(project=GCP_PROJECT_ID, location=GCP_LOCATION)
           # Load the model
        gemini_pro_model = GenerativeModel("gemini-1.0-pro")

        # Query the model
        contents = f"{prompt}{text if text is not None else ''}"
        if not contents.strip():
            raise ValueError("Content is empty or invalid")
        model_response = gemini_pro_model.generate_content(contents)

        # response = multimodal_model.generate_content(
        #     stream=False,
        #     generation_config={
        #          "temperature": 0.0,
        #     },
        #     contents=contents
        # )
        if model_response.candidates and model_response.candidates[0].content.parts:
            return model_response.candidates[0].content.parts[0].text
        else:
            return ""  # Return empty string if the response does not contain valid text
    except Exception as e:
        raise Exception("Gemini has failed to generate text",e) from e

