"""
特征提取模块

提供6个维度的特征提取功能
"""

import re
import pandas as pd


# 垃圾邮件关键词列表
SPAM_KEYWORDS = [
    'free', 'win', 'winner', 'won', 'prize', 'cash', 'urgent', 'offer',
    'limited', 'click', 'subscribe', 'buy', 'order', 'discount', 'save',
    'money', 'credit', 'loan', 'earn', 'income', 'profit', 'rich',
    'million', 'billion', 'congratulations', 'selected', 'chosen',
    'guarantee', 'guaranteed', 'no obligation', 'risk free', 'act now',
    'call now', 'apply now', 'sign up', 'join now', 'get started'
]


def extract_features(text: str) -> dict:
    """
    提取6个维度的特征

    Args:
        text: 清洗后的文本

    Returns:
        dict: 特征字典
        - length: 消息长度（字符数）
        - uppercase_ratio: 大写字母占比
        - exclamation_count: 感叹号数量
        - keyword_match: 关键词匹配数量
        - digit_count: 数字数量
        - currency_symbol: 货币符号数量
    """
    if not text or not isinstance(text, str):
        return {
            'length': 0,
            'uppercase_ratio': 0.0,
            'exclamation_count': 0,
            'keyword_match': 0,
            'digit_count': 0,
            'currency_symbol': 0
        }

    # 1. 消息长度
    length = len(text)

    # 2. 大写字母占比
    upper_count = sum(1 for c in text if c.isupper())
    total_alpha = sum(1 for c in text if c.isalpha())
    uppercase_ratio = upper_count / total_alpha if total_alpha > 0 else 0.0

    # 3. 感叹号数量
    exclamation_count = text.count('!')

    # 4. 关键词匹配数量
    text_lower = text.lower()
    keyword_match = sum(1 for keyword in SPAM_KEYWORDS if keyword in text_lower)

    # 5. 数字数量
    digit_count = sum(1 for c in text if c.isdigit())

    # 6. 货币符号数量
    currency_symbols = ['$', '£', '€', '¥', '₹']
    currency_symbol = sum(text.count(symbol) for symbol in currency_symbols)

    return {
        'length': length,
        'uppercase_ratio': uppercase_ratio,
        'exclamation_count': exclamation_count,
        'keyword_match': keyword_match,
        'digit_count': digit_count,
        'currency_symbol': currency_symbol
    }


def extract_features_batch(texts: list) -> pd.DataFrame:
    """
    批量提取特征

    Args:
        texts: 文本列表

    Returns:
        DataFrame: 特征数据框
    """
    features_list = [extract_features(text) for text in texts]
    return pd.DataFrame(features_list)
