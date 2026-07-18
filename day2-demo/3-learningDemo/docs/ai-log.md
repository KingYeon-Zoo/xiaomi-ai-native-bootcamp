# AI 协作日志 — 小红书文案生成器

> 记录每次与 AI 协作的决策链，每条包含：目的 / 输入 / 建议 / 人工判断 / 验证。
> **关键决策标记**：🔴 拒绝 AI 建议 / 🟡 修改 AI 建议 / 🟢 采纳但有附加条件

---

## 阶段一：方案选择

### 记录 1：选择学习方向 🔴

| 字段 | 内容 |
|------|------|
| **目的** | 确定 LangChain 学习 demo 的类型 |
| **输入** | 任务要求（30 分钟内、陌生技术、最小可验证） |
| **建议** | AI 建议 3 个方案：A. 代码解释器（最简单）、B. RAG 知识库问答、C. Agent 工具调用 |
| **人工判断** | **拒绝方案 A（太简单）和方案 C（太复杂）**。最终选择小红书文案生成器（基于方案 A 框架但更实用）。理由：方案 A 流程太单薄，学不到 LangChain 的 Chain 串联能力；方案 C 超出 30 分钟限制；小红书文案生成器有多轮信息收集 + Prompt 组装 + LLM 生成，覆盖核心概念且实用 |
| **验证** | 最终 demo 能覆盖 PromptTemplate、LLM、Chain 三个核心概念 |

---

## 阶段二：功能设计

### 记录 2：确定信息收集字段 🔴

| 字段 | 内容 |
|------|------|
| **目的** | 确定 AI 需要向用户收集哪些信息 |
| **输入** | 小红书文案的常见要素（产品、受众、卖点、风格） |
| **建议** | AI 建议收集 5 个字段：product、target_user、selling_points、style、extra |
| **人工判断** | **拒绝 5 字段方案，缩减为 3 字段**：product（必填）、target_user（必填）、style（可选）。理由：5 个字段输入成本太高，用户体验差；产品和用户是核心，风格可选增加灵活性；selling_points 可以让 AI 自行推断，extra 增加复杂度但收益不大 |
| **验证** | 只填 2 个必填字段时能正常生成文案 |

### 记录 3：确定交互方式 🟡

| 字段 | 内容 |
|------|------|
| **目的** | 确定信息收集的交互形式 |
| **输入** | 3 个字段（产品、用户、风格） |
| **建议** | AI 建议每个问题提供备选建议项，用户可输入或参考建议 |
| **人工判断** | **采纳，但要求备选项必须是小红书常见品类**。理由：备选项能降低用户思考成本，但必须贴近真实场景（如小米SU7、iPhone 15），不能是泛泛的例子 |
| **验证** | 终端显示建议项，用户可以直接输入或参考 |

### 记录 4：确定 Prompt 模板结构 🟢

| 字段 | 内容 |
|------|------|
| **目的** | 设定生成文案的 Prompt 模板 |
| **输入** | 小红书文案的写作规范（标题吸睛、正文种草、标签引流） |
| **建议** | AI 建议 Prompt 包含：角色设定 + 产品信息 + 输出要求 + 风格参考 |
| **人工判断** | **采纳，附加条件**：输出要求明确字数范围（标题 15-20 字、正文 300-500 字、标签 5-8 个）。理由：没有字数约束的 LLM 输出不稳定，可能过长或过短 |
| **验证** | 生成的文案符合字数要求 |

### 记录 5：确定技术方案 🟢

| 字段 | 内容 |
|------|------|
| **目的** | 确定实现的技术复杂度 |
| **输入** | 30 分钟时间限制、学习目标（PromptTemplate + LLMChain） |
| **建议** | AI 建议两种方案：A. 用 ConversationChain + Memory 管理多轮对话；B. 用简单 input() 循环 |
| **人工判断** | **采纳方案 B（最简单方式）**。理由：学习目标是 PromptTemplate 和 LLMChain，不是 Memory 机制；input() 循环更直观，30 分钟能完成；不需要上下文记忆，每次输入独立 |
| **验证** | 代码结构清晰，main.py 用 while True + input() 实现循环 |

### 记录 6：确定测试策略 🟡

| 字段 | 内容 |
|------|------|
| **目的** | 确定自动测试的实现方式 |
| **输入** | PRD 验收标准（8 项）、避免测试时消耗 API 额度 |
| **建议** | AI 建议用 pytest + mock LLM |
| **人工判断** | **采纳，但要求 mock 必须覆盖完整调用链**。理由：不能只 mock 返回值，要验证 PromptTemplate 填充、LLMChain 调用参数是否正确；测试要覆盖正常流程和异常流程（必填为空） |
| **验证** | `pytest test_main.py` 全部通过，且不消耗 API 额度 |

---

## 阶段三：环境与配置

### 记录 7：确定环境管理方案 🔴

| 字段 | 内容 |
|------|------|
| **目的** | 确定 Python 虚拟环境和依赖管理方式 |
| **输入** | 当前环境（Python 3.12、pip、uv 已安装）、需要方便他人验证 |
| **建议** | AI 建议用 uv（速度快 10-100 倍、依赖解析更可靠） |
| **人工判断** | **拒绝 uv，选择 .venv + pip**。理由：项目要给他人验证，不能要求对方安装 uv；.venv 是 Python 内置，零额外依赖；小项目依赖少，uv 的速度优势不明显 |
| **验证** | 他人只需 `python -m venv .venv && pip install -r requirements.txt` 即可运行 |

### 记录 8：确定 API 配置方式 🟢

| 字段 | 内容 |
|------|------|
| **目的** | 确定 OpenAI API Key 的配置方式 |
| **输入** | 需要区分测试（mock）和运行（真实 API）两种场景 |
| **建议** | AI 建议用 `.env` 文件 + `python-dotenv` |
| **人工判断** | **采纳**。理由：测试时用 mock，不读 .env；运行时从 .env 读取真实 key；.env 加入 .gitignore，避免泄露 |
| **验证** | 不配置 .env 时测试通过；配置 .env 后运行成功调用 API |

---

## 阶段四：实现与调试

### 记录 9：LangChain 导入路径问题 🔴

| 字段 | 内容 |
|------|------|
| **目的** | 解决 langchain 模块导入失败 |
| **输入** | `from langchain.prompts import PromptTemplate` 报错 ModuleNotFoundError |
| **建议** | AI 建议检查 langchain 版本，尝试 `from langchain_core.prompts import PromptTemplate` |
| **人工判断** | **拒绝盲目尝试，查文档确认**。最终使用 `langchain_core.prompts`。理由：新版 langchain 将核心组件拆分到 langchain_core 包，PromptTemplate 属于核心组件 |
| **验证** | `from langchain_core.prompts import PromptTemplate` 导入成功 |

### 记录 10：LLMChain 弃用问题 🔴

| 字段 | 内容 |
|------|------|
| **目的** | 解决 `from langchain.chains import LLMChain` 导入失败 |
| **输入** | langchain 新版本已移除 LLMChain |
| **建议** | AI 建议用 `prompt | llm` 新语法创建 RunnableSequence |
| **人工判断** | **拒绝安装旧版本兼容包，采用新语法**。理由：新语法更简洁，是 LangChain 的发展方向；`prompt | llm` 创建 RunnableSequence，调用 `.invoke()` 代替 `.run()` |
| **验证** | `chain = PROMPT_TEMPLATE | llm` 创建成功，`chain.invoke(info)` 正常工作 |

### 记录 11：Mock 测试策略调整 🟡

| 字段 | 内容 |
|------|------|
| **目的** | 解决 mock ChatOpenAI 后测试仍然失败 |
| **输入** | mock ChatOpenAI 后，`PROMPT_TEMPLATE | mock_llm` 的 invoke 行为不符合预期 |
| **建议** | AI 建议 mock 整个 create_chain 函数而非 ChatOpenAI 类 |
| **人工判断** | **采纳**。理由：mock 粒度应该在函数级别而非类级别；mock create_chain 更直接，避免处理 RunnableSequence 的内部调用链 |
| **验证** | `@patch("generator.create_chain")` 后测试通过 |

---

## 阶段五：文档更新

（见本文档更新记录）
