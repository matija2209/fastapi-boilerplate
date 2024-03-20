

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
from urllib.parse import urlparse

from app.lib.urlparse import get_url_path
from app.schemas.site import PageInfo
from app.utils.image_utils import download_and_process_image

list_of_irrelevant_urls = ['ecommerce', 'e-commerce', 'b2c', 'fulfillment', 'fulfilment', "shopify", "woocommerce", "magento", "prestashop", "bigcommerce", "webshop", "amazon", "ebay", "fba"]

def find_relevant_urls(links: List[str])->List[PageInfo]:
    """
    Find URLs that contain relevant keywords
    """
    matching_keywords = list_of_irrelevant_urls
    found_match = []

    for link in links:
        url = link.lower()
        parsed_url = urlparse(url)
        path = parsed_url.path

        for kw in matching_keywords:
            if kw.lower() in path:
                found_match.append({"keyword": kw, "url": get_url_path(url)})
                break
    return found_match


def determine_country_from_domain(domain: str):
    """
    Determine the country from the domain
    """
    country = lambda domain: {"al": "albania", "ad": "andorra", "am": "armenia", "at": "austria", "by": "belarus", "be": "belgium", "ba": "bosnia and herzegovina", "bg": "bulgaria", "hr": "croatia", "cy": "cyprus", "cz": "czech republic", "dk": "denmark", "ee": "estonia", "fi": "finland", "fr": "france", "ge": "georgia", "de": "germany", "gr": "greece", "hu": "hungary", "is": "iceland", "ie": "ireland", "it": "italy", "kz": "kazakhstan", "xk": "kosovo", "lv": "latvia", "li": "liechtenstein", "lt": "lithuania", "lu": "luxembourg", "mk": "north macedonia", "mt": "malta", "md": "moldova", "mc": "monaco", "me": "montenegro", "nl": "netherlands", "no": "norway", "pl": "poland", "pt": "portugal", "ro": "romania", "ru": "russia", "sm": "san marino", "rs": "serbia", "sk": "slovakia", "si": "slovenia", "es": "spain", "se": "sweden", "ch": "switzerland", "tr": "turkey", "ua": "ukraine", "gb": "united kingdom", "va": "vatican city"}.get(domain.split('.')[-1].lower(), "")
    return country(domain)



def download_and_process_images_concurrently(base_url: str, images_and_alts: list) -> list:
    """
    Downloads and processes images in parallel, returning a list of results.
    
    :param base_url: The base URL to resolve relative image paths.
    :param images_and_alts: A list of dictionaries, each containing the 'src' and 'alt' for an image.
    :param download_and_process_image_function: The function to use for downloading and processing each image.
    :return: A list of dictionaries with processed image data.
    """
    images_downloaded = []

    if images_and_alts:
        with ThreadPoolExecutor(max_workers=3) as executor:
            # Submit all images for downloading and processing in parallel
            future_to_img = {executor.submit(download_and_process_image, base_url, img): img for img in images_and_alts}
            
            # As each future completes, collect the result
            for future in as_completed(future_to_img):
                try:
                    result = future.result()
                    if result:  # If the result is not None, append it to the list
                        images_downloaded.append(result)
                except:
                    print(f"Image failed downloading!")
    return images_downloaded

