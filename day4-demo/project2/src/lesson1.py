"""
Lesson 1：数据探索与文本清洗

实现数据加载、邮件解析、文本清洗
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import load_emails
from src.text_cleaner import parse_email_from_raw, clean_text


def main():
    """主函数"""
    print("=" * 60)
    print("Lesson 1：数据探索与文本清洗")
    print("=" * 60)

    # 1. 加载所有邮件
    print("\n[1/4] 加载邮件数据...")
    df = load_emails('data')

    # 2. 数据探索
    print("\n[2/4] 数据探索...")
    print(f"数据形状: {df.shape}")
    print(f"\n标签分布:")
    print(df['label'].value_counts())
    print(f"\n来源分布:")
    print(df['source'].value_counts())

    # 3. 解析邮件正文
    print("\n[3/4] 解析邮件正文...")
    df['body'] = df['raw_email'].apply(parse_email_from_raw)

    # 统计解析结果
    empty_body_count = (df['body'] == '').sum()
    print(f"空正文邮件数量: {empty_body_count}")

    # 4. 清洗文本
    print("\n[4/4] 清洗文本...")
    df['body'] = df['body'].fillna('')
    df['cleaned_text'] = df['body'].apply(clean_text)

    # 统计清洗结果
    empty_cleaned_count = (df['cleaned_text'] == '').sum()
    print(f"清洗后为空的消息数量: {empty_cleaned_count}")

    # 保存到CSV
    output_path = 'output/cleaned_data.csv'
    df[['label', 'source', 'body', 'cleaned_text']].to_csv(output_path, index=False)
    print(f"\n✓ 数据已保存到 {output_path}")
    print(f"  - 总记录数: {len(df)}")
    print(f"  - ham: {len(df[df['label'] == 'ham'])} 条")
    print(f"  - spam: {len(df[df['label'] == 'spam'])} 条")

    # 显示样例
    print("\n" + "=" * 60)
    print("数据样例（前3条）:")
    print("=" * 60)
    for i, row in df.head(3).iterrows():
        print(f"\n[{i+1}] 标签: {row['label']}")
        print(f"    来源: {row['source']}")
        print(f"    正文（前100字符）: {row['body'][:100]}...")
        print(f"    清洗后（前100字符）: {row['cleaned_text'][:100]}...")

    print("\n" + "=" * 60)
    print("Lesson 1 完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
