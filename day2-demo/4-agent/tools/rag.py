"""RAG 检索工具 — 从 course-faq.md 中按关键词匹配检索信息"""

import re
import os

MAX_QUERY_LENGTH = 200

# 同义词映射表
SYNONYMS = {
    "要交": "提交",
    "五字段": "五个字段",
    "五步": "五步法",
}

# 停用词表
STOP_WORDS = {"的", "是", "了", "什么", "怎么", "和", "有", "吗", "呢", "一个", "这", "那", "都", "也", "说", "个"}


def _load_chunks(faq_path: str) -> list[dict]:
    """按 ## [faq-XX] 切片，返回 [{id, title, content}]"""
    if not os.path.exists(faq_path):
        return []
    with open(faq_path, "r", encoding="utf-8") as f:
        text = f.read()
    sections = re.split(r'\n(?=##\s*\[faq-\d{2}\])', text)
    chunks = []
    for section in sections:
        m = re.search(r'\[faq-(\d{2})\]', section)
        if not m:
            continue
        faq_id = f'faq-{m.group(1)}'
        lines = section.strip().split('\n')
        title = re.sub(r'^##\s*\[faq-\d{2}\]\s*', '', lines[0]).strip() if lines else ''
        body = '\n'.join(lines[1:]).strip()
        chunks.append({"id": faq_id, "title": title, "content": body})
    return chunks


def _tokenize(text: str) -> list[str]:
    """分词：同义词替换 → 按标点空格分段 → 去停用词 → 按字符类型边界拆分 → 保留 2+ 字符"""
    # 应用同义词替换
    for src, dst in SYNONYMS.items():
        text = text.replace(src, dst)

    # 按标点和空格分段
    segments = re.split(r'[,，.!?!\s()（）【】\[\]]+', text)
    segments = [s for s in segments if s]

    # 对每个段：用停用词拆分
    parts = []
    for seg in segments:
        pieces = [seg]
        for sw in sorted(STOP_WORDS, key=len, reverse=True):
            new_pieces = []
            for p in pieces:
                if p in STOP_WORDS:
                    continue
                if sw in p:
                    new_pieces.extend(p.split(sw))
                else:
                    new_pieces.append(p)
            pieces = [p for p in new_pieces if p]
        parts.extend(pieces)

    # 按字符类型边界拆分（英文/数字 vs 中文），保留 2+ 字符
    tokens = []
    for p in parts:
        sub_parts = re.findall(r'[a-zA-Z0-9]+|[一-鿿]+', p)
        tokens.extend([s for s in sub_parts if len(s) >= 2])

    return tokens


def _score_chunk(title: str, content: str, keywords: list[str]) -> int:
    """评分：命中关键词数 + proximity 加分"""
    text = (title + ' ' + content).lower()
    matched = []
    for kw in keywords:
        pos = text.find(kw.lower())
        if pos != -1:
            matched.append((kw, pos))
    if not matched:
        return 0
    score = len(matched)
    if len(matched) >= 2:
        positions = sorted([p for _, p in matched])
        min_dist = min(positions[i+1] - positions[i] for i in range(len(positions)-1))
        if min_dist <= 5:
            score += 3
        elif min_dist <= 15:
            score += 2
        elif min_dist <= 30:
            score += 1
    return score


def rag_search(query: str, faq_path: str = None) -> dict:
    """RAG 检索入口。返回 {success, answer, sources}"""
    if not query or not query.strip():
        return {"success": False, "answer": "请输入您的问题", "sources": []}

    if len(query) > MAX_QUERY_LENGTH:
        query = query[:MAX_QUERY_LENGTH]

    if faq_path is None:
        faq_path = os.path.join(os.path.dirname(__file__), "..", "data", "course-faq.md")
    chunks = _load_chunks(faq_path)
    if not chunks:
        return {"success": False, "answer": "知识库加载失败", "sources": []}

    keywords = _tokenize(query)
    if not keywords:
        return {"success": True, "answer": "资料中没有找到依据", "sources": []}

    scored = []
    for chunk in chunks:
        score = _score_chunk(chunk["title"], chunk["content"], keywords)
        if score > 0:
            scored.append({"id": chunk["id"], "score": score, "content": chunk["title"] + "\n" + chunk["content"]})

    if not scored:
        return {"success": True, "answer": "资料中没有找到依据", "sources": []}

    scored.sort(key=lambda x: x["score"], reverse=True)
    top = scored[:3]

    answer = "\n\n".join(item["content"] for item in top)
    sources = [item["id"] for item in top]
    return {"success": True, "answer": answer, "sources": sources}
