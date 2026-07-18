"""
朴素贝叶斯分类器模块

使用scikit-learn的CountVectorizer + MultinomialNB
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np


class NaiveBayesClassifier:
    """朴素贝叶斯分类器"""

    def __init__(self):
        """初始化分类器"""
        self.vectorizer = CountVectorizer(max_features=5000)
        self.model = MultinomialNB()
        self.is_trained = False

    def train(self, texts: list, labels: list):
        """
        训练模型

        Args:
            texts: 文本列表
            labels: 标签列表
        """
        # 转换为数值特征
        X = self.vectorizer.fit_transform(texts)

        # 训练模型
        self.model.fit(X, labels)
        self.is_trained = True

    def predict(self, text: str) -> str:
        """
        预测单个样本

        Args:
            text: 文本

        Returns:
            str: 'ham' 或 'spam'
        """
        if not self.is_trained:
            raise ValueError("模型尚未训练，请先调用train()方法")

        X = self.vectorizer.transform([text])
        return self.model.predict(X)[0]

    def predict_batch(self, texts: list) -> list:
        """
        批量预测

        Args:
            texts: 文本列表

        Returns:
            list: 预测结果列表
        """
        if not self.is_trained:
            raise ValueError("模型尚未训练，请先调用train()方法")

        X = self.vectorizer.transform(texts)
        return self.model.predict(X).tolist()

    def get_feature_importance(self, top_n: int = 20) -> dict:
        """
        获取特征重要性

        Args:
            top_n: 返回前N个重要特征

        Returns:
            dict: 特征重要性字典
        """
        if not self.is_trained:
            raise ValueError("模型尚未训练，请先调用train()方法")

        feature_names = self.vectorizer.get_feature_names_out()
        log_probs = self.model.feature_log_prob_

        # 计算spam和ham的特征差异
        spam_probs = log_probs[1]  # spam类的对数概率
        ham_probs = log_probs[0]   # ham类的对数概率

        # 差异越大，该特征对分类越重要
        diff = spam_probs - ham_probs

        # 获取top_n个最重要的特征
        top_indices = np.argsort(diff)[-top_n:][::-1]

        return {
            'spam_features': [(feature_names[i], diff[i]) for i in top_indices],
            'ham_features': [(feature_names[i], diff[i]) for i in np.argsort(diff)[:top_n]]
        }
