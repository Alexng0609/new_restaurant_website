import hashlib
import logging

from django.core.cache import cache
from django.utils.translation import get_language

logger = logging.getLogger(__name__)

CACHE_TIMEOUT = 60 * 60 * 24 * 30  # 30 days


def is_english():
    lang = get_language() or ""
    return lang.lower().startswith("en")


def translate_vi_to_en(text):
    """Translate Vietnamese text to English, with cache."""
    text = str(text).strip()
    if not text:
        return text

    cache_key = f"l10n:vi-en:{hashlib.md5(text.encode('utf-8')).hexdigest()}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        from deep_translator import GoogleTranslator

        translated = GoogleTranslator(source="vi", target="en").translate(text)
    except Exception as exc:
        logger.warning("Auto-translation failed: %s", exc)
        translated = text

    cache.set(cache_key, translated, CACHE_TIMEOUT)
    return translated


def localized_text(primary, english=""):
    """Return English when EN is active — manual translation first, then auto-translate."""
    if not is_english():
        return primary
    if english and str(english).strip():
        return english
    return translate_vi_to_en(primary)
