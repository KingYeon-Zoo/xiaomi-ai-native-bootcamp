# 小米 AI Native 训练营：6 天学习与项目实践

本仓库整理了我在小米 AI Native 训练营 6 天课程中的练习、个人作业、团队项目、代码实现、测试记录与 AI 协作证据。

这里不只是最终代码的集合，也保留了从需求澄清、方案设计、任务拆分、AI 协作、实现测试到复盘答辩的完整工程过程。希望它能帮助正在学习 AI Native 开发、Spec Coding、Agent 工程或 AI 辅助软件研发的同学，理解如何把一次 AI 编程实践做成可运行、可验证、可追溯的交付。

> [!IMPORTANT]
> `slide/` 目录包含训练营内部课件及可能涉及公司内部信息的材料，**不属于本公开仓库的发布范围，也不会上传到 GitHub**。README 只介绍本人完成的学习内容和项目成果，不复述、不转载内部课件。请勿通过提交、Issue、Pull Request 或其他方式补传相关文件。

## 仓库亮点

- 覆盖 6 天训练内容：从最小 RAG、Bug 修复，到 Spec Coding、Agent、全栈应用、数据分析和团队大作业。
- 同时保留课堂 Demo 与个人提交，便于对照学习材料和最终交付。
- 强调“可复核交付”：代码、Spec、Design、Tasks、AI Log、测试和复盘相互关联。
- 包含 Python、FastAPI、React、LangChain、LangGraph、MongoDB、传统机器学习等多种实践。
- Day 5–6 团队项目 LOOPS 提供完整的问题诊断、方案取舍、系统设计、原型、验证和答辩材料。

## 六天学习路线

| 天数 | 主题 | 主要内容 | 代表产物 |
|---|---|---|---|
| Day 1 | AI Native 工程入门 | 可复核交付、Bug 修复、最小 RAG、Mock LLM、测试闭环 | RAG 课程助手、任务管理器 Bug 修复 |
| Day 2 | 工作流、Spec Coding 与 Agent | 提交检查工作流、Spec/Plan/Tasks、Eval、LangChain Demo、助教 Agent | 学习任务 CLI、训练营助教 Agent |
| Day 3 | AI 辅助全栈开发 | PRD、计划、前后端协作、接口契约、端到端测试 | TripSplit 旅行 AA 结算助手 |
| Day 4 | AI 数据工程实践 | Apache 日志分析、垃圾邮件过滤、可视化、Agent 代码可信审查 | 日志分析器、垃圾邮件分类器 |
| Day 5 | 团队项目：诊断与方案 | 真实问题澄清、多方案反证、人工取舍、MVP 与端到端设计 | LOOPS 双路线 AI 内容审核方案 |
| Day 6 | 团队项目：集成与交付 | Agent 实现、人工复核、验证、风险审查、复盘与答辩 | LOOPS 可运行原型与完整证据链 |

## 目录导航

```text
.
├── day1-demo/                     # Day 1 课堂练习与模板
├── day1-submission/               # Day 1 个人提交
├── day2-demo/                     # Day 2 工作流、Spec Coding、LangChain、Agent Demo
├── day2-submission/               # Day 2 个人提交
├── day3-demo/                     # Day 3 TripSplit 参考 Demo
├── day3-submission/               # Day 3 全栈项目提交
├── day4-data/                     # Day 4 使用的公开数据集与数据说明
├── day4-demo/                     # Day 4 日志分析与垃圾邮件过滤 Demo
├── day4-submission/               # Day 4 数据项目提交
├── day5-submission-Loops Aget/    # Day 5–6 LOOPS 团队大作业
└── .agents/                       # 本仓库使用的项目级工程规范与检查工具
```

为保证仓库可安全公开，以下本地生成内容不会提交：内部 `slide/`、`.env`、虚拟环境、`node_modules`、缓存、日志、嵌套仓库元数据和操作系统文件。需要依赖时，请按各子项目的 `requirements.txt` 或 `package-lock.json` 在本地重新安装。

## Day 1：可复核交付、Bug 修复与最小 RAG

Day 1 的重点不是堆叠功能，而是建立 AI Native 项目的最小工程闭环：

1. 先写清目标、非目标和验收标准。
2. 使用测试复现 Bug，记录根因假设，再进行最小修复。
3. 将检索、Prompt、回答和引用组成最小 RAG 链路。
4. 使用本地 Mock LLM，让测试不依赖外部 API。
5. 用 README、Spec、Design、AI Log、Test Record 和 Reflection 构成可复核证据。

主要目录：

- [`day1-demo/`](day1-demo/)：提交包评审练习、Bug 修复练习、RAG 材料和文档模板。
- [`day1-submission/`](day1-submission/)：个人完成的 RAG 课程助手与 Bug 修复提交。
- [`day1-submission/docs/`](day1-submission/docs/)：需求、设计、任务、AI 协作、测试与复盘证据。

快速验证：

```bash
cd day1-submission
python3 bug-fix-lab/test.py
python3 rag-assistant/tests/test_basic.py
python3 rag-assistant/tests/test_rag.py
```

Day 1 项目只使用 Python 标准库。RAG 自动测试会自行启动和关闭本地 Mock LLM，不需要 API Key。

## Day 2：工作流、Spec Coding、LangChain 与 Agent

Day 2 将“让 AI 写代码”扩展为“给 AI 一个可执行的工程上下文”。内容分为四部分：

- 提交检查工作流：将必交文件、状态规则和报告模板编码为可执行检查器。
- Spec Coding：围绕任务清单 CLI 编写 Spec、Plan、Tasks、Eval Cases 与上下文包。
- 陌生技术学习：通过 LangChain 最小 Demo 验证 Prompt、Runnable 和 Mock 测试。
- Agent 工程：把 RAG、任务管理和提交校验封装成助教 Agent 工具，并审查不安全样例。

主要目录：

- [`day2-demo/1-workflow/`](day2-demo/1-workflow/)：工作流定义与资源。
- [`day2-demo/2-specCoding/`](day2-demo/2-specCoding/)：Spec Coding 示例。
- [`day2-demo/3-learningDemo/`](day2-demo/3-learningDemo/)：小红书文案生成器与 LangChain 学习记录。
- [`day2-demo/4-agent/`](day2-demo/4-agent/)：训练营 Agent 工具示例。
- [`day2-submission/`](day2-submission/)：整合后的 Day 2 个人提交。

快速验证：

```bash
cd day2-submission
python3 -m unittest discover -s 01-submission-workflow/tests -v
python3 -m unittest discover -s 02-task-assistant/tests -v
python3 -m unittest discover -s 04-training-agent/tests -v
bash check-submission.sh
```

LangChain Demo 需要单独安装依赖：

```bash
cd day2-submission
python3 -m venv .venv
.venv/bin/python -m pip install -r 03-learning-demo/requirements.txt
.venv/bin/python -m unittest discover -s 03-learning-demo/tests -v
```

## Day 3：TripSplit AI 辅助全栈项目

Day 3 使用 TripSplit 旅行 AA 结算助手练习全栈交付。项目支持创建旅行、添加成员、记录共同支出、计算个人余额，并生成尽量精简的转账方案。

这一阶段重点关注：

- 从 PRD 到 Plan、Tasks 和测试的任务分解。
- React 前端与 FastAPI 后端之间的 API 契约。
- JSON 本地持久化和结算算法。
- 正常、边界和失败场景测试。
- 对老师提供的业务基线与个人完成部分进行清晰归因。

技术栈：

- 前端：React、Vite、原生 Fetch、Vitest。
- 后端：Python、FastAPI、Pydantic、Pytest。
- 存储：本地 JSON。

主要目录：

- [`day3-demo/tripSplit/`](day3-demo/tripSplit/)：TripSplit 参考实现。
- [`day3-submission/`](day3-submission/)：个人整理、验证并建立证据链的提交版本。
- [`day3-submission/docs/交付文档/`](day3-submission/docs/交付文档/)：PRD、方案、开发流程、测试策略和质量门禁。

启动后端：

```bash
cd day3-submission/backend
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn main:app --reload
```

启动前端：

```bash
cd day3-submission/frontend
npm ci
npm run dev
```

测试：

```bash
cd day3-submission/backend
.venv/bin/python -m pytest tests/ -q

cd ../frontend
npm test -- --run
```

## Day 4：日志分析、垃圾邮件过滤与 Agent 审查

Day 4 关注 AI 在数据分析和可信工程中的应用，包含三个方向。

### Project 1：Apache 日志分析

- 解析 Apache 错误日志并结构化时间、级别、模块和错误码。
- 按错误级别、模块、关键词和日期进行统计。
- 输出 CSV 分析结果和趋势、分布、模块对比图表。
- 使用单元测试与集成测试验证解析、过滤、统计和可视化链路。

### Project 2：垃圾邮件过滤

- 清洗 SpamAssassin 公开邮件语料。
- 提取文本特征。
- 对比规则过滤器和朴素贝叶斯分类器。
- 生成混淆矩阵、词频对比和模型指标图。
- 记录误判、限制和适用边界。

### Project 3：Agent 代码可信审查

- 从安全性、可靠性和可维护性角度审查 Agent 代码。
- 区分可验证问题、风险推断与改进建议。
- 避免把不安全的 Review Target 当作可执行程序运行。

主要目录：

- [`day4-data/`](day4-data/)：Loghub Apache 日志与 SpamAssassin 公开语料说明及压缩数据。
- [`day4-demo/`](day4-demo/)：两个数据项目的课堂 Demo。
- [`day4-submission/project1/`](day4-submission/project1/)：Apache 日志分析实现、测试、输出与图表。
- [`day4-submission/project2/`](day4-submission/project2/)：垃圾邮件过滤实现、测试、输出与图表。
- [`day4-submission/docs/agent-review-report.md`](day4-submission/docs/agent-review-report.md)：Agent 代码审查报告。

安装与测试：

```bash
cd day4-submission
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
```

使用仓库中的公开数据复现：

```bash
cd day4-submission
(cd project1 && ../.venv/bin/python main.py --archive ../../day4-data/project1/Apache.tar.gz)
(cd project2 && ../.venv/bin/python main.py --data-dir ../../day4-data/project2)
```

数据集版权与使用条件以各自上游项目为准，来源说明见 [`day4-data/README.md`](day4-data/README.md)。

## Day 5–6：LOOPS 双路线 AI 内容审核系统

Day 5 和 Day 6 共用一个连续的团队大作业，因此合并保存在 [`day5-submission-Loops Aget/`](day5-submission-Loops%20Aget/) 中。

LOOPS 讨论的是一个比“让模型输出标签”更复杂的问题：当规则、文本语义、图片证据和模型判断发生冲突时，系统如何给出可解释、可追溯、可恢复的结论，同时确保人类拥有最终控制权。

### Day 5：问题诊断与方案设计

- 识别真实用户、利益相关方、关键冲突、约束、信息缺口和非目标。
- 提出并反证多条本质不同的解决路线。
- 使用取舍矩阵记录人工决策、代价和拒绝理由。
- 确定双路线架构：传统 ML 处理稳定高吞吐场景，Agent 处理复杂和高风险内容。
- 设计从输入、结构化取证、风险路由、策略门到人工复核的端到端链路。

### Day 6：实现、验证与答辩

- 使用 FastAPI 提供内容创建、审核运行、轨迹查询和人工决定接口。
- 使用 LangGraph 编排文本、视觉、Critic、Arbiter 和人工中断/恢复。
- 使用确定性策略门限制模型权限，避免 LLM 单独触发硬拦截。
- 使用 MongoDB 保存内容、运行、Checkpoint、审计轨迹和演示快照。
- 使用 React 构建 Agent、机器学习和双方案对比控制台。
- 覆盖正常、边界、失败、安全回归和端到端场景。
- 整理 AI 协作、团队决策、个人贡献、复盘和 6 分钟答辩材料。

核心证据导航：

- [问题诊断](day5-submission-Loops%20Aget/docs/diagnosis/problem-diagnosis.md)
- [方案取舍矩阵](day5-submission-Loops%20Aget/docs/options/tradeoff-matrix.md)
- [端到端系统设计](day5-submission-Loops%20Aget/docs/design/end-to-end-system-design.md)
- [验证用例与结果](day5-submission-Loops%20Aget/docs/validation/cases-and-results.md)
- [AI 协作记录](day5-submission-Loops%20Aget/docs/ai/ai-collaboration-log.md)
- [证据映射](day5-submission-Loops%20Aget/docs/evidence-map.md)
- [答辩提纲](day5-submission-Loops%20Aget/docs/defense/defense-outline.md)

详细安装、配置、Demo 主路径、API 和限制请阅读 [LOOPS README](day5-submission-Loops%20Aget/README.md)。

> [!NOTE]
> LOOPS 的云模型能力需要自行配置 API Key。仓库只提供 `.env.example`，不会提交任何真实密钥。没有云模型密钥时，可使用明确标注的数据快照了解界面和流程，但这不等同于完成真实 Agent 取证。

## 如何阅读这个仓库

如果你刚开始学习，推荐按下面的顺序阅读：

1. 从本 README 了解六天主线。
2. 阅读每一天的 `submission/README.md`，理解目标、运行方式和限制。
3. 阅读 `docs/spec.md` 或 PRD，确认项目明确做什么、不做什么。
4. 阅读 Design、Tasks 和实现代码，观察需求如何落到模块与任务。
5. 阅读 Test Record 和实际测试，判断实现是否真的满足验收。
6. 最后阅读 AI Log、决策记录和 Reflection，理解 AI 建议如何被人工采纳、修改或拒绝。

如果你只想看可运行项目：

- 最小 Python/RAG：[`day1-submission/`](day1-submission/)
- CLI、工作流与 Agent 工具：[`day2-submission/`](day2-submission/)
- React + FastAPI 全栈：[`day3-submission/`](day3-submission/)
- 数据分析与传统机器学习：[`day4-submission/`](day4-submission/)
- LangGraph 多 Agent 与人工复核：[`day5-submission-Loops Aget/`](day5-submission-Loops%20Aget/)

## 环境与安全说明

- 仓库中的命令以 macOS/Linux 为主，Windows 用户需要调整虚拟环境激活和 Shell 命令。
- 不要提交 `.env`、API Key、访问令牌、Cookie、内部地址或个人数据。
- `.env.example` 只描述变量名和示例结构；复制后应在本地填写，并确保 `.env` 始终被 Git 忽略。
- `review-target/`、不安全 Agent 示例或故意保留的 Bug 只用于学习和测试，请先阅读相邻说明，不要直接用于生产。
- `day4-data/` 中的公开数据来自各自上游项目，使用时应遵守原始数据集许可与引用要求。
- 本仓库不包含小米内部 `slide/` 课件。若发现疑似内部材料，请停止传播并通过私下渠道联系维护者处理。

## 关于内部课件

训练营课件用于内部教学，可能包含公司内部信息、案例、流程或其他不适合公开传播的内容。因此：

- `slide/`、`slides/`、`silde/`、`课件/` 等目录均被公开仓库的忽略规则排除。
- 本仓库只公开个人或团队完成的代码、文档和可公开数据。
- 不接受补传内部课件的 Pull Request。
- 引用本仓库时，请引用公开代码和本人产出的文档，不要引用或转述未公开课程材料。

## 说明与致谢

感谢小米 AI Native 训练营的课程设计、讲师和同学们提供的学习机会与协作环境。仓库中的课堂 Demo、个人作业和团队成果已尽量通过目录和文档标注来源与贡献边界。

部分子项目有独立许可证；第三方框架、数据集和素材遵循其各自许可证。未明确标注开放许可的课程相关内容仅用于学习交流，不代表获得复制、再分发或商业使用授权。

