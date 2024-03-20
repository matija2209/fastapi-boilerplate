from app.modules.llm.llm_apis import (generate_company_description_with_llm,
                                      get_country_from_text_with_llm,
                                      get_list_of_services_with_llm,
                                      get_shippers_offered_with_llm,
                                      get_supported_platforms_with_llm,
                                      get_warehouse_locations_with_llm)


async def extract_company_country_with_llm(text):
    """
    Extract company information from the text asynchronously
    """
    response = await get_country_from_text_with_llm(text)
    return response 

async def extract_company_description_with_llm(text: str):
    """
    Generate company description asynchronously
    """
    response = await generate_company_description_with_llm(text)
    return response
