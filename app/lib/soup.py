
import json
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.utils.url_utils import (has_anchor, is_matching_domain,
                                 to_root_relative)


def extract_emails(soup: BeautifulSoup) -> list:
    """
    Extract emails from the BeautifulSoup object, lowercase, and remove duplicates.
    """
    text = soup.get_text()
    emails = set()  # Use a set to avoid duplicates
    if text:  # Check if text is not empty
        # Find all email addresses, automatically avoiding duplicates due to set usage
        raw_emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        # Process each email: trim, lowercase, and add to the set
        emails = set(map(lambda email: email.strip().lower(), raw_emails))
    return list(emails)
    
def extract_seo_tags(soup: BeautifulSoup) -> dict:
    """
    Extract meta tags from the BeautifulSoup object.
    """
    seo = {
        'meta_tags':{
            'title': soup.title.string.strip() if soup.title else None,
            'meta_title': None,
            'meta_description': None,
        },
        'og_tags': {}
    }
    
    # Meta title
    title_tag = soup.find("meta", {"name": "title"})
    if title_tag and "content" in title_tag.attrs:
        seo["meta_tags"]['meta_title'] = title_tag["content"]
    
    # Meta description
    description_tag = soup.find("meta", {"name": "description"})
    if description_tag and "content" in description_tag.attrs:
        seo["meta_tags"]['meta_description'] = description_tag["content"]
    
    # OG tags
    seo['og_tags'] = [{'key': tag['property'], 'value': tag['content']} for tag in soup.find_all('meta', property=lambda x: x and x.startswith('og:')) if 'property' in tag.attrs and 'content' in tag.attrs]
    
    return seo


def extract_internal_links(soup: BeautifulSoup, base_url: str, domain: str) -> list:
    """
    Extract internal links from the BeautifulSoup object.
    """
    internal_links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        # Skip anchor links and check for anchors in URLs
        if href.startswith('#') or has_anchor(href):
            continue
        # Check for absolute URLs that match the domain, or relative URLs
        if href.startswith('/'):
            internal_links.append(href)
        elif href.startswith('http'):
            if is_matching_domain(href, domain):
                root_relative_url = to_root_relative(href, base_url)
                internal_links.append(root_relative_url)
        else:  # Handle relative URLs
            full_url = urljoin(base_url, href)
            if is_matching_domain(full_url, domain):
                root_relative_url = to_root_relative(full_url, base_url)
                internal_links.append(root_relative_url)

    return list(set(internal_links))  # Remove duplicates and ensure all URLs are unique


def extract_contact_links(soup: BeautifulSoup) -> list:
    """
    Extract contact links from the BeautifulSoup object.
    """
    contact_words = ['kontakt', 'contact', 'contacto', 'contatto', 'contactez', 'kontakte']
    contact_links = [a['href'] for a in soup.find_all('a', href=True) if any(contact_word in a.text.lower() for contact_word in contact_words) and a['href'].startswith('/')]
    
    return list(set(contact_links))  # Remove duplicates


def extract_images_and_alts(soup: BeautifulSoup) -> list:
    """
    Gather image sources and alternative texts from the BeautifulSoup object.
    """
    images_and_alts = [{'src': img['src'], 'alt': img.get('alt', '')} for img in soup.find_all('img', src=True)]
    return images_and_alts

def extract_favicon(soup: BeautifulSoup, base_url: str) -> str:
    """
    Extract favicon URL from the BeautifulSoup object.
    """
    favicon = soup.find('link', rel=lambda x: x and 'icon' in x)
    favicon_url = urljoin(base_url, favicon['href']) if favicon and favicon.has_attr('href') else None
    return favicon_url



def extract_schema_data(soup: BeautifulSoup) -> list:
    """
    Extract schema JSON-LD data from the BeautifulSoup object.
    """
    schema_data = []
    for script in soup.find_all('script', {'type': 'application/ld+json'}):
        if script.string and script.string.strip():
            try:
                data = json.loads(script.string)
                schema_data.append(data)
            except json.JSONDecodeError:
                pass  # Handle error or log as needed
    return schema_data


def extract_social_media_links(soup: BeautifulSoup) -> list:
    """
    Extract social media links from a BeautifulSoup object.
    
    :param soup: BeautifulSoup object parsed from a webpage.
    :return: A list of unique social media links found on the page.
    """
    social_media_domains = ['facebook.com', 'tiktok.com', 'instagram.com', 'linkedin.com']
    social_media_links = set()  # Use a set to avoid duplicates

    for a in soup.find_all('a', href=True):
        href = a['href']
        if any(domain in href for domain in social_media_domains):
            social_media_links.add(href)

    return list(social_media_links)


def extract_headings(soup: BeautifulSoup) -> dict:
    """
    Extract all h1 and h2 headings and their values from the BeautifulSoup object.
    """
    headings = {'h1': [], 'h2': []}  # Initialize a dictionary to hold the headings
    
    for h_tag in ['h1', 'h2']:
        for tag in soup.find_all(h_tag):
            headings[h_tag].append(tag.get_text(strip=True))
    
    return headings