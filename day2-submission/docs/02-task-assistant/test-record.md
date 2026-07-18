# Test Record — Day2 学习任务清单助手

## 测试环境

- Python 3.9.6
- macOS，测试状态使用临时目录
- 测试日期：2026-07-13

## 修复前结果

命令：`python3 -m unittest discover -s 02-task-assistant/tests -v`

| 输入 | 预期输出 | 实际输出 | 结果 |
|------|----------|----------|------|
| `submit readme.MD` | 映射为 `README.md`，退出码 0 | 输出“不在任务清单中”，退出码 2 | ❌ FAIL |

### 失败定位

- **定位结论**：`cli.py` 实现问题，不是 `AGENTS.md` 漏规则。Spec 和 AGENTS 都明确文件名大小写不敏感，但 `submit_task()` 使用 `filename not in TASKS` 精确比较。
- **修复方向**：比较时统一小写，找到后继续使用清单中的规范名称作为状态键和输出。
- **最小修复**：只修改 `submit_task()` 的名称解析和后续键引用，没有扩大清单或修改测试期望。

## 修复后结果

命令：`python3 -m unittest discover -s 02-task-assistant/tests -v`

| # | 输入 | 预期输出 | 实际输出 | 结果 |
|---|------|----------|----------|------|
| 1 | `today` | 五个任务与状态 | 五个 `⬜` 和规范文件名 | ✅ PASS |
| 2 | `submit readme.MD` | 规范化并提交 README | `✅ README.md 已提交` | ✅ PASS |
| 3 | 重复 `submit spec.md` | 提示重复，退出码 1 | `ℹ️ spec.md 已提交过` | ✅ PASS |
| 4 | `submit fake.txt` | 拒绝，退出码 2 | `❌ fake.txt 不在任务清单中` | ✅ PASS |
| 5 | 提交 spec 后 `check` | 只列剩余四项 | 不包含 spec，包含 plan 等四项 | ✅ PASS |
| 6 | 损坏 JSON 后 `today` | 提示并重建 | 输出损坏提示，生成五字段 JSON | ✅ PASS |
| 7 | 只有 spec 字段的 JSON | 判断不完整并重建 | 输出损坏提示，剩余五项 | ✅ PASS |
| 8 | 无子命令 | 帮助和退出码 2 | 输出 today/submit/check 帮助 | ✅ PASS |

## 汇总与下一步

- 修复前：7 PASS / 1 FAIL；失败归因于 `cli.py`。
- 修复后：8 PASS / 0 FAIL。
- 下一步：如果未来允许动态任务，先扩展 Spec 与状态迁移测试，不能直接放开任意文件名。
