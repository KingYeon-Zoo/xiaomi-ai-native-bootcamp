# 训练营助教 Agent 工具

提供课程 FAQ 检索、Day2 任务管理和提交包校验三个本地工具，并通过 `agent-design.md` 定义 Router、Validator 和 Answer 的边界。

## 安装

需要 Python 3.9+，无第三方依赖。

## 运行

```bash
cd 04-training-agent
python3 -c "from tools.rag import rag_search; print(rag_search('什么是可复核交付？'))"
```

## 测试

从仓库根目录执行：

```bash
python3 -m unittest discover -s 04-training-agent/tests -v
```

预期 13 条工具测试全部通过。

## 边界

- RAG 只查本地 FAQ，无依据固定拒答。
- 任务清单固定五项，不记录历史。
- 提交校验只能读取显式 allowed root 下的固定文件。
- `review-target/` 为代码审查夹具，禁止运行。
