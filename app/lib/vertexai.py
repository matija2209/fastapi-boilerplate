import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def generate(prompt:str, text:str):
    model = GenerativeModel("gemini-pro")
    responses = model.generate_content(
    f"{prompt} {text}",generation_config={
        "max_output_tokens": 2048,
        "temperature": 0,
        "top_p": 1
    },
    safety_settings=[],
    stream=True,
    )
    copy = []
    for response in responses:
        copy.append(response.text)
    return "".join(copy)

