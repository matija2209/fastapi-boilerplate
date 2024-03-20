from typing import Union

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.modules.llm.llm_controller import (process_country_for_ecf)

router = APIRouter()

# Determine waht type of request we weant, comapny address or list of serivces

@router.post("/extract_country",tags=["LLM"])
async def handle_country_llm_request(request):
    if request.page_type == "ecf":
        return await process_country_for_ecf(request)
    elif request.page_type == "mf":
        # Handle mf case
        pass
    else:
        raise HTTPException(status_code=400, detail="Invalid page_type")

