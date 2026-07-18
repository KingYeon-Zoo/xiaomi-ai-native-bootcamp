# TripSplit 实现计划

> 本文件关注实施细节，需求层面见 `product-prd.md`

---

## 环境与配置

| 项 | 值 |
|----|-----|
| 前端 | React + Vite，npm 管理依赖 |
| 后端 | Python FastAPI，.venv + requirements.txt |
| 样式 | Plain CSS（零配置，每个组件对应一个 .css 文件） |
| API 调用 | 原生 fetch（不装 axios） |
| 测试 | 后端 pytest / 前端 vitest |
| 存储 | `backend/data/trips.json` |
| 前端端口 | 5173 |
| 后端端口 | 8000 |
| CORS | 允许跨域 |
| 界面语言 | 中文 |
| 货币 | 人民币 ¥ |

### 环境要求
- Node.js ≥ 18（自带 npm）
- Python ≥ 3.10（自带 pip、venv）
- `.venv/` 和 `node_modules/` 不提交 git

### 依赖清单

**前端 package.json**
```
react
react-dom
react-router-dom
```
开发依赖：
```
vite
@vitejs/plugin-react
vitest
@testing-library/react
@testing-library/jest-dom
jsdom
```

**后端 requirements.txt**
```
fastapi
uvicorn[standard]
pydantic
pytest
httpx
```

---

## 项目结构

```
tripSplit/
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx               # 路由：列表 / 详情
│       ├── api/
│       │   └── trips.js          # 封装后端 API 调用
│       ├── pages/
│       │   ├── TripList.jsx      # 旅行列表页
│       │   └── TripDetail.jsx    # 旅行详情页
│       └── components/
│           ├── TripForm.jsx      # 创建旅行表单
│           ├── MemberForm.jsx    # 添加成员表单
│           ├── ExpenseForm.jsx   # 添加/编辑账单表单
│           ├── ExpenseList.jsx   # 账单列表
│           ├── MemberStats.jsx   # 成员统计概览
│           ├── Settlement.jsx    # 结算结果展示
│           └── EmptyState.jsx    # 空状态引导
├── backend/
│   ├── requirements.txt
│   ├── main.py                   # FastAPI 入口 + CORS
│   ├── models.py                 # Pydantic 数据模型
│   ├── routes/
│   │   └── trips.py              # API 端点
│   ├── services/
│   │   ├── storage.py            # JSON 文件读写
│   │   └── settle.py             # 结算算法
│   └── data/
│       └── trips.json
└── docs/
    ├── product-prd.md
    ├── plan.md
    └── ai-log.md
```

---

## 数据模型

### trips.json

```json
{
  "trips": [
    {
      "id": "uuid",
      "name": "南京 3 日游",
      "startDate": "2026-07-01",
      "endDate": "2026-07-03",
      "members": ["小王", "小李", "小张"],
      "expenses": [
        {
          "id": "uuid",
          "name": "酒店",
          "amount": 900.00,
          "payer": "小王",
          "participants": ["小王", "小李", "小张"],
          "category": "住宿",
          "date": "2026-07-01",
          "note": ""
        }
      ],
      "settlement": null
    }
  ]
}
```

### settlement 字段（点击结算后写入）

```json
{
  "settlement": {
    "totalAmount": 1340.00,
    "members": [
      { "name": "小王", "paid": 900, "shouldPay": 460, "balance": 440 },
      { "name": "小李", "paid": 360, "shouldPay": 420, "balance": -60 },
      { "name": "小张", "paid": 80, "shouldPay": 460, "balance": -380 }
    ],
    "transfers": [
      { "from": "小张", "to": "小王", "amount": 380 },
      { "from": "小李", "to": "小王", "amount": 60 }
    ],
    "settledAt": "2026-06-24T10:30:00"
  }
}
```

### Pydantic 模型

```
TripCreate:    name, startDate, endDate
MemberAdd:     name (str)
ExpenseCreate: name, amount(>0), payer, participants(≥1), category, date, note?
ExpenseUpdate: 同 ExpenseCreate，全字段 Optional，未传字段保留原值
Settlement:    totalAmount, members[], transfers[]
```

---

## API 端点

| 方法 | 路径 | 请求体 | 响应 | 校验 |
|------|------|--------|------|------|
| GET | /trips | — | 列表（id/name/dates/members.count/expenses.count） | — |
| POST | /trips | TripCreate | 创建的 trip | name 非空，startDate ≤ endDate |
| GET | /trips/{id} | — | 完整数据（含 expenses、settlement） | id 存在 |
| DELETE | /trips/{id} | — | 204 | id 存在 |
| POST | /trips/{id}/members | MemberAdd | 更新后的 members | name 非空、不重复 |
| POST | /trips/{id}/expenses | ExpenseCreate | 创建的 expense | amount > 0，payer 在 members 中，participants 非空且都在 members 中 |
| PUT | /trips/{id}/expenses/{eid} | ExpenseUpdate | 更新的 expense | 同上，未传字段保留原值；同时清除 settlement |
| DELETE | /trips/{id}/expenses/{eid} | — | 204 | eid 存在；同时清除 settlement |
| POST | /trips/{id}/settle | — | Settlement | expenses 非空 |

---

## 结算算法

```python
def settle(expenses: list, members: list) -> dict:
    # 1. 初始化每人余额为 0
    balance = {m: 0.0 for m in members}

    # 2. 遍历账单，均摊
    for exp in expenses:
        share = exp.amount / len(exp.participants)
        balance[exp.payer] += exp.amount
        for p in exp.participants:
            balance[p] -= share

    # 3. 四舍五入到两位小数
    balance = {k: round(v, 2) for k, v in balance.items()}

    # 4. 贪心匹配
    transfers = []
    debtors = [(name, -amt) for name, amt in balance.items() if amt < 0]
    creditors = [(name, amt) for name, amt in balance.items() if amt > 0]
    debtors.sort(key=lambda x: x[1], reverse=True)
    creditors.sort(key=lambda x: x[1], reverse=True)

    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        d_name, d_amt = debtors[i]
        c_name, c_amt = creditors[j]
        transfer = min(d_amt, c_amt)
        transfers.append({"from": d_name, "to": c_name, "amount": round(transfer, 2)})
        debtors[i] = (d_name, round(d_amt - transfer, 2))
        creditors[j] = (c_name, round(c_amt - transfer, 2))
        if debtors[i][1] == 0: i += 1
        if creditors[j][1] == 0: j += 1

    # 5. 返回结果
    return {
        "totalAmount": sum(e.amount for e in expenses),
        "members": [...],
        "transfers": transfers,
        "settledAt": datetime.now().isoformat()
    }
```

---

## 前端页面

### 路由

```
App.jsx
├── /           → TripList.jsx
└── /trips/:id  → TripDetail.jsx
```

### TripList（旅行列表）

- 顶部「新建旅行」按钮 → 弹出 TripForm
- 卡片列表：名称 / 日期 / 成员数 / 账单数，按创建时间倒序
- 点击卡片 → 跳转详情
- 空状态：引导文案 + 创建按钮

### TripDetail（旅行详情）

左右分栏 + 底部结算：

```
┌────────────────────────────────────────────┐
│  ← 返回    南京 3 日游        7.1-7.3      │
├──────────────┬─────────────────────────────┤
│  👤 成员      │  📋 账单          [+ 添加]  │
│              │                             │
│  ┌────────┐  │  酒店  ¥900  小王付  住宿    │
│  │ 小王    │  │  晚饭  ¥360  小李付  餐饮    │
│  │ 小李    │  │  打车  ¥80   小张付  交通    │
│  │ 小张    │  │                             │
│  └────────┘  │                             │
│  [+ 添加成员] │                             │
│              │                             │
│  ─ 统计 ─    │                             │
│  小王 +440   │                             │
│  小李 -60    │                             │
│  小张 -380   │                             │
├──────────────┴─────────────────────────────┤
│  [💰 生成结算]                              │
│  结算结果展示区（转账方案）                   │
└────────────────────────────────────────────┘

成员统计：前端从 expenses 实时计算，不请求后端
```

### 组件交互

**ExpenseForm（添加/编辑账单）**
- 名称：文本输入
- 金额：数字输入，> 0
- 付款人：下拉单选（从 members 中选）
- 参与人：checkbox 多选（从 members 中选）
- 分类：下拉选择（住宿/餐饮/交通/门票/购物/其他）
- 日期：日期选择器，默认当天
- 备注：文本输入，选填
- 编辑模式：未传字段保留原值

**Settlement（结算结果展示）**
- 总支出金额
- 成员统计表：姓名 / 已付 / 应付 / 余额
- 转账方案：A → B：XX 元
- 余额正数标绿（应收），负数标红（应付）
- 无复制、无导出，纯前端展示

**分类预设**

```javascript
const CATEGORIES = ["住宿", "餐饮", "交通", "门票", "购物", "其他"]
```

选"其他"时出现文本输入框，自定义内容仅当前账单使用。

---

## 测试计划

### 后端 pytest

| 测试文件 | 覆盖 |
|----------|------|
| test_trips.py | 创建/获取/删除旅行 |
| test_members.py | 添加成员：正常、空名、重复名 |
| test_expenses.py | 添加/编辑/删除账单：正常、金额≤0、payer不在members、participants为空 |
| test_settle.py | 结算算法：3人均摊、2人、边界金额、浮点精度 |
| test_storage.py | JSON 读写、文件不存在时自动创建 |

### 前端 vitest

| 测试文件 | 覆盖 |
|----------|------|
| TripForm.test.jsx | 创建旅行：正常、名称为空拒绝 |
| MemberForm.test.jsx | 添加成员：正常、空名拒绝、重复名拒绝 |
| ExpenseForm.test.jsx | 添加账单：正常、金额≤0 拒绝、参与人为空拒绝 |
| ExpenseList.test.jsx | 账单列表渲染、编辑/删除触发回调 |
| Settlement.test.jsx | 结算结果渲染、余额颜色（正绿负红） |

---

## 实现顺序

1. 后端骨架：main.py + storage.py + trips.json 初始化
2. 后端 API：Trip CRUD + Member + Expense CRUD
3. 后端结算：settle.py + /settle 端点
4. 后端测试：pytest 全覆盖
5. 前端骨架：Vite + React + 路由
6. 前端页面：TripList + TripDetail
7. 前端组件：表单 + 列表 + 结算展示
8. 前端联调：对接 API
9. 端到端验证：手动走一遍主流程
