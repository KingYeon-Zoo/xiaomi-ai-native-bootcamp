# Day3 实际验证记录

- 执行日期：2026-07-15
- 环境：macOS，Python 3，Node.js/npm（具体版本以执行机为准）
- 规则：这里只记录本次实际执行结果；demo 历史结果不作为个人 PASS 证据。

## 自动验证

| ID | 输入/命令 | 预期 | 实际 | 结果 |
|---|---|---|---|---|
| V-01 | `backend/.venv/bin/python -m pytest backend/tests -q` | 后端全部通过 | `25 passed in 0.21s` | PASS |
| V-02 | `cd frontend && npm test -- --run` | 前端全部通过 | `5 files passed，15 tests passed` | PASS |
| V-03 | 后端启动后请求 `GET /trips` | 返回空旅行列表 | HTTP 成功，响应 `{"trips":[]}` | PASS |
| V-04 | `cd frontend && npm run build` | Vite 生产构建成功 | 33 modules transformed，built in 984ms | PASS |

## 失败与复测

| 事件 | 原因 | 修正 | 复测 |
|---|---|---|---|
| 第一次后端启动冒烟请求无法连接 | 已进入 `backend/`，命令仍写 `backend/.venv/bin/python`，路径重复 | 改用 `.venv/bin/python -m uvicorn ...` | V-03 PASS |
| 第一次 Git 推送认证失败 | Git HTTP 端点不接受 Bearer 认证方式 | 保持无凭据远端 URL，改用进程内 PAT Basic 请求头 | `main` 推送成功 |

## 未执行项

- 浏览器手动 E2E 10 步：本次未执行，因此不标 PASS；自动化测试已覆盖核心计算、接口校验和前端组件行为。
- 真实多用户并发与生产部署：属于 PRD 非目标。

## 提交审计

| 审计 | 实际结果 | 结论 |
|---|---|---|
| `bash check-submission.sh .` | PASS 62，WARNING 1，BLOCKED 0，评级 PASS | PASS；WARNING 是检查器只识别 Windows `.venv/Scripts/python.exe`，故在 macOS 跳过内置 pytest；V-01 已用 macOS 路径独立通过 |
| `audit-xiaomi-project.sh . personal` | PASS 39，WARNING 0，BLOCKED 0 | PASS |
