"""日志解析模块 - Apache 错误日志正则解析与字段提取"""

import re
import pandas as pd

PATTERN = r'\[([^\]]+)\]\s+\[([^\]]+)\]\s+(.*)'

MONTH_MAP = {
    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
    'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
    'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
}


def parse_log_line(line: str) -> dict | None:
    """
    解析单行日志

    Args:
        line: 原始日志行

    Returns:
        dict: {'timestamp': str, 'level': str, 'content': str}
        None: 格式异常行
    """
    line = line.strip()
    if not line:
        return None
    match = re.match(PATTERN, line)
    if not match:
        return None
    return {
        'timestamp': match.group(1),
        'level': match.group(2),
        'content': match.group(3)
    }


def parse_log_file(filepath: str) -> pd.DataFrame:
    """
    解析整个日志文件

    Args:
        filepath: 日志文件路径

    Returns:
        DataFrame: 包含 timestamp, level, content 三列
    """
    records = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            result = parse_log_line(line)
            if result is not None:
                records.append(result)
    return pd.DataFrame(records, columns=['timestamp', 'level', 'content'])


def convert_date(timestamp: str) -> str:
    """
    日期格式转换

    Args:
        timestamp: 原始时间戳 'Thu Jun 09 06:07:04 2005'

    Returns:
        str: 转换后日期 '2005-06-09'
    """
    parts = timestamp.split()
    return f"{parts[4]}-{MONTH_MAP[parts[1]]}-{parts[2].zfill(2)}"
