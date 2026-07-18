# 📝 小红书文案生成器

> 通过终端对话收集产品信息，AI 自动生成小红书风格的种草文案

## 功能特点

- 🤖 多轮对话收集产品信息（产品、目标用户、风格）
- 💡 每个问题提供 AI 建议备选项
- ✨ 生成小红书风格文案（标题 + 正文 + 标签）
- 🔄 循环生成，输入 `quit` 退出

## 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API Key

```bash
# 复制配置模板
cp .env.example .env

# 编辑 .env，填入你的 API Key
```

**支持的 API 服务：**

| 服务 | 配置示例 |
|------|----------|
| OpenAI | `OPENAI_API_KEY=sk-xxx` |
| 小米 MIMO | `OPENAI_API_KEY=sk-xxx`<br>`OPENAI_API_BASE=https://api.xiaomimimo.com/v1`<br>`OPENAI_MODEL=mimo-v2.5-pro` |

### 3. 运行程序

```bash
python src/main.py
```

### 4. 使用示例

```
════════════════════════════════════════════════════════════
📝 小红书文案生成器
════════════════════════════════════════════════════════════

回答几个问题，我来帮你写小红书文案～
输入 "quit" 退出程序

🤖 你要推广什么产品？
   💡 建议: 小米SU7、iPhone 15、戴森吹风机、元气森林、兰蔻小黑瓶
   > 小米SU7

🤖 目标用户是谁？
   💡 建议: 大学生、白领、宝妈、程序员、健身人群、学生党
   > 25-35岁年轻白领

🤖 想要什么风格？（可选，回车跳过）
   💡 建议: 种草安利、测评干货、情绪共鸣
   > 种草安利

⏳ 正在生成文案...
```

## 运行测试

```bash
# 运行自动测试（不需要 API Key，全部 mock）
pytest src/test_main.py -v
```

测试覆盖：
- ✅ PromptTemplate 模板填充
- ✅ 退出命令识别
- ✅ 必填字段校验
- ✅ 可选字段跳过
- ✅ LLM 调用流程（Mock）

## 项目结构

```
3-learningDemo/
├── docs/
│   ├── PRD.md              # 产品需求文档
│   └── tasks.md            # 任务清单
├── src/
│   ├── main.py             # 主程序入口
│   ├── prompt.py           # PromptTemplate 定义
│   ├── collector.py        # 信息收集逻辑
│   ├── generator.py        # 文案生成逻辑
│   └── test_main.py        # 自动测试
├── .env.example            # API Key 配置模板
├── .gitignore              # Git 忽略规则
├── requirements.txt        # Python 依赖
└── README.md               # 本文件
```

## 技术栈

- **Python 3.12+**
- **LangChain** - LLM 应用框架
- **OpenAI API / 小米 MIMO** - 大语言模型（兼容 OpenAI 格式）
- **pytest** - 测试框架

## 学习要点

本项目演示了 LangChain 的核心概念：

1. **PromptTemplate** - 定义提示词模板，支持变量绑定
2. **RunnableSequence** - 使用 `prompt | llm` 语法创建调用链
3. **ChatOpenAI** - 调用 OpenAI API
4. **Mock 测试** - 使用 `unittest.mock` 测试 LLM 调用

## 边界说明

### ✅ 支持的功能

- 输入产品名称、目标用户、风格三个字段生成文案
- 必填字段校验（产品、目标用户为空时提示重新输入）
- 可选字段跳过（风格可为空，使用默认值）
- 循环生成多篇文案
- 支持 OpenAI 和小米 MIMO 等兼容 OpenAI 格式的 API

### ❌ 不支持的功能

- **多轮上下文记忆**：每次生成独立，不保留历史对话
- **历史记录保存**：关闭程序后输入信息丢失
- **Web UI / GUI**：仅支持终端交互
- **多语言支持**：仅支持中文文案生成
- **广告法违禁词检测**：不对生成内容做合规性检查
- **实时联网搜索**：不获取实时热点信息

### ⚠️ 已知限制

- 生成文案字数可能不稳定（Prompt 要求 300-500 字，但 LLM 不一定严格遵守）
- 需要有效的 API Key 才能运行完整流程
- 测试使用 Mock，不验证实际 API 调用效果

## 常见问题

### Q: 测试时报错 `ModuleNotFoundError: No module named 'langchain'`

A: 确保已激活虚拟环境并安装依赖：
```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

### Q: 运行程序时报错 `OPENAI_API_KEY not set`

A: 检查 `.env` 文件是否存在且包含有效的 API Key：
```bash
cat .env
# 应该看到: OPENAI_API_KEY=sk-xxx...
```

### Q: 如何使用其他模型？

A: 在 `.env` 中添加：
```
OPENAI_MODEL=gpt-4
```

## License

MIT
