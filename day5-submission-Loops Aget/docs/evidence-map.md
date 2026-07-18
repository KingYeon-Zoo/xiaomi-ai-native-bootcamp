# 证据映射

## 代码证据

| 编号 | 能力声明 | 可复核位置 |
|---|---|---|
| C01 | 文本与视觉分工、结构化 Evidence | `src/backend/app/agents/moderators.py`、`schemas.py` |
| C02 | 规则预检、并行取证、风险路由、条件仲裁、HITL | `src/backend/app/agents/graph.py` |
| C03 | LLM 无权覆盖硬规则，缺必要证据转人工 | `src/backend/app/agents/policy.py` |
| C04 | Responses API、重试、JSON 对象兼容回退、图片校验 | `src/backend/app/agents/ark.py` |
| C05 | 异步队列、失败记录、重启重排队、同 run 恢复 | `src/backend/app/agents/runtime.py`、`repositories.py` |
| C06 | 发帖入队、运行状态、轨迹、人工决定 API | `src/backend/app/api/posts.py`、`agent_moderation.py` |
| C07 | Agent/ML 双架构看板与确定性快照 | `src/backend/app/services/control_center_metrics.py`、`src/frontend/src/components/ModelMetrics/ModelMetricsDashboard.jsx` |
| C08 | 96/64/32/3 演示数据生成逻辑 | `src/backend/seed_demo_data.py` |
| C09 | 旧 ML 路线保留 | `src/backend/app/ml/`、`src/backend/app/services/_moderation_service_ensemble.py` |

## 测试证据

| 编号 | 覆盖 | 文件 |
|---|---|---|
| T01 | Graph 快速、硬规则、冲突/人工路径 | `src/backend/tests/agents/test_graph.py` |
| T02 | 权限提升、缺视觉证据、风险路由 | `test_policy.py` |
| T03 | 方舟配置、结构校验回退、图片 data URL、四类 Agent | `test_ark_agents.py` |
| T04 | 后台完成、异常失败、重启恢复、人审恢复 | `test_runtime.py` |
| T05 | 用户状态隐藏信息、管理员轨迹、人工接口 | `test_agent_api.py` |
| T06 | 规则工具和提示注入 | `test_rule_tool.py` |
| T07 | Agent/ML 同口径快照与 Mongo 回退 | `test_control_center_metrics.py` |

## Git 与运行证据

| 编号 | 事实 | 证据 |
|---|---|---|
| G01 | 旧 ML 基线 | `973ab58`，2026-07-17 12:59 +08:00 |
| G02 | Agent 架构提交 | `e1bc2b7`，2026-07-17 14:45 +08:00 |
| G03 | 可核验提交署名 | 两次提交作者均为 `ChinyenZoo` |
| R01 | 服务健康 | 2026-07-17 本地 `/health` 返回 healthy、Mongo connected、`llm_api` |
| R02 | 看板数据源 | `/api/metrics/control-center?hours=24` 返回 `mongodb_demo_snapshot`，Agent/ML 均为 12,847 |
| R03 | 演示集合 | 96 Posts、64 Agent runs、32 ML metrics、3 snapshots |
| R04 | 浏览器验收 | `prototype/assets/dashboard-agent-24h-current.png`、`dashboard-comparison-current.png` |

## 证据使用限制

- C07/C08/R02 中的精度、成本、吞吐和聚合数量是演示快照字段，不是实测生产 KPI。
- 自动化云模型测试使用 fake client；真实云调用是否可用取决于本地密钥和供应商状态。
- 本地 AI 工具缓存、旧 PDF 和旧测试输出不作为当前版本完成证明。
- Git 历史只能证明已存在的提交署名，不能据此推导未记录的协作者。

## 质量维度映射

| 维度 | 权重 | 主要证据 | 当前结论 |
|---|---:|---|---|
| 问题定义与诊断 | 15 | `docs/diagnosis/` | 用户、冲突、约束、非目标与成功标准齐全 |
| 关键澄清问题 | 10 | `clarifying-questions.md` | 14 个问题、3 个 P0，均说明方案影响 |
| AI 协作与人工判断 | 15 | `docs/ai/`、`review-record.md` | 六类协作齐全，至少两条拒绝/修改，人工边界明确 |
| 方案对比与取舍 | 15 | `docs/options/`、`docs/decision/` | 三条本质路线、权重矩阵、代价与放弃理由齐全 |
| 端到端系统设计 | 10 | `end-to-end-system-design.md`、C01–C09 | Web、服务端、数据、AI、人工复核与失败处理齐全 |
| MVP 与核心判断 | 10 | `src/`、`prototype/`、R01–R04 | 主路径、硬规则、冲突与人工路径可演示 |
| 测试、反例与风险 | 10 | `docs/validation/`、T01–T07 | 正常、边界、失败、回归、安全与端到端均有实际结果 |
| 协作与过程证据 | 10 | `docs/collaboration/`、Git | 四个真实同步节点与个人责任可定位；无多人协作证据 |
| 表达与演示 | 5 | `README.md`、`docs/defense/`、截图 | 六分钟脚本、追问卡和失败兜底齐全 |

## 个人责任映射

| 维度 | 权重 | 证据 | 当前结论 |
|---|---:|---|---|
| 角色责任完成 | 25 | `role-division.md`、C01–C09 | 个人维护者覆盖产品、后端、前端、验证与文档 |
| 过程证据 | 25 | G01–G03、`docs/collaboration/` | 提交、决策、问题与同步节点可定位 |
| AI 使用质量 | 20 | `docs/ai/` | 澄清、对比、反证、实现、验证、Review 均有人工作用说明 |
| 协作贡献 | 15 | `meeting-minutes.md`、`decision-log.md` | 可证明人机协作；当前没有多人协作可供声明 |
| 演示解释能力 | 15 | `defense-outline.md`、`demo_guide.md` | 关键判断、边界、失败预案与追问回答齐全 |
