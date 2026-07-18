"""只基于课程 FAQ 的轻量检索工具。"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional


def load_chunks(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    chunks: list[dict[str, str]] = []
    for match in re.finditer(
        r"^## \[(faq-\d{2})\]\s*(.*?)\n(.*?)(?=^## \[faq-|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    ):
        chunks.append({"id": match.group(1), "title": match.group(2).strip(), "content": match.group(3).strip()})
    return chunks


def query_tokens(query: str) -> set[str]:
    cleaned = query.lower()
    for word in ("什么", "怎么", "如何", "请问", "是否", "的是", "一个"):
        cleaned = cleaned.replace(word, "")
    cleaned = re.sub(r"[^a-z0-9\u4e00-\u9fff]", "", cleaned)
    latin = set(re.findall(r"[a-z0-9]{2,}", cleaned))
    chinese = "".join(re.findall(r"[\u4e00-\u9fff]", cleaned))
    grams = {chinese[index:index + size] for size in (2, 3) for index in range(max(0, len(chinese) - size + 1))}
    return latin | grams


def rag_search(query: str, faq_path: Optional[Path] = None) -> dict:
    if not query or not query.strip():
        return {"success": False, "answer": "请输入课程问题", "sources": []}
    path = faq_path or Path(__file__).resolve().parents[1] / "data" / "course-faq.md"
    chunks = load_chunks(Path(path))
    if not chunks:
        return {"success": False, "answer": "课程资料加载失败，请检查 course-faq.md", "sources": []}
    tokens = query_tokens(query[:200])
    scored = []
    for chunk in chunks:
        text = f"{chunk['title']} {chunk['content']}".lower()
        score = sum(1 for token in tokens if token in text)
        if score:
            scored.append((score, chunk))
    if not scored:
        return {"success": True, "answer": "资料中没有找到依据", "sources": []}
    scored.sort(key=lambda item: item[0], reverse=True)
    top = [chunk for _, chunk in scored[:3]]
    answer = "\n\n".join(f"{chunk['title']}：{chunk['content']}" for chunk in top)
    return {"success": True, "answer": answer, "sources": [chunk["id"] for chunk in top]}

