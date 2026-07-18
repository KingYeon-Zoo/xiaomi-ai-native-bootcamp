"""小红书文案生成器 - 主程序入口"""

from collector import collect_info
from generator import generate_copywriting, format_output


def print_welcome() -> None:
    """打印欢迎语"""
    print("=" * 60)
    print("📝 小红书文案生成器")
    print("=" * 60)
    print("\n回答几个问题，我来帮你写小红书文案～")
    print('输入 "quit" 退出程序\n')


def main() -> None:
    """主循环"""
    print_welcome()

    while True:
        # 收集信息
        info = collect_info()

        # 用户输入 quit 退出
        if info is None:
            print("\n👋 再见！")
            break

        # 生成文案
        print("\n⏳ 正在生成文案...")
        try:
            result = generate_copywriting(info)
            print(format_output(result))
        except Exception as e:
            print(f"\n❌ 生成失败: {e}")
            print("请检查 .env 中的 OPENAI_API_KEY 是否正确\n")


if __name__ == "__main__":
    main()
