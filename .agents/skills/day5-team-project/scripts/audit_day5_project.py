#!/usr/bin/env python3
"""对 Day5-Day6 团队项目做只读静态审计。"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "README.md",
    "prototype/prototype-readme.md",
    "prototype/screenshots-or-video.md",
    "docs/diagnosis/problem-diagnosis.md",
    "docs/diagnosis/clarifying-questions.md",
    "docs/diagnosis/assumptions-and-non-goals.md",
    "docs/design/end-to-end-system-design.md",
    "docs/options/solution-options.md",
    "docs/options/tradeoff-matrix.md",
    "docs/options/rejected-options.md",
    "docs/decision/decision-memo.md",
    "docs/decision/final-recommendation.md",
    "docs/validation/validation-plan.md",
    "docs/validation/cases-and-results.md",
    "docs/validation/risk-and-edge-cases.md",
    "docs/validation/review-record.md",
    "docs/ai/ai-collaboration-log.md",
    "docs/ai/accepted-and-rejected-ai-advice.md",
    "docs/collaboration/role-division.md",
    "docs/collaboration/meeting-minutes.md",
    "docs/collaboration/decision-log.md",
    "docs/collaboration/issue-log.md",
    "docs/reflection/team-retrospective.md",
    "docs/reflection/individual-contributions.md",
    "docs/defense/defense-outline.md",
]

PLACEHOLDER_PATTERNS = [
    re.compile(r"【\s*(?:填写|待填写|补充)[^】]*】"),
    re.compile(r"\b(?:TODO|TBD|FIXME)\b", re.IGNORECASE),
    re.compile(r"^\s*-\s*(?:项目名称|运行或访问方式|打开方式|最终选择|选择原因)：\s*$", re.MULTILINE),
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def table_rows(text: str) -> list[str]:
    rows = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        if re.fullmatch(r"\|[\s:|-]+\|", stripped):
            continue
        rows.append(stripped)
    return rows


def nonempty_data_rows(text: str) -> list[str]:
    rows = table_rows(text)
    if rows:
        rows = rows[1:]
    return [
        row
        for row in rows
        if len([cell for cell in row.strip("|").split("|") if cell.strip()]) >= 2
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="Day5 项目根目录")
    args = parser.parse_args()
    root = args.project.expanduser().resolve()

    blocked: list[str] = []
    warnings: list[str] = []
    passes: list[str] = []

    if not root.is_dir():
        print(f"BLOCKED: 项目目录不存在：{root}")
        return 2

    if not (root / "src").is_dir():
        blocked.append("缺少 src/，无法确认原型源码位置")
    else:
        source_files = [p for p in (root / "src").rglob("*") if p.is_file() and p.name != ".gitkeep"]
        if source_files:
            passes.append(f"src/ 包含 {len(source_files)} 个文件")
        else:
            blocked.append("src/ 为空或只有占位文件")

    missing = [rel for rel in REQUIRED_FILES if not (root / rel).is_file()]
    if missing:
        blocked.extend(f"缺少必需文件：{rel}" for rel in missing)
    else:
        passes.append(f"{len(REQUIRED_FILES)} 个核心 Markdown 文件路径齐全")

    for rel in REQUIRED_FILES:
        path = root / rel
        if not path.is_file():
            continue
        text = read_text(path)
        if not text.strip():
            blocked.append(f"文件为空：{rel}")
            continue
        for pattern in PLACEHOLDER_PATTERNS:
            if pattern.search(text):
                warnings.append(f"疑似占位内容：{rel}")
                break
        empty_rows = sum(
            1
            for row in table_rows(text)
            if not any(cell.strip() for cell in row.strip("|").split("|"))
        )
        if empty_rows:
            warnings.append(f"存在 {empty_rows} 个全空表格行：{rel}")

    clarifying = root / "docs/diagnosis/clarifying-questions.md"
    if clarifying.is_file():
        text = read_text(clarifying)
        question_rows = re.findall(r"^\|\s*P[0-9]\s*\|", text, re.MULTILINE | re.IGNORECASE)
        p0_rows = re.findall(r"^\|\s*P0\s*\|", text, re.MULTILINE | re.IGNORECASE)
        if len(question_rows) < 10:
            warnings.append(f"澄清问题可识别行数为 {len(question_rows)}，要求至少 10")
        else:
            passes.append(f"澄清问题可识别行数：{len(question_rows)}")
        if len(p0_rows) < 3:
            warnings.append(f"P0 可识别行数为 {len(p0_rows)}，要求至少 3")
        else:
            passes.append(f"P0 可识别行数：{len(p0_rows)}")

    options = root / "docs/options/solution-options.md"
    if options.is_file():
        option_rows = [
            row
            for row in nonempty_data_rows(read_text(options))
            if re.search(r"(?:方案|路线)\s*[A-C一二三123]", row, re.IGNORECASE)
        ]
        if len(option_rows) < 3:
            warnings.append(f"可识别的本质方案行数为 {len(option_rows)}，要求至少 3")
        else:
            passes.append(f"可识别方案行数：{len(option_rows)}")

    meetings = root / "docs/collaboration/meeting-minutes.md"
    if meetings.is_file():
        meeting_count = len(
            re.findall(r"^#{2,4}\s+.*(?:会议|同步|复盘|站会)", read_text(meetings), re.MULTILINE)
        )
        if meeting_count < 4:
            warnings.append(f"可识别会议/同步节点为 {meeting_count}，要求至少 4 个真实节点")
        else:
            passes.append(f"可识别会议/同步节点：{meeting_count}")

    ai_log = root / "docs/ai/ai-collaboration-log.md"
    if ai_log.is_file():
        text = read_text(ai_log)
        categories = ["澄清", "对比", "反证", "实现", "验证", "Review"]
        covered = [category for category in categories if category.lower() in text.lower()]
        if len(covered) < 5:
            warnings.append(f"AI 六类关键词覆盖 {len(covered)}/6，要求至少 5 类真实记录")
        else:
            passes.append(f"AI 六类关键词覆盖 {len(covered)}/6；仍需人工核验真实性")
        if "反证" not in covered and "风险" not in text:
            warnings.append("未识别到 AI 反证或风险审查")

    rejected = root / "docs/ai/accepted-and-rejected-ai-advice.md"
    if rejected.is_file():
        rows = [
            row
            for row in nonempty_data_rows(read_text(rejected))
            if "拒绝" in row or "修改" in row
        ]
        if len(rows) < 2:
            warnings.append(f"可识别的 AI 拒绝/修改记录为 {len(rows)}，要求至少 2")
        else:
            passes.append(f"可识别 AI 拒绝/修改记录：{len(rows)}")

    results = root / "docs/validation/cases-and-results.md"
    if results.is_file() and len(nonempty_data_rows(read_text(results))) < 2:
        warnings.append("验证结果缺少可识别的实际执行记录")

    final_recommendation = root / "docs/decision/final-recommendation.md"
    if final_recommendation.is_file():
        body = re.sub(r"[#>*_`|\-\s]", "", read_text(final_recommendation))
        if len(body) > 800:
            warnings.append(f"最终建议约 {len(body)} 字符，课程要求 800 字以内")

    print(f"Day5 静态审计：{root}")
    for item in passes:
        print(f"PASS: {item}")
    for item in warnings:
        print(f"WARNING: {item}")
    for item in blocked:
        print(f"BLOCKED: {item}")

    print(
        f"SUMMARY: PASS={len(passes)} WARNING={len(warnings)} BLOCKED={len(blocked)}"
    )
    if blocked:
        return 2
    if warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
