"""信息收集逻辑"""

from typing import Optional
from prompt import SUGGESTIONS

# 退出命令
EXIT_COMMANDS = {"quit", "exit"}


def is_exit_command(text: str) -> bool:
    """判断是否是退出命令"""
    return text.lower().strip() in EXIT_COMMANDS


def show_suggestions(field: str) -> None:
    """显示建议备选项"""
    suggestions = SUGGESTIONS.get(field, [])
    if suggestions:
        print(f"   💡 建议: {'、'.join(suggestions)}")


def collect_field(field: str, required: bool = True) -> Optional[str]:
    """收集单个字段，返回 None 表示退出"""
    while True:
        answer = input("   > ").strip()

        # 检查退出命令
        if is_exit_command(answer):
            return None

        # 必填校验
        if required and not answer:
            print("⚠️  这个是必填项哦～")
            continue

        # 可选字段为空时使用默认值
        if not answer:
            return "（无）"

        return answer


def collect_info() -> Optional[dict]:
    """收集所有信息，返回 None 表示退出"""
    info = {}

    # 产品（必填）
    print("\n🤖 你要推广什么产品？")
    show_suggestions("product")
    product = collect_field("product", required=True)
    if product is None:
        return None
    info["product"] = product

    # 目标用户（必填）
    print("\n🤖 目标用户是谁？")
    show_suggestions("target_user")
    target_user = collect_field("target_user", required=True)
    if target_user is None:
        return None
    info["target_user"] = target_user

    # 风格（可选）
    print("\n🤖 想要什么风格？（可选，回车跳过）")
    show_suggestions("style")
    style = collect_field("style", required=False)
    if style is None:
        return None
    info["style"] = style

    return info
