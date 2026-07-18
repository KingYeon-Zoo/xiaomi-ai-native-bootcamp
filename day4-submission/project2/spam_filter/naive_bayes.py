"""只允许在训练集 fit 的 CountVectorizer + MultinomialNB 封装。"""

from __future__ import annotations

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


class NaiveBayesClassifier:
    def __init__(self, max_features: int = 12_000) -> None:
        # min_df=1 使题目要求的小型 Smoke Test 也可训练；max_features 控制全量词表上限。
        self.vectorizer = CountVectorizer(max_features=max_features, min_df=1, ngram_range=(1, 2))
        self.model = MultinomialNB(alpha=0.5)
        self.is_fitted = False
        self.fit_sample_count = 0

    def fit(self, texts, labels) -> "NaiveBayesClassifier":
        matrix = self.vectorizer.fit_transform(texts)
        self.model.fit(matrix, labels)
        self.is_fitted = True
        self.fit_sample_count = matrix.shape[0]
        return self

    def predict(self, texts) -> list[str]:
        if not self.is_fitted:
            raise RuntimeError("模型尚未 fit")
        return self.model.predict(self.vectorizer.transform(texts)).tolist()
