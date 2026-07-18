# Project 1 测试策略

- 状态：Final Approved（2026-07-15 全量验收通过）
- 原则：测试语义口径，而不只测试结果非空

## 1. 分层

| 层级 | 覆盖 | 关键反例 |
|---|---|---|
| 单行解析 | 正常、空、坏结构、坏时间、普通数字 | `init 1 0` 不得成为 error_code |
| 批量解析 | 混合有效/非法行 | 非法行计数且不阻断后续 |
| 筛选 | level/state/keyword 独立 | 关键词含 `.` 时按字面量而非正则通配 |
| 统计 | 日期、类型、模块计数/率 | 构造模块 Error 份额与自身 Error 率不相等的数据 |
| 集成 | 小日志生成全部清单文件 | CSV、PNG、报告均存在且非空 |
| 全量 | 课程 Apache.tar.gz | 行数、级别、时间范围、输出与报告一致 |

## 2. AC 映射

| AC | 测试文件 | 预期证据 |
|---|---|---|
| P1-AC1 | `tests/test_log_parser.py` | 五字段与 invalid_count |
| P1-AC2 | `tests/test_error_filter.py` | 三筛选独立结果 |
| P1-AC3 | `tests/test_statistics.py` | 固定分子分母的精确值 |
| P1-AC4 | `tests/test_integration.py` + 主流程 | 9 类产物 |
| P1-AC5 | 全量 CSV 复算与报告 Review | `docs/test-record.md` |

## 3. 失败处理

失败用例不删除、不修改 Expected Result 来迎合实现。若真实数据暴露词表遗漏，先记录为限制；只有影响题目验收时才最小修复并增加回归。图表测试只验证可生成和输入列契约，关键数字在统计单测中精确断言。

## 4. 命令

```bash
../.venv/bin/python -m pytest tests -q
../.venv/bin/python main.py --archive ../../day4-data/project1/Apache.tar.gz
```

实际结果统一记录在仓库 `docs/test-record.md`。
