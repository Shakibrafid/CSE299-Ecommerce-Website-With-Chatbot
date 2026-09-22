"""Lightweight bidirectional AI firewall for the BestCommerce chatbots.

Included controls:
1. Input normalization
2. Prompt-injection filtering
3. Customer sensitive-request filtering
4. Output sensitive-data filtering
5. JWT leak detection

Rate limiting is configured in Django REST Framework settings and applied
through ScopedRateThrottle in chatbot/views.py.
"""

import re
import unicodedata


INPUT_BLOCKED_REPLY = (
    "That request was blocked by the AI input firewall because it appears to "
    "contain a prompt-injection or protected-data request."
)

CUSTOMER_BLOCKED_REPLY = (
    "That request asks for protected business or security data. "
    "The customer assistant can only discuss public product details "
    "and availability."
)

OUTPUT_BLOCKED_REPLY = (
    "The AI response was blocked by the output firewall because it may "
    "contain protected or sensitive information."
)


_ZERO_WIDTH_RE = re.compile(r"[\u200B-\u200D\u2060\uFEFF]")
_CONTROL_RE = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")
_WHITESPACE_RE = re.compile(r"\s+")

# General attacks that are blocked for BOTH customer and admin chatbots.
_GENERAL_INPUT_PATTERNS = (
    re.compile(
        r"\bignore\b.{0,50}\b(previous|prior|all|system|developer)\b"
        r".{0,50}\b(instruction|instructions|rules|prompt|message)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(reveal|show|print|repeat|dump|expose)\b.{0,50}"
        r"\b(system prompt|hidden prompt|developer message|hidden instructions)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(jailbreak|prompt injection|bypass safety|bypass security)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(reveal|show|print|give|dump|expose)\b.{0,50}"
        r"\b(password|secret key|api key|access token|refresh token|jwt|credential|credentials)\b",
        re.IGNORECASE,
    ),
)

# Extra restrictions for the PUBLIC customer chatbot only.
_CUSTOMER_SENSITIVE_PATTERNS = (
    re.compile(r"\b(act|pretend|switch|enter)\b.{0,30}\badmin\b", re.IGNORECASE),
    re.compile(r"\b(admin mode|database dump|dump the database|database snapshot)\b", re.IGNORECASE),
    re.compile(r"\b(show|list|reveal|give)\b.{0,30}\ball users\b", re.IGNORECASE),
    re.compile(r"\bcustomer emails?\b", re.IGNORECASE),
    re.compile(r"\b(total users|total orders|latest orders|order details)\b", re.IGNORECASE),
    re.compile(r"\b(sales revenue|total revenue|sales value)\b", re.IGNORECASE),
    re.compile(r"\b(exact stock|stock count|inventory count|how many units)\b", re.IGNORECASE),
)

# JWTs normally start with eyJ because the first JSON segment is base64url encoded.
_JWT_RE = re.compile(
    r"\beyJ[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{5,}\b"
)

# Secret-looking assignments/headers/connection strings in model output.
_SECRET_ASSIGNMENT_RE = re.compile(
    r"(?i)\b(secret[_ -]?key|api[_ -]?key|password|database[_ -]?password|"
    r"access[_ -]?token|refresh[_ -]?token|auth[_ -]?token)\b\s*[:=]\s*"
    r"[\"']?[^\s\"']{4,}"
)
_BEARER_RE = re.compile(r"(?i)\bauthorization\s*:\s*bearer\s+[^\s]+")
_DB_URL_RE = re.compile(
    r"(?i)\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?)://[^\s:@/]+:[^\s@/]+@"
)
_DJANGO_SECRET_RE = re.compile(r"(?i)django-insecure-[^\s\"']+")

# Exact internal prompt text should never be sent to a client.
_PROTECTED_PROMPT_MARKERS = (
    "you are the public customer shopping assistant for bestcommerce",
    "you are the private admin assistant for bestcommerce",
)


def normalize_input(text):
    """Normalize user text before security checks and before sending to Ollama."""
    if not isinstance(text, str):
        return ""

    normalized = unicodedata.normalize("NFKC", text)
    normalized = _ZERO_WIDTH_RE.sub("", normalized)
    normalized = _CONTROL_RE.sub("", normalized)
    normalized = _WHITESPACE_RE.sub(" ", normalized)
    return normalized.strip()


def check_input(message, customer_mode=False):
    """Return (allowed, reason) for normalized user input."""
    if not isinstance(message, str) or not message.strip():
        return False, "invalid_or_empty_input"

    for pattern in _GENERAL_INPUT_PATTERNS:
        if pattern.search(message):
            return False, "prompt_injection_or_security_request"

    if customer_mode:
        for pattern in _CUSTOMER_SENSITIVE_PATTERNS:
            if pattern.search(message):
                return False, "protected_business_data_request"

    return True, None


def check_output(reply):
    """Return (allowed, reason) before an Ollama response reaches the frontend."""
    if not isinstance(reply, str):
        return False, "invalid_ai_output"

    if _JWT_RE.search(reply):
        return False, "jwt_leak_detected"

    if _SECRET_ASSIGNMENT_RE.search(reply):
        return False, "sensitive_data_leak_detected"

    if _BEARER_RE.search(reply):
        return False, "bearer_token_leak_detected"

    if _DB_URL_RE.search(reply):
        return False, "database_credential_leak_detected"

    if _DJANGO_SECRET_RE.search(reply):
        return False, "secret_key_leak_detected"

    lowered = reply.lower()
    if any(marker in lowered for marker in _PROTECTED_PROMPT_MARKERS):
        return False, "system_prompt_leak_detected"

    return True, None
