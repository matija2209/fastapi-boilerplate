from typing import List

from app.lib import firebase
from app.lib.urlparse import get_base_url, get_url_path
from app.schemas.site import PageInfo


def save_page(url:str, data:str,tag:str,slug:str,pageType:str,domain:str):
    doc_id = firebase.create_firestore_document(collection_name="pages",data=dict(domain=domain,url=url,pageType=pageType,data=data,tag=tag,slug=slug))
    return doc_id
