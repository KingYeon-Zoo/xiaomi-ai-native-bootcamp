# TripSplit Day3 提交工程约束

## 1. 项目身份

- 项目名称：TripSplit · 旅行 AA 结算助手
- 项目类型：个人课程练习
- 业务角色：旅行记账人与结算发起人
- 时间限制：Day3 当日提交
- 核心目标：基于老师提供的正确 demo，形成可复核的 Day3 八份交付文档与运行证据
- 当前阶段：提交审计

## 2. 文档目录规范与来源边界

- 所有过程 Markdown 写入 `docs/`；根目录仅保留 `README.md` 与 `AGENTS.md`。
- 老师原始材料 `../day3-demo/` 是只读输入，不修改。
- 本目录复用 demo 的正确业务实现；个人贡献是按训练营 skill 补齐工程约束、重新验证、修正文档证据状态并完成提交审计。
- 不把老师实现或历史测试记录表述为个人原创。

## 3. 权威资料优先级

1. `../day3-demo/任务.txt`
2. `../day3-demo/tripSplit/` 中的老师 demo 与专用检查器
3. `docs/交付文档/product-prd.md`
4. `docs/交付文档/design-options.md` 与 `docs/plan.md`
5. 当前代码、本次测试与审计输出

发生冲突时优先服从任务原文和本次实际执行结果，并在 `docs/ai-log.md` 记录人工判断。

## 4. 目标与非目标

### 目标

- 8 份 Day3 交付文档齐全，且按题目顺序形成流转链。
- 后端 25 条 pytest、前端 15 条 vitest 在本机重新通过。
- README 中的安装、运行、测试与审计命令可复制执行。
- 专用检查器与训练营项目审计均无 BLOCKED。

### 非目标

- 不扩展登录、云同步、真实支付、多币种或移动端能力。
- 不重写老师已确认正确的业务实现。
- 不把未执行的浏览器手动 E2E 写成 PASS。
- 不提交 `.env`、访问令牌、虚拟环境、依赖目录和构建产物。

## 5. 阶段门禁与允许范围

1. 先读任务与 demo，再建立范围和来源基线。
2. 先确认八份交付文档，再验证实现。
3. 只有实际执行的命令可以写入 PASS 证据。
4. 失败必须记录原因、最小修正和复测结果。
5. 存在 BLOCKED 时不得提交。

允许修改本提交目录内的文档和为验收所需的最小代码；禁止修改 `../day3-demo/`、扩展非目标功能、降低测试预期或泄露密钥。

## 6. 文件路由

| 内容 | 权威位置 |
|---|---|
| 题目八项流转 | `docs/交付文档/project-flow-map.md` |
| 范围与验收 | `docs/交付文档/product-prd.md` |
| 方案取舍 | `docs/交付文档/design-options.md` |
| 开发拆分 | `docs/交付文档/dev-workflow.md`、`docs/tasks.md` |
| 测试策略与实际结果 | `docs/交付文档/test-strategy.md`、`docs/test-record.md` |
| AI 协作与人工判断 | `docs/ai-log.md` |
| 风险与复盘 | `docs/reflection.md` |

## 7. 运行与验证命令

```bash
# 后端安装与测试
cd backend
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest tests -q

# 前端安装、测试与构建
cd ../frontend
npm ci
npm test -- --run
npm run build

# 返回项目根目录执行审计
cd ..
bash check-submission.sh .
bash ../.agents/skills/xiaomi-ai-bootcamp/scripts/audit-xiaomi-project.sh . personal
```

## 8. 验收证据映射

| 验收标准 | 实现位置 | 测试/Review | 实际证据 | 状态 |
|---|---|---|---|---|
| AC-1 创建旅行与 CRUD 可用 | `backend/routes/trips.py` | `backend/tests/test_trips.py` | `docs/test-record.md` | PASS |
| AC-2 成员与账单校验正确 | `backend/routes/trips.py` | `test_members.py`、`test_expenses.py` | `docs/test-record.md` | PASS |
| AC-3 结算结果正确 | `backend/services/settle.py` | `backend/tests/test_settle.py` | `docs/test-record.md` | PASS |
| AC-4 前端表单与展示可测试 | `frontend/src/components/` | 5 个 Vitest 文件 | `docs/test-record.md` | PASS |
| AC-5 八份文档齐全且串联 | `docs/交付文档/` | `check-submission.sh` | `docs/test-record.md` | PASS |

## 9. AI 协作与失败处理

关键协作按“目的、输入、建议、人工判断、验证”五字段写入 `docs/ai-log.md`。命令失败时保留事实并记录复测；资料冲突时停止扩展，由个人负责人基于题目做判断；测试失败时状态为 BLOCKED。

## 10. 团队规则

不适用，本项目为个人课程练习。

## 11. 完成定义

- **PASS**：必需文件非空、无占位符、自动测试和构建通过、两个检查器无 BLOCKED、GitLab 推送成功。
- **WARNING**：主要证据存在，但手动 E2E 等非阻断项未执行或映射不足。
- **BLOCKED**：关键文件缺失、测试失败、命令不可复现、存在占位符或证据真实性风险。
