# 工程约束

## 文档与目录

- 根目录保留项目入口与开源社区文件：`README.md`、`LICENSE`、`CONTRIBUTING.md`、`CODE_OF_CONDUCT.md`、`SECURITY.md`。
- `src/` 只放可运行源码、脚本和模拟数据；服务端在 `src/backend/`，Web 前端在 `src/frontend/`。
- `prototype/` 只放原型说明、截图与演示兜底证据。
- `docs/` 放诊断、方案、设计、决策、验证、AI 协作、责任记录、复盘与演示文档。
- 本地 AI 工具缓存、环境变量、构建产物、依赖目录和临时日志不进入版本库。

## 事实优先级

1. 当前可运行代码、自动化测试和实际命令输出。
2. Git 提交时间、作者和 diff。
3. 已确认的需求与项目决策。
4. 文档；与前三类冲突时必须改写。
5. 无法复核的历史说明只能作为待确认信息。

## 目标与非目标

目标是交付一个可运行、可解释、可恢复的内容审核 Agent，同时保留 ML 快速方案，并在同一控制台解释取舍。

非目标包括：当前版本重训旧模型、声明生产准确率、构建分布式任务平台、公开 API Key、保存隐藏思维链或补写无法核验的历史过程。

## 阶段门禁

1. **诊断门**：至少 10 个澄清问题、3 个 P0，并写明不同答案的方案影响。
2. **方案门**：至少三条本质不同路线，有权重、评分与被拒原因。
3. **实现门**：架构声明必须映射到文件、接口或测试。
4. **验证门**：覆盖正常、边界、失败、回归和端到端；计划与实际结果分开。
5. **发布门**：README 可复现、敏感信息不入库、文档链接有效、限制明确披露。

## 运行与验证命令

```bash
./start.sh

cd src/backend
.venv/bin/python seed_demo_data.py
.venv/bin/python -m pytest tests/agents -q

cd ../frontend
npm run lint
npm run build
```

`seed_demo_data.py` 会清空演示数据库中的四个集合，只能用于本地演示环境。

## 验收证据映射

- Agent 编排：`src/backend/app/agents/graph.py` + `src/backend/tests/agents/test_graph.py`
- 权限边界：`src/backend/app/agents/policy.py` + `test_policy.py`
- 云模型协议与图片输入：`ark.py`、`moderators.py` + `test_ark_agents.py`
- 持久化与人审恢复：`runtime.py`、`repositories.py` + `test_runtime.py`
- 双方案看板：`control_center_metrics.py`、`ModelMetricsDashboard.jsx` + `test_control_center_metrics.py`
- 运行态：`/health`、`/api/metrics/control-center`、Mongo 集合计数和浏览器截图

完整条目见 `docs/evidence-map.md`。

## AI 协作边界

- AI 可用于澄清、方案对比、反证、实现辅助、验证和 Review。
- 项目维护者负责目标、取舍、授权和最终发布。
- AI 不是项目成员；AI 输出不能冒充用户访谈、外部审查或已验证事实。
- 不回显、提交或传播本地 `.env`、访问令牌与会话缓存。

## 完成定义

- 核心路径可启动，Agent 测试、前端 lint/build 与浏览器主路径均有实际结果。
- 演示数据明确标注为确定性快照。
- README、原型、诊断、方案、设计、决策、验证、AI 协作、复盘和演示材料路径齐全。
- 所有强事实可定位；无法验证的生产指标和外部审查不做完成声明。
