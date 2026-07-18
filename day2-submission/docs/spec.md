# Day 2 仓库级规格说明

## 目标

1. 交付可执行的提交检查工作流，显式处理 PASS、WARNING、BLOCKED 和至少两类异常。
2. 交付 today/submit/check 任务助手，并用 Spec、Plan、Tasks、AGENTS、Eval 和测试记录约束实现。
3. 交付不依赖真实 API 的 LangChain 最小学习 Demo，以及有证据、有问题结论的同桌评审。
4. 交付训练营助教 Agent 的数据流、工具、校验、测试和六类 AI 代码风险审查。
5. 用统一 `docs/`、README 命令和一键检查形成仓库级证据链。

## 非目标

1. 不实现 Web UI、账户、多人协作、跨日期归档或自定义任务。
2. 不使用真实模型、外部数据库、网络服务或真实 API Key。
3. 不把 Demo 扩展为完整 RAG 产品，也不测试模型文案质量。
4. 不修复审查夹具 `unsafe_agent.py`；其用途是保留风险证据。
5. 不宣称完成未执行的真实 API、并发、跨平台或穷尽安全验证。

## 边界与失败行为

- 工作流遇到缺 README、测试无法启动或失败时必须 BLOCKED；非关键文档不足或超时按规则 WARNING。
- 任务助手的未知文件、重复提交、损坏状态和无子命令必须给出人类可读结果，不泄露堆栈。
- LangChain Demo 的资料外问题固定拒答，空问题抛明确异常。
- Agent 访问允许根目录外路径时必须 BLOCKED；RAG 无命中与知识库加载失败必须区分。
- 课程要求的旧 Markdown 路径必须可访问，但正文不得复制散落。

## 验收标准

| ID | 可复现标准 | 验证方式 |
|---|---|---|
| AC-1 | 工作流 5 条测试通过，ai-workflow 含三输入、两工具、三状态、规则表、失败兜底和证据位置 | `01-submission-workflow/tests`、专用检查器 |
| AC-2 | 任务助手 8 条测试通过，Eval JSON 合法并覆盖正确回答、范围外拒答、工具失败 | `02-task-assistant/tests`、`python3 -m json.tool` |
| AC-3 | LangChain 4 条离线测试通过，学习记录包含已知、未知、验证和残留疑问 | `03-learning-demo/tests`、对应 docs |
| AC-4 | Agent 13 条测试通过，设计含数据流、工具定义、校验规则和测试用例 | `04-training-agent/tests`、对应 docs |
| AC-5 | 审查清单覆盖六类风险，每项含位置、影响、修复和测试方法 | `review-checklist.md` 字段检查 |
| AC-6 | `bash check-submission.sh` 与项目审计均无 BLOCKED | 两条审计命令 |
