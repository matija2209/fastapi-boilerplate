import asyncio
import json
import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
from typing import List

from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content:str


OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

client = OpenAI(
    # This is the default and can be omitted
    api_key=OPENAI_API_KEY,
)

# https://github.com/openai/openai-python/blob/main/api.md
def generate_with_gpt(messages:List[Message],tools, max_token=512) -> str:
    """
    Ask GPT to generate a response
    """
    try:
        model = "gpt-3.5-turbo-0125"

        chat_completion = client.chat.completions.create(
            messages=messages,
            response_format={ "type": "json_object" },
            model=model,
            max_tokens=max_token,
            # tools=tools if tools else None
        )
        if chat_completion.choices[0].finish_reason == "length":
            raise Exception("not enough token to finish this JSON")
        message_response = chat_completion.choices[0].message.content
        return message_response
        #  response.choices[0].finish_reason == “length”,
        # https://pub.towardsai.net/openai-json-mode-vs-functions-92b15baa38d9
    except Exception as e:
        # Manage the error 
        # Add logging
        # TODO: What is this
        raise e

async def async_generate_with_gpt(messages: List[Message], max_token=256,tools=None) -> str:
    """
    Asynchronously ask GPT to generate a response
    """
    loop = asyncio.get_running_loop()
    # Run the synchronous function in a thread pool
    response = await loop.run_in_executor(
        None,  # Uses the default executor
        generate_with_gpt, messages, tools,max_token
    )
    return response