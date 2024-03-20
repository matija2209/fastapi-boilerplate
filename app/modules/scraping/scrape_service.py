
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup

from app.lib.phonenumbers import extract_phone_numbers
from app.lib.requests import process_logo
from app.lib.soup import (extract_contact_links, extract_emails,
                          extract_favicon, extract_headings,
                          extract_images_and_alts, extract_internal_links,
                          extract_schema_data, extract_seo_tags,
                          extract_social_media_links)
from app.lib.urlparse import get_base_url, get_domain
from app.modules.scraping import scrape_apis, scrape_db
from app.modules.scraping.scrape_helpers import (
    determine_country_from_domain, download_and_process_images_concurrently,
    structure_webpage_data)
from app.schemas.site import WebPageData


async def process_and_store_homepage(url: str, tag: str, pageType: str):
    removed_trailing_slash = url.rstrip('/')
    domain = get_domain(url)
    page_data = scrape_page(removed_trailing_slash)
    # TODO: This needs to be migrated to LLM module
    company_name = await scrape_apis.find_out_name_from_scraped_data(url,page_data.get("title") if page_data else None)
    # TODO: This needs to be migrated to LLM module
    language = await scrape_apis.determine_language(page_data.get("cleaned_text")[:100])
    images = scrape_db.saved_images_in_storage(page_data.get("images_downloaded"),domain)
    data = structure_webpage_data(page_data,company_name,language,images)
    
    document_id = scrape_db.save_page(removed_trailing_slash, data,
        tag=tag,
        slug=company_name.replace(" ","-").lower(),
        pageType=pageType,
        domain=domain
    )
    
    return document_id,company_name,removed_trailing_slash
