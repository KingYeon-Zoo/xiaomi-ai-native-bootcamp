# 项目实现概览

## 当前主线

`MODERATION_APPROACH=llm_api` 时，FastAPI 创建 Post 后把审核任务交给 LangGraph Agent 运行时。规则工具先产生确定性证据；未命中硬规则时，文本 Agent 与视觉 Agent 按输入模态取证；风险路由决定直接进入策略门，还是调用 critic 与 arbiter。缺少必要证据或仲裁仍不确定时，Graph 通过 `interrupt()` 暂停，人工决定用相同 `run_id/thread_id` 恢复。

实际实现：

- `src/backend/app/agents/graph.py`
- `src/backend/app/agents/policy.py`
- `src/backend/app/agents/runtime.py`
- `src/backend/app/agents/ark.py`
- `src/backend/app/api/agent_moderation.py`

## 保留的机器学习路线

原始 ML 基线中的规则、文本归一化、毒性/仇恨识别、意图实体分析、EfficientNet、CLIP 和决策融合代码仍位于 `src/backend/app/ml/` 与 `src/backend/app/services/`。这些资产没有被描述为当前版本重新训练的模型；轻量启动脚本也不会自动下载全部权重。

## 双方案看板

`GET /api/metrics/control-center?hours=1|24|168` 返回同一演示口径下的 Agent、ML 和比较数据。服务优先读取 MongoDB `dashboard_snapshots`，无快照时回退到确定性内置数据；前端 API 失败时还有同结构的本地降级数据。

演示指标用于讲清架构取舍，不代表真实生产准确率、吞吐、成本或线上流量。对应实现：

- `src/backend/app/services/control_center_metrics.py`
- `src/backend/seed_demo_data.py`
- `src/frontend/src/components/ModelMetrics/ModelMetricsDashboard.jsx`
- `src/frontend/src/data/controlCenterDemo.js`

## 当前运行边界

MongoDB 同时保存 Post、Agent run、LangGraph checkpoint、旧 ML prediction metric 和看板快照。运行时队列仍是单进程实现；管理端鉴权、跨实例消费、正式标注集评测和生产 SLO 不在当前 MVP 内。
