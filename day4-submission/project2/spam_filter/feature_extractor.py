"""按数据契约从 raw/cleaned 两种文本提取六类特征。"""

from __future__ import annotations

import re

SPAM_KEYWORDS = (
    "act now", "buy now", "click", "credit", "free", "guarantee", "limited offer",
    "loan", "money", "prize", "risk free", "urgent", "winner",
)


def extract_features(raw_message: str | None, cleaned_message: str | None) -> dict[str, float | int]:
    raw = raw_message if isinstance(raw_message, str) else ""
    cleaned = cleaned_message if isinstance(cleaned_message, str) else ""
    alpha_count = sum(char.isalpha() for char in raw)
    uppercase_count = sum(char.isupper() for char in raw)
    keyword_hits = sum(
        len(re.findall(rf"(?<!\w){re.escape(keyword)}(?!\w)", cleaned)) for keyword in SPAM_KEYWORDS
    )
    return {
        "message_length": len(raw),
        "uppercase_ratio": uppercase_count / alpha_count if alpha_count else 0.0,
        "exclamation_count": raw.count("!"),
        "keyword_hits": keyword_hits,
        "digit_count": sum(char.isdigit() for char in raw),
        "currency_symbol_count": sum(raw.count(symbol) for symbol in "$£€¥₹"),
    }

