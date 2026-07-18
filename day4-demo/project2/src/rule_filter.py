"""
规则过滤器模块

基于特征权重的规则过滤
"""

import pandas as pd


class RuleFilter:
    """规则过滤器"""

    def __init__(self, weights: dict = None, threshold: float = None):
        """
        初始化规则过滤器

        Args:
            weights: 特征权重字典
            threshold: 阈值
        """
        # 默认权重
        self.weights = weights or {
            'length': 0.01,
            'uppercase_ratio': 10,
            'exclamation_count': 2,
            'keyword_match': 5,
            'digit_count': 0.1,
            'currency_symbol': 3
        }

        # 默认阈值
        self.threshold = threshold or 15

    def predict(self, features: dict) -> str:
        """
        预测单个样本

        Args:
            features: 特征字典

        Returns:
            str: 'ham' 或 'spam'
        """
        score = 0.0

        for feature_name, weight in self.weights.items():
            if feature_name in features:
                score += features[feature_name] * weight

        return 'spam' if score >= self.threshold else 'ham'

    def predict_batch(self, features_df: pd.DataFrame) -> list:
        """
        批量预测

        Args:
            features_df: 特征数据框

        Returns:
            list: 预测结果列表
        """
        predictions = []
        for _, row in features_df.iterrows():
            features = row.to_dict()
            predictions.append(self.predict(features))
        return predictions

    def get_score(self, features: dict) -> float:
        """
        计算特征得分

        Args:
            features: 特征字典

        Returns:
            float: 得分
        """
        score = 0.0
        for feature_name, weight in self.weights.items():
            if feature_name in features:
                score += features[feature_name] * weight
        return score
