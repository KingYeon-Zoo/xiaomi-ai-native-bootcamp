# 提交检查助手工作流

> 目标：在 `rag-assistant` 项目包提交前，检查必需文件、运行项目自带测试、生成证据和综合检查报告。

---

## 1. 适用范围

本工作流默认检查：

```text
D:\code\xiaomi\day1-demo-students\rag-assistant
```

当前版本以 `rag-assistant` 为模板标准：源代码实现可以变化，但提交包必须能通过文件存在性检查和项目自带测试。

---

## 2. 输入字段

最低输入字段：

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `project_dir` | string | `D:\code\xiaomi\day1-demo-students\rag-assistant` | 待检查项目目录 |
| `required_files` | string[] | 见 `resources/required-files.md` | 必须存在的提交证据文件 |
| `test_command` | string | `python tests/test_basic.py` | 兼容最低要求的单条测试命令 |

本工作流实际使用扩展字段：

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `test_commands` | object[] | 见下方 | 项目自带测试命令列表 |
| `evidence_dir` | string | `.submission-check` | 证据和最终报告目录 |
| `timeout_seconds` | number | `60` | 单条测试命令超时时间 |

默认测试命令：

```yaml
test_commands:
  - name: "基础结构与接口测试"
    command: "python tests/test_basic.py"
    required: true
  - name: "RAG 行为自动化测试"
    command: "python tests/test_rag.py"
    required: true
```

---

## 3. 工具定义

### 3.1 `checkFiles()`

功能：

- 检查 `required_files` 是否全部存在。
- 对 README 做轻量线索检查：是否包含安装、运行、测试相关文本。
- 对 ai-log 做轻量标签检查：是否包含 `目的`、`输入`、`建议`、`人工判断`、`验证` 五个标签。
- 生成文件检查证据。

输入：

| 字段 | 类型 | 说明 |
|------|------|------|
| `project_dir` | string | 待检查项目目录 |
| `required_files` | string[] | 必须存在的文件列表 |
| `evidence_dir` | string | 证据输出目录 |

输出：

| 字段 | 类型 | 说明 |
|------|------|------|
| `missing_files` | string[] | 缺失的必需文件 |
| `warnings` | string[] | README 线索缺失或 ai-log 标签缺失 |
| `evidence_file` | string | 文件检查证据路径 |

证据文件：

```text
.submission-check/file-check.md
```

### 3.2 `runTests()`

功能：

- 按顺序执行 `test_commands`。
- 对每条测试命令设置超时。
- 记录退出码、是否超时、标准输出和错误摘要。
- 生成测试证据。

输入：

| 字段 | 类型 | 说明 |
|------|------|------|
| `project_dir` | string | 测试执行目录 |
| `test_commands` | object[] | 测试命令列表 |
| `timeout_seconds` | number | 单条命令超时时间 |
| `evidence_dir` | string | 证据输出目录 |

输出：

| 字段 | 类型 | 说明 |
|------|------|------|
| `failed_tests` | object[] | 失败或超时的测试 |
| `passed_tests` | object[] | 通过的测试 |
| `evidence_file` | string | 测试结果证据路径 |

证据文件：

```text
.submission-check/test-result.md
```

---

## 4. 三个状态

### `PASS`

含义：必需文件全部存在，所有必跑测试通过，没有轻量检查警告。

下一步：可以提交，并附上 `.submission-check/final-report.md`。

### `WARNING`

含义：必需文件全部存在，所有必跑测试通过，但存在轻量质量警告。

当前触发条件：

- README 缺少安装、运行、测试任一类线索。
- ai-log 缺少 `目的`、`输入`、`建议`、`人工判断`、`验证` 任一标签。

下一步：建议补充 README 或 ai-log 后重新检查；如必须提交，需要在报告中带风险说明。

### `BLOCKED`

含义：提交包无法被可靠评审或验证。

触发条件：

- `project_dir` 不存在。
- 任一必需文件缺失。
- 任一必跑测试失败。
- 任一必跑测试超时。
- 测试命令无法执行。

下一步：必须先修复阻塞项，再重新运行工作流。

---

## 5. 状态判断表

| 条件 | 状态 | 下一步 |
|------|------|--------|
| 必需文件全部存在，两个测试都通过，README 和 ai-log 轻量检查无警告 | `PASS` | 可以提交，保留最终报告 |
| 必需文件全部存在，两个测试都通过，但 README 缺少安装/运行/测试线索 | `WARNING` | 补充 README 后重新检查 |
| 必需文件全部存在，两个测试都通过，但 ai-log 缺少五字段标签之一 | `WARNING` | 补充 ai-log 后重新检查 |
| 任一必需文件缺失 | `BLOCKED` | 补齐文件后重新检查 |
| 任一必跑测试失败或超时 | `BLOCKED` | 修复代码、环境或测试依赖后重新检查 |

完整规则见 `resources/status-rules.md`。

---

## 6. 失败兜底

| 失败场景 | 状态 | 具体处理 |
|----------|------|----------|
| 缺少必需文件 | `BLOCKED` | 在 `file-check.md` 记录缺失文件；提示参考 `D:\code\xiaomi\day1-demo-students\templates` 补齐 |
| 测试失败 | `BLOCKED` | 在 `test-result.md` 记录命令、退出码、输出摘要；报告中列为下一步修复动作 |
| 测试超时 | `BLOCKED` | 停止等待，记录超时时间和命令；建议检查死循环、mock server 或外部依赖 |
| README 轻量线索缺失 | `WARNING` | 在 `file-check.md` 记录缺失线索；不阻塞提交，但建议补充 |
| ai-log 五字段标签缺失 | `WARNING` | 在 `file-check.md` 记录缺失标签；不阻塞提交，但建议补充 |

---

## 7. 证据与报告

工作流运行后生成：

```text
.submission-check/
  file-check.md
  test-result.md
  final-report.md
```

每个判断的证据位置：

| 判断内容 | 证据文件 |
|----------|----------|
| 必需文件是否存在 | `.submission-check/file-check.md` |
| README 轻量线索是否完整 | `.submission-check/file-check.md` |
| ai-log 五字段标签是否完整 | `.submission-check/file-check.md` |
| 测试是否通过、失败或超时 | `.submission-check/test-result.md` |
| 综合状态和下一步动作 | `.submission-check/final-report.md` |

最终报告至少包含：

- 文件检查
- 测试结果
- 综合状态判定
- 下一步动作

报告模板见 `resources/report-template.md`。

---

## 8. 推荐执行方式

在 PowerShell 7 中运行：

```powershell
.\resources\check-submission.ps1
```

指定项目目录：

```powershell
.\resources\check-submission.ps1 -ProjectDir "D:\code\xiaomi\day1-demo-students\rag-assistant"
```

脚本输出最终状态，并生成 `.submission-check/final-report.md`。
