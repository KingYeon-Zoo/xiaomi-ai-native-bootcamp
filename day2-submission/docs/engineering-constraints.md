# Day 2 提交包工程约束

## 1. 项目身份

- 项目名称：Day 2 AI Native 训练营作业
- 项目类型：个人项目的四个课程最小闭环
- 业务角色：训练营学员，负责设计、实现、评测、审查与提交
- 时间限制：Day 2 课堂任务范围
- 核心目标：评审者能从一个仓库复核工作流、Spec Coding、陌生技术 Demo 和训练营 Agent 四组产物
- 当前阶段：提交审计

## 2. 文档目录规范

- 所有过程 Markdown 的唯一正文目录为根 `docs/` 及其编号子目录。
- 根目录只保留 `README.md`、`AGENTS.md`；课程检查器要求的根 AI 日志、复盘和各任务原路径只作为符号链接兼容入口。
- Python 源码、测试、JSON、依赖和审查夹具保留在对应编号工程目录。
- `docs/` 内按 `01` 至 `04` 分区保存任务证据，仓库级证据固定使用 `spec.md`、`design.md`、`tasks.md`、`ai-log.md`、`test-record.md`、`reflection.md`。

## 3. 资料优先级

1. 课程任务原文：`../课件/day2.docx`
2. 本仓库课程专用检查器：`check-submission.sh`
3. `docs/spec.md` 与各编号目录的任务规格
4. `docs/design.md`、`docs/tasks.md` 与各任务设计
5. 当前源码、测试和实际执行结果

课程要求固定文件名而 Skill 要求 `docs/` 唯一正文时，不改写课程要求，使用 Git 符号链接提供兼容入口，并在 `docs/ai-log.md` 记录人工判断。

## 4. 目标与非目标

### 目标

- 完成提交检查工作流及 PASS/WARNING/BLOCKED 证据。
- 完成 today/submit/check 任务助手的 Spec Coding、Eval 和上下文包。
- 完成可离线复现的 LangChain 最小 Demo 与证据型同桌评审。
- 完成训练营助教 Agent 的设计、工具、校验和六类代码风险审查。

### 非目标

- 不构建 Web、登录、多人协作或跨日期任务系统。
- 不接入真实模型 API、数据库或远程服务。
- 不把单文件安全审查描述为全仓库穷尽扫描。
- 不改写课程题目、硬性文件清单或测试预期来迁就实现。

详细范围以 `docs/spec.md` 为准。

## 5. 阶段门禁

1. 先读任务原文与硬性验收，再更新仓库级范围。
2. 先完成目标、非目标、边界与验收，再修改代码。
3. 方案选择必须记录成本、风险、拒绝理由和两天可交付性。
4. 每个任务必须写输入、产出、验证命令和证据路径。
5. 保留修复前失败；只有复测结果才能标记最终 PASS。
6. 专用检查或项目审计存在 BLOCKED 时不得提交。

## 6. 允许与禁止

### 允许

- 在 `01-submission-workflow/` 至 `04-training-agent/` 和 `docs/` 内完成 Spec 覆盖的最小调整。
- 为验收增加测试、证据索引和课程旧路径兼容入口。
- 在有实际结果时同步更新设计、测试记录和残留风险。

### 禁止

- 修改 `../课件/day2.docx` 或训练营原始材料。
- 在 `docs/` 外维护过程 Markdown 正文或复制两份内容。
- 增加真实密钥、任意命令执行、任意文件读取或超范围功能。
- 删除失败证据、伪造同桌评审、测试、AI 判断或提交结果。
- 提交 `.venv`、`.DS_Store`、缓存、状态文件或凭证。

## 7. 项目结构与文件路由

| 内容 | 权威 Markdown |
|---|---|
| 工程约束正文 | `docs/engineering-constraints.md` |
| 仓库级范围与验收 | `docs/spec.md` |
| 总体数据流与方案取舍 | `docs/design.md` |
| 仓库级可验证任务 | `docs/tasks.md` |
| 根 AI 协作日志 | `docs/ai-log.md` |
| 根测试与审计结果 | `docs/test-record.md` |
| 个人复盘 | `docs/reflection.md` |
| 提交检查工作流证据 | `docs/01-submission-workflow/` |
| Spec Coding 与 Eval | `docs/02-task-assistant/` |
| LangChain Demo 与同桌评审 | `docs/03-learning-demo/` |
| 训练营 Agent 与安全审查 | `docs/04-training-agent/` |

## 8. 运行与验证命令

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r 03-learning-demo/requirements.txt
python3 -m unittest discover -s 01-submission-workflow/tests -v
python3 -m unittest discover -s 02-task-assistant/tests -v
.venv/bin/python -m unittest discover -s 03-learning-demo/tests -v
python3 -m unittest discover -s 04-training-agent/tests -v
bash check-submission.sh
bash ../.agents/skills/xiaomi-ai-bootcamp/scripts/audit-xiaomi-project.sh . personal
```

## 9. 验收证据映射

| 验收标准 | 实现位置 | 测试/Review | 实际证据 Markdown | 状态 |
|---|---|---|---|---|
| AC-1 工作流三状态和异常兜底可执行 | `01-submission-workflow/` | 5 条 unittest | `docs/01-submission-workflow/`、`docs/test-record.md` | PASS |
| AC-2 任务助手三命令、边界与 Eval 可复核 | `02-task-assistant/` | 8 条 unittest + JSON 检查 | `docs/02-task-assistant/` | PASS |
| AC-3 LangChain 最小链离线可运行 | `03-learning-demo/` | 4 条 unittest | `docs/03-learning-demo/test-record.md` | PASS |
| AC-4 Agent 工具、校验和路径边界可复核 | `04-training-agent/` | 13 条 unittest | `docs/04-training-agent/test-record.md` | PASS |
| AC-5 六类代码风险审查有位置、影响、修复和测试 | 审查夹具 | Review 清单字段检查 | `docs/04-training-agent/review-checklist.md` | PASS |
| AC-6 课程提交包无缺项、缓存和凭证 | 全仓库 | `bash check-submission.sh` | `docs/test-record.md` | PASS |

## 10. AI 协作

根关键决策写入 `docs/ai-log.md`，任务局部决策写入对应编号目录的 `ai-log.md`。每条包含目的、输入、建议、人工判断、验证，重点保留范围收窄、失败修复、安全取舍和文档目录冲突处理。

## 11. 失败处理

- 测试失败：保留输入、预期、实际和归因，最小修复后全量复测。
- LangChain 依赖失败：先按 README 重建 `.venv`，不隐藏安装错误。
- 工具超时或命令不存在：按工作流状态表记录并给出人工复测动作。
- 路径校验失败：默认 BLOCKED，不回退到字符串 `..` 判断。
- 课程路径冲突：保留兼容入口，不修改老师检查器。

## 12. 团队规则

不适用。本仓库为个人提交；`peer-review.md` 是对课堂样例的证据型评审，不虚构团队分工或会议。

## 13. 完成定义

- **PASS**：课程必交文件非空；正文集中在 `docs/`；README 命令可复现；30 条最终自动测试通过；失败记录和验收映射完整；两个检查器无阻塞。
- **WARNING**：主要证据存在，但命令、映射、边界、Review 或人工判断仍不足。
- **BLOCKED**：关键文件缺失、过程正文散落、测试失败、JSON 无效、跟踪缓存或凭证、存在占位符或结果真实性风险。
