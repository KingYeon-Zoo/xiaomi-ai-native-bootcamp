# Day 2 仓库级可验证任务

| 任务 | 输入 | 产出 | 验证命令/Review | 证据位置 | 状态 |
|---|---|---|---|---|---|
| T1 提交检查工作流 | 课程三状态与工具要求 | 工作流文档、执行器、规则、测试 | `python3 -m unittest discover -s 01-submission-workflow/tests -v` | `docs/01-submission-workflow/` | 完成 |
| T2 Spec Coding 任务助手 | today/submit/check 契约 | Spec、Plan、Tasks、AGENTS、CLI | `python3 -m unittest discover -s 02-task-assistant/tests -v` | `docs/02-task-assistant/` | 完成 |
| T3 Eval 与上下文包 | 三类 Eval、七层上下文要求 | JSON、测试记录、context pack | `python3 -m json.tool 02-task-assistant/eval-cases.json` | `docs/02-task-assistant/` | 完成 |
| T4 LangChain 最小学习 | 30 分钟陌生技术任务 | Demo、学习记录、测试、局部日志 | `.venv/bin/python -m unittest discover -s 03-learning-demo/tests -v` | `docs/03-learning-demo/` | 完成 |
| T5 同桌证据型评审 | 课堂小红书 Demo | 四维 Review、问题和 WARNING 结论 | 核对命令、行号、限制和建议 | `docs/03-learning-demo/peer-review.md` | 完成 |
| T6 训练营助教 Agent | RAG、任务、提交校验要求 | 设计、工具、Validator、测试 | `python3 -m unittest discover -s 04-training-agent/tests -v` | `docs/04-training-agent/` | 完成 |
| T7 六类风险审查 | `unsafe_agent.py` | 六项 finding 与回归计划 | 专用检查器统计六行 finding | `docs/04-training-agent/review-checklist.md` | 完成 |
| T8 规范化与提交审计 | 全仓库 | `docs/` 唯一正文、兼容入口、审计结论 | `bash check-submission.sh` + Skill 审计 | `docs/test-record.md` | 完成 |

只有对应验证实际通过后，任务才能标记“完成”。
