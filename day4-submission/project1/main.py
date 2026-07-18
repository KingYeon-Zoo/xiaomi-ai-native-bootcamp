"""Project 1 可复现入口：解析、筛选、统计、绘图和报告。"""

from __future__ import annotations

import argparse
from contextlib import nullcontext
from pathlib import Path

import pandas as pd

from log_analyzer.error_filter import filter_by_error_state, filter_by_keywords, filter_by_level
from log_analyzer.log_parser import parse_log_file
from log_analyzer.statistics import daily_error_stats, error_type_stats, module_error_stats
from log_analyzer.utils import apache_log_from_archive
from log_analyzer.visualizer import (
    plot_daily_error_trend,
    plot_error_type_distribution,
    plot_module_error_comparison,
)

ROOT = Path(__file__).resolve().parent
DEFAULT_ARCHIVE = ROOT.parent.parent / "day4-data" / "project1" / "Apache.tar.gz"


def _write_report(frame: pd.DataFrame, invalid_count: int, module_stats: pd.DataFrame) -> None:
    error_rows = frame.loc[frame["level"] == "error"]
    state_rows = frame.loc[frame["error_code"].notna()]
    level_counts = frame["level"].value_counts().to_dict()
    top_module = module_stats.loc[module_stats["module"] != "unknown"].head(1)
    top_module_text = "无可识别模块"
    if not top_module.empty:
        row = top_module.iloc[0]
        top_module_text = f"{row['module']}（{int(row['error_count'])} 条 Error，模块 Error 率 {row['error_rate']:.2%}）"

    report = f"""# Apache HTTP 服务器日志分析报告

## 1. 项目概述

本报告由 `python main.py` 基于课程 Apache.log 实际生成，目标是把原始错误日志转换为可追溯的结构化结果，并定位主要故障现象。

## 2. 数据探索

- 成功解析：{len(frame):,} 行；非法或空行：{invalid_count:,} 行。
- 时间范围：{frame['timestamp'].min()} 至 {frame['timestamp'].max()}。
- 级别分布：`{level_counts}`。

## 3. 日志解析规则

每行必须同时具有时间戳、级别和内容；时间戳还需通过 `%a %b %d %H:%M:%S %Y` 校验。模块按固定词表、长词优先识别；错误码仅来自 `error state N`，不会从 PID、端口等普通数字误提取。

## 4. 异常识别结果

- `level=error`：{len(error_rows):,} 行。
- 含 `error state N`：{len(state_rows):,} 行。
- 三类筛选分别输出 CSV，避免把“error 级别”“error state”和“关键词命中”混成同一口径。

## 5. 统计分析结果

已识别模块中 Error 数最高的是 {top_module_text}。模块 Error 率定义为“该模块 Error 日志数 / 该模块全部日志数”，而不是该模块占全部 Error 的份额。

## 6. 可视化分析

三张图分别消费每日统计、错误类型统计和模块统计表；图表不在绘图函数内重新聚合，因此数字与 CSV/报告共用同一统计口径。

## 7. 故障原因推测

**事实**：日志中存在大量 error 级别记录及 `error state N`。**推测**：高频模块可能存在后端连接、初始化或配置问题。仅凭日志文本无法证明根因，需要结合对应时间段的服务配置、后端健康状态和请求链路验证。

## 8. 优化建议

优先按模块 Error 率与绝对数量的交叉结果排查；为高频 `error state` 建立运行手册；上线时增加请求量作为归一化分母，避免把流量增长误判为稳定性下降。

## 9. 已知限制

模块识别依赖题目词表；`unknown` 不等于无模块，只表示文本未命中词表。当前数据只有 Apache error log，不能单独完成因果归因。
"""
    (ROOT / "analysis_report.md").write_text(report, encoding="utf-8")


def run(log_path: Path) -> dict[str, int]:
    outputs, charts = ROOT / "outputs", ROOT / "charts"
    outputs.mkdir(exist_ok=True)
    charts.mkdir(exist_ok=True)

    frame, invalid_count = parse_log_file(log_path)
    if frame.empty:
        raise ValueError("未解析到有效 Apache 日志")

    error_level = filter_by_level(frame)
    error_state = filter_by_error_state(frame)
    keyword_rows = filter_by_keywords(frame, ["failed", "error", "denied", "unable"])
    daily = daily_error_stats(frame)
    types = error_type_stats(frame)
    modules = module_error_stats(frame)

    frame.to_csv(outputs / "structured_logs.csv", index=False)
    error_level.to_csv(outputs / "error_level_logs.csv", index=False)
    error_state.to_csv(outputs / "error_state_logs.csv", index=False)
    keyword_rows.to_csv(outputs / "keyword_logs.csv", index=False)
    reference = (
        error_state.groupby("error_code", as_index=False)
        .agg(count=("content", "size"), example=("content", "first"))
        .sort_values("error_code")
    )
    reference.to_csv(outputs / "error_code_reference.csv", index=False)

    plot_daily_error_trend(daily, charts / "daily_error_trend.png")
    plot_error_type_distribution(types, charts / "error_type_distribution.png")
    plot_module_error_comparison(modules, charts / "module_error_comparison.png")
    _write_report(frame, invalid_count, modules)
    return {"parsed": len(frame), "invalid": invalid_count, "errors": len(error_level)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Apache 日志智能清洗与故障分析")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--log", type=Path, help="已解压的 Apache.log")
    source.add_argument("--archive", type=Path, help="课程 Apache.tar.gz")
    args = parser.parse_args()

    if args.log:
        context = nullcontext(args.log)
    else:
        archive = args.archive or DEFAULT_ARCHIVE
        if not archive.exists():
            parser.error("未找到数据；请使用 --archive /path/to/Apache.tar.gz 或 --log /path/to/Apache.log")
        context = apache_log_from_archive(archive)

    with context as log_path:
        result = run(Path(log_path))
    print(f"处理完成：{result}")


if __name__ == "__main__":
    main()

