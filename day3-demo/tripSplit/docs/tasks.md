# TripSplit 任务清单

> 每个任务独立可验证。执行前阅读 `docs/product-prd.md` 和 `docs/plan.md`。
> 每完成一个任务，提交一次代码。
> **阻塞原则：遇到重大问题无法在 3 轮内解决，立刻停下，向用户寻求帮助。不要死循环。**

---

## T1：后端骨架

**目的**：搭建后端最小可运行结构，启动服务即可访问 API。

**输入**：`docs/plan.md` 中的项目结构、数据模型、环境与配置

**要做的事**：
1. 创建 `backend/` 目录结构（main.py、models.py、routes/、services/、data/、tests/）
2. `requirements.txt`：fastapi、uvicorn[standard]、pydantic、pytest、httpx
3. `models.py`：Pydantic 模型（TripCreate、MemberAdd、ExpenseCreate、ExpenseUpdate）
4. `services/storage.py`：JSON 文件读写（读取 trips.json，不存在则自动创建空结构 `{"trips": []}`）
5. `main.py`：FastAPI 入口 + CORS 配置（允许 localhost:5173）+ 挂载路由
6. `routes/trips.py`：先实现 GET /trips 返回空列表
7. `data/trips.json`：初始文件 `{"trips": []}`

**验证**：
```bash
cd backend
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
# 访问 http://localhost:8000/trips 应返回 {"trips": []}
# 访问 http://localhost:8000/docs 应看到 Swagger UI
```

**提交信息**：`feat(backend): 初始化后端骨架`

---

## T2：后端 API + 测试

**目的**：实现所有 CRUD 接口 + 业务校验 + pytest 验证。

**输入**：T1 的代码、`docs/plan.md` 中的 API 端点表和校验规则、`docs/tests.md` 中的 test_trips/members/expenses 用例

**要做的事**：

### API 实现
- POST /trips — 创建旅行（name 非空，startDate ≤ endDate，自动生成 uuid）
- GET /trips — 列表（返回 id/name/startDate/endDate/members.count/expenses.count）
- GET /trips/{id} — 详情（返回完整数据含 expenses、settlement）
- DELETE /trips/{id} — 删除旅行（不存在返回 404）
- POST /trips/{id}/members — 添加成员（name 非空、不重复，返回更新后的 members）
- POST /trips/{id}/expenses — 添加账单（amount > 0，payer 在 members 中，participants 非空且都在 members 中）
- PUT /trips/{id}/expenses/{eid} — 编辑账单（未传字段保留原值，同时清除 settlement）
- DELETE /trips/{id}/expenses/{eid} — 删除账单（同时清除 settlement）

### 测试实现
1. `tests/conftest.py`：pytest fixture（创建测试客户端、初始化临时 trips.json）
2. `tests/test_trips.py`：创建旅行（正常/名称为空/日期倒置）、获取列表、获取详情（正常/不存在）、删除旅行（正常/不存在）
3. `tests/test_members.py`：添加成员（正常/空名/重复名）
4. `tests/test_expenses.py`：添加账单（正常/金额≤0/payer不在members/participants为空）、编辑账单（部分字段更新）、删除账单、编辑/删除后settlement清除

**验证**：
```bash
cd backend
.venv\Scripts\activate
pytest tests/ -v
# 全部通过
```

**提交信息**：`feat(backend): 实现 CRUD API + pytest 测试`

---

## T3：后端结算

**目的**：实现结算算法 + /settle 端点 + 测试。

**输入**：T2 的代码、`docs/plan.md` 中的结算算法和 settlement 数据结构、`docs/tests.md` 中的 test_settle 用例

**要做的事**：

### 结算算法
1. 创建 `services/settle.py`
2. 实现 `settle(expenses, members)` 函数
3. 贪心匹配，余额 round(v, 2)，详细逻辑见 plan.md

### API 端点
- POST /trips/{id}/settle — 调用 settle()，结果写入 trip.settlement 并持久化
- 校验：expenses 为空时返回 400

### 测试
1. `tests/test_settle.py`：3人均摊、2人场景、浮点精度（100.01/3）、总额对账、余额归零

**验证**：
```bash
cd backend
.venv\Scripts\activate
pytest tests/ -v
# 全部通过（含 T2 的测试）
```

**提交信息**：`feat(backend): 实现结算算法 + /settle 端点 + 测试`

---

## T4：前端骨架

**目的**：搭建前端最小可运行结构，两个路由可切换，vitest 可运行。

**输入**：`docs/plan.md` 中的项目结构、环境与配置、依赖清单

**要做的事**：
1. `npm create vite@latest frontend -- --template react` 初始化项目
2. `package.json` 添加依赖：react-router-dom
3. 开发依赖：vitest、@testing-library/react、@testing-library/jest-dom、jsdom
4. `vite.config.js`：配置 proxy 代理 /api → localhost:8000 + vitest test 配置
5. `src/App.jsx`：路由配置（/ → TripList，/trips/:id → TripDetail）
6. `src/main.jsx`：入口，挂载 App
7. `src/pages/TripList.jsx`：占位，显示"旅行列表"
8. `src/pages/TripDetail.jsx`：占位，显示"旅行详情"
9. `src/api/trips.js`：封装 fetch 调用的基础函数（getTrips、getTrip、createTrip、deleteTrip、addMember、addExpense、updateExpense、deleteExpense、settleTrip）
10. 基础 CSS reset（body margin/padding 清零、字体设置）

**验证**：
```bash
cd frontend
npm install
npm run dev
# 浏览器打开 http://localhost:5173，两个路由可切换
npm test -- --run
# vitest 可运行（即使 0 个测试也不报错）
```

**提交信息**：`feat(frontend): 初始化前端骨架 + 路由 + vitest 配置`

---

## T5：前端页面 + 组件 + 联调 + 测试

**目的**：实现完整 UI、对接后端 API、vitest 覆盖关键组件，手动走通主流程。

**输入**：T4 的代码、T2/T3 的 API、`docs/plan.md` 中的页面布局和组件交互、`docs/tests.md` 中的前端测试用例

**要做的事**（按顺序）：

### 5a：TripList 页面
- 调用 GET /trips 展示卡片列表（名称/日期/成员数/账单数）
- 顶部「新建旅行」按钮 → 弹出 TripForm
- TripForm：名称输入 + 日期选择 → 调用 POST /trips
- 空状态引导
- 点击卡片 → 跳转 /trips/:id
- **同步写 TripForm.test.jsx**：创建成功、名称为空拒绝

### 5b：TripDetail 页面 — 成员区（左侧）
- 调用 GET /trips/{id} 获取数据
- 成员列表展示
- MemberForm：输入名字 → 调用 POST /members
- MemberStats：前端从 expenses 实时计算每人已付/应付/余额
- **同步写 MemberForm.test.jsx**：添加成功、空名拒绝、重复名拒绝

### 5c：TripDetail 页面 — 账单区（右侧）
- ExpenseList：展示所有账单，按时间倒序
- ExpenseForm（添加模式）：名称/金额/付款人(下拉)/参与人(checkbox)/分类(下拉)/日期(默认当天)/备注
- ExpenseForm（编辑模式）：预填数据，保存调用 PUT
- 删除账单：调用 DELETE
- **同步写 ExpenseForm.test.jsx**：添加成功、金额≤0拒绝、参与人为空拒绝
- **同步写 ExpenseList.test.jsx**：列表渲染、编辑/删除回调触发

### 5d：结算区（底部）
- 「生成结算」按钮 → 调用 POST /settle
- Settlement 组件：展示总支出、成员统计表、转账方案
- 余额正数标绿、负数标红
- 账单变更后 settlement 自动清除（后端已处理）
- **同步写 Settlement.test.jsx**：结果渲染、余额颜色

### 5e：样式完善
- 每个组件对应一个 .css 文件
- 简洁工具风，中文界面
- 左右分栏布局

**验证**：
```bash
# 测试
cd frontend && npm test -- --run
# 全部通过

# 手动 e2e
# 启动后端 + 前端，走一遍完整流程：
# 1. 创建旅行"南京 3 日游"
# 2. 添加成员：小王、小李、小张
# 3. 添加账单：酒店 900（小王付，3人均摊）
# 4. 添加账单：晚饭 360（小李付，3人均摊）
# 5. 添加账单：打车 80（小张付，小王/小张参与）
# 6. 查看成员统计
# 7. 点击生成结算
# 8. 验证：小张→小王 380，小李→小王 60
# 9. 编辑一笔账单，验证 settlement 清除
# 10. 删除一笔账单，验证列表更新
```

**提交信息**：`feat(frontend): 实现完整 UI + 联调 + vitest 测试`
