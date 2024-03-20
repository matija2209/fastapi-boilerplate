from fastapi import APIRouter

from app.modules.scraping import scrape_controller
from app.schemas.site import ScrapeHomepageRequest

router = APIRouter()

# Routes
@router.post("/page",tags=["Scraping"])
async def scrape_and_save_page(request: ScrapeHomepageRequest):
    try:
        """
        Scrapes the homepage for text and saves it to the database
        """
        return await scrape_controller.scrape_homepage_controller(url=request.url, tag=request.tag,pageType=request.pageType)
    except Exception as e:
        return {"error": str(e)}
        
