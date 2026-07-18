"""
数据加载工具模块

提供邮件数据加载功能
"""

import os
import pandas as pd


def load_emails(data_dir: str) -> pd.DataFrame:
    """
    加载所有邮件

    Args:
        data_dir: 数据目录路径

    Returns:
        DataFrame，包含列：
        - label: ham/spam
        - raw_email: 原始邮件内容
        - source: 来源目录
    """
    emails = []

    # 定义目录到标签的映射
    dir_label_map = {
        'easy_ham': 'ham',
        'easy_ham_2': 'ham',
        'hard_ham': 'ham',
        'spam': 'spam',
        'spam_2': 'spam'
    }

    for dir_name, label in dir_label_map.items():
        dir_path = os.path.join(data_dir, dir_name)
        if not os.path.exists(dir_path):
            print(f"警告：目录 {dir_path} 不存在，跳过")
            continue

        # 遍历目录中的所有文件
        for filename in os.listdir(dir_path):
            filepath = os.path.join(dir_path, filename)

            # 跳过目录和非文件
            if not os.path.isfile(filepath):
                continue

            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    raw_email = f.read()

                emails.append({
                    'label': label,
                    'raw_email': raw_email,
                    'source': dir_name
                })
            except Exception as e:
                print(f"警告：读取文件 {filepath} 失败: {e}")

    df = pd.DataFrame(emails)
    print(f"加载完成：共 {len(df)} 条邮件")
    print(f"  - ham: {len(df[df['label'] == 'ham'])} 条")
    print(f"  - spam: {len(df[df['label'] == 'spam'])} 条")

    return df
