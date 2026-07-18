"""最小使用示例：展示同一邮件的 raw/cleaned 特征与两种规则结果。"""

from spam_filter.feature_extractor import extract_features
from spam_filter.rule_filter import RuleFilter
from spam_filter.text_cleaner import clean_text

raw = "URGENT! You WIN a FREE $500 prize. Click now!"
cleaned = clean_text(raw)
features = extract_features(raw, cleaned)
print({"raw_message": raw, "cleaned_message": cleaned, "features": features})
print({"rule_prediction": RuleFilter().predict(features)})

