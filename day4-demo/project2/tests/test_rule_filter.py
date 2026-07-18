"""
测试规则过滤器模块
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rule_filter import RuleFilter


def test_rule_filter_predict():
    """测试规则过滤器预测"""
    rule_filter = RuleFilter()

    # 测试正常邮件
    features = {
        'length': 100,
        'uppercase_ratio': 0.1,
        'exclamation_count': 0,
        'keyword_match': 0,
        'digit_count': 5,
        'currency_symbol': 0
    }
    result = rule_filter.predict(features)
    assert result == 'ham', f"应预测为ham，实际{result}"

    # 测试垃圾邮件
    features = {
        'length': 200,
        'uppercase_ratio': 0.8,
        'exclamation_count': 5,
        'keyword_match': 3,
        'digit_count': 10,
        'currency_symbol': 2
    }
    result = rule_filter.predict(features)
    assert result == 'spam', f"应预测为spam，实际{result}"


def test_rule_filter_threshold():
    """测试阈值"""
    rule_filter = RuleFilter(threshold=10)

    # 边界情况
    features = {
        'length': 100,
        'uppercase_ratio': 0.5,
        'exclamation_count': 1,
        'keyword_match': 1,
        'digit_count': 5,
        'currency_symbol': 0
    }

    result = rule_filter.predict(features)
    assert result in ['ham', 'spam'], f"预测结果应为ham或spam，实际{result}"


def test_rule_filter_weights():
    """测试权重"""
    weights = {
        'length': 0.01,
        'uppercase_ratio': 10,
        'exclamation_count': 2,
        'keyword_match': 5,
        'digit_count': 0.1,
        'currency_symbol': 3
    }
    rule_filter = RuleFilter(weights=weights)

    features = {
        'length': 100,
        'uppercase_ratio': 0.1,
        'exclamation_count': 0,
        'keyword_match': 0,
        'digit_count': 5,
        'currency_symbol': 0
    }

    result = rule_filter.predict(features)
    assert result in ['ham', 'spam'], f"预测结果应为ham或spam，实际{result}"


def test_rule_filter_batch():
    """测试批量预测"""
    import pandas as pd

    rule_filter = RuleFilter()

    features_df = pd.DataFrame([
        {
            'length': 100,
            'uppercase_ratio': 0.1,
            'exclamation_count': 0,
            'keyword_match': 0,
            'digit_count': 5,
            'currency_symbol': 0
        },
        {
            'length': 200,
            'uppercase_ratio': 0.8,
            'exclamation_count': 5,
            'keyword_match': 3,
            'digit_count': 10,
            'currency_symbol': 2
        }
    ])

    predictions = rule_filter.predict_batch(features_df)
    assert len(predictions) == 2, f"应返回2个预测，实际{len(predictions)}"
    assert all(p in ['ham', 'spam'] for p in predictions), "预测结果应为ham或spam"


def test_rule_filter_score():
    """测试得分计算"""
    rule_filter = RuleFilter()

    features = {
        'length': 100,
        'uppercase_ratio': 0.5,
        'exclamation_count': 2,
        'keyword_match': 1,
        'digit_count': 10,
        'currency_symbol': 1
    }

    score = rule_filter.get_score(features)
    assert isinstance(score, float), f"得分应为float，实际{type(score)}"
    assert score >= 0, "得分应非负"
