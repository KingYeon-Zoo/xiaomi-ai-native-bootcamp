#!/usr/bin/env python3
"""Day2 学习任务清单助手 - 命令行工具"""

import argparse
import json
import os
import sys

# 任务列表（硬编码）
TASKS = {
    "spec.md": "需求规格",
    "plan.md": "技术设计",
    "tasks.md": "任务拆解",
    "README.md": "项目说明",
    "ai-log.md": "AI 协作日志"
}

STATUS_FILE = "status.json"


def load_status():
    """加载提交状态，如果文件不存在或损坏则初始化"""
    if not os.path.exists(STATUS_FILE):
        return init_status()

    try:
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            status = json.load(f)
        # 验证格式：必须是 dict，且 key 与 TASKS 一致
        if not isinstance(status, dict):
            raise ValueError("status.json 格式错误")
        return status
    except (json.JSONDecodeError, ValueError):
        print("⚠️  status.json 文件损坏，已重新初始化")
        return init_status()


def init_status():
    """初始化状态文件，所有文件标记为未提交"""
    status = {filename: False for filename in TASKS}
    save_status(status)
    return status


def save_status(status):
    """保存提交状态到文件"""
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2, ensure_ascii=False)


def cmd_today():
    """today 命令：显示任务列表"""
    status = load_status()  # 确保状态文件存在
    print("Day2 学习任务清单：")
    for filename, desc in TASKS.items():
        print(f"  - {filename}: {desc}")


def cmd_submit(filename):
    """submit 命令：标记文件为已提交"""
    status = load_status()

    # 检查文件是否在任务列表中
    if filename not in TASKS:
        print(f"❌ {filename} 不在任务清单中")
        return

    # 检查是否已提交
    if status[filename]:
        print(f"ℹ️  {filename} 已提交过")
        return

    # 标记为已提交
    status[filename] = True
    save_status(status)
    print(f"✅ {filename} 已提交")


def cmd_check():
    """check 命令：查看未提交文件清单"""
    status = load_status()

    unsubmitted = [f for f, submitted in status.items() if not submitted]

    if not unsubmitted:
        print("🎉 全部完成！")
        return

    print("未提交的文件：")
    for filename in unsubmitted:
        print(f"  - {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Day2 学习任务清单助手"
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # today 命令
    subparsers.add_parser("today", help="查看 Day2 任务列表")

    # submit 命令
    submit_parser = subparsers.add_parser("submit", help="标记文件为已提交")
    submit_parser.add_argument("filename", help="要提交的文件名")

    # check 命令
    subparsers.add_parser("check", help="查看未提交文件清单")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    if args.command == "today":
        cmd_today()
    elif args.command == "submit":
        cmd_submit(args.filename)
    elif args.command == "check":
        cmd_check()


if __name__ == "__main__":
    main()
