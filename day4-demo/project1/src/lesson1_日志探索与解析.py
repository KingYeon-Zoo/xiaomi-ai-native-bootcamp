"""Lesson 1: 日志探索与解析

功能：
1. 数据探索：统计总行数、各级别数量、时间范围、格式异常行数
2. 调用 log_parser.py 解析日志
3. 保存 structured_logs.csv 到 output/ 目录
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 项目根目录（Apache.log、output/ 所在位置）
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import re
from log_parser import parse_log_file, convert_date, PATTERN


def explore_log(filepath: str):
    """数据探索：统计日志基本信息"""
    total_lines = 0
    abnormal_lines = 0
    level_counts = {}

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            match = re.match(PATTERN, line)
            if match:
                level = match.group(2)
                level_counts[level] = level_counts.get(level, 0) + 1
            else:
                abnormal_lines += 1

    parsed_count = sum(level_counts.values())
    print("=" * 60)
    print("Apache 日志探索报告")
    print("=" * 60)
    print(f"总行数: {total_lines}")
    print(f"格式完整行数: {parsed_count}")
    print(f"格式异常行数: {abnormal_lines}")
    print()
    print("日志级别分布:")
    for level, count in sorted(level_counts.items(), key=lambda x: -x[1]):
        pct = count / parsed_count * 100
        print(f"  {level:>10}: {count:>6} ({pct:.1f}%)")
    print("=" * 60)


def main():
    """主函数"""
    log_file = os.path.join(PROJECT_ROOT, 'Apache.log')
    output_dir = os.path.join(PROJECT_ROOT, 'output')

    # 1. 数据探索
    explore_log(log_file)

    # 2. 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 3. 解析日志
    print("\n正在解析日志...")
    df = parse_log_file(log_file)
    print(f"解析完成: {len(df)} 行")

    # 4. 保存 CSV
    output_path = os.path.join(output_dir, 'structured_logs.csv')
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"已保存: {output_path}")

    # 5. 验证
    print(f"\n验证结果:")
    print(f"  行数: {len(df)}")
    print(f"  列: {list(df.columns)}")
    print(f"  缺失值: {df.isnull().sum().sum()}")
    print(f"  时间范围: {df['timestamp'].iloc[0]} ~ {df['timestamp'].iloc[-1]}")


if __name__ == '__main__':
    main()
