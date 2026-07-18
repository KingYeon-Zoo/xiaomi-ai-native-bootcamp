"""学习管理工具 — 管理 Day2 任务清单（today / submit / check）"""

import json
import os

TASKS = {
    "spec.md": "需求规格",
    "plan.md": "技术设计",
    "tasks.md": "任务拆解",
    "README.md": "项目说明",
    "ai-log.md": "AI 协作日志",
}

STATUS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "status.json")


def _load_status() -> dict:
    """加载 status.json，不存在或损坏时自动初始化"""
    if os.path.exists(STATUS_PATH):
        try:
            with open(STATUS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            # 校验格式
            if isinstance(data, dict) and all(k in data for k in TASKS):
                return data
        except (json.JSONDecodeError, KeyError):
            pass
    # 初始化
    return {f: False for f in TASKS}


def _save_status(status: dict):
    """保存 status.json"""
    os.makedirs(os.path.dirname(STATUS_PATH), exist_ok=True)
    with open(STATUS_PATH, "w", encoding="utf-8") as f:
        json.dump(status, f, ensure_ascii=False, indent=2)


def _reset_status():
    """重置 status.json（测试用）"""
    if os.path.exists(STATUS_PATH):
        os.remove(STATUS_PATH)


def task_today() -> dict:
    """返回 Day2 任务列表"""
    status = _load_status()
    tasks = []
    for filename, desc in TASKS.items():
        submitted = status.get(filename, False)
        mark = "✅" if submitted else "⬜"
        tasks.append({"file": filename, "desc": desc, "submitted": submitted, "mark": mark})
    return {"success": True, "tasks": tasks}


def task_submit(filename: str) -> dict:
    """标记文件为已提交"""
    if filename not in TASKS:
        return {"success": False, "message": f"{filename} 不在任务清单中"}

    status = _load_status()
    if status.get(filename, False):
        return {"success": False, "message": f"{filename} 已提交过"}

    status[filename] = True
    _save_status(status)
    return {"success": True, "message": f"{filename} 已提交"}


def task_check() -> dict:
    """检查未提交文件"""
    status = _load_status()
    remaining = [f for f, submitted in status.items() if not submitted]
    if not remaining:
        return {"success": True, "remaining": [], "message": "全部完成！"}
    return {"success": True, "remaining": remaining, "message": f"还有 {len(remaining)} 个文件未提交"}
