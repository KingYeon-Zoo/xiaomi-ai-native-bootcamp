# 用例与实际结果

执行日期：2026-07-17；环境：macOS、本地 MongoDB 7、Python 3.13 虚拟环境、React/Vite。

| 类型 | 输入或命令 | 预期 | 实际结果 | 状态 |
|---|---|---|---|---|
| 正常 | `.venv/bin/python -m pytest tests/agents -q` | Agent 测试全通过 | 31 通过；4 个 httpx 弃用警告 | 通过 |
| 正常 | `GET /health` 与 Mongo `ping` | API、数据库与审核服务就绪 | `healthy`、`database=connected`、`ping=1` | 通过 |
| 正常 | DeepSeek 文本烟测：FastAPI/LangGraph 技术内容 | 返回结构化 Evidence | `deepseek-v4-flash-260425` 返回 allow，1 条 Evidence | 通过 |
| 正常 | 豆包视觉烟测：`src/frontend/src/assets/hero.png` | 图片真实发送并返回 Evidence | `doubao-seed-2-0-lite-260428` 返回 allow，1 条 Evidence | 通过 |
| 边界 | fake 文本/视觉建议冲突 | 进入 critic、arbiter、人工 interrupt | `test_graph.py` 覆盖对应节点与恢复 | 通过 |
| 边界 | 必需视觉 Evidence 缺失 | 不自动放行 | `test_policy.py` 判为 `waiting_human` | 通过 |
| 失败 | fake Graph 抛出异常 | run 记录 failed | `test_runtime.py` 断言状态与错误 | 通过 |
| 失败 | 模型拒绝 `json_schema` | 仅此类错误降级为 `json_object` | `test_ark_agents.py` 验证回退后仍做 Pydantic 校验 | 通过 |
| 失败推动修复 | 移动源码目录后首次执行 `./start.sh` | 自动启动后端 | 先出现 `uvicorn: command not found`，初修后进一步发现无效虚拟环境 | 失败已保留 |
| 回归 | 受信规则产生硬拦截 | 跳过文本、视觉、critic、arbiter | `test_graph.py` 验证直接进入策略门 | 通过 |
| 回归 | 启动器改用虚拟环境解释器并检测失效环境 | 目录移动后仍可自愈启动 | 后端 8008、前端 5173、Mongo 27017 均就绪 | 通过 |
| 安全 | LLM 伪造硬规则代码 | 不获得硬权限 | `test_policy.py` 验证来源校验 | 通过 |
| API | 用户状态与管理轨迹 | 用户接口隐藏 text/trace，管理接口返回节点 | `test_agent_api.py` 覆盖状态、轨迹、人工决定、404 | 通过 |
| 数据 | `seed_demo_data.py` | 重建四类演示集合 | 96 Posts、64 moderation runs、32 ML metrics、3 snapshots | 通过 |
| 接口 | `/api/metrics/control-center?hours=24` | 从 Mongo 返回双方案数据 | `source=mongodb_demo_snapshot`，Agent/ML 均为 12,847 | 通过 |
| 前端 | `npm run lint && npm run build` | lint 与生产构建成功 | 成功；主 JS 1,014.60 kB，Vite 提示大于 500 kB | 通过，保留警告 |
| 浏览器 | Agent、ML、对比、1 小时/24 小时/7 天 | 切换与数据更新正常 | 1280 × 720 验证；控制台 error/warn 为 0 | 通过 |
| 端到端 | `./start.sh`、`/health`、指标接口、Mongo 计数、浏览器 | 三端与主视图闭环可用 | 服务健康、Mongo 快照返回、截图已保存 | 通过 |
| 回归 | http://localhost:5173/ 直接登录 | 页面正常加载，无白屏，可正常登录 | 成功登录，正常渲染 AppShell，且控制台无 `ReferenceError` | 通过 |
| 回归 | 修改密码模态框错误提示 | 触发密码不一致错误时，三角形警告图标正常渲染 | 成功渲染警告图标且控制台无 JS 崩溃报错 | 通过 |

## 解释限制

- 两个真实云烟测只证明当前密钥、模型名、图片传输和结构化解析可用；单个安全样本不能证明准确率。
- 31 个测试集中在新增 Agent 与看板服务；旧 ML 全量测试未在本轮宣称全部通过。
- 看板上的 97.8%、2.84 秒、326 次/秒等是演示快照字段，不是上述测试测得。
- Vite 大包警告未阻塞演示，但属于待优化项。
