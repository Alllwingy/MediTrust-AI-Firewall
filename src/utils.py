import re

def clean_text(text):
    """
    Text normalization:
    1. Convert to lowercase.
    2. Remove hyphens by joining parts of words (Cis-platinum -> cisplatinum).
    3. Extract words, ignoring punctuation.
    """

    if not text:
        return []

    normalized = text.lower().replace("-", "")
    return re.findall(r"\w+", normalized)