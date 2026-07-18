# Day 1 可验证任务拆分

| 任务 | 输入 | 产出 | 验证命令 | 证据位置 | 状态 |
|---|---|---|---|---|---|
| T1 固化范围与验收 | 原题、六类文件定义、FAQ | `spec.md` | 人工核对目标≤5、非目标≥3、验收≥3 | `docs/spec.md` | 完成 |
| T2 设计 RAG 最小链路 | Spec、FAQ、Mock 接口 | 数据流、接口、取舍、失败策略 | Review 数据流与接口是否闭合 | `docs/design.md` | 完成 |
| T3 验证工程骨架 | RAG 源码与 FAQ | 模块和接口可加载 | `python3 rag-assistant/tests/test_basic.py` | `docs/test-record.md` | 完成 |
| T4 验证 RAG 行为 | 13 条问题集、Mock LLM | 正确匹配、引用、拒答与边界结果 | `python3 rag-assistant/tests/test_rag.py` | `docs/test-record.md` | 完成 |
| T5 完成 Bug 最小闭环 | 课程失败记录、任务管理器源码 | 根因假设、最小修复、回归 | `python3 bug-fix-lab/test.py` | `docs/bugs/` | 完成 |
| T6 整理 AI 决策与复盘 | 方案取舍、失败和测试结果 | 五字段日志、个人复盘 | 检查每条含目的/输入/建议/人工判断/验证 | `docs/ai-log.md`、`docs/reflection.md` | 完成 |
| T7 审计提交包 | 全部交付文件 | 专用检查与 Skill 审计结论 | README 中两条审计命令 | `docs/test-record.md` | 完成 |

任务只有在对应命令实际执行且结果写入证据后才标记“完成”。
