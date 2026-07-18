"""Day2 固定任务的状态管理工具。"""

from __future__ import annotations

import json
import os
from pathlib import Path


TASKS = {
    "spec.md": "需求规格",
    "plan.md": "技术设计",
    "tasks.md": "任务拆解",
    "README.md": "项目说明",
    "ai-log.md": "AI 协作日志",
}


def status_path() -> Path:
    override = os.environ.get("AGENT_STATUS_FILE")
    return Path(override) if override else Path(__file__).resolve().parents[1] / "data" / "status.json"


def load_status() -> dict[str, bool]:
    path = status_path()
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if set(data) == set(TASKS) and all(isinstance(value, bool) for value in data.values()):
                return data
        except (OSError, json.JSONDecodeError, TypeError):
            pass
    return {filename: False for filename in TASKS}


def save_status(status: dict[str, bool]) -> None:
    path = status_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def task_today() -> dict:
    status = load_status()
    tasks = [{"file": filename, "description": description, "submitted": status[filename]} for filename, description in TASKS.items()]
    return {"success": True, "tasks": tasks}


def task_submit(filename: str) -> dict:
    canonical = next((task for task in TASKS if task.lower() == filename.lower()), None)
    if canonical is None:
        return {"success": False, "message": f"{filename} 不在任务清单中"}
    status = load_status()
    if status[canonical]:
        return {"success": False, "message": f"{canonical} 已提交过"}
    status[canonical] = True
    save_status(status)
    return {"success": True, "message": f"{canonical} 已提交"}


def task_check() -> dict:
    status = load_status()
    remaining = [filename for filename in TASKS if not status[filename]]
    message = "全部完成！" if not remaining else f"还有 {len(remaining)} 个文件未提交"
    return {"success": True, "remaining": remaining, "message": message}

