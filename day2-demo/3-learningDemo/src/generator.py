"""文案生成逻辑"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence
from prompt import PROMPT_TEMPLATE

# 加载环境变量
load_dotenv()


def create_chain() -> RunnableSequence:
    """创建 chain (prompt | llm)"""
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE")  # 支持自定义 API 端点（如 MIMO）
    model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    # 构建参数
    kwargs = {
        "model": model,
        "temperature": 0.7,
        "openai_api_key": api_key,
    }
    if api_base:
        kwargs["openai_api_base"] = api_base

    llm = ChatOpenAI(**kwargs)

    # 新语法：prompt | llm
    return PROMPT_TEMPLATE | llm


def generate_copywriting(info: dict) -> str:
    """生成文案"""
    chain = create_chain()
    result = chain.invoke(info)
    # result 是 AIMessage，取 content
    return result.content


def format_output(result: str) -> str:
    """格式化输出"""
    return f"""
════════════════════════════════════════════════════════════
✨ 生成结果
════════════════════════════════════════════════════════════

{result}

════════════════════════════════════════════════════════════
"""
