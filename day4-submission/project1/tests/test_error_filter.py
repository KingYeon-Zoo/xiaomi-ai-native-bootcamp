import pandas as pd

from log_analyzer.error_filter import filter_by_error_state, filter_by_keywords, filter_by_level


def sample_frame():
    return pd.DataFrame(
        [
            {"level": "error", "error_code": 6, "content": "Backend FAILED", "module": "mod_jk"},
            {"level": "notice", "error_code": pd.NA, "content": "ready", "module": "ldap"},
            {"level": "warn", "error_code": pd.NA, "content": "a.b literal", "module": "unknown"},
        ]
    )


def test_three_filters_keep_independent_semantics():
    frame = sample_frame()
    assert len(filter_by_level(frame)) == 1
    assert len(filter_by_error_state(frame)) == 1
    assert len(filter_by_keywords(frame, ["failed"])) == 1


def test_keyword_filter_escapes_regex_and_empty_input_returns_empty():
    frame = sample_frame()
    assert len(filter_by_keywords(frame, ["a.b"])) == 1
    assert filter_by_keywords(frame, []).empty

