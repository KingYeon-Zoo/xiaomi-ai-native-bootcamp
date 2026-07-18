"""提交包完整性与文档线索校验工具。"""

from __future__ import annotations

from pathlib import Path
from typing import Optional


REQUIRED = {
    "README.md": ("安装", "运行", "测试"),
    "agent-design.md": ("数据流", "工具定义", "校验规则", "测试用例"),
    "ai-log.md": ("目的", "输入", "建议", "人工判断", "验证"),
    "tests/test_tools.py": (),
}


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def validate_submission(project_dir: Path, allowed_root: Optional[Path] = None) -> dict:
    project = Path(project_dir).resolve()
    root = (Path(allowed_root) if allowed_root is not None else Path.cwd()).resolve()
    if not is_within(project, root):
        return {"status": "BLOCKED", "missing_files": [], "warnings": [], "details": {"project_dir": "项目目录超出允许范围"}}
    if not project.is_dir():
        return {"status": "BLOCKED", "missing_files": ["项目目录不存在"], "warnings": [], "details": {"project_dir": "不存在"}}
    missing: list[str] = []
    warnings: list[str] = []
    details: dict[str, str] = {}
    for relative, keywords in REQUIRED.items():
        path = project / relative
        if not path.is_file():
            missing.append(relative)
            details[relative] = "缺失"
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        absent = [keyword for keyword in keywords if keyword not in content]
        if absent:
            warnings.append(f"{relative} 缺少：{', '.join(absent)}")
            details[relative] = f"缺少：{', '.join(absent)}"
        else:
            details[relative] = "通过"
    status = "BLOCKED" if missing else "WARNING" if warnings else "PASS"
    return {"status": status, "missing_files": missing, "warnings": warnings, "details": details}

