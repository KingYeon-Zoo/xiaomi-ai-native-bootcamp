"""工具函数模块"""

import os


def ensure_dir(path: str):
    """确保目录存在，不存在则创建"""
    os.makedirs(path, exist_ok=True)


def count_lines(filepath: str) -> int:
    """统计文件行数"""
    count = 0
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for _ in f:
            count += 1
    return count


def print_section(title: str, content: str):
    """格式化输出章节"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")
    print(content)
