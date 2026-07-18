# Day 1 AI Native 训练营提交包

本仓库交付两个可独立复核的 Day 1 练习：`rag-assistant/` 完成基于课程 FAQ 的最小 RAG 闭环，`bug-fix-lab/` 完成任务管理器的复现、根因分析、最小修复与回归。过程证据统一写入 `docs/`，课程检查器要求的旧文件路径通过兼容入口指向同一正文。

## 快速开始

```bash
git clone https://github.com/KingYeon-Zoo/xiaomi-ai-native-bootcamp.git
cd xiaomi-ai-native-bootcamp/day1-submission
python3 --version
```

## 安装

项目只使用 Python 标准库，无第三方依赖。已验证环境为 macOS、Python 3.9.6；Python 3.9 及以上可直接运行。

## 运行

RAG 助手的自动测试会自动启动和关闭本地 Mock LLM：

```bash
python3 rag-assistant/tests/test_rag.py
```

手动查询时，先在一个终端启动 Mock LLM，再在另一个终端提问：

```bash
python3 rag-assistant/llm-mock/mock_server.py
python3 rag-assistant/src/main.py "什么是可复核交付？"
```

## 测试

```bash
python3 bug-fix-lab/test.py
python3 rag-assistant/tests/test_basic.py
python3 rag-assistant/tests/test_rag.py
```

提交前从训练营总目录运行：

```bash
bash day1/check-submission.sh day1-submission
bash .agents/skills/xiaomi-ai-bootcamp/scripts/audit-xiaomi-project.sh day1-submission personal
```

## 项目结构

```text
day1-submission/
├── AGENTS.md
├── README.md
├── docs/
│   ├── engineering-constraints.md
│   ├── spec.md
│   ├── design.md
│   ├── tasks.md
│   ├── ai-log.md
│   ├── test-record.md
│   ├── reflection.md
│   └── bugs/
├── rag-assistant/
│   ├── data/course-faq.md
│   ├── llm-mock/mock_server.py
│   ├── src/
│   └── tests/
└── bug-fix-lab/
    ├── src/task_manager.py
    └── test.py
```

## 证据导航

| 评审问题 | 权威证据 |
|---|---|
| 做什么、不做什么、怎么算完成 | `docs/spec.md` |
| 为什么采用当前数据流与技术方案 | `docs/design.md` |
| 每项任务如何验证 | `docs/tasks.md` |
| AI 建议如何被采纳、修改或拒绝 | `docs/ai-log.md` |
| 测试输入、预期、实际与结果 | `docs/test-record.md` |
| Bug 复现、假设、修复和回归 | `docs/bugs/` |
| 个人判断与后续改进 | `docs/reflection.md` |

## 约束与限制

- RAG 只检索固定的 `course-faq.md`，不支持文件上传、向量数据库或 Web UI。
- 回答由本地 Mock LLM 生成，用于验证检索、Prompt、引用和拒答链路，不代表真实模型效果。
- 关键词检索不具备语义召回能力；未命中资料时返回固定拒答。
- `bug-fix-lab/` 只修复课程指定的优先级类型与空标题问题，不扩展完整任务管理产品。

## 故障排查

- 端口 `9876` 被占用：关闭占用进程后重试 `test_rag.py`。
- 手动运行出现“调用 LLM 时出错”：确认 `mock_server.py` 已启动。
- 导入失败：确认从仓库根目录执行上述命令，不要移动 `src/`、`data/` 或 `tests/`。
- 专用检查器报告缺文件：确认 Git 客户端保留了仓库中的符号链接兼容入口。
