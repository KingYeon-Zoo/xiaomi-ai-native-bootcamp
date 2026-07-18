# Test Record — LangChain 最小 Demo

## 环境

- Python 3.9.6
- `langchain-core==0.3.86`
- `urllib3==1.26.20`
- 测试日期：2026-07-13

## 验证结果

命令：`.venv/bin/python -m unittest discover -s 03-learning-demo/tests -v`

| # | 输入/命令 | 预期 | 实际 | 结果 |
|---|-----------|------|------|------|
| 1 | 检查 Prompt 变量 | context/question 两项 | 集合恰好包含两项 | ✅ PASS |
| 2 | “什么是可复核交付？” | 基于资料回答并引用 demo-01 | 返回可复核交付定义和 `[demo-01]` | ✅ PASS |
| 3 | “今天北京天气怎么样？” | 固定拒答 | `资料中没有找到依据。` | ✅ PASS |
| 4 | 三个空格 | 明确拒绝空问题 | 抛出 `ValueError: 问题不能为空` | ✅ PASS |

## 运行日志

```text
Ran 4 tests in 0.006s
OK
```

最小运行命令：`.venv/bin/python 03-learning-demo/demo.py '什么是可复核交付？'`

实际输出：`根据资料，可复核交付要求保存输入、预期、实际输出和测试结论，让他人无需询问即可验证。 [demo-01]`

## 未解决疑问和下一步

当前只验证同步 `.invoke()`，未验证 `.batch()` 中部分输入失败时的返回语义。下一步加入批处理异常实验，但不纳入本次最小 Demo 范围。
