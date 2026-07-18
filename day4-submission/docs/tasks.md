# Day4 可验证任务

| ID | 输入 | 产出 | 验证命令/证据 | 状态 |
|---|---|---|---|---|
| T1 | Day4 三份要求与数据说明 | 最终清单、冲突裁决、非目标 | `docs/engineering-constraints.md` | 已完成（文档落盘晚于实现骨架，偏差已记录） |
| T2 | Apache.tar.gz | P1 五字段、筛选、统计、图表、报告 | P1 pytest + `python main.py` | 已完成并全量验证 |
| T3 | 六个邮件压缩包 | P2 清洗、特征、规则/NB、图表、报告 | P2 pytest + `python main.py` | 已完成并全量验证 |
| T4 | P1/P2 初版代码 | 三维审查、一个受控修改、V1/V2/V3 | `agent_review_report.md` + Git diff | 已完成：产品改动 2 文件 |
| T5 | 全部产物 | 清单审计、证据复算、反思 | `docs/test-record.md`、`docs/reflection.md` | 已完成：专用清单与 Skill 审计通过 |
| T6 | 已审计提交 | 小米 GitLab 远端提交 | `git status`、`git log`、`git ls-remote` | 已完成：私有项目创建、main 推送、远端 HEAD 核验 |
