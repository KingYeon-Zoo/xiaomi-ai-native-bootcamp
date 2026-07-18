# `log_analyzer` 包

模块职责保持单一：`log_parser` 负责五字段解析，`error_filter` 负责三类筛选，`statistics` 统一统计口径，`visualizer` 只消费统计表，`utils` 负责压缩包入口。公开接口见 `__init__.py`。

非法日志行不会中断批处理，而是计入 `invalid_count`；这一选择避免静默失败，同时保留验收证据。
