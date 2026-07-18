#!/usr/bin/env python3
"""提交检查助手：检查文件、运行测试并生成可追溯报告。"""

from __future__ import annotations

import argparse
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass
class FileCheckResult:
    missing_files: list[str]
    warnings: list[str]
    details: dict[str, str]


@dataclass
class TestRunResult:
    passed_tests: list[dict[str, Any]]
    failed_tests: list[dict[str, Any]]


def check_files(project_dir: Path, required_files: Iterable[str]) -> FileCheckResult:
    """检查必需文件，并对 README 与 AI 日志进行轻量字段检查。"""
    project_dir = project_dir.resolve()
    missing: list[str] = []
    warnings: list[str] = []
    details: dict[str, str] = {}
    for relative in required_files:
        path = project_dir / relative
        if not path.is_file():
            missing.append(relative)
            details[relative] = "缺失"
            continue
        details[relative] = "存在"
        content = path.read_text(encoding="utf-8", errors="replace")
        name = path.name.lower()
        if name == "readme.md":
            absent = [word for word in ("安装", "运行", "测试") if word not in content]
            if absent:
                warnings.append(f"{relative} 缺少线索：{', '.join(absent)}")
        if name == "ai-log.md":
            absent = [word for word in ("目的", "输入", "建议", "人工判断", "验证") if word not in content]
            if absent:
                warnings.append(f"{relative} 缺少字段：{', '.join(absent)}")
    return FileCheckResult(missing, warnings, details)


def run_tests(project_dir: Path, test_commands: Iterable[dict[str, Any]], timeout_seconds: int = 60) -> TestRunResult:
    """顺序执行测试命令；不使用 shell，超时和非零退出均记录为失败。"""
    passed: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    for item in test_commands:
        name = str(item["name"])
        command = list(item["command"])
        try:
            completed = subprocess.run(command, cwd=project_dir, capture_output=True, text=True, timeout=timeout_seconds, check=False)
            evidence = {"name": name, "command": command, "exit_code": completed.returncode, "stdout": completed.stdout.strip(), "stderr": completed.stderr.strip()}
            if completed.returncode == 0:
                passed.append(evidence)
            else:
                evidence["reason"] = f"退出码 {completed.returncode}"
                failed.append(evidence)
        except subprocess.TimeoutExpired:
            failed.append({"name": name, "command": command, "reason": "测试超时"})
        except OSError as exc:
            failed.append({"name": name, "command": command, "reason": f"无法执行：{exc}"})
    return TestRunResult(passed, failed)


def evaluate_status(files: FileCheckResult, tests: TestRunResult) -> str:
    """按 BLOCKED > WARNING > PASS 的优先级判断状态。"""
    if files.missing_files or tests.failed_tests:
        return "BLOCKED"
    if files.warnings:
        return "WARNING"
    return "PASS"


def write_reports(evidence_dir: Path, files: FileCheckResult, tests: TestRunResult, status: str) -> None:
    """写文件、测试和最终三份 Markdown 证据。"""
    evidence_dir.mkdir(parents=True, exist_ok=True)
    file_lines = ["# 文件检查证据", "", f"缺失：{files.missing_files or '无'}", ""]
    file_lines.extend(f"- {item}" for item in files.warnings or ["无质量警告"])
    (evidence_dir / "file-check.md").write_text("\n".join(file_lines) + "\n", encoding="utf-8")
    test_lines = ["# 测试结果证据", ""]
    test_lines.extend(f"- PASS：{item['name']}" for item in tests.passed_tests)
    test_lines.extend(f"- FAIL：{item['name']}（{item['reason']}）" for item in tests.failed_tests)
    if len(test_lines) == 2:
        test_lines.append("- 未配置测试命令")
    (evidence_dir / "test-result.md").write_text("\n".join(test_lines) + "\n", encoding="utf-8")
    next_step = {"PASS": "可以提交并保留本报告。", "WARNING": "补齐文档线索后重新检查。", "BLOCKED": "补齐文件或修复失败测试后重新检查。"}[status]
    final = f"# 提交检查最终报告\n\n- 文件检查：缺失 {len(files.missing_files)} 项，警告 {len(files.warnings)} 项\n- 测试结果：通过 {len(tests.passed_tests)} 项，失败 {len(tests.failed_tests)} 项\n- 综合状态：**{status}**\n- 下一步：{next_step}\n"
    (evidence_dir / "final-report.md").write_text(final, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="提交检查助手")
    parser.add_argument("project_dir", type=Path)
    parser.add_argument("--required-file", action="append", default=[])
    parser.add_argument("--test-command", action="append", default=[], help="不经 shell 执行的测试命令，可重复传入")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--evidence-dir", default=".submission-check")
    args = parser.parse_args()
    project_dir = args.project_dir.resolve()
    if not project_dir.is_dir():
        print("BLOCKED：项目目录不存在")
        return 2
    commands = [{"name": f"测试 {index}", "command": shlex.split(command)} for index, command in enumerate(args.test_command, 1)]
    files = check_files(project_dir, args.required_file)
    tests = run_tests(project_dir, commands, args.timeout)
    status = evaluate_status(files, tests)
    write_reports(project_dir / args.evidence_dir, files, tests, status)
    print(f"综合状态：{status}")
    return {"PASS": 0, "WARNING": 1, "BLOCKED": 2}[status]


if __name__ == "__main__":
    raise SystemExit(main())
