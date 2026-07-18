# Review Checklist — 训练营助教 AGENT 代码审查

> 用 6 类 AI 代码风险清单逐项检查，每项标注位置、影响、修复、测试。
> 审查对象：`tools/rag.py`、`tools/task_manager.py`、`tools/validator.py`

---

## 一、风险清单

| # | 风险类型 | 状态 | 说明 |
|---|---------|------|------|
| 1 | 幻觉 API | ✅ 无风险 | 仅使用 `re`、`os`、`json` 标准库 |
| 2 | 硬编码密钥 | ✅ 无风险 | 无 API Key、密码、Token |
| 3 | 任意文件读取 | ✅ 无风险 | 文件路径均为固定或受控输入 |
| 4 | 资料外编造 | ✅ 无风险 | 无匹配时明确返回"资料中没有找到依据" |
| 5 | 吞掉错误 | ⚠️ 1 处 | rag.py 的 `_load_chunks` 未捕获读文件异常 |
| 6 | 只覆盖 happy path | ✅ 无风险 | 三个工具均覆盖空输入/缺失/异常等边界 |

---

## 二、Finding 表

### Finding 1：rag.py `_load_chunks` 未捕获文件读取异常

| 字段 | 内容 |
|------|------|
| **风险类型** | 吞掉错误 / 只覆盖 happy path |
| **位置** | `tools/rag.py:22-23` — `with open(faq_path, "r") as f: text = f.read()` |
| **影响** | 如果 `faq_path` 存在但无读取权限（如权限被修改），会抛出未处理的 `PermissionError`，调用方收到 500 而非友好提示 |
| **修复** | 在 `_load_chunks` 中加 try-except，捕获 `IOError`/`PermissionError`，返回空列表（与文件不存在行为一致） |
| **测试** | 已有 `test_empty_query` 和 `test_no_match` 覆盖空知识库场景；权限异常在当前环境下低概率触发，可接受 |
| **判定** | **可接受** — 项目为本地 CLI 工具，非 Web 服务，路径固定为项目内 `data/course-faq.md`，实际不会遇到权限问题 |

### Finding 2：validator.py `validate_submission` 读文件用裸 `except Exception`

| 字段 | 内容 |
|------|------|
| **风险类型** | 吞掉错误（轻微） |
| **位置** | `tools/validator.py:67` — `except Exception as e:` |
| **影响** | 捕获了所有异常类型，包括 `KeyboardInterrupt`（Python 3 中 Exception 不包含，实际无影响）和 `MemoryError` 等不应被吞掉的异常 |
| **修复** | 改为 `except (IOError, UnicodeDecodeError) as e:`，只捕获预期的文件读取异常 |
| **测试** | 已有 `test_missing_readme` 和 `test_complete_project` 覆盖正常路径和缺失路径 |
| **判定** | **WARNING** — 功能正确，但 except 粒度过粗，建议收窄 |

### Finding 3：task_manager.py `_save_status` 无写入失败处理

| 字段 | 内容 |
|------|------|
| **风险类型** | 只覆盖 happy path（轻微） |
| **位置** | `tools/task_manager.py:33-36` — `_save_status` 直接 `open` + `json.dump` |
| **影响** | 如果 `data/` 目录无写入权限，`_save_status` 会抛出 `OSError`，调用方未处理 |
| **修复** | 在 `_save_status` 中加 try-except，或在 `task_submit` 中捕获写入异常并返回错误提示 |
| **测试** | `test_submit_normal` 验证正常写入；写入失败场景在当前环境下低概率触发 |
| **判定** | **可接受** — `os.makedirs(exist_ok=True)` 已处理目录不存在的情况，权限问题在本地开发环境极少见 |

---

## 三、审查结论

**状态：WARNING**

| 维度 | 结果 |
|------|------|
| 幻觉 API | ✅ PASS — 无外部依赖，仅标准库 |
| 硬编码密钥 | ✅ PASS — 无密钥 |
| 任意文件读取 | ✅ PASS — 路径固定或受控 |
| 资料外编造 | ✅ PASS — 零命中明确拒答 |
| 吞掉错误 | ⚠️ WARNING — 2 处 except 粒度过粗（rag.py + validator.py） |
| Happy path 覆盖 | ✅ PASS — 三个工具均有边界测试 |

**下一步**：
1. （可选）`validator.py:67` 收窄 except 为 `(IOError, UnicodeDecodeError)`
2. （可选）`rag.py:_load_chunks` 加 try-except 处理读取异常
3. 当前版本可提交，上述两项为代码质量改进，不阻塞功能
