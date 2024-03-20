from app.lib.firebase import async_update_firestore_document_by_key


async def save_country_to_ecf_document(domain: str, country: str) -> None:
    """
    Saves the extracted country information to the 'ecf' collection for a given domain.

    Args:
        domain (str): The domain representing the document ID in the 'ecf' collection.
        country (str): The country information to save.
    """
    await async_update_firestore_document_by_key("ecf", domain, "country", country)
