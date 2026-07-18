# Day 1 提交包工程约束

## 1. 项目身份

- 项目名称：Day 1 AI Native 训练营提交包
- 项目类型：个人项目的最小闭环
- 业务角色：训练营学员，负责实现、验证、记录与提交
- 时间限制：Day 1 课堂练习范围
- 核心目标：第三方仅凭仓库文件与 README 命令即可复核 RAG 助手和 Bug 修复结果
- 当前阶段：提交审计

## 2. 文档目录规范

- 开发过程 Markdown 的唯一正文目录是根 `docs/` 及其子目录。
- 根目录只保留 `README.md`、`AGENTS.md`；课程检查器硬编码的 `ai-log.md`、`reflection.md` 以及子项目旧路径只作为符号链接兼容入口。
- 源码、测试、FAQ 数据与 Mock 服务按工程目录放置，不混入 `docs/`。
- 不在多个位置复制同一份 Spec、Design、测试记录或复盘正文。

## 3. 资料优先级

1. 训练营原题与六类文件定义：`../day1/README.md`、`../day1/day1材料/6份文件的定义.txt`
2. Day 1 专用检查器：`../day1/check-submission.sh`
3. 本仓库 `docs/spec.md`
4. 本仓库 `docs/design.md` 与 `docs/tasks.md`
5. 当前源码、测试和实际执行结果

题目要求旧路径而 Skill 要求 `docs/` 唯一正文时，保留符号链接兼容入口，并在 `docs/ai-log.md` 记录人工判断。

## 4. 目标与非目标

### 目标

- 交付可运行、可拒答且带来源的 FAQ RAG 最小闭环。
- 交付可复核的 Bug 复现、双假设根因、最小修复与回归证据。
- 让课程专用检查器和项目证据审计都能从明确入口复核。

### 非目标

- 不增加 Web UI、登录、上传或数据库，避免超出 Day 1 范围。
- 不接入真实外部模型 API，避免密钥、网络与费用影响复现。
- 不把关键词检索扩展为向量检索，本次只验证课程最小链路。
- 不重写老师提供的原题、FAQ 或检查脚本。

详细范围以 `docs/spec.md` 为准。

## 5. 阶段门禁

1. 先读题目、评分定义和检查器，再调整提交结构。
2. 先确定目标、非目标、验收和边界，再修改实现。
3. 技术路线必须比较至少两个方案，并记录人工取舍。
4. 每个任务必须写明输入、产出、验证命令和证据位置。
5. 只有实际执行并得到预期结果后才能记录 PASS。
6. 专用检查或审计出现 BLOCKED 时不得宣布完成。

## 6. 允许与禁止

### 允许

- 在 `rag-assistant/`、`bug-fix-lab/`、`docs/` 内完成 Spec 覆盖的最小工作。
- 增加必要测试、证据索引和课程兼容入口。
- 在有执行证据时同步更新 Design、测试记录和风险。

### 禁止

- 修改训练营总目录中的 `day1/` 原题、模板、FAQ 和检查器。
- 在 `docs/` 外新增过程 Markdown 正文。
- 增加与 Spec 无关的框架、服务或产品功能。
- 删除失败记录、降低验收标准或伪造命令输出。
- 提交 `.DS_Store`、缓存、虚拟环境或真实凭证。

## 7. 项目结构与文件路由

| 内容 | 权威 Markdown |
|---|---|
| 工程约束正文 | `docs/engineering-constraints.md` |
| 目标、非目标、验收与边界 | `docs/spec.md` |
| 数据流、接口、方案取舍 | `docs/design.md` |
| 可执行任务 | `docs/tasks.md` |
| AI 协作与人工判断 | `docs/ai-log.md` |
| 测试实际结果 | `docs/test-record.md` |
| Bug 修复证据 | `docs/bugs/` |
| 个人复盘 | `docs/reflection.md` |

## 8. 运行与验证命令

无需安装第三方依赖。

```bash
python3 bug-fix-lab/test.py
python3 rag-assistant/tests/test_basic.py
python3 rag-assistant/tests/test_rag.py
bash ../day1/check-submission.sh .
bash ../.agents/skills/xiaomi-ai-bootcamp/scripts/audit-xiaomi-project.sh . personal
```

## 9. 验收证据映射

| 验收标准 | 实现位置 | 测试/Review | 实际证据 Markdown | 状态 |
|---|---|---|---|---|
| AC-1 FAQ 问题可检索并返回来源 | `rag-assistant/src/` | `tests/test_rag.py` 正确匹配用例 | `docs/test-record.md` | PASS |
| AC-2 资料外问题稳定拒答 | `retrieve.py`、`main.py` | 资料外、混淆、停用词用例 | `docs/test-record.md` | PASS |
| AC-3 接口与项目骨架可加载 | `rag-assistant/` | `tests/test_basic.py` | `docs/test-record.md` | PASS |
| AC-4 空标题与字符串优先级问题已修复 | `bug-fix-lab/src/task_manager.py` | `bug-fix-lab/test.py` | `docs/bugs/`、`docs/test-record.md` | PASS |
| AC-5 提交文件与路径完整 | 全仓库 | Day 1 专用检查器 | `docs/test-record.md` | PASS |

## 10. AI 协作

关键协作写入 `docs/ai-log.md`，每条必须包含目的、输入、建议、人工判断、验证。人工判断要说明采纳、修改或拒绝的具体内容与理由，不能只写“同意”。

## 11. 失败处理

- 测试失败：保留输入、预期、实际和失败结论，定位后最小修复并全量回归。
- Mock 服务失败：先检查端口和进程，不改为不可复现的外部 API。
- 资料冲突：以原题和专用检查器为准，由个人负责人记录判断。
- 路径兼容失败：检查符号链接是否被 Git 正确保留。

## 12. 团队规则

不适用。本提交为个人练习；同学互评只作为外部 Review 证据，不替代个人责任。

## 13. 完成定义

- **PASS**：必交文件非空；过程正文统一位于 `docs/`；README 命令可复现；验收与测试可追溯；AI 日志包含实质人工判断；两个检查器无阻塞。
- **WARNING**：主要证据存在，但命令、映射、边界或人工判断仍不充分。
- **BLOCKED**：关键文件缺失、存在过程正文散落、命令不可复现、测试失败、模板占位符或结果真实性风险。
