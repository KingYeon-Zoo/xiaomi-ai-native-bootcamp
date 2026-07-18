from spam_filter.naive_bayes import NaiveBayesClassifier


def test_vectorizer_is_fitted_only_on_training_rows():
    train_texts = ["team meeting notes", "free cash prize", "project status", "urgent loan offer"]
    train_labels = ["ham", "spam", "ham", "spam"]
    model = NaiveBayesClassifier(max_features=100).fit(train_texts, train_labels)
    assert model.fit_sample_count == len(train_texts)
    assert len(model.predict(["free prize", "team notes"])) == 2


def test_predict_before_fit_fails_loudly():
    try:
        NaiveBayesClassifier().predict(["hello"])
    except RuntimeError as exc:
        assert "尚未 fit" in str(exc)
    else:
        raise AssertionError("未 fit 的模型不应静默预测")

