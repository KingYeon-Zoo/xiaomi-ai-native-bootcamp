from pathlib import Path

from main import run


def test_small_realistic_flow_generates_all_required_outputs(tmp_path: Path, monkeypatch):
    source = tmp_path / "Apache.log"
    source.write_text(
        "[Thu Jun 09 06:07:04 2005] [notice] LDAP: ready\n"
        "[Thu Jun 09 06:07:20 2005] [error] mod_jk child workerEnv in error state 6\n"
        "[Thu Jun 09 06:08:20 2005] [warn] child process still did not exit\n",
        encoding="utf-8",
    )
    import main

    monkeypatch.setattr(main, "ROOT", tmp_path)
    result = run(source)
    assert result == {"parsed": 3, "invalid": 0, "errors": 1}
    for relative in [
        "outputs/structured_logs.csv",
        "outputs/error_level_logs.csv",
        "outputs/error_state_logs.csv",
        "outputs/keyword_logs.csv",
        "outputs/error_code_reference.csv",
        "charts/daily_error_trend.png",
        "charts/error_type_distribution.png",
        "charts/module_error_comparison.png",
        "analysis_report.md",
    ]:
        assert (tmp_path / relative).is_file(), relative

