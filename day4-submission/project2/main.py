"""Project 2 可复现入口：加载、清洗、固定切分、分类、评估和报告。"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from spam_filter.evaluator import calculate_metrics, plot_confusion, plot_metrics, plot_word_frequency
from spam_filter.feature_extractor import extract_features
from spam_filter.naive_bayes import NaiveBayesClassifier
from spam_filter.rule_filter import RuleFilter
from spam_filter.text_cleaner import clean_text
from spam_filter.utils import load_email_archives

ROOT = Path(__file__).resolve().parent
DEFAULT_DATA_DIR = ROOT.parent.parent / "day4-data" / "project2"


def _metric_table(metrics: dict[str, object]) -> str:
    return " | ".join(f"{name}={metrics[name]:.4f}" for name in ["accuracy", "precision", "recall", "f1"])


def _sample_errors(test: pd.DataFrame, pred_column: str, actual: str, predicted: str) -> list[str]:
    rows = test.loc[(test["label"] == actual) & (test[pred_column] == predicted), "raw_message"].head(3)
    return [" ".join(str(value).split())[:140] for value in rows]


def _write_report(
    frame: pd.DataFrame,
    test: pd.DataFrame,
    rule_metrics: dict[str, object],
    nb_metrics: dict[str, object],
    failures: list[str],
    train_size: int,
) -> None:
    counts = frame["label"].value_counts().to_dict()
    empty_count = int((frame["cleaned_message"] == "").sum())
    rule_fp = _sample_errors(test, "rule_pred", "ham", "spam")
    rule_fn = _sample_errors(test, "rule_pred", "spam", "ham")
    nb_fp = _sample_errors(test, "nb_pred", "ham", "spam")
    nb_fn = _sample_errors(test, "nb_pred", "spam", "ham")
    report = f"""# 垃圾邮件智能过滤分析报告

## 1. 项目概述

本项目用同一测试集比较可解释规则与 `CountVectorizer + MultinomialNB`。报告数字由 `python main.py` 基于真实语料生成。

## 2. 数据探索

- 总邮件：{len(frame):,}；ham：{counts.get('ham', 0):,}；spam：{counts.get('spam', 0):,}。
- 解析告警：{len(failures)}；清洗后空文本：{empty_count}。

## 3. 文本清洗

依次执行小写、HTML 文本化、URL、邮箱、电话、标点、空白、停用词和空文本处理。空文本保留为空字符串，不删除样本或改标签。

## 4. 数据契约

`raw_message` 是 Subject + 正文，不含其余邮件头；`cleaned_message` 是模型输入。大写率、感叹号、数字和货币符号只从 raw 提取，关键词只从 cleaned 提取。

## 5. 特征提取

六类特征为消息长度、大写字母占比、感叹号数量、关键词命中、数字数量和货币符号数量。规则对计数设置上限，避免单一长邮件让得分无限增长。

## 6. 规则过滤

规则阈值固定为 5.0，没有使用最终测试集反复调参。测试集结果：{_metric_table(rule_metrics)}；混淆矩阵（行真实、列预测，ham/spam）：`{rule_metrics['confusion_matrix']}`。

## 7. 朴素贝叶斯

使用最多 12,000 个 unigram/bigram 特征与 `MultinomialNB(alpha=0.5)`。测试集结果：{_metric_table(nb_metrics)}；混淆矩阵：`{nb_metrics['confusion_matrix']}`。

## 8. 实验协议

使用 `train_test_split(test_size=0.2, random_state=42, stratify=y)`；训练 {train_size:,} 封、测试 {len(test):,} 封，两种方法共享完全相同的测试行。

## 9. 模型指标

朴素贝叶斯验收门槛为 Accuracy≥95%、spam Precision≥90%、spam Recall≥85%。是否达标由上述实际数字判断，不修改标签或测试集迎合门槛。

## 10. 混淆矩阵

四张图均由本次测试标签和预测直接生成；矩阵标签顺序固定为 `[ham, spam]`，避免类别排序导致 TP/FP 解释反转。

## 11. False Positive 分析

- 规则样例：`{rule_fp}`
- 朴素贝叶斯样例：`{nb_fp}`

正常邮件可能因营销词、金额或强烈标点被误判；这说明“像垃圾邮件”不等同于真实标签。

## 12. False Negative 分析

- 规则样例：`{rule_fn}`
- 朴素贝叶斯样例：`{nb_fn}`

隐晦表达、图片型内容或清洗后信息稀少会漏判。降低阈值虽能提高召回，但也可能增加正常邮件拦截成本。

## 13. 数据泄漏检查

Vectorizer 仅在训练集 `fit`，之后对测试集 `transform`；代码和集成测试检查 `fit_sample_count == train_size`。词频图只作离线说明，不参与模型训练。

## 14. 改进建议

下一步应使用独立验证集选择规则阈值与超参数，并按 `hard_ham`、时间批次分层报告，以观察分布漂移，而不是继续消费最终测试集。

## 15. 已知限制

语料来自 2003—2005 年，不能代表当代钓鱼与多语言邮件；附件和图片内容未做 OCR；随机分层切分不能替代跨时间外部验证。
"""
    (ROOT / "analysis_report.md").write_text(report, encoding="utf-8")


def run(archives: list[Path]) -> dict[str, object]:
    outputs, charts = ROOT / "outputs", ROOT / "charts"
    outputs.mkdir(exist_ok=True)
    charts.mkdir(exist_ok=True)
    frame, failures = load_email_archives(archives)
    if frame.empty:
        raise ValueError("未加载到邮件")
    frame["cleaned_message"] = frame["raw_message"].map(clean_text)

    train_indices, test_indices = train_test_split(
        frame.index, test_size=0.2, random_state=42, stratify=frame["label"]
    )
    frame["split"] = "train"
    frame.loc[test_indices, "split"] = "test"
    train = frame.loc[train_indices].copy()
    test = frame.loc[test_indices].copy()

    rule = RuleFilter(threshold=5.0)
    test["rule_pred"] = [
        rule.predict(extract_features(raw, cleaned))
        for raw, cleaned in zip(test["raw_message"], test["cleaned_message"])
    ]
    model = NaiveBayesClassifier().fit(train["cleaned_message"], train["label"])
    test["nb_pred"] = model.predict(test["cleaned_message"])

    rule_metrics = calculate_metrics(test["label"], test["rule_pred"])
    nb_metrics = calculate_metrics(test["label"], test["nb_pred"])
    frame.to_csv(outputs / "cleaned_data.csv", index=False)
    plot_confusion(rule_metrics, "规则过滤混淆矩阵", charts / "rule_confusion_matrix.png")
    plot_confusion(nb_metrics, "朴素贝叶斯混淆矩阵", charts / "nb_confusion_matrix.png")
    plot_metrics(rule_metrics, nb_metrics, charts / "model_metrics_comparison.png")
    plot_word_frequency(frame["cleaned_message"], frame["label"], charts / "word_frequency_comparison.png")
    _write_report(frame, test, rule_metrics, nb_metrics, failures, len(train))
    return {
        "total": len(frame),
        "train": len(train),
        "test": len(test),
        "parse_warnings": len(failures),
        "rule_metrics": rule_metrics,
        "nb_metrics": nb_metrics,
        "fit_sample_count": model.fit_sample_count,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="SpamAssassin 垃圾邮件过滤实验")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR, help="含六个 tar.bz2 的目录")
    args = parser.parse_args()
    archives = sorted(args.data_dir.glob("*.tar.bz2"))
    if len(archives) != 6:
        parser.error(f"预期 6 个 tar.bz2，实际找到 {len(archives)} 个：{args.data_dir}")
    result = run(archives)
    print(f"处理完成：total={result['total']}, train={result['train']}, test={result['test']}")
    print(f"规则：{_metric_table(result['rule_metrics'])}")
    print(f"朴素贝叶斯：{_metric_table(result['nb_metrics'])}")


if __name__ == "__main__":
    main()

