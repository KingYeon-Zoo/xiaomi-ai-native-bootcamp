"""提交校验工具 — 检查 Day2 作业的提交完整性"""

import os

REQUIRED_FILES = {
    "README.md": {
        "desc": "项目说明",
        "check_content": True,
        "keywords": ["安装", "运行", "测试"],
    },
    "agent-design.md": {
        "desc": "架构设计",
        "check_content": True,
        "keywords": ["架构图", "工具定义", "测试用例"],
    },
    "ai-log.md": {
        "desc": "AI 协作日志",
        "check_content": True,
        "keywords": ["目的", "输入", "建议", "人工判断", "验证"],
    },
    "test_tools.py": {
        "desc": "测试文件",
        "check_content": False,
    },
}


def validate_submission(project_dir: str) -> dict:
    """
    校验项目提交完整性。

    返回:
        {status: "PASS"|"WARNING"|"BLOCKED", missing_files: [], warnings: [], details: {}}
    """
    missing_files = []
    warnings = []
    details = {}

    # 目录不存在
    if not os.path.isdir(project_dir):
        return {
            "status": "BLOCKED",
            "missing_files": ["项目目录不存在"],
            "warnings": [],
            "details": {},
        }

    # 检查每个必需文件
    for filename, config in REQUIRED_FILES.items():
        filepath = os.path.join(project_dir, filename)
        if not os.path.exists(filepath):
            missing_files.append(filename)
            details[filename] = "缺失"
            continue

        # 内容检查
        if config.get("check_content"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                missing_keywords = [kw for kw in config["keywords"] if kw not in content]
                if missing_keywords:
                    warnings.append(f"{filename} 缺少内容线索：{', '.join(missing_keywords)}")
                    details[filename] = f"缺少：{', '.join(missing_keywords)}"
                else:
                    details[filename] = "通过"
            except Exception as e:
                warnings.append(f"{filename} 读取失败：{e}")
                details[filename] = f"读取失败：{e}"
        else:
            details[filename] = "存在"

    # 状态判定
    if missing_files:
        status = "BLOCKED"
    elif warnings:
        status = "WARNING"
    else:
        status = "PASS"

    return {
        "status": status,
        "missing_files": missing_files,
        "warnings": warnings,
        "details": details,
    }
