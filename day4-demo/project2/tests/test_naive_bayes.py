"""
测试朴素贝叶斯分类器模块
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.naive_bayes import NaiveBayesClassifier


def test_naive_bayes_train():
    """测试朴素贝叶斯训练"""
    classifier = NaiveBayesClassifier()

    texts = ['free entry win prize', 'hello how are you', 'win cash now', 'good morning friend']
    labels = ['spam', 'ham', 'spam', 'ham']

    classifier.train(texts, labels)

    assert classifier.is_trained, "模型应该已训练"
    assert classifier.model is not None, "模型不应为None"


def test_naive_bayes_predict():
    """测试朴素贝叶斯预测"""
    classifier = NaiveBayesClassifier()

    texts = ['free entry win prize', 'hello how are you', 'win cash now', 'good morning friend']
    labels = ['spam', 'ham', 'spam', 'ham']

    classifier.train(texts, labels)

    # 预测
    result = classifier.predict('free win prize')
    assert result in ['ham', 'spam'], f"预测结果应为ham或spam，实际{result}"


def test_naive_bayes_predict_batch():
    """测试朴素贝叶斯批量预测"""
    classifier = NaiveBayesClassifier()

    texts = ['free entry win prize', 'hello how are you', 'win cash now', 'good morning friend']
    labels = ['spam', 'ham', 'spam', 'ham']

    classifier.train(texts, labels)

    # 批量预测
    test_texts = ['free win', 'hello friend']
    results = classifier.predict_batch(test_texts)

    assert len(results) == 2, f"应返回2个预测，实际{len(results)}"
    assert all(r in ['ham', 'spam'] for r in results), "预测结果应为ham或spam"


def test_naive_bayes_not_trained():
    """测试未训练时预测"""
    classifier = NaiveBayesClassifier()

    try:
        classifier.predict('test')
        assert False, "应抛出异常"
    except ValueError as e:
        assert '尚未训练' in str(e), f"错误信息不正确: {e}"


def test_naive_bayes_feature_importance():
    """测试特征重要性"""
    classifier = NaiveBayesClassifier()

    texts = [
        'free entry win prize cash',
        'hello how are you today',
        'win cash prize now',
        'good morning friend'
    ]
    labels = ['spam', 'ham', 'spam', 'ham']

    classifier.train(texts, labels)

    importance = classifier.get_feature_importance(top_n=5)

    assert 'spam_features' in importance, "缺少spam_features"
    assert 'ham_features' in importance, "缺少ham_features"
    assert len(importance['spam_features']) <= 5, "spam特征数量应<=5"
    assert len(importance['ham_features']) <= 5, "ham特征数量应<=5"
