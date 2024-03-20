import json

from app.lib.openai import async_generate_with_gpt
from app.lib.vertexai import generate_with_bard

COMPANY_ADDRESS_PROMPT = "Extract the country name in English from provided text" ## address (location, street, country, city, zip code, etc.)

# To get URL out.
""" 
From the provided list choose a string that most likely includes information about e-commerce fulfilment service. 

Follow these rules:
- 1) Return only string (identical to the one found)
- 2) If not 100% confident return nothing
"""

LANGUAGE_PROMPT = """
What is the language of the text? (only language in response). Output JSON

```
{
    "language": "<your to the user's question>"
}
```

"""

NAME_PROMPT = """
What is the company name?. Output JSON

```
{
    "name": "<your to the user's question>"
}
```

"""

async def find_out_name_from_scraped_data(url:str,*args)->str:
    """
    Get ouf the name of the scraped data
    """
    args_str = ', '.join(str(arg) for arg in args)
    messages = [{
        "role":"system",
        "content":NAME_PROMPT
        },
        {
            "role":"user",
            "content":f"{url} {args_str}"
            }
    ]
    # Create the formatted string
    # result_str = f"Deduct a company from the url: {url} and the following info: {args_str}"
    response = await async_generate_with_gpt(messages=messages) ## generate_with_bard(result_str)
    
    # Generate the response
    dict_loaded =  json.loads(response)
    return dict_loaded.get("name")

