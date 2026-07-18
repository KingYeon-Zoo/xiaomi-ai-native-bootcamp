"""Lesson 3: 可视化展示与报告

功能：
1. 加载统计数据
2. 调用 visualizer.py 生成图表到 output/charts/

支持两种导入方式:
- 从 log_analyzer 包导入（最终交付）
- 从 src/ 模块导入（开发阶段）
"""

import sys, os
# 项目根目录（log_analyzer 包所在位置）
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# src/ 目录（独立模块所在位置）
_SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _PROJECT_ROOT)
sys.path.insert(0, _SRC_DIR)

# 优先从 log_analyzer 包导入，回退到 src/ 模块
try:
    from log_analyzer.log_parser import parse_log_file
    from log_analyzer.error_filter import filter_errors
    from log_analyzer.statistics import daily_stats, type_stats, module_stats
    from log_analyzer.visualizer import plot_daily_trend, plot_error_types, plot_modules
except ImportError:
    from log_parser import parse_log_file
    from error_filter import filter_errors
    from statistics import daily_stats, type_stats, module_stats
    from visualizer import plot_daily_trend, plot_error_types, plot_modules


def main():
    """主函数"""
    output_dir = os.path.join(_PROJECT_ROOT, 'output')
    charts_dir = os.path.join(output_dir, 'charts')

    # 1. 加载数据并统计
    print("正在加载数据...")
    df = parse_log_file(os.path.join(_PROJECT_ROOT, 'Apache.log'))
    error_df = filter_errors(df)

    daily = daily_stats(error_df)
    types = type_stats(error_df)
    modules = module_stats(error_df)
    print(f"数据加载完成: {len(error_df)} 条 error 日志")

    # 2. 创建输出目录
    os.makedirs(charts_dir, exist_ok=True)

    # 3. 生成图表
    print("\n正在生成图表...")

    # 时序图
    trend_path = os.path.join(charts_dir, 'daily_trend.png')
    plot_daily_trend(daily, trend_path)
    print(f"  已生成: {trend_path}")

    # 饼图
    types_path = os.path.join(charts_dir, 'error_types.png')
    plot_error_types(types, types_path)
    print(f"  已生成: {types_path}")

    # 柱状图
    modules_path = os.path.join(charts_dir, 'modules.png')
    plot_modules(modules, modules_path)
    print(f"  已生成: {modules_path}")

    print("\n可视化完成!")
    print(f"图表保存目录: {charts_dir}")


if __name__ == '__main__':
    main()
