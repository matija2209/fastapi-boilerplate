import base64
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def process_logo(soup: BeautifulSoup, base_url: str) -> str:
    """
    Find logo URL, download it, and convert it to a data URI.
    """
    logo_image = soup.find('img', src=lambda x: 'logo' in x.lower() if x else False)
    logo_url = logo_image['src'] if logo_image else None
    logo_img_data_uri = None

    if logo_url:
        logo_url = urljoin(base_url, logo_url)
        try:
            r = requests.get(logo_url, timeout=5)
            if r.status_code == 200:
                encoded_logo = base64.b64encode(r.content).decode('utf-8')  # Ensure string output
                mime_type = r.headers.get('Content-Type', 'image/jpeg')  # Use a default if not provided
                logo_img_data_uri = f"data:{mime_type};base64,{encoded_logo}"
        except requests.exceptions.RequestException as e:
            print(f"Logo could not be exported: {logo_url}")

    return logo_img_data_uri
