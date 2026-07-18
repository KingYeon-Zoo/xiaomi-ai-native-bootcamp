"""RFC 邮件正文抽取与九步文本清洗。"""

from __future__ import annotations

import re
from email import policy
from email.parser import BytesParser
from html.parser import HTMLParser

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "but", "by", "for",
    "from", "had", "has", "have", "he", "her", "his", "i", "if", "in", "is",
    "it", "its", "me", "my", "of", "on", "or", "our", "she", "so", "that",
    "the", "their", "them", "they", "this", "to", "was", "we", "were", "will",
    "with", "you", "your",
}
_URL = re.compile(r"\b(?:https?://|www\.)\S+", re.IGNORECASE)
_EMAIL = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
_PHONE = re.compile(r"(?<!\d)(?:\+?\d[\d(). -]{7,}\d)(?!\d)")


class _HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self._ignored_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"script", "style"}:
            self._ignored_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self._ignored_depth:
            self._ignored_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self._ignored_depth:
            self.parts.append(data)


def html_to_text(value: str) -> str:
    parser = _HTMLTextExtractor()
    try:
        parser.feed(value)
        return " ".join(parser.parts)
    except (ValueError, TypeError):
        return re.sub(r"<[^>]+>", " ", value)


def _body_from_message(message) -> str:
    plain_parts: list[str] = []
    html_parts: list[str] = []
    parts = message.walk() if message.is_multipart() else [message]
    for part in parts:
        if part.is_multipart() or part.get_content_disposition() == "attachment":
            continue
        content_type = part.get_content_type()
        if content_type not in {"text/plain", "text/html"}:
            continue
        try:
            content = part.get_content()
        except (LookupError, UnicodeDecodeError, AttributeError):
            payload = part.get_payload(decode=True) or b""
            content = payload.decode(part.get_content_charset() or "utf-8", errors="replace")
        if content_type == "text/plain":
            plain_parts.append(str(content))
        else:
            html_parts.append(html_to_text(str(content)))
    return "\n".join(plain_parts or html_parts)


def extract_raw_message(raw_email: bytes) -> str:
    """返回 Subject + 正文；明确排除其余邮件头和附件内容。"""
    message = BytesParser(policy=policy.default).parsebytes(raw_email)
    subject = str(message.get("Subject", ""))
    body = _body_from_message(message)
    return "\n".join(part for part in (subject, body) if part).strip()


def clean_text(text: str | None) -> str:
    """依次执行小写、HTML、URL、邮箱、电话、标点、空格、停用词和空文本处理。"""
    if not isinstance(text, str) or not text.strip():
        return ""
    value = text.lower()
    value = html_to_text(value)
    value = _URL.sub(" ", value)
    value = _EMAIL.sub(" ", value)
    value = _PHONE.sub(" ", value)
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    words = [word for word in value.split() if word not in STOP_WORDS]
    return " ".join(words)

