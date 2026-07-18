"""数据源定位与压缩包读取工具。"""

from __future__ import annotations

import tarfile
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


@contextmanager
def apache_log_from_archive(archive: str | Path) -> Iterator[Path]:
    """安全地从课程压缩包提取 Apache.log 到临时目录。"""
    archive_path = Path(archive)
    with tempfile.TemporaryDirectory(prefix="day4-apache-") as temp_dir:
        with tarfile.open(archive_path, "r:gz") as bundle:
            member = next((item for item in bundle.getmembers() if Path(item.name).name == "Apache.log"), None)
            if member is None or not member.isfile():
                raise ValueError("压缩包中未找到 Apache.log")
            member.name = "Apache.log"
            bundle.extract(member, temp_dir, filter="data")
        yield Path(temp_dir) / "Apache.log"

