# 范围与验收路由

本项目的范围、用户、目标、非目标、核心对象、需求优先级、验收条件和失败路径，以 [`docs/交付文档/product-prd.md`](交付文档/product-prd.md) 为唯一正文。

## 最小验收索引

| 范围 | 验收条目 | 实现与测试证据 |
|---|---|---|
| 旅行 CRUD | P0-1、P1-1、P1-4 | `backend/routes/trips.py`、`backend/tests/test_trips.py` |
| 成员管理 | P0-2 | `backend/tests/test_members.py`、前端 MemberForm 测试 |
| 账单管理 | P0-3、P0-4、P1-2、P1-3 | `backend/tests/test_expenses.py`、前端 Expense 测试 |
| 结算 | P0-5、P0-6 | `backend/services/settle.py`、`backend/tests/test_settle.py` |

实际执行结果统一记录在 [`docs/test-record.md`](test-record.md)。
