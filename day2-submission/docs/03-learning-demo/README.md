# LangChain RunnableSequence 离线最小 Demo

使用 LangChain Core 的 `PromptTemplate | RunnableLambda` 跑通“准备上下文 → Prompt → fake model”链。内置三条课程资料，运行一次查询即可看到回答与来源；资料外问题固定拒答。

## 安装

```bash
cd day2-submission
python3 -m venv .venv
.venv/bin/python -m pip install -r 03-learning-demo/requirements.txt
```

Python 3.9 的系统 LibreSSL 与 urllib3 v2 会产生兼容警告，因此依赖显式限制 `urllib3<2`。

## 运行

```bash
.venv/bin/python 03-learning-demo/demo.py "什么是可复核交付？"
```

实际输出：

```text
根据资料，可复核交付要求保存输入、预期、实际输出和测试结论，让他人无需询问即可验证。 [demo-01]
```

## 测试

```bash
.venv/bin/python -m unittest discover -s 03-learning-demo/tests -v
```

预期：4 条测试全部 `ok`。

## Demo 数据流

```text
question → RunnableLambda(检索三条内置资料) → PromptTemplate → RunnableLambda(fake model) → 回答+来源
```

## 边界与限制

- 只匹配三条内置资料的显式关键词，不做向量检索或语义召回。
- fake model 只转述 Prompt 上下文，不代表真实 LLM 质量。
- 不需要 API Key、网络、数据库或 `.env`。
- 空问题抛出中文 `ValueError`；资料外问题返回固定拒答。
- 这是最小学习 Demo，不保存历史、不提供 UI，也不处理并发。
