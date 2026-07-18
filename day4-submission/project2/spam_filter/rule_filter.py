"""可解释、有限幅的规则分类器。"""

from __future__ import annotations


class RuleFilter:
    """将六类特征转为分段分数，避免邮件长度一项无限支配结果。"""

    def __init__(self, threshold: float = 5.0) -> None:
        self.threshold = threshold

    def score(self, features: dict[str, float | int]) -> float:
        score = 0.0
        score += min(float(features.get("keyword_hits", 0)), 4.0) * 1.5
        score += 1.5 if float(features.get("uppercase_ratio", 0)) >= 0.30 else 0.0
        score += min(float(features.get("exclamation_count", 0)), 6.0) * 0.35
        score += min(float(features.get("currency_symbol_count", 0)), 3.0) * 0.75
        score += 0.75 if float(features.get("digit_count", 0)) >= 12 else 0.0
        score += 0.50 if float(features.get("message_length", 0)) >= 3000 else 0.0
        return score

    def predict(self, features: dict[str, float | int]) -> str:
        return "spam" if self.score(features) >= self.threshold else "ham"

