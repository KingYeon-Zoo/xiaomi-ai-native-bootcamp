# 角色与责任

LOOPS 当前由 `ChinyenZoo` 独立重构与维护。角色可以集中在一人，职责与验收证据不能消失。

| 职责域 | 负责人 | 备份人 | 主要产出 | 验收标准 | 证据 |
|---|---|---|---|---|---|
| 产品与范围 | ChinyenZoo | 不适用：个人维护 | 问题诊断、非目标、方案取舍 | 三条路线、P0 澄清与边界一致 | `docs/diagnosis/`、`docs/options/` |
| Agent 与服务端 | ChinyenZoo | 不适用：个人维护 | Evidence、Graph、策略门、运行时、API | 正常/冲突/失败/恢复路径通过 | `src/backend/app/agents/`、后端测试 |
| Web 前端 | ChinyenZoo | 不适用：个人维护 | 动态流、人审、Agent/ML 控制台 | 生产构建通过，关键交互可演示 | `src/frontend/src/`、截图 |
| 数据与演示 | ChinyenZoo | 不适用：个人维护 | Mongo 快照、回退协议、种子数据 | 数据来源明确，现场无数据也可解释 | `seed_demo_data.py`、指标服务 |
| 验证与文档 | ChinyenZoo | 不适用：个人维护 | 自动化测试、证据映射、README | 命令可复现，事实可定位 | `docs/validation/`、`README.md` |

AI 编码工具只协助澄清、对比、反证、实现、验证与审查，不是项目成员，也不拥有范围、授权或发布决策。
