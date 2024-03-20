from typing import List

from usp.tree import sitemap_tree_for_homepage

from app.lib.urlparse import get_base_url, get_domain, get_url_path
from app.utils.url_utils import clean_url


def get_sitemap_urls(url:str) -> List[str]:
    """
    Get all URLs from a sitemap
    """
    trusted_url = clean_url(url)
    tree = sitemap_tree_for_homepage(trusted_url)
    links = []

    for page in tree.all_pages():
        nested_url = page.url.lower()  # Convert URL to lowercase to make the search case-insensitive
        links.append(nested_url)
    return links
