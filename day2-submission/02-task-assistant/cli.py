#!/usr/bin/env python3
"""Day2 学习任务清单助手。"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence


TASKS = {
    "spec.md": "需求规格",
    "plan.md": "技术设计",
    "tasks.md": "任务拆解",
    "README.md": "项目说明",
    "ai-log.md": "AI 协作日志",
}


@dataclass(frozen=True)
class CommandResult:
    message: str
    exit_code: int = 0


def status_path() -> Path:
    override = os.environ.get("DAY2_STATUS_FILE")
    return Path(override) if override else Path(__file__).with_name("status.json")


def save_status(status: dict[str, bool], path: Optional[Path] = None) -> None:
    target = path or status_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def initial_status() -> dict[str, bool]:
    return {filename: False for filename in TASKS}


def load_status(path: Optional[Path] = None) -> dict[str, bool]:
    target = path or status_path()
    if not target.exists():
        status = initial_status()
        save_status(status, target)
        return status
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
        valid = (
            isinstance(data, dict)
            and set(data) == set(TASKS)
            and all(isinstance(value, bool) for value in data.values())
        )
        if not valid:
            raise ValueError("字段不完整")
        return data
    except (OSError, json.JSONDecodeError, ValueError):
        print("⚠️ 状态文件损坏或字段不完整，已重新初始化")
        status = initial_status()
        save_status(status, target)
        return status


def submit_task(filename: str, path: Optional[Path] = None) -> CommandResult:
    canonical = next((task for task in TASKS if task.lower() == filename.lower()), None)
    if canonical is None:
        return CommandResult(f"❌ {filename} 不在任务清单中", 2)
    status = load_status(path)
    if status[canonical]:
        return CommandResult(f"ℹ️ {canonical} 已提交过", 1)
    status[canonical] = True
    save_status(status, path)
    return CommandResult(f"✅ {canonical} 已提交")


def remaining_tasks(path: Optional[Path] = None) -> list[str]:
    status = load_status(path)
    return [filename for filename in TASKS if not status[filename]]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Day2 学习任务清单助手")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("today", help="查看任务列表")
    submit = subparsers.add_parser("submit", help="标记文件已提交")
    submit.add_argument("filename")
    subparsers.add_parser("check", help="查看未提交文件")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 2
    if args.command == "today":
        status = load_status()
        print("Day2 学习任务清单：")
        for filename, description in TASKS.items():
            mark = "✅" if status[filename] else "⬜"
            print(f"  {mark} {filename}: {description}")
        return 0
    if args.command == "submit":
        result = submit_task(args.filename)
        print(result.message)
        return result.exit_code
    remaining = remaining_tasks()
    if not remaining:
        print("🎉 全部完成！")
    else:
        print("未提交的文件：")
        for filename in remaining:
            print(f"  - {filename}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
