from spam_filter.feature_extractor import extract_features
from spam_filter.rule_filter import RuleFilter
from spam_filter.text_cleaner import clean_text


def test_obvious_offer_is_spam_and_normal_note_is_ham():
    classifier = RuleFilter()
    spam = "URGENT!!! FREE prize, ACT NOW and click to win $500!!!"
    ham = "Hi team, the design review starts tomorrow morning."
    assert classifier.predict(extract_features(spam, clean_text(spam))) == "spam"
    assert classifier.predict(extract_features(ham, clean_text(ham))) == "ham"


def test_long_message_alone_cannot_dominate_score():
    raw = "project update " * 1000
    features = extract_features(raw, clean_text(raw))
    assert RuleFilter().predict(features) == "ham"

