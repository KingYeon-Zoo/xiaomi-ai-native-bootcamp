# 设计证据路由

本文件只提供标准入口，不复制设计正文：

- 方案比较、最终选型、失败路径与存储/算法取舍：[`docs/交付文档/design-options.md`](交付文档/design-options.md)
- 数据模型、API、页面布局与实现细节：[`docs/plan.md`](plan.md)
- 小步开发的输入、输出与验证：[`docs/交付文档/dev-workflow.md`](交付文档/dev-workflow.md)

## 端到端数据流

`React 表单 → fetch → FastAPI 路由 → 业务校验/结算服务 → JSON 存储 → API 响应 → React 展示`

## 模块与接口索引

- 前端模块：`frontend/src/pages/`、`frontend/src/components/`、`frontend/src/api/trips.js`
- 后端模块：`backend/routes/trips.py`、`backend/services/storage.py`、`backend/services/settle.py`
- HTTP 接口：旅行、成员、账单与结算的 9 个端点，完整定义见 `docs/plan.md` 和 README 的 API 表。

核心风险是 JSON 并发写入与浏览器手动 E2E 尚未在本次执行；详见 [`docs/reflection.md`](reflection.md) 和 [`docs/test-record.md`](test-record.md)。
