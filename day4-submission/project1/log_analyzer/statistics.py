"""统计口径集中定义，避免报告和图表各算一遍。"""

from __future__ import annotations

import pandas as pd


def daily_error_stats(frame: pd.DataFrame) -> pd.DataFrame:
    errors = frame.loc[frame["level"] == "error"].copy()
    errors["date"] = pd.to_datetime(errors["timestamp"]).dt.date.astype(str)
    return errors.groupby("date", as_index=False).size().rename(columns={"size": "error_count"})


def error_type_stats(frame: pd.DataFrame) -> pd.DataFrame:
    errors = frame.loc[frame["level"] == "error"].copy()
    errors["error_type"] = errors["error_code"].map(
        lambda value: f"error_state_{int(value)}" if pd.notna(value) else "other_error"
    )
    result = errors.groupby("error_type", as_index=False).size().rename(columns={"size": "count"})
    total = int(result["count"].sum())
    result["percentage"] = (result["count"] / total * 100).round(2) if total else 0.0
    return result.sort_values("count", ascending=False, ignore_index=True)


def module_error_stats(frame: pd.DataFrame) -> pd.DataFrame:
    """统计模块 Error 数与模块自身 Error 率。"""
    totals = frame.groupby("module", as_index=False).size().rename(columns={"size": "total_count"})
    errors = (
        frame.loc[frame["level"] == "error"]
        .groupby("module", as_index=False)
        .size()
        .rename(columns={"size": "error_count"})
    )
    result = totals.merge(errors, on="module", how="left")
    result["error_count"] = result["error_count"].fillna(0).astype(int)
    result["error_rate"] = result["error_count"] / result["total_count"]
    return result.sort_values("error_count", ascending=False, ignore_index=True)
