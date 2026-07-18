# Peer Review — 小红书文案生成器

> **评审人**：李思威
>
> **评审对象**：小红书文案生成器（LangChain 学习 Demo）
>
> **评审日期**：2026-06-23

---

## Step 1：按 README 运行 Demo

### 操作过程

```bash
# 1. 创建虚拟环境
python -m venv .venv

# 2. 激活虚拟环境
.venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行测试（不需要 API Key）
pytest src/test_main.py -v
```

### 运行结果

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\code\xiaomi\day2-workflow\3-learningDemo
collected 17 items

src/test_main.py::TestPromptTemplate::test_template_has_variables PASSED
src/test_main.py::TestPromptTemplate::test_template_fill PASSED
src/test_main.py::TestPromptTemplate::test_suggestions_exist PASSED
src/test_main.py::TestExitCommand::test_quit_command PASSED
src/test_main.py::TestExitCommand::test_exit_command PASSED
src/test_main.py::TestExitCommand::test_normal_text PASSED
src/test_main.py::TestCollectField::test_normal_input PASSED
src/test_main.py::TestCollectField::test_quit_returns_none PASSED
src/test_main.py::TestCollectField::test_required_empty_then_valid PASSED
src/test_main.py::TestCollectField::test_optional_empty_returns_default PASSED
src/test_main.py::TestCollectInfo::test_collect_all_fields PASSED
src/test_main.py::TestCollectInfo::test_collect_with_optional_empty PASSED
src/test_main.py::TestCollectInfo::test_quit_on_first_field PASSED
src/test_main.py::TestCollectInfo::test_quit_on_second_field PASSED
src/test_main.py::TestCollectInfo::test_required_empty_retry PASSED
src/test_main.py::TestGenerator::test_generate_calls_chain PASSED
src/test_main.py::TestGenerator::test_generate_with_default_style PASSED

============================= 17 passed in 0.98s ==============================
```

> ⏳ 主程序 `python src/main.py` 需要配置 API Key 才能完整运行，未做端到端验证。

---

## Step 2：检查 README 完整性

### 检查清单

| 检查项 | 是否完整 | 证据 |
|--------|----------|------|
| 安装步骤（venv + pip） | ✅ 完整 | README 有 Windows/Linux/Mac 三平台激活命令 |
| 依赖说明（requirements.txt） | ✅ 完整 | 文件存在，包含 langchain、langchain-openai、pytest、python-dotenv |
| API Key 配置说明 | ✅ 完整 | 有 .env.example 模板，有 OpenAI 和 MIMO 两种配置示例 |
| 运行命令 | ✅ 完整 | `python src/main.py` 和 `pytest src/test_main.py -v` 都有写明 |
| 使用示例 | ✅ 完整 | 有终端交互的完整示例输出 |
| 项目结构 | ✅ 完整 | 目录树 + 每个文件的职责说明 |
| 常见问题 FAQ | ✅ 完整 | 覆盖了 3 个常见报错场景 |

### 发现的问题

| # | 问题 | 严重程度 | 说明 |
|---|------|----------|------|
| 1 | 缺少 Python 版本要求的明确声明 | 低 | README 写了"Python 3.12+"，但 requirements.txt 没有 `python_requires` 约束，低版本 Python 安装依赖时可能报错不明确 |
| 2 | `.env.example` 默认值指向 MIMO | 低 | 模板默认填了 MIMO 配置，用户如果想用 OpenAI 需要手动注释/取消注释，可以更清晰地说明 |
| 3 | 缺少运行截图 | 低 | README 有文字示例但没有实际运行截图（test-record.md 有终端输出可以作为补充） |

---

## Step 3：边界测试

### 边界问题 1：超长产品名输入

**测试方法**：在 `collect_field` 中输入一个 200 字符的产品名。

**测试代码**（mock 测试验证）：

```python
# 在 test_main.py 中已有相关测试：
# test_normal_input — 验证普通文本输入正常接收
# 但没有专门测试超长输入的边界
```

**结论**：代码层面没有输入长度限制，超长文本会直接传给 LLM。这在功能上不影响运行（LLM 本身支持长输入），但 Prompt 中没有说明对超长产品名的处理策略。

**影响**：⚠️ 低风险。LLM 能处理，但生成的文案标题可能因产品名过长而超出 15-20 字限制。

---

### 边界问题 2：API Key 未配置时的行为

**测试方法**：不配置 .env 文件，直接运行 `python src/main.py`，输入信息后观察报错。

**预期行为**：程序应捕获异常并给出友好提示。

**实际行为**：代码中有 try-except 捕获：

```python
# src/main.py 第 34-36 行
except Exception as e:
    print(f"\n❌ 生成失败: {e}")
    print("请检查 .env 中的 OPENAI_API_KEY 是否正确\n")
```

**结论**：✅ 边界处理合理。程序不会崩溃，会提示用户检查 API Key 配置。

---

## Step 4：四维度评审结论

### 🏃 维度一：能运行

| 项目 | 结论 |
|------|------|
| **结论** | ✅ 通过 |
| **证据** | `pytest src/test_main.py -v` 运行 17 个测试全部通过（0.98s），测试覆盖了 PromptTemplate、退出命令、必填校验、可选字段、LLM 调用等核心逻辑 |
| **备注** | 主程序需要 API Key 才能端到端运行，但 mock 测试已验证核心逻辑正确 |

---

### 📋 维度二：README 完整

| 项目 | 结论 |
|------|------|
| **结论** | ✅ 通过 |
| **证据** | README 包含：安装步骤（3 步）、API 配置说明（2 种服务）、运行命令、使用示例、项目结构、技术栈、学习要点、FAQ（3 条）。从零开始的用户按 README 操作可以跑通测试 |
| **可改进** | 可补充实际运行截图；Python 版本约束可以更严格 |

---

### 🧱 维度三：边界诚实

| 项目 | 结论 |
|------|------|
| **结论** | ✅ 通过 |
| **证据** | PRD 第 9 节明确列出了 6 个"非目标"（不做多轮记忆、不做历史保存、不做 Web UI、不做 RAG、不做多语言、不做违禁词检测）。代码中对 API Key 缺失做了异常捕获和友好提示。测试记录中"未解决疑问"部分诚实列出了 3 个待验证问题 |
| **可改进** | 可在 README 中增加一个"已知限制"小节，方便用户快速了解边界 |

---

### 🤖 维度四：AI 依赖可解释

| 项目 | 结论 |
|------|------|
| **结论** | ✅ 通过 |
| **证据** | `docs/ai-log.md` 记录了 11 条 AI 协作决策，每条包含：目的、输入、AI 建议、人工判断、验证。关键决策有明确的标记（🔴 拒绝 6 条、🟡 修改 3 条、🟢 采纳 2 条），说明作者对 AI 建议有独立判断而非全盘接受 |
| **亮点** | 拒绝了 AI 建议的 uv 环境管理（选择更通用的 .venv+pip）、拒绝了 5 字段方案（缩减为 3 字段）、拒绝了旧版 LLMChain 写法（采用新语法）——这些决策都有合理理由 |

---

## 总结

| 维度 | 结论 |
|------|------|
| 🏃 能运行 | ✅ 通过 |
| 📋 README 完整 | ✅ 通过 |
| 🧱 边界诚实 | ✅ 通过 |
| 🤖 AI 依赖可解释 | ✅ 通过 |

**整体评价**：这是一个结构清晰、文档完整的 LangChain 学习 Demo。代码质量好（模块拆分合理、有类型提示）、测试覆盖全面（17 个用例全通过）、AI 协作记录详实（有拒绝/修改/采纳的明确判断）。主要改进空间在于补充运行截图和在 README 中增加"已知限制"说明。
