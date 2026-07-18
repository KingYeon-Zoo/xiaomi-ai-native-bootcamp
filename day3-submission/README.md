# TripSplit · 旅行 AA 结算助手

多人旅行共同支出结算工具。录入账单，一键算清谁该转给谁多少钱。

> 本 Day3 提交以老师提供的正确 demo 为业务实现基线，个人工作聚焦于按课程题纲整理八份交付文档、补齐训练营工程约束、重新执行测试并建立可复核证据链。来源和个人贡献边界见 `docs/engineering-constraints.md`。

## 功能

- 创建旅行账本，添加同行成员
- 记录共同支出（名称、金额、付款人、参与人、分类）
- 自动计算每人已付 / 应付 / 余额
- 生成最简转账方案（贪心算法，转账次数尽量少）
- 账单支持编辑 / 删除，结算一键重新生成

## 环境要求

| 工具 | 最低版本 | 用途 |
|------|----------|------|
| Node.js | ≥ 18 | 前端运行（自带 npm） |
| Python | ≥ 3.10 | 后端运行（自带 pip、venv） |

## 快速启动

### 后端

```bash
cd backend

# 创建虚拟环境并安装依赖（macOS / Linux）
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

# 启动服务（默认 http://localhost:8000）
.venv/bin/python -m uvicorn main:app --reload
```

### 前端

```bash
cd frontend

# 按锁文件安装依赖
npm ci

# 启动开发服务器（默认 http://localhost:5173）
npm run dev
```

启动后浏览器访问 http://localhost:5173 即可使用。

## 运行测试

### 后端 pytest

```bash
cd backend
.venv/bin/python -m pytest tests/ -q
```

### 前端 vitest

```bash
cd frontend
npm test -- --run
```

### 完整性审计

```bash
# 在项目根目录执行
bash check-submission.sh .
bash ../.agents/skills/xiaomi-ai-bootcamp/scripts/audit-xiaomi-project.sh . personal
```

## 项目结构

```
tripSplit/
├── README.md
├── docs/
│   ├── product-prd.md         # 需求文档
│   ├── plan.md                # 实现计划
│   ├── tasks.md               # 任务清单
│   ├── tests.md               # 测试用例
│   └── ai-log.md              # AI 协作决策日志
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── api/trips.js       # API 调用（fetch）
│       ├── pages/             # 页面组件
│       ├── components/        # 业务组件 + 测试
│       └── test/setup.js      # vitest 配置
├── backend/
│   ├── requirements.txt
│   ├── main.py                # FastAPI 入口
│   ├── models.py              # Pydantic 数据模型
│   ├── routes/trips.py        # API 端点
│   ├── services/
│   │   ├── storage.py         # JSON 文件读写
│   │   └── settle.py          # 结算算法
│   ├── tests/                 # pytest 测试
│   └── data/trips.json        # 持久化数据
└── .gitignore
```

## 技术栈

| 层 | 选型 |
|----|------|
| 前端 | React + Vite + Plain CSS |
| 后端 | Python FastAPI |
| API 调用 | 原生 fetch |
| 测试 | 后端 pytest / 前端 vitest |
| 存储 | 本地 JSON 文件 |

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /trips | 旅行列表 |
| POST | /trips | 创建旅行 |
| GET | /trips/{id} | 旅行详情 |
| DELETE | /trips/{id} | 删除旅行 |
| POST | /trips/{id}/members | 添加成员 |
| POST | /trips/{id}/expenses | 添加账单 |
| PUT | /trips/{id}/expenses/{eid} | 编辑账单 |
| DELETE | /trips/{id}/expenses/{eid} | 删除账单 |
| POST | /trips/{id}/settle | 生成结算 |

Swagger 文档：http://localhost:8000/docs
