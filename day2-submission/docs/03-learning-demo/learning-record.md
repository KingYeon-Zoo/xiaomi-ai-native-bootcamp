# Learning Record — LangChain RunnableSequence

## 我知道

1. PromptTemplate 可以声明输入变量，并把字典格式化为 PromptValue。
2. LangChain 的 `|` 可以把 Runnable 连接成顺序链，`.invoke()` 执行一次输入。
3. 外部模型会引入密钥、网络和费用，因此最小技术验证应先隔离模型变量。

## 我不知道

1. `PromptTemplate | RunnableLambda` 的中间值究竟是字符串还是 PromptValue？可验证方式：在 fake model 中检查对象是否提供 `to_string()`，并用单元测试调用完整链。
2. RunnableSequence 能否在不接 API 的情况下证明链式组合真实发生？可验证方式：让准备阶段插入 `[demo-XX]`，只有 Prompt 后的 fake model 才负责提取并输出来源。
3. Python 3.9 系统 LibreSSL 对 LangChain 间接网络依赖是否会产生警告？可验证方式：在干净虚拟环境安装后运行测试，观察 stderr；若 urllib3 v2 警告则限制兼容版本并复测。

## 如何验证

| 问题 | 命令/方法 | 可观察证据 | 结论 |
|------|-----------|------------|------|
| Prompt 变量 | 断言 `PROMPT.input_variables` | 恰好为 context/question | 已验证 |
| 链式组合 | 查询“可复核交付” | 回答包含资料文本和 `[demo-01]` | 已验证 |
| 无依据拒答 | 查询天气 | 固定输出“资料中没有找到依据。” | 已验证 |
| 空输入 | 调用 `run_demo('   ')` | 抛出“问题不能为空” | 已验证 |
| LibreSSL 警告 | 安装后执行 4 条测试 | 限制 `urllib3<2` 后无警告 | 已验证 |

## 人工判断与取舍

AI 建议直接接 OpenAI/MiMo 展示“真实效果”。我拒绝：本次目标是 30 分钟内跑通陌生技术的最小可验证链，不是评估模型文案质量。fake model 让链结构、PromptValue、引用和拒答都可离线复现，也避免把密钥问题误当成 LangChain 学习结果。

## 未解决疑问与下一步

- 未验证 RunnableSequence 的异步 `.ainvoke()` 与批处理 `.batch()` 在并发异常时如何传播错误。
- 下一步增加一个会主动抛错的 Runnable，分别比较 `.invoke()`、`.batch()` 的错误语义并记录证据。
