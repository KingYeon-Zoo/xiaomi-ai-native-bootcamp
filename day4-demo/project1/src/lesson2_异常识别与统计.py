"""Lesson 2: 异常识别与统计分析

功能：
1. 加载 structured_logs.csv
2. 筛选 error 日志并分类
3. 执行三个维度统计
4. 保存 error_logs.csv 和 error_code_reference.csv 到 output/
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 项目根目录（Apache.log、output/ 所在位置）
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from log_parser import parse_log_file
from error_filter import filter_errors, get_error_reference
from statistics import daily_stats, type_stats, module_stats


def main():
    """主函数"""
    log_file = os.path.join(PROJECT_ROOT, 'Apache.log')
    output_dir = os.path.join(PROJECT_ROOT, 'output')

    # 1. 加载结构化日志
    print("正在加载 structured_logs.csv...")
    df = parse_log_file(log_file)
    print(f"加载完成: {len(df)} 行")

    # 2. 筛选 error 日志
    print("\n正在筛选 error 日志...")
    error_df = filter_errors(df)
    print(f"error 日志: {len(error_df)} 行")
    print(f"错误类型: {error_df['error_type'].nunique()} 种")
    print(f"模块数量: {error_df['module'].nunique()} 个")

    # 3. 保存 error_logs.csv
    os.makedirs(output_dir, exist_ok=True)
    error_path = os.path.join(output_dir, 'error_logs.csv')
    error_df.to_csv(error_path, index=False, encoding='utf-8')
    print(f"\n已保存: {error_path}")

    # 4. 保存 error_code_reference.csv
    ref_df = get_error_reference()
    ref_path = os.path.join(output_dir, 'error_code_reference.csv')
    ref_df.to_csv(ref_path, index=False, encoding='utf-8')
    print(f"已保存: {ref_path}")

    # 5. 统计分析
    print("\n" + "=" * 60)
    print("统计分析结果")
    print("=" * 60)

    # 每日统计
    daily = daily_stats(error_df)
    print(f"\n每日统计: {len(daily)} 天")
    print(f"  最大: {daily['count'].max()} 条/天")
    print(f"  最小: {daily['count'].min()} 条/天")
    print(f"  平均: {daily['count'].mean():.1f} 条/天")

    # 类型统计
    types = type_stats(error_df)
    print(f"\n错误类型统计 (Top 5):")
    for _, row in types.head(5).iterrows():
        print(f"  {row['error_type']:>25}: {row['count']:>6} ({row['percentage']:.1f}%)")

    # 模块统计
    modules = module_stats(error_df)
    print(f"\n模块统计:")
    for _, row in modules.iterrows():
        print(f"  {row['module']:>10}: {row['count']:>6} ({row['percentage']:.1f}%)")

    print("=" * 60)


if __name__ == '__main__':
    main()
