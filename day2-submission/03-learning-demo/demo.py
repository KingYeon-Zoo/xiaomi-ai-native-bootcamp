#!/usr/bin/env python3
"""LangChain PromptTemplate + RunnableSequence 离线最小 Demo。"""

from __future__ import annotations

import argparse
import re
from typing import Any

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda


DOCS = (
    {
        "id": "demo-01",
        "keywords": ("可复核", "交付", "证据"),
        "text": "可复核交付要求保存输入、预期、实际输出和测试结论，让他人无需询问即可验证。",
    },
    {
        "id": "demo-02",
        "keywords": ("上下文", "context", "资料"),
        "text": "上下文包应写目标、非目标、资料、代码、日志、约束和输出格式，并删除冲突内容。",
    },
    {
        "id": "demo-03",
        "keywords": ("ai", "日志", "人工判断"),
        "text": "AI 日志包含目的、输入、建议、人工判断和验证；人工判断必须说明采纳、修改或拒绝的理由。",
    },
)

PROMPT = PromptTemplate.from_template(
    """你是离线课程资料助手，只能使用上下文回答。
上下文：
{context}

问题：{question}

输出要求：资料存在时概括回答并保留来源编号；无资料时固定拒答。"""
)


def retrieve(question: str) -> list[dict[str, Any]]:
    lowered = question.lower()
    return [doc for doc in DOCS if any(keyword in lowered for keyword in doc["keywords"])]


def prepare_prompt(data: dict[str, str]) -> dict[str, str]:
    question = data["question"].strip()
    matches = retrieve(question)
    context = "[NO_MATCH]" if not matches else "\n".join(
        f"[{doc['id']}] {doc['text']}" for doc in matches
    )
    return {"context": context, "question": question}


def fake_model(prompt_value: Any) -> str:
    """模拟模型：只转述 Prompt 上下文，不联网。"""
    text = prompt_value.to_string()
    if "[NO_MATCH]" in text:
        return "资料中没有找到依据。"
    context = text.split("上下文：\n", 1)[1].split("\n\n问题：", 1)[0]
    sources = re.findall(r"\[(demo-\d{2})\]", context)
    statements = re.sub(r"\[demo-\d{2}\]\s*", "", context).replace("\n", " ")
    citations = " ".join(f"[{source}]" for source in sources)
    return f"根据资料，{statements} {citations}".strip()


def build_chain():
    """构造 RunnableSequence：准备上下文 → PromptTemplate → fake model。"""
    return RunnableLambda(prepare_prompt) | PROMPT | RunnableLambda(fake_model)


def run_demo(question: str) -> str:
    if not question or not question.strip():
        raise ValueError("问题不能为空")
    return build_chain().invoke({"question": question})


def main() -> int:
    parser = argparse.ArgumentParser(description="LangChain 离线最小 Demo")
    parser.add_argument("question", nargs="+", help="要查询的课程问题")
    args = parser.parse_args()
    print(run_demo(" ".join(args.question)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
