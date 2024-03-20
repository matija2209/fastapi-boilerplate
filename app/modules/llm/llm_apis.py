import json

from app.lib.openai import async_generate_with_gpt
from app.lib.vertexai import generate_with_bard

LIST_OF_SERVICES_PROMPT =  """Extract the list of services offered by the e-commerce fullfillment company from provided text. Return none if cannot be found. Translate to English. Output this JSON format:
```
{
    "listOfServices": "<your to the user's question>"
}
```
"""

LIST_OF_WAREHOUSE_LOCATIONS_PROMPT =  """You are provided a text of a e-commerce fullfilmennt company. Try to extract list of locations of their warehouses or logistics sites. If none return none. Output this JSON format:
```
{
    "warehouseLocations": "<your to the user's question>"
}
```
"""

LIST_OF_PLATFORMS_PROMPT =  """Extract a list of supported platforms the company integrates with If none return none. Output this JSON format:
```
{
    "supportedPlatforms": "<your to the user's question>"
} 
```
"""

LIST_OF_SHIPPERS = """You are provided a text of an e-commerce fulfillment company. Try to extract a list of shippers they work with. If none, return 'none'.
 Output this JSON format:
```
{
    "shippers": "<your to the user's question>"
} 
```

"""

COMPANY_DESCRIPTION_PROMPT = """Write succint maximum 300 characters long, and accurate company description without repeating yourself based on the provided text Output this JSON format:.
```
{
    "shortDescription": "<your to the user's question>"
} 
```
"""


COUNTRY_PROMPT = """In what country is this company located in based on the provided text. Output this JSON format:
```
    {
        "country": "<your to the user's question>"
    } 
```
"""

async def get_list_of_services_with_llm(text:str)->str:
    # TODO: I need to get JSON back, define what data-points do we want to collect, about us, company name, email, phone, services
    response = await async_generate_with_gpt(messages=[
        {
            "role":"system","content":LIST_OF_SERVICES_PROMPT
        },
        {
            "role":"user","content":text},
    ])
    loaded_dict = json.loads(response)

    return loaded_dict
