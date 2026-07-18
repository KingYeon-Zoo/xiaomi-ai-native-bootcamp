"""可视化模块 - 生成三种图表：时序图、饼图、柱状图"""

import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False


def plot_daily_trend(df: pd.DataFrame, output_path: str):
    """
    绘制每日错误趋势时序图

    Args:
        df: daily_stats DataFrame (date, count)
        output_path: PNG 文件保存路径
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    dates = pd.to_datetime(df['date'])
    ax.plot(dates, df['count'], linewidth=0.8, color='#2196F3')

    ax.set_title('Apache Error Log - Daily Trend', fontsize=14)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Error Count', fontsize=12)

    # X 轴每 30 天一个刻度
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=30))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45, ha='right')

    ax.grid(True, alpha=0.3)
    ax.set_xlim(dates.min(), dates.max())

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def plot_error_types(df: pd.DataFrame, output_path: str):
    """
    绘制错误类型占比饼图

    Args:
        df: type_stats DataFrame (error_type, count, percentage)
        output_path: PNG 文件保存路径
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # 占比 < 2% 的合并为"其他"
    main_types = df[df['percentage'] >= 2].copy()
    other_count = df[df['percentage'] < 2]['count'].sum()

    if other_count > 0:
        other_row = pd.DataFrame({
            'error_type': ['Other'],
            'count': [other_count],
            'percentage': [round(other_count / df['count'].sum() * 100, 2)]
        })
        main_types = pd.concat([main_types, other_row], ignore_index=True)

    colors = ['#F44336', '#2196F3', '#4CAF50', '#FFC107', '#9C27B0',
              '#00BCD4', '#FF9800', '#795548', '#607D8B', '#E91E63']

    wedges, texts, autotexts = ax.pie(
        main_types['count'],
        labels=main_types['error_type'],
        autopct='%1.1f%%',
        colors=colors[:len(main_types)],
        startangle=90,
        pctdistance=0.85
    )

    # 调整标签大小
    for text in texts:
        text.set_fontsize(9)
    for autotext in autotexts:
        autotext.set_fontsize(8)

    ax.set_title('Apache Error Log - Error Type Distribution', fontsize=14)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def plot_modules(df: pd.DataFrame, output_path: str):
    """
    绘制模块错误数量柱状图（对数坐标）

    Args:
        df: module_stats DataFrame (module, count)
        output_path: PNG 文件保存路径
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.bar(df['module'], df['count'], color=['#F44336', '#2196F3', '#4CAF50', '#FFC107'])

    ax.set_title('Apache Error Log - Module Error Distribution', fontsize=14)
    ax.set_xlabel('Module', fontsize=12)
    ax.set_ylabel('Error Count (log scale)', fontsize=12)

    # 对数坐标
    ax.set_yscale('log')

    # 显示数值标签
    for bar, count in zip(bars, df['count']):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f'{count:,}', ha='center', va='bottom', fontsize=10)

    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
