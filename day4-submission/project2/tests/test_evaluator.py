from spam_filter.evaluator import calculate_metrics


def test_positive_label_and_confusion_matrix_order_are_explicit():
    metrics = calculate_metrics(
        ["ham", "ham", "spam", "spam"],
        ["ham", "spam", "spam", "spam"],
    )
    assert metrics["confusion_matrix"] == [[1, 1], [0, 2]]
    assert metrics["precision"] == 2 / 3
    assert metrics["recall"] == 1.0


def test_zero_positive_predictions_do_not_crash():
    metrics = calculate_metrics(["ham", "spam"], ["ham", "ham"])
    assert metrics["precision"] == 0.0
    assert metrics["recall"] == 0.0

