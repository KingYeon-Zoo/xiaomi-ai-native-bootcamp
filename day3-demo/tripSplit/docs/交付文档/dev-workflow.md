# TripSplit · 开发计划

> 先规划后实现，每步有输入输出和验证命令。

---

## T1 后端骨架

**入**：PRD 核心对象定义 + 技术约束
**出**：main.py + storage.py + models.py + trips.json 初始化
**验**：`uvicorn main:app --reload` → GET /trips 返回 `{"trips": []}`

△ 风险：CORS 配置遗漏 → 前端跨域失败 → 已在 main.py 配置 allow_origins

---

## T2 后端 API + 测试

**入**：T1 骨架 + PRD 需求（P0 六条 + P1 四条）+ 失败路径
**出**：routes/trips.py（9 个端点）+ tests/（4 个测试文件，25 条用例）
**验**：`pytest tests/ -v` → 25 passed

### 端点清单

| 方法 | 路径 | 校验 |
|------|------|------|
| POST | /trips | name 非空，startDate ≤ endDate |
| GET | /trips | 列表返回 memberCount / expenseCount |
| GET | /trips/{id} | 不存在返回 404 |
| DELETE | /trips/{id} | 不存在返回 404 |
| POST | /trips/{id}/members | name 非空、不重复 |
| POST | /trips/{id}/expenses | amount > 0，payer/participants 校验 |
| PUT | /trips/{id}/expenses/{eid} | 未传字段保留原值，清除 settlement |
| DELETE | /trips/{id}/expenses/{eid} | 清除 settlement |
| POST | /trips/{id}/settle | expenses 非空 |

---

## T3 后端结算

**入**：T2 API + PRD 结算规则（贪心算法、均摊不处理尾差）
**出**：services/settle.py + /settle 端点 + test_settle.py（5 条用例）
**验**：`pytest tests/test_settle.py -v` → 5 passed

### 算法要点

1. 遍历账单，累计每人余额
2. 余额 round(v, 2) 消除浮点残留
3. 贪心匹配：最大应收 × 最大应付，取较小值
4. 验证：总转账金额 = 总支出，余额归零

△ 风险：浮点精度 → round 处理，已验证 100.01/3 场景通过

---

## T4 前端骨架

**入**：PRD 技术约束 + plan.md 依赖清单
**出**：Vite + React + 路由 + fetch 封装 + vitest 配置
**验**：`npm run dev` → 两个路由可切换；`npm test -- --run` → vitest 可运行

△ 风险：Vite proxy 配置错误 → API 请求 404 → 已在 vite.config.js 配置 /trips 代理

---

## T5 前端页面 + 组件 + 联调 + 测试

**入**：T4 骨架 + T2/T3 API + PRD 交互路径 + plan.md 布局
**出**：2 个页面 + 7 个组件 + 5 个测试文件（15 条用例）+ Plain CSS 样式
**验**：`npm test -- --run` → 15 passed；手动走通完整流程

### 实现顺序

| 步 | 内容 | 同步测试 |
|----|------|----------|
| 5a | TripList + TripForm | TripForm.test.jsx |
| 5b | 成员区（MemberForm + MemberStats） | MemberForm.test.jsx |
| 5c | 账单区（ExpenseForm + ExpenseList） | ExpenseForm.test.jsx + ExpenseList.test.jsx |
| 5d | 结算区（Settlement） | Settlement.test.jsx |
| 5e | 样式完善 | — |

---

## 断点记录

| 断点 | 状态 |
|------|------|
| 成员不可删除，前端交互是否阻断 | ✅ 已对齐，MemberForm 无删除入口 |
| 均摊不处理尾差，多场景金额对得上 | ✅ 已验证（test_settle 5 条全过） |
| JSON 文件并发写入风险 | ⚠️ 已知限制，单机场景可接受 |
