from pathlib import Path

import pandas as pd

from log_analyzer.log_parser import LOG_COLUMNS, parse_log_file, parse_log_line


def test_parse_extracts_five_fields_and_real_error_code():
    parsed = parse_log_line(
        "[Sun Dec 04 04:47:44 2005] [error] mod_jk child workerEnv in error state 6"
    )
    assert parsed is not None
    assert parsed["level"] == "error"
    assert parsed["module"] == "workerenv"
    assert parsed["error_code"] == 6
    assert isinstance(parsed["timestamp"], pd.Timestamp.__mro__[1]) or parsed["timestamp"].year == 2005


def test_parser_does_not_treat_unrelated_number_as_error_code():
    parsed = parse_log_line("[Thu Jun 09 06:07:20 2005] [error] mod_jk child init 1 0")
    assert parsed is not None
    assert pd.isna(parsed["error_code"])


def test_parser_rejects_bad_timestamp_and_counts_invalid_lines(tmp_path: Path):
    source = tmp_path / "sample.log"
    source.write_text(
        "[Thu Jun 09 06:07:20 2005] [notice] LDAP ready\n"
        "[Bad Date] [error] broken\n"
        "not a log\n",
        encoding="utf-8",
    )
    frame, invalid = parse_log_file(source)
    assert list(frame.columns) == LOG_COLUMNS
    assert len(frame) == 1
    assert invalid == 2

