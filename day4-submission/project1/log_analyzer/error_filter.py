"""三种彼此独立、口径明确的异常筛选。"""

from __future__ import annotations

import re
from collections.abc import Iterable

import pandas as pd


def filter_by_level(frame: pd.DataFrame, level: str = "error") -> pd.DataFrame:
    """按日志级别精确筛选，比较时忽略大小写。"""
    mask = frame["level"].astype("string").str.casefold() == level.casefold()
    return frame.loc[mask].copy().reset_index(drop=True)


def filter_by_error_state(frame: pd.DataFrame) -> pd.DataFrame:
    """筛选实际出现 ``error state N``、因此 ``error_code`` 非空的记录。"""
    return frame.loc[frame["error_code"].notna()].copy().reset_index(drop=True)


def filter_by_keywords(frame: pd.DataFrame, keywords: Iterable[str]) -> pd.DataFrame:
    """按任一关键词作不区分大小写的字面量匹配。"""
    normalized = [word.strip() for word in keywords if word and word.strip()]
    if not normalized:
        return frame.iloc[0:0].copy()
    pattern = "|".join(re.escape(word) for word in normalized)
    mask = frame["content"].astype("string").str.contains(pattern, case=False, na=False)
    return frame.loc[mask].copy().reset_index(drop=True)

