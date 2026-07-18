"""
测试特征提取模块
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.feature_extractor import extract_features, extract_features_batch


def test_extract_features():
    """测试特征提取功能"""
    text = 'Free entry! Win $100 cash prize'
    features = extract_features(text)

    # 检查所有特征都存在
    assert 'length' in features, "缺少length特征"
    assert 'uppercase_ratio' in features, "缺少uppercase_ratio特征"
    assert 'exclamation_count' in features, "缺少exclamation_count特征"
    assert 'keyword_match' in features, "缺少keyword_match特征"
    assert 'digit_count' in features, "缺少digit_count特征"
    assert 'currency_symbol' in features, "缺少currency_symbol特征"

    # 检查特征值
    assert features['length'] > 0, "长度应大于0"
    assert features['exclamation_count'] == 1, f"感叹号数量应为1，实际{features['exclamation_count']}"
    assert features['keyword_match'] > 0, "应匹配到关键词"
    assert features['digit_count'] == 3, f"数字数量应为3，实际{features['digit_count']}"
    assert features['currency_symbol'] == 1, f"货币符号应为1，实际{features['currency_symbol']}"


def test_extract_features_empty():
    """测试空文本特征提取"""
    features = extract_features('')

    assert features['length'] == 0, "空文本长度应为0"
    assert features['uppercase_ratio'] == 0.0, "空文本大写占比应为0"
    assert features['exclamation_count'] == 0, "空文本感叹号应为0"
    assert features['keyword_match'] == 0, "空文本关键词应为0"
    assert features['digit_count'] == 0, "空文本数字应为0"
    assert features['currency_symbol'] == 0, "空文本货币符号应为0"


def test_extract_features_batch():
    """测试批量特征提取"""
    texts = [
        'Free entry! Win $100',
        'Hello, how are you?',
        'URGENT: You have won a prize!'
    ]

    features_df = extract_features_batch(texts)

    assert len(features_df) == 3, f"应返回3条特征，实际{len(features_df)}"
    assert 'length' in features_df.columns, "缺少length列"
    assert 'keyword_match' in features_df.columns, "缺少keyword_match列"


def test_extract_features_ham():
    """测试正常邮件特征"""
    text = 'Hello, how are you doing today?'
    features = extract_features(text)

    assert features['exclamation_count'] == 0, "正常邮件感叹号应为0"
    assert features['keyword_match'] == 0, "正常邮件关键词应为0"
    assert features['currency_symbol'] == 0, "正常邮件货币符号应为0"


def test_extract_features_spam():
    """测试垃圾邮件特征"""
    text = 'FREE!!! WIN $1000 CASH NOW!!! URGENT OFFER!!!'
    features = extract_features(text)

    assert features['exclamation_count'] > 0, "垃圾邮件应有感叹号"
    assert features['keyword_match'] > 0, "垃圾邮件应有关键词匹配"
    assert features['currency_symbol'] > 0, "垃圾邮件应有货币符号"
    assert features['uppercase_ratio'] > 0.5, "垃圾邮件大写占比应较高"
