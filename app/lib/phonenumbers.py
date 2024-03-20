import phonenumbers


def extract_phone_numbers(page_text: str) -> list:
    """
    Extract phone numbers from the page text.
    """
    phone_numbers = []
    for match in phonenumbers.PhoneNumberMatcher(page_text, None):
        phone_numbers.append(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL))
    return list(set(phone_numbers))
