# RAG 课程助手 — 学生项目

> Day1 S3-S8 渐进式构建项目：从零开始搭建一个基于 course-faq.md 的 CLI RAG 问答助手。

## 项目目标

构建一个 CLI 工具，用户输入 Day1 训练营相关问题，系统检索相关 FAQ 条目，拼接 Prompt，调用 LLM 生成带来源引用的回答。

## 目录结构

```
rag-assistant/
├── data/
│   └── course-faq.md           # 知识库（10 条 FAQ，按 [faq-XX] 编号）
├── src/
│   ├── main.py                 # CLI 入口
│   ├── retrieve.py             # 检索模块（切片 + 关键词匹配）
│   └── answer.py               # 回答模块（Prompt 拼接 + LLM 调用）
├── llm-mock/
│   ├── mock_server.py          # LLM Mock 服务（端口 9876）
│   └── README.md               # Mock 使用说明
├── tests/
│   ├── test_basic.py           # 基础测试（文件存在 + 模块加载 + 接口契约）
│   ├── test_rag.py             # 自动化测试（13 个用例，自动启停 mock）
│   └── questions.json          # 测试用例数据
├── docs/
│   ├── spec.md                 # Spec（目标/非目标/验收标准）
│   ├── design.md               # 设计文档（逻辑视图/流程视图/接口标准）
│   ├── ai-log.md               # AI 协作日志（12 条决策记录）
│   ├── test-record.md          # 测试记录（34 个用例全部通过）
│   ├── task.md                 # 任务计划
│   └── reflection.md           # 复盘反思
└── README.md                   # 本文件
```

## 快速开始

### 运行 RAG 助手

```bash
# 直接调用（会自动使用 mock LLM）
python src/main.py "Day1要交什么？"
python src/main.py "奖学金政策？"       # 应拒答
python src/main.py ""                   # 应提示输入
```

### 运行测试

```bash
# 基础测试（文件存在 + 接口契约）
python tests/test_basic.py

# 自动化测试（13 个用例，自动启停 mock server）
python tests/test_rag.py
```

### 启动 LLM Mock（手动调试用）

```bash
python llm-mock/mock_server.py
# 默认监听 http://localhost:9876
```

## 技术方案

- **检索**：关键词匹配 + 同义词映射 + 停用词过滤 + proximity 评分
- **切片**：按 `## [faq-XX]` 标题分割为 10 个 chunk
- **拒答**：零命中拒答（retrieve 返回空）+ mock 自身拒答（混淆类问题）
- **LLM**：使用 mock_server.py，兼容 OpenAI Chat Completions API 格式

## 约束

- CLI 工具，不支持 Web UI
- 不引入数据库或外部存储
- 仅基于 `course-faq.md` 回答问题
- 资料外问题必须拒答，不能编造
- 回答必须注明来源 `[faq-XX]`
- 仅使用 Python 标准库
