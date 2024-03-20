from urllib.parse import urlparse


def get_url_path(url:str):
    parsed_url = urlparse(url)
    return parsed_url.path.lstrip('/')

def get_base_url(url:str):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"
    return base_url

def get_domain(url):
    """
    Extracts and returns the domain from a given URL.

    Args:
    url (str): The URL from which the domain is to be extracted.

    Returns:
    str: The extracted domain.
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc
