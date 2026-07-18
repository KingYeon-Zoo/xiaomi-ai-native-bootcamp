# main.py — RAG 课程助手 CLI 入口

import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from retrieve import retrieve
from answer import answer


def main():
    # 空输入判断
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print("请输入您的问题")
        return

    question = sys.argv[1].strip()

    # 超长截断
    if len(question) > 200:
        question = question[:200]

    # 读取 FAQ 数据
    faq_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'course-faq.md')
    with open(faq_path, 'r', encoding='utf-8') as f:
        faq_content = f.read()

    # 检索
    chunks = retrieve(question, faq_content)

    # 零命中 → 拒答
    if not chunks:
        print("资料中没有找到依据。")
        return

    # 生成回答
    result = answer(question, chunks)

    # 输出回答（去掉 mock 自带的来源行，避免重复）
    answer_text = result["answer"]
    answer_text = re.sub(r'\n?来源:.*$', '', answer_text, flags=re.MULTILINE).strip()
    print(answer_text)

    # 输出来源
    if result["sources"]:
        print(f"\n来源: {', '.join(result['sources'])}")


if __name__ == "__main__":
    main()
