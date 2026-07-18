# retrieve.py — RAG 检索模块

import re

# 同义词映射表
SYNONYMS = {
    "要交": "提交",
    "五字段": "五个字段",
    "五步": "五步法",
}

# 停用词表
STOP_WORDS = {"的", "是", "了", "什么", "怎么", "和", "有", "吗", "呢", "一个", "这", "那", "都", "也", "说", "个"}


def _chunk_faq(content):
    """按 ## [faq-XX] 切片，返回 chunk 列表"""
    sections = re.split(r'\n(?=##\s*\[faq-\d{2}\])', content)
    chunks = []
    for section in sections:
        m = re.search(r'\[faq-(\d{2})\]', section)
        if not m:
            continue
        faq_id = f'faq-{m.group(1)}'
        lines = section.strip().split('\n')
        # 标题行：## [faq-XX] 标题内容
        title_line = lines[0] if lines else ''
        title = re.sub(r'^##\s*\[faq-\d{2}\]\s*', '', title_line).strip()
        body = '\n'.join(lines[1:]).strip()
        chunks.append({
            'id': faq_id,
            'title': title,
            'content': body,
        })
    return chunks


def _tokenize(question):
    # 分词：按标点空格分段，去停用词，按字符类型拆分，保留 2+ 字符 token
    # 应用同义词替换
    text = question
    for src, dst in SYNONYMS.items():
        text = text.replace(src, dst)

    # 按标点和空格分段
    segments = re.split(r'[,，.!?!\s()]+', text)
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

    # 按字符类型边界拆分（英文/数字 vs 中文）
    tokens = []
    for p in parts:
        sub_parts = re.findall(r'[a-zA-Z0-9]+|[一-鿿]+', p)
        tokens.extend([s for s in sub_parts if len(s) >= 2])

    return tokens


def retrieve(question, chunks):
    """
    检索相关 FAQ 条目。

    Args:
        question: 用户问题
        chunks: course-faq.md 的原始内容（字符串）

    Returns:
        list[dict]，按 score 降序，最多 3 条
    """
    if not question or not chunks:
        return []

    # 如果 chunks 是字符串，做切片
    if isinstance(chunks, str):
        chunk_list = _chunk_faq(chunks)
    else:
        chunk_list = chunks

    # 分词
    keywords = _tokenize(question)
    if not keywords:
        return []

    # 关键词匹配评分（基础分 + 近 proximity 加分）
    results = []
    for chunk in chunk_list:
        text = (chunk.get('title', '') + ' ' + chunk.get('content', '')).lower()
        matched = []
        for kw in keywords:
            pos = text.find(kw.lower())
            if pos != -1:
                matched.append((kw, pos))
        if not matched:
            continue
        # 基础分：命中关键词数
        score = len(matched)
        # 近 proximity 加分：多关键词时，按最近距离加分（距离越近加分越多）
        if len(matched) >= 2:
            positions = sorted([p for _, p in matched])
            min_dist = min(positions[i+1] - positions[i] for i in range(len(positions)-1))
            # 距离越近加分越多，最大 +3
            if min_dist <= 5:
                score += 3
            elif min_dist <= 15:
                score += 2
            elif min_dist <= 30:
                score += 1
        results.append({
            'id': chunk['id'],
            'title': chunk.get('title', ''),
            'content': chunk.get('content', ''),
            'score': score,
        })

    # 排序：score 降序，取 top3
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:3]
