"""Apache error log 的严格解析与字段提取。"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

import pandas as pd

LOG_COLUMNS = ["timestamp", "level", "module", "error_code", "content"]
_LINE_PATTERN = re.compile(r"^\[([^\]]+)\]\s+\[([^\]]+)\]\s+(.+)$")
_ERROR_STATE_PATTERN = re.compile(r"\berror\s+state\s+(\d+)\b", re.IGNORECASE)
_MODULE_TOKENS = (
    "mod_security",
    "mod_python",
    "workerenv",
    "jk2_init",
    "mod_jk2",
    "mod_jk",
    "urimap",
    "ldap",
    "config",
    "env",
)


def _extract_module(content: str) -> str:
    lowered = content.lower()
    for token in _MODULE_TOKENS:
        if re.search(rf"(?<![a-z0-9_]){re.escape(token)}(?![a-z0-9_])", lowered):
            return token
    return "unknown"


def parse_log_line(line: str) -> dict[str, object] | None:
    """解析单行；空行、格式错误或无效时间戳返回 ``None``。"""
    match = _LINE_PATTERN.fullmatch(line.strip())
    if not match:
        return None

    raw_timestamp, raw_level, content = match.groups()
    try:
        timestamp = datetime.strptime(raw_timestamp, "%a %b %d %H:%M:%S %Y")
    except ValueError:
        return None

    error_match = _ERROR_STATE_PATTERN.search(content)
    return {
        "timestamp": timestamp,
        "level": raw_level.lower(),
        "module": _extract_module(content),
        "error_code": int(error_match.group(1)) if error_match else pd.NA,
        "content": content,
    }


def parse_log_file(path: str | Path) -> tuple[pd.DataFrame, int]:
    """解析文件并返回数据框和被跳过的非法行数量。"""
    records: list[dict[str, object]] = []
    invalid_count = 0
    with Path(path).open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            parsed = parse_log_line(line)
            if parsed is None:
                invalid_count += 1
            else:
                records.append(parsed)

    frame = pd.DataFrame(records, columns=LOG_COLUMNS)
    if not frame.empty:
        frame["error_code"] = frame["error_code"].astype("Int64")
    return frame, invalid_count

