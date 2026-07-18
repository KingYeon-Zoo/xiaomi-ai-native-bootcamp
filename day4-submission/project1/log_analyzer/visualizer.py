"""从统计表生成三张确定性 PNG 图表。"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas as pd


def _configure_chinese_font() -> None:
    candidates = [
        Path("/System/Library/Fonts/STHeiti Light.ttc"),
        Path("/Library/Fonts/Arial Unicode.ttf"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    ]
    for candidate in candidates:
        if candidate.exists():
            font_manager.fontManager.addfont(candidate)
            plt.rcParams["font.family"] = font_manager.FontProperties(fname=candidate).get_name()
            break
    plt.rcParams["axes.unicode_minus"] = False


_configure_chinese_font()


def _save(fig: plt.Figure, path: str | Path) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_daily_error_trend(stats: pd.DataFrame, path: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(11, 5))
    dates = pd.to_datetime(stats["date"])
    ax.plot(dates, stats["error_count"], color="#f56600", linewidth=1.2)
    ax.set(title="Apache 每日 Error 趋势", xlabel="日期", ylabel="Error 数量")
    ax.grid(alpha=0.25)
    _save(fig, path)


def plot_error_type_distribution(stats: pd.DataFrame, path: str | Path) -> None:
    top = stats.head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(top["error_type"], top["count"], color="#ff8b3d")
    ax.set(title="Error 类型分布（Top 10）", xlabel="错误类型", ylabel="数量")
    ax.tick_params(axis="x", rotation=35)
    _save(fig, path)


def plot_module_error_comparison(stats: pd.DataFrame, path: str | Path) -> None:
    shown = stats.loc[stats["module"] != "unknown"].head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(shown["module"], shown["error_count"], color="#5f87ff")
    ax.set(title="已识别模块 Error 数量", xlabel="模块", ylabel="Error 数量")
    ax.tick_params(axis="x", rotation=30)
    _save(fig, path)
