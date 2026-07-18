# Day 2 仓库级测试与审计记录

## 1. 环境

- 日期：2026-07-15
- 系统：macOS
- Python：3.9.6
- LangChain Demo：仓库 `.venv`，依赖见 `03-learning-demo/requirements.txt`

## 2. 自动测试结果

| 模块 | 命令 | 预期 | 实际结果 | 结果 |
|---|---|---|---|---|
| 提交工作流 | `python3 -m unittest discover -s 01-submission-workflow/tests -v` | 5 条通过 | 5 条通过 | PASS |
| 任务助手 | `python3 -m unittest discover -s 02-task-assistant/tests -v` | 8 条通过 | 8 条通过 | PASS |
| LangChain Demo | `.venv/bin/python -m unittest discover -s 03-learning-demo/tests -v` | 4 条通过 | 4 条通过 | PASS |
| 训练营 Agent | `python3 -m unittest discover -s 04-training-agent/tests -v` | 13 条通过 | 13 条通过 | PASS |

最终自动测试合计 30 条通过、0 条失败。任务助手修复前 1 条大小写失败保留在 `docs/02-task-assistant/test-record.md`，不与最终状态混淆。

## 3. 结构与内容检查

| 检查 | 预期 | 实际结果 | 结果 |
|---|---|---|---|
| Eval JSON | 标准 JSON，覆盖三类 Eval | 语法通过，三类均检出 | PASS |
| 根 AI 日志 | 至少 7 条且含五字段 | 8 条，五字段完整 | PASS |
| 安全审查 | 六类风险 finding | 6 类均有位置、影响、修复和测试 | PASS |
| 提交卫生 | 不跟踪凭证、缓存、`.DS_Store` | 专用检查未发现 | PASS |

## 4. 提交审计

| 命令 | 预期 | 实际结果 | 结果 |
|---|---|---|---|
| `bash check-submission.sh` | 0 项 BLOCKED | 36 项通过、0 项阻塞 | PASS |
| `bash ../.agents/skills/xiaomi-ai-bootcamp/scripts/audit-xiaomi-project.sh . personal` | 无 BLOCKED | 39 PASS、0 WARNING、0 BLOCKED | PASS |

## 5. 未执行与残留风险

- 未运行真实模型 API，不宣称真实回答效果。
- 未验证 Windows 下的符号链接工作树与命令。
- 未执行 LangChain `.batch()`、`.ainvoke()` 或并发异常测试。
- 未对整个仓库做穷尽安全扫描；只完成课程指定六类风险审查。
