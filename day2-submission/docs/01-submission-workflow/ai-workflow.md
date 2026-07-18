# 提交检查助手工作流

## 1. 目标与输入字段

在项目提交前检查证据文件、运行项目测试、生成 Markdown 证据，并给出 PASS、WARNING 或 BLOCKED。

| 字段 | 类型 | 是否必需 | 说明 |
|------|------|----------|------|
| `project_dir` | 路径 | 是 | 待检查项目根目录 |
| `required_files` | 字符串列表 | 是 | 相对项目根目录的必需文件 |
| `test_command` | 命令参数列表 | 是 | 不经 shell 执行的测试命令 |
| `timeout_seconds` | 正整数 | 否 | 单条命令超时，默认 60 秒 |
| `evidence_dir` | 路径 | 否 | 默认 `.submission-check/` |

## 2. 工具定义

### `checkFiles()`

- 功能：检查 `required_files`；对 README 检查安装/运行/测试线索，对 AI 日志检查五字段。
- 输入：`project_dir`、`required_files`。
- 输出：`missing_files`、`warnings`、逐文件 `details`。
- 边界：只读取清单文件，不解析或执行文件内容。
- 失败：文件缺失进入 BLOCKED 证据，编码异常以替换字符读取。

### `runTests()`

- 功能：按顺序执行测试，记录命令、退出码、stdout、stderr 和超时。
- 输入：`project_dir`、结构化命令列表、`timeout_seconds`。
- 输出：`passed_tests` 与 `failed_tests`。
- 边界：命令按参数数组执行，禁止 `shell=True`。
- 失败：非零退出码、超时、命令不存在都进入失败清单，最终 BLOCKED。

## 3. 状态定义

- **PASS**：文件齐全、测试全部通过且无文档警告。下一步是提交并保留报告。
- **WARNING**：文件齐全、测试通过，但 README 或 AI 日志线索不完整。下一步是补文档后复测。
- **BLOCKED**：项目目录不存在、必需文件缺失、测试失败、超时或无法执行。下一步是修复阻塞项。

## 4. 判断表

| 条件 | 状态 | 下一步 |
|------|------|--------|
| 文件齐全、测试通过、无警告 | PASS | 提交并附报告 |
| 文件齐全、测试通过、文档线索缺失 | WARNING | 补文档并复测 |
| 任一必需文件缺失 | BLOCKED | 补齐文件 |
| 任一测试失败、超时或无法执行 | BLOCKED | 修复测试或环境 |

## 5. 失败兜底

1. 缺文件：记录相对路径，不猜测内容，状态为 BLOCKED。
2. 测试失败：记录命令、退出码和输出摘要，状态为 BLOCKED。
3. 测试超时：终止命令并记录超时，继续生成报告，状态为 BLOCKED。
4. README 线索不足：列出缺失关键词，状态为 WARNING。
5. AI 日志字段不足：列出缺失字段，状态为 WARNING。

## 6. 证据位置

| 判断 | 证据文件 |
|------|----------|
| 文件存在性与文档线索 | `.submission-check/file-check.md` |
| 测试命令、通过与失败 | `.submission-check/test-result.md` |
| 综合状态和下一步 | `.submission-check/final-report.md` |

## 7. 执行示例

```bash
python3 check_submission.py ../02-task-assistant \
  --required-file README.md \
  --required-file spec.md \
  --required-file ai-log.md \
  --test-command "python3 -m unittest discover -s tests -v"
```
