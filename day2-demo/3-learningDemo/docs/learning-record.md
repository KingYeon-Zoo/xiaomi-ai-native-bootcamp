# 学习记录 — LangChain 小红书文案生成器

## 我知道（学之前已掌握）

| 知识点 | 掌握程度 | 实际应用 |
|--------|----------|----------|
| Python 基础语法 | 熟练 | 函数定义、类、类型提示、装饰器 |
| API 调用 | 熟练 | HTTP 请求、JSON 解析、OpenAI API 格式 |
| Prompt 概念 | 了解 | 系统提示词、用户输入、模板化提示词 |
| 虚拟环境 | 了解 | .venv 创建、pip install |
| pytest 基础 | 了解 | assert 断言、简单的 fixture |

---

## 我不知道（学之后发现的问题 → 已解决）

### 1. LangChain 的 PromptTemplate 怎么用？

**问题**：知道 Prompt 需要模板化，但不知道 LangChain 的具体 API。

**学习过程**：
```python
# ❌ 错误尝试：from langchain.prompts import PromptTemplate
# ✅ 正确路径：from langchain_core.prompts import PromptTemplate

# 方式 1：from_template（简单）
prompt = PromptTemplate.from_template("请介绍一下{product}")

# 方式 2：完整定义（推荐）
prompt = PromptTemplate(
    input_variables=["product", "target_user"],
    template="请为{target_user}介绍{product}"
)
```

**踩坑**：新版 langchain 将核心组件拆分到 `langchain_core` 包，直接 `from langchain.prompts` 会报 ModuleNotFoundError。

**验证**：能独立定义 PromptTemplate 并正确填充变量。

---

### 2. LangChain 的 Chain 机制怎么用？

**问题**：知道需要串联 Prompt → LLM，但不知道具体实现方式。

**学习过程**：
```python
# ❌ 旧版方式（已弃用）
from langchain.chains import LLMChain
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(product="小米SU7")

# ✅ 新版方式（推荐）
chain = prompt | llm  # 创建 RunnableSequence
result = chain.invoke({"product": "小米SU7"})
# result 是 AIMessage，需要 result.content 获取文本
```

**踩坑**：`LLMChain` 在新版 langchain 中已移除，搜索到的很多教程都是旧版写法。

**验证**：`prompt | llm` 创建的 chain 能正常调用 invoke() 并返回结果。

---

### 3. 如何用 pytest + mock 测试 LLM 调用？

**问题**：测试 LLM 调用会消耗 API 额度，需要 mock 但不知道怎么写。

**学习过程**：
```python
from unittest.mock import patch, MagicMock

# ❌ 错误方式：mock ChatOpenAI 类
@patch("generator.ChatOpenAI")
def test_generate(self, mock_llm_cls):
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = MagicMock(content="测试文案")
    mock_llm_cls.return_value = mock_llm
    # 这样写有问题：prompt | mock_llm 的行为不符合预期

# ✅ 正确方式：mock 整个 create_chain 函数
@patch("generator.create_chain")
def test_generate(self, mock_create_chain):
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = MagicMock(content="测试文案")
    mock_create_chain.return_value = mock_chain
    # 直接 mock 函数返回值，避免处理内部调用链
```

**踩坑**：mock 的粒度很重要。mock 类的实例方法比 mock 函数更复杂，因为需要处理 `__init__` 和 `__or__` 运算符。

**验证**：17 个测试用例全部通过，不消耗 API 额度。

---

### 4. 如何用 python-dotenv 管理环境变量？

**问题**：API Key 不能硬编码，需要从环境变量读取。

**学习过程**：
```python
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

# 读取环境变量
api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_BASE")  # 可选，支持自定义端点
model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")  # 有默认值
```

**踩坑**：`load_dotenv()` 必须在 `os.getenv()` 之前调用，否则读不到 .env 中的值。

**验证**：不配置 .env 时测试通过；配置 .env 后能正确读取 API Key。

---

### 5. 如何支持多个 API 服务（OpenAI / MIMO）？

**问题**：用户可能使用不同的 API 服务，需要支持自定义 API 端点。

**学习过程**：
```python
# ChatOpenAI 支持 openai_api_base 参数
kwargs = {
    "model": model,
    "temperature": 0.7,
    "openai_api_key": api_key,
}
if api_base:  # 有值才设置
    kwargs["openai_api_base"] = api_base

llm = ChatOpenAI(**kwargs)
```

**踩坑**：如果 `openai_api_base=None`，ChatOpenAI 会使用默认的 OpenAI 端点，不会报错。

**验证**：配置 MIMO API 后能正常调用。

---

## 如何验证（验收标准）

| # | 验证项 | 验证方式 | 结果 |
|---|--------|----------|------|
| 1 | Demo 能运行 | `python src/main.py` 启动正常 | ✅ |
| 2 | 信息收集完整 | 输入产品+用户+风格，正常接收 | ✅ |
| 3 | 必填校验生效 | 产品名留空，提示必填 | ✅ |
| 4 | 文案生成成功 | 输入完整信息，输出文案 | ⏳ 需配置 API |
| 5 | 能解释组件作用 | 能说清 PromptTemplate、chain、invoke 的作用 | ✅ |
| 6 | 能修改 Prompt | 修改模板后输出变化 | ✅ |
| 7 | 测试全部通过 | `pytest src/test_main.py -v` | ✅ 17 passed |

---

## 学习总结

### 关键收获

1. **LangChain 版本变化大**：很多教程是旧版写法（LLMChain、chain.run），新版用 `prompt | llm` 和 `chain.invoke()`。
2. **导入路径要查文档**：`langchain.prompts` → `langchain_core.prompts`，不能盲目抄代码。
3. **Mock 粒度很重要**：mock 函数比 mock 类更简单可靠。
4. **环境变量管理**：dotenv 是标准做法，API Key 不能硬编码。

### 踩坑记录

| 坑 | 原因 | 解决方案 |
|----|------|----------|
| ModuleNotFoundError: langchain.prompts | 新版拆分到 langchain_core | 改用 `from langchain_core.prompts` |
| ModuleNotFoundError: langchain.chains | LLMChain 已移除 | 改用 `prompt | llm` 语法 |
| Mock 测试失败 | mock ChatOpenAI 类后 chain 行为异常 | 改为 mock create_chain 函数 |
