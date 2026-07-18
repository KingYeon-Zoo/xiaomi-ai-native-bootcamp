"""统一计算指标并生成验收图表。"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score


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


def calculate_metrics(y_true, y_pred) -> dict[str, object]:
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, pos_label="spam", zero_division=0),
        "recall": recall_score(y_true, y_pred, pos_label="spam", zero_division=0),
        "f1": f1_score(y_true, y_pred, pos_label="spam", zero_division=0),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=["ham", "spam"]).tolist(),
    }


def _save(fig, path: str | Path) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_confusion(metrics: dict[str, object], title: str, path: str | Path) -> None:
    matrix = np.asarray(metrics["confusion_matrix"])
    fig, ax = plt.subplots(figsize=(5.5, 5))
    image = ax.imshow(matrix, cmap="Blues")
    fig.colorbar(image, ax=ax)
    ax.set(xticks=[0, 1], yticks=[0, 1], xticklabels=["ham", "spam"], yticklabels=["ham", "spam"])
    ax.set(title=title, xlabel="预测标签", ylabel="真实标签")
    for row in range(2):
        for col in range(2):
            ax.text(col, row, int(matrix[row, col]), ha="center", va="center")
    _save(fig, path)


def plot_metrics(rule: dict[str, object], nb: dict[str, object], path: str | Path) -> None:
    names = ["accuracy", "precision", "recall", "f1"]
    positions = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(positions - 0.18, [rule[name] for name in names], 0.36, label="规则")
    ax.bar(positions + 0.18, [nb[name] for name in names], 0.36, label="朴素贝叶斯")
    ax.set(xticks=positions, xticklabels=names, ylim=(0, 1.05), title="模型指标对比")
    ax.legend()
    _save(fig, path)


def plot_word_frequency(texts, labels, path: str | Path, top_n: int = 15) -> None:
    counters = {"ham": Counter(), "spam": Counter()}
    for text, label in zip(texts, labels):
        counters[label].update(str(text).split())
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    for ax, label, color in zip(axes, ["ham", "spam"], ["#5f87ff", "#f56600"]):
        pairs = counters[label].most_common(top_n)
        words, counts = zip(*pairs) if pairs else ([], [])
        ax.barh(words[::-1], counts[::-1], color=color)
        ax.set_title(f"{label} 高频词 Top {top_n}")
    _save(fig, path)
