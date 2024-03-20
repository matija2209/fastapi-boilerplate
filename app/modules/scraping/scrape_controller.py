from fastapi.responses import JSONResponse

from app.lib.urlparse import get_base_url, get_domain, get_url_path
from app.lib.usp import get_sitemap_urls
from app.modules.scraping.scrape_db import save_sitemap
from app.modules.scraping.scrape_helpers import find_relevant_urls
from app.modules.scraping.scrape_service import process_and_store_homepage


async def scrape_homepage_controller(url: str,tag:str,pageType:str):
    """
    Function to scrape the homepage of a website.
    """
    document_id,company_name,removed_trailing_slash = await process_and_store_homepage(url,tag,pageType)
    return JSONResponse(dict(document_id=document_id,company_name=company_name,url=removed_trailing_slash), status_code=200)

