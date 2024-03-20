from typing import List, Optional

from fastapi.responses import JSONResponse

from app.lib.firebase import (append_to_firestore_document,
                              async_update_firestore_document_by_key)
from app.modules.llm.llm_dbs import (
    save_company_short_description_to_ecf_document,
    save_country_to_ecf_document, save_list_of_services_to_ecf_document)
from app.modules.llm.llm_service import (extract_company_country_with_llm,
                                         extract_company_description_with_llm,
                                         extract_list_of_services_with_llm,
                                         extract_shippers_offered_with_llm,
                                         extract_supported_platforms_with_llm,
                                         extract_warehouse_locations_llm)
from app.schemas.site import HomepageLLM


async def process_country_for_ecf(data: HomepageLLM):
    """
    Extract information from text asynchronously.
    """
    response = await extract_company_country_with_llm(data.text)
    return JSONResponse(content=response, status_code=200)
