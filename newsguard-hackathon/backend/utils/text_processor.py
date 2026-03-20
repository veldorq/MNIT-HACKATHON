import re

URL_RE = re.compile(r"https?://\S+|www\.\S+")
EMAIL_RE = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b")
SPECIAL_RE = re.compile(r"[^a-zA-Z0-9\.\s]")
WHITESPACE_RE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    lowered = text.lower()
    no_urls = URL_RE.sub(" ", lowered)
    no_emails = EMAIL_RE.sub(" ", no_urls)
    alpha_num = SPECIAL_RE.sub(" ", no_emails)
    normalized = WHITESPACE_RE.sub(" ", alpha_num).strip()
    return normalized
