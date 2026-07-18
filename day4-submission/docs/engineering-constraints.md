# Day4 提交工程约束

## 1. 项目身份

- 项目名称：小米 AI Native 训练营 Day4 数据分析与机器学习作业
- 项目类型：个人课程项目
- 业务角色：运维日志分析者、邮件过滤实验开发者、Agent 代码审查者
- 时间限制：Project 1 三课时、Project 2 三课时、Project 3 一课时 45 分钟
- 核心目标：第三方只依靠仓库和 README 命令即可复核两条数据流程与一次受控代码审查
- 当前阶段：已提交

## 2. 文档目录规范与冲突裁决

训练营通用 Skill 要求过程 Markdown 位于 `docs/`，而 Day4 最新数据说明明确要求每个项目根目录存在 `spec.md`、`test-strategy.md`、`AI-log.md`、`analysis_report.md`，并写明不得重命名。采用“更具体、更新的任务规则优先”：上述必交文件保留在题目指定位置；跨项目的工程约束、任务、测试总记录、AI 总日志与复盘位于仓库 `docs/`。不创建 Demo 旧版 `prd.md`、`design.md`、`dev.md`。

## 3. 权威资料优先级

1. `../day4-data/README.md`
2. `../day4-data/project1/项目一_Apache日志分析_作业要求与评分标准_精简版.md`
3. `../day4-data/project2/项目二_垃圾邮件过滤_作业要求与评分标准_精简版.md`
4. `../day4-data/项目三_作业要求.md`
5. Project 1/2 的 `spec.md` 与 `test-strategy.md`
6. 当前代码、自动化测试与实际输出
7. `../day4-demo/` 仅作反例和接口参考，不作为最终结构依据

老师提供的数据、题目、Demo 均只读，不修改、不提交副本。

## 4. 目标与非目标

### 目标

- P1 对约 56,481 行 Apache 日志生成五字段 CSV、三类筛选、三张图与可追溯报告。
- P2 对六个 SpamAssassin 压缩包执行 raw/cleaned 数据契约、固定切分、规则/NB 对比、四张图与误判分析。
- P3 覆盖两个项目的三维审查，只选一个真实问题，最多修改两个文件，并完成 V1/V2/V3。
- 全部必交文件名称与最终清单一致，命令实际可执行。

### 非目标

- 不分析可选 Linux.log：它不影响必交验收，加入第二种格式会扩大解析边界。
- 不引入深度学习、LLM、数据库或 Web UI：课堂重点是数据契约、测试和可信判断。
- 不把附件、图片 OCR 或多语言模型加入邮件过滤：数据与时间不足以可靠验证。
- 不为追求指标反复使用最终测试集调参，也不修改标签或删除困难样本。
- 不复制 Demo 的旧目录、冗长模板或未验证数字。

## 5. 阶段门禁与事实状态

1. 先读题目与最终清单，再确定结构；Demo 与最终要求冲突时记录裁决。
2. 验收标准必须映射到测试或真实主流程。
3. 报告数字只能由本次 `main.py` 生成。
4. Project 3 的修改阶段必须先保存可复现的修改前证据，再改一个问题。
5. 测试、主流程、清单审计任一失败均为 BLOCKED，不得推送。

已验证事实：六个邮件压缩包共加载 7,449 个样本；P1 结构化 52,004 行并记录 4,478 条非标准续行；P2 NB 的 Accuracy/Precision/Recall 均达到建议门槛；系统自带 Python 3.9.6 缺依赖，验收使用项目 `.venv` 的 Python 3.12.13；小米 GitLab 私有项目 main 已推送并核验远端 commit。

## 6. 允许与禁止

允许修改 `day4-submission/`；允许读取 `day4-data/`、`day4-demo/` 和课程材料。禁止修改只读输入、提交 `.env`/token/原始语料、伪造 TDD 顺序、伪造测试结果、降低门槛、无关重构或绕过失败。

## 7. 文件与证据路由

| 内容 | 权威位置 |
|---|---|
| 总览与复现 | `README.md` |
| 工程约束 | `docs/engineering-constraints.md` |
| 跨项目任务 | `docs/tasks.md` |
| AI 决策总账 | `docs/ai-log.md` |
| 测试实际记录 | `docs/test-record.md` |
| 深度复盘 | `docs/reflection.md` |
| P1/P2 范围、设计、任务、变更 | 各项目 `spec.md`（按题目合并） |
| P1/P2 测试策略 | 各项目 `test-strategy.md` |
| 每课时 AI 记录 | 各项目 `AI-log.md` |
| Project 3 唯一报告 | `agent_review_report.md` |

## 8. 运行与验证命令

```bash
# 安装
python3.10 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

# 单元与集成测试
.venv/bin/python -m pytest project1/tests project2/tests -q

# 全量运行（从仓库根目录）
(cd project1 && ../.venv/bin/python main.py --archive ../../day4-data/project1/Apache.tar.gz)
(cd project2 && ../.venv/bin/python main.py --data-dir ../../day4-data/project2)

# 提交审计（从训练营工作区根目录）
bash .agents/skills/xiaomi-ai-bootcamp/scripts/audit-xiaomi-project.sh day4-submission personal
```

命令状态以 `docs/test-record.md` 为准；此处不预先宣称 PASS。

## 9. 验收证据映射

| 验收标准 | 实现 | 测试/Review | 证据 | 当前状态 |
|---|---|---|---|---|
| P1 五字段、非法行不中断 | `project1/log_analyzer/log_parser.py` | `test_log_parser.py` + 全量入口 | `docs/test-record.md` | PASS |
| P1 三筛选、四统计、三图 | `error_filter.py`、`statistics.py`、`visualizer.py` | P1 单测/集成/全量 | 同上 | PASS |
| P2 数据契约与九步清洗 | `text_cleaner.py`、`utils.py` | `test_text_cleaner.py` + 全量输出字段检查 | 同上 | PASS |
| P2 同测试集比较且无 fit 泄漏 | `project2/main.py`、`naive_bayes.py` | 集成测试 + 报告指标 | 同上 | PASS |
| P3 一问题、三验证、≤2 文件 | `agent_review_report.md` | Git 历史与实际命令 | 同上 | PASS |

## 10. AI 协作与失败处理

关键记录必须含目的、输入、AI 建议、人工判断、验证。实现骨架早于本工程约束文件落盘，这是一次真实流程偏差，不能在文档中改写为“先写完约束再编码”；通过补做事实基线、验收映射和审计纠正，并在复盘说明如何避免复发。

命令失败时保留现象、根因、修复和复测；资料冲突由个人负责人朱清扬依据最新题目裁决；测试失败即 BLOCKED。

## 11. 完成定义

- PASS：必交文件齐全、无占位符、两项目测试与全量入口通过、报告数字可由输出复算、P3 修改范围可由 Git 复核、专用清单与 Skill 审计无 BLOCKED、远端 commit 可核验。
- WARNING：主要流程通过但文档映射、边界证据或外部复现有不足。
- BLOCKED：关键文件缺失、命令失败、结果不一致、token 泄漏、测试被弱化或远端提交失败。
