"""直接读取六个课程压缩包，避免同名解压目录互相覆盖。"""

from __future__ import annotations

import tarfile
from pathlib import Path

import pandas as pd

from .text_cleaner import extract_raw_message


def _label_for_archive(path: Path) -> str:
    return "ham" if "ham" in path.name else "spam"


def load_email_archives(paths: list[str | Path]) -> tuple[pd.DataFrame, list[str]]:
    records: list[dict[str, str]] = []
    failures: list[str] = []
    for raw_path in sorted((Path(path) for path in paths), key=lambda item: item.name):
        label = _label_for_archive(raw_path)
        with tarfile.open(raw_path, "r:bz2") as archive:
            members = sorted((member for member in archive.getmembers() if member.isfile()), key=lambda item: item.name)
            for member in members:
                handle = archive.extractfile(member)
                if handle is None:
                    failures.append(f"{raw_path.name}:{member.name}: 无法读取")
                    continue
                try:
                    raw_message = extract_raw_message(handle.read())
                except Exception as exc:  # 单封坏邮件不应中断批处理，但必须留证据
                    failures.append(f"{raw_path.name}:{member.name}: {type(exc).__name__}")
                    raw_message = ""
                records.append({
                    "label": label,
                    "source": raw_path.name,
                    "message_id": member.name,
                    "raw_message": raw_message,
                })
    return pd.DataFrame(records), failures

