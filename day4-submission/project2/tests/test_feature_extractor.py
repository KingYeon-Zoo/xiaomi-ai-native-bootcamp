from spam_filter.feature_extractor import extract_features
from spam_filter.text_cleaner import clean_text


def test_raw_features_are_not_destroyed_by_cleaning():
    raw = "FREE!!! Pay $100 NOW"
    features = extract_features(raw, clean_text(raw))
    # FREE(4) + Pay(1) + NOW(3) / 10 个字母 = 0.8
    assert features["uppercase_ratio"] == 0.8
    assert features["exclamation_count"] == 3
    assert features["digit_count"] == 3
    assert features["currency_symbol_count"] == 1
    assert features["keyword_hits"] == 1


def test_keyword_matching_uses_word_boundaries():
    assert extract_features("carefree", "carefree")["keyword_hits"] == 0
