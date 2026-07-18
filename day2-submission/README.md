# Day2 AI Native 训练营作业

本仓库是 Day 2 独立提交包，覆盖提交检查工作流、Spec Coding 任务助手、LangChain 陌生技术 Demo、同桌评审、训练营助教 Agent 设计与 AI 代码审查。过程 Markdown 正文统一位于根 `docs/`，课程要求的旧路径保留为兼容入口；所有结论均附带可运行命令或文件证据。

## 快速开始

```bash
git clone https://github.com/KingYeon-Zoo/xiaomi-ai-native-bootcamp.git
cd xiaomi-ai-native-bootcamp/day2-submission
python3 --version
bash check-submission.sh
```

## 四部分作业

| 目录 | 任务 | 核心产物 |
|------|------|----------|
| `01-submission-workflow/` | 提交检查助手工作流 | `ai-workflow.md`、执行器、状态规则与证据模板 |
| `02-task-assistant/` | Day2 学习任务清单助手 | Spec 三件套、AGENTS、CLI、Eval、上下文包 |
| `03-learning-demo/` | LangChain 最小 Demo 与同桌评审 | Demo、学习记录、测试记录、`peer-review.md` |
| `04-training-agent/` | 训练营助教 Agent 与代码审查 | `agent-design.md`、工具、测试、`review-checklist.md` |

## 安装

核心任务只需要 Python 3.9+。LangChain Demo 使用独立虚拟环境：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r 03-learning-demo/requirements.txt
```

## 运行

```bash
python3 02-task-assistant/cli.py today
python3 02-task-assistant/cli.py submit spec.md
python3 02-task-assistant/cli.py check

.venv/bin/python 03-learning-demo/demo.py "什么是可复核交付？"
```

## 测试

```bash
python3 -m unittest discover -s 01-submission-workflow/tests -v
python3 -m unittest discover -s 02-task-assistant/tests -v
.venv/bin/python -m unittest discover -s 03-learning-demo/tests -v
python3 -m unittest discover -s 04-training-agent/tests -v
bash check-submission.sh
```

最终自动测试共 30 条：工作流 5 条、任务助手 8 条、LangChain Demo 4 条、训练营 Agent 工具 13 条。另对课堂现有 Demo 实际运行 17 条 pytest，结果记录在 `03-learning-demo/peer-review.md`。

## Mission 对照

| Mission 产物 | 文件 |
|--------------|------|
| 提交检查工作流 | `docs/01-submission-workflow/ai-workflow.md` |
| Spec Coding 五件套 | `docs/02-task-assistant/spec.md`、`plan.md`、`tasks.md`、`AGENTS.md` 与 `02-task-assistant/cli.py` |
| Eval 与失败定位 | `02-task-assistant/eval-cases.json`、`docs/02-task-assistant/test-record.md` |
| 七层上下文包 | `docs/02-task-assistant/context-pack.md` |
| 陌生技术 Demo | `docs/03-learning-demo/learning-record.md`、`03-learning-demo/demo.py`、`docs/03-learning-demo/test-record.md` |
| 同桌评审 | `docs/03-learning-demo/peer-review.md` |
| Agent 设计 | `docs/04-training-agent/agent-design.md` |
| AI 代码审查 | `docs/04-training-agent/review-checklist.md` |

## 项目结构

```text
day2-submission/
├── AGENTS.md                # Codex 发现入口
├── docs/                    # 全部过程 Markdown 唯一正文与证据索引
│   ├── engineering-constraints.md
│   ├── spec.md
│   ├── design.md
│   ├── tasks.md
│   ├── ai-log.md
│   ├── test-record.md
│   ├── reflection.md
│   └── 01-*/ 02-*/ 03-*/ 04-*/
├── 01-submission-workflow/  # 执行器、测试及课程文档兼容入口
├── 02-task-assistant/       # 任务清单 CLI、Eval、测试及兼容入口
├── 03-learning-demo/        # LangChain Demo、测试及兼容入口
├── 04-training-agent/       # Agent 工具、测试、审查夹具及兼容入口
└── check-submission.sh      # 根级一键验收
```

## 环境要求

- Python 3.9 或更高版本
- Bash 3.2 或更高版本
- LangChain Core 0.3–1.x（仅自学 Demo 使用）
- 运行测试不需要 API Key、数据库或网络

## 约束

- 任务助手为单用户本地 CLI，不提供 Web UI、登录、协作或历史版本。
- Demo 使用本地 fake model 验证 LangChain 链式组合，不代表真实模型效果。
- Agent 的 RAG 只基于仓库 FAQ 回答；无依据时固定拒答。
- `review-target/` 是有意保留的待审不安全样例，禁止运行或导入。
- Git 符号链接用于兼容课程硬编码文件路径；过程正文只维护在 `docs/`。

## 故障排查

- `ModuleNotFoundError: langchain_core`：执行安装章节中的虚拟环境和依赖命令。
- `status.json` 损坏：任务助手会重建文件，并在终端明确提示。
- 根检查显示 BLOCKED：根据输出补齐缺失文件或先修复失败测试，再重新运行。
- 无执行权限：用 `bash check-submission.sh` 运行，无需修改文件权限。
- 旧路径文件无法打开：请通过 Git clone 获取仓库，或直接阅读 `docs/` 下同名权威正文。
