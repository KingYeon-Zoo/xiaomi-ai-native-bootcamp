"""统计分析模块 - 多维度统计 error 日志"""

import pandas as pd
from log_parser import convert_date


def daily_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    每日错误数量统计

    Args:
        df: error_logs DataFrame (timestamp, content, error_type, module)

    Returns:
        DataFrame: 包含 date, count 列，按日期排序
    """
    df = df.copy()
    df['date'] = df['timestamp'].apply(convert_date)
    daily = df.groupby('date').size().reset_index(name='count')
    daily = daily.sort_values('date').reset_index(drop=True)
    return daily


def type_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    错误类型统计

    Args:
        df: error_logs DataFrame

    Returns:
        DataFrame: 包含 error_type, count, percentage 列，按数量降序
    """
    type_counts = df['error_type'].value_counts().reset_index()
    type_counts.columns = ['error_type', 'count']
    type_counts['percentage'] = (type_counts['count'] / type_counts['count'].sum() * 100).round(2)
    return type_counts.reset_index(drop=True)


def module_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    模块维度统计

    Args:
        df: error_logs DataFrame

    Returns:
        DataFrame: 包含 module, count, percentage 列，按数量降序
    """
    module_counts = df['module'].value_counts().reset_index()
    module_counts.columns = ['module', 'count']
    module_counts['percentage'] = (module_counts['count'] / module_counts['count'].sum() * 100).round(2)
    return module_counts.reset_index(drop=True)
