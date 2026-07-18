# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目定位

LOOPS 是一个双路线 AI 内容审核系统：传统 ML 流水线负责高吞吐低风险内容，LangGraph 有状态 Agent 负责复杂图文、冲突与高风险内容。核心不是“打标签”，而是在规则/文本/视觉/模型判断互相冲突时给出**可追溯**结论、**限制 LLM 权限**、并在证据不足时安全**转人工复核**。

## 常用命令

一键启动全栈（MongoDB via Docker → FastAPI → Vite），Ctrl+C 停止：

```bash
cp src/backend/.env.example src/backend/.env   # 首次，填入 ARK_API_KEY
./start.sh
```

后端（在 `src/backend/` 下，虚拟环境为 `.venv/`）：

```bash
.venv/bin/python -m pytest tests/agents -q          # Agent 核心测试套件
.venv/bin/python -m pytest tests/agents/test_graph.py -q   # 单个测试文件
.venv/bin/python -m pytest tests/agents/test_policy.py::<test_name>   # 单个测试用例
.venv/bin/python seed_demo_data.py                  # 生成演示数据（会清空演示库四个集合，勿对生产执行）
```

前端（在 `src/frontend/` 下）：

```bash
npm run lint        # ESLint
npm run build       # Vite 生产构建
npm run dev         # 开发服务器（start.sh 会自动带 VITE_API_TARGET 代理 /api）
```

注意：后端首选端口 8008，被占用时 `start.sh` 会自动向上探测空闲端口，Vite 代理随之调整。Mongo 容器 `loops-mongo` 在退出后保留以持久化数据。

## 运行模式（关键分叉）

`MODERATION_APPROACH` 环境变量决定加载哪条审核路径，这是理解代码的第一入口：

- `llm_api`（默认，`.env.example` 设定）：**LangGraph Agent 运行时是唯一审核路径**。`app/services/moderation_service.py` 只是一个按环境变量转发的 shim；在 `llm_api` 模式下 `posts.py` 里的 `moderation_service` 为 `None`，帖子创建走 `app/agents/container.get_agent_runtime()`。
- `ensemble`：本地多模型 ML（~2.2GB torch/transformers/clip），走 `_moderation_service_ensemble.py`。
- `ollama`：本地 Llama，走 `_moderation_service_ollama.py`。

`requirements-llm.txt` 是 `llm_api` 模式的轻量依赖（无 torch）；`requirements.txt` 是全量 ML 依赖。`start.sh` 只装前者。

## Agent 架构（llm_api 路径）

审核请求的生命周期串联三层，改动时需整体理解：

1. **入口** `app/api/posts.py` → 保存内容/图片 → `runtime.enqueue()`。
2. **运行时** `app/agents/runtime.py`（`ModerationRuntime`）：单进程异步队列 + MongoDB 持久化。`enqueue` 创建 run 并入队；`_process` 调用 LangGraph；人工决定通过 `resume()` 用同一 `run_id`（即 `thread_id`）恢复。启动时 `list_recoverable()` 把中断的 run 重新入队。
3. **编排图** `app/agents/graph.py`（`build_moderation_graph`）：

```
START → precheck(规则取证)
      → [命中可信硬规则] → policy_gate
      → [继续]           → dispatch → text_agent ∥ vision_agent → risk_route
                            → [一致且低风险] → policy_gate
                            → [冲突/低置信/高风险/模型不可用] → critic_agent → arbitrator → policy_gate
      policy_gate → [证据充分] → END
                  → [证据不足] → human_review(interrupt) → finalize_human → END
```

### 权限隔离的核心不变量

这是本项目的设计灵魂，改动 `policy.py` / `graph.py` 时**绝不能破坏**：

- LLM 输出 `HARD_BLOCK_*` **不足以**触发硬拦截。`ModerationPolicy` 只承认 `TRUSTED_HARD_POLICY_SOURCES = {"rule", "attack_tool"}` 来源的硬拦截码（见 `policy.py:53`、`graph.py` 的 `route_precheck`/`policy_gate`）。
- `policy_gate` 是确定性最终裁决者，LLM 建议无法绕过它。缺失必要证据、Agent 不可用、仲裁要求人审、无仲裁下建议冲突 —— 一律转 `WAITING_HUMAN`。
- 任何 Agent 抛异常都被 `_unavailable()` 包成 `HUMAN_REVIEW` 证据，**失败保守降级**而非放行。
- `RiskRouter`（`policy.py:14`）决定是否触发 critic/arbiter 辩论路径：建议冲突、置信度 < 0.75、Agent 不可用、或证据 severity ≥ 0.6。

### 数据契约

所有节点统一输出 `AgentAssessment` / `Evidence`（`app/agents/schemas.py`）。枚举值：`ModerationStatus`（queued/running/waiting_human/completed/failed）、`ModerationVerdict`（allow/block/human_review）。LangGraph state 里 `assessments` 和 `trace` 用 `operator.add` 累加。

### 云模型与依赖注入

`app/agents/container.py` 是唯一的组装点（全局单例 runtime）：把火山方舟 Responses API 客户端（`ark.py`）、四个 moderator（`moderators.py`）、`RuleEvidenceTool`(`tools.py` 包 `services/rule_engine.py`)、`RiskRouter`、`ModerationPolicy` 和 `MongoDBSaver` checkpointer 注入图。模型名由 `.env` 的 `AGENT_*_MODEL` 指定。没有 `ARK_API_KEY` 时 Agent 取证不可用，策略会保守转人审。

## 指标看板与降级协议

`app/services/control_center_metrics.py` 为 Agent/ML/双方案对比三视图提供**确定性演示快照**（非生产跑分）。三级数据源同一协议，外部不可用时仍能诚实演示：`mongodb_demo_snapshot`（Mongo 有数据）→ `deterministic_demo_snapshot`（后端内置）→ 前端 `src/data/controlCenterDemo.js` 本地副本。前端见到 `source` 字段应据此标注数据来源，不得伪装成实时生产数据。

## API 摘要

| 方法 | 路径 | 用途 |
|---|---|---|
| `POST` | `/api/posts/` | 创建内容并启动审核 |
| `GET` | `/api/moderation/runs/{run_id}` | 用户安全视图（排除 text/trace） |
| `GET` | `/api/moderation/runs/{run_id}/trace` | 管理侧结构化轨迹 |
| `POST` | `/api/moderation/runs/{run_id}/human-decision` | 提交人工决定并恢复运行 |
| `GET` | `/api/metrics/control-center` | Agent/ML 控制台数据 |
| `GET` | `/health` | 服务与当前 `moderation_approach` |

## 前端结构

React 19 + Vite + Tailwind v4 + framer-motion + recharts + i18next。`src/services/*` 封装 axios 调用（`api.js` 自动附带 JWT、处理 401）；`src/hooks/*`（useModeration/usePosts/useAuth）承载状态逻辑；`src/pages/*` 是四个主页面（Feed/Analytics/HumanModeration/MetricsDashboard）；`src/components/ModelMetrics/*` 是看板可视化组件群。

## 约定与边界

- 文档不是装饰：关键判断沿“问题 → 澄清 → 方案 → 决策 → 实现 → 测试 → Review”追溯，证据索引见 [docs/evidence-map.md](docs/evidence-map.md)，工程约束见 [docs/engineering-constraints.md](docs/engineering-constraints.md)。
- 事实优先级：可运行代码与测试输出 > git diff > 已确认决策 > 文档。文档与代码冲突时改文档。
- 密钥只进本地 `.env`，绝不入库。开发用 Mongo 无鉴权，仅绑定 `127.0.0.1`。
- 已知限制：ML 与 Agent 未接通统一在线分流入口；任务队列是单进程实现（无跨实例租约/幂等）；trace 与人审接口未接 RBAC；无正式标注集/漂移监控，不能声明生产准确率。
