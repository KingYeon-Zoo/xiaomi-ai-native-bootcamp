import pandas as pd

from log_analyzer.statistics import daily_error_stats, error_type_stats, module_error_stats


def sample_frame():
    return pd.DataFrame(
        [
            {"timestamp": "2005-06-09 01:00:00", "level": "error", "module": "mod_jk", "error_code": 1},
            {"timestamp": "2005-06-09 02:00:00", "level": "notice", "module": "mod_jk", "error_code": pd.NA},
            {"timestamp": "2005-06-10 01:00:00", "level": "error", "module": "ldap", "error_code": pd.NA},
        ]
    )


def test_daily_and_type_stats_have_explicit_denominators():
    frame = sample_frame()
    assert daily_error_stats(frame)["error_count"].tolist() == [1, 1]
    types = error_type_stats(frame)
    assert types["count"].sum() == 2
    assert round(types["percentage"].sum(), 2) == 100.0


def test_module_stats_uses_each_modules_total_as_error_rate_denominator():
    stats = module_error_stats(sample_frame()).set_index("module")
    assert stats.loc["mod_jk", "error_count"] == 1
    assert stats.loc["mod_jk", "total_count"] == 2
    assert stats.loc["mod_jk", "error_rate"] == 0.5
    assert stats.loc["ldap", "error_count"] == 1
    assert stats.loc["ldap", "total_count"] == 1
    assert stats.loc["ldap", "error_rate"] == 1.0
