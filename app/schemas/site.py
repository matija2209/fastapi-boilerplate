from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, HttpUrl


class ScrapeHomepageRequest(BaseModel):
    url: str
    tag:str
    pageType:str

class SitemapRequest(BaseModel):
    url: str

class SiteDocument(BaseModel):
    domain: str
    url: HttpUrl
    companyName: str
    aboutInfo: str
    otherInfo: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    services: List[str]
