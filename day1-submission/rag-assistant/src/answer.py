# answer.py — RAG 回答模块

import json
import urllib.request

LLM_API_BASE = "http://localhost:9876/v1"
LLM_MODEL = "mock"


def answer(question, chunks):
    """
    基于检索结果生成回答。

    Args:
        question: 用户问题
        chunks: retrieve() 返回的结果列表

    Returns:
        {"answer": str, "sources": list}
    """
    # 空 chunks → 拒答
    if not chunks:
        return {"answer": "资料中没有找到依据。", "sources": []}

    # 拼接 Prompt
    system_msg = (
        "你是一个课程助手，只基于以下资料回答问题。"
        "回答必须注明来源编号。资料外问题请回答'资料中没有找到依据'。"
    )

    # 组装参考资料
    faq_text = ""
    for c in chunks:
        faq_text += f"\n[{c['id']}] {c.get('title', '')}\n{c.get('content', '')}\n"

    user_msg = f"参考资料：\n{faq_text}\n\n用户问题：{question}"

    # 调用 LLM (mock)
    try:
        payload = json.dumps({
            "model": LLM_MODEL,
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{LLM_API_BASE}/chat/completions",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            answer_text = data["choices"][0]["message"]["content"]
    except Exception as e:
        answer_text = f"调用 LLM 时出错：{e}"

    # sources：直接取 chunk id
    sources = [f"[{c['id']}]" for c in chunks]

    return {"answer": answer_text, "sources": sources}
