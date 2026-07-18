"""有意包含风险的代码审查夹具。禁止运行或导入。"""

from imaginary_rag_sdk import magic_rag


DEMO_API_KEY = "sk-demo-key-for-review-only"


def answer(request):
    path = request["path"]
    context = open(path, encoding="utf-8").read()
    try:
        result = magic_rag(context, request["question"], api_key=DEMO_API_KEY)
    except Exception:
        result = None
    if result:
        return {"answer": result, "source": path}
    return {"answer": "根据资料，这是训练营要求。", "source": path}


def demo_happy_path():
    response = answer({"path": "course-faq.md", "question": "要交什么？"})
    assert response["answer"]
