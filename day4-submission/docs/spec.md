# Day4 跨项目范围与验收索引

## 目标

1. 完成 Apache 日志五字段解析、三类异常筛选、统计、图表和事实驱动报告。
2. 完成 SpamAssassin 邮件 raw/cleaned 数据契约、规则/NB 同测试集比较和误判分析。
3. 对两个项目做三维代码审查，只修改一个最高优先级问题并提供 V1/V2/V3。
4. 让课程清单、README 命令、测试记录、AI/人工判断和输出形成可追溯证据链。

## 非目标

- 不处理可选 Linux.log、实时服务、数据库、Web UI、深度学习或附件 OCR。
- 不把测试集作为调参集，不删除困难样本，不修改标签迎合指标。
- 不复制 Demo 旧版 PRD/Design/Dev 结构，不用文档数量替代判断质量。

## 边界与失败

- P1 对不符合标准前缀的续行计入 invalid，不猜测其时间归属；压缩包缺少 Apache.log 或有效记录为空时明确失败。
- P2 目录不含恰好六个压缩包时拒绝运行；单封 MIME 异常记录告警并保留空文本样本；模型未 fit 时拒绝预测。
- 任一测试、全量入口、清单或证据审计出现 BLOCKED，均不得提交。

## 验收索引

| 范围 | 详细规格入口 | 关键验收 | 实际证据 |
|---|---|---|---|
| Project 1 | `project1/spec.md` | 5 CSV、3 图、报告；模块 Error 率分母正确 | `docs/test-record.md` 的 E2E-1、DATA-1、REV-1 |
| Project 2 | `project2/spec.md` | 7,449 封；固定切分；四指标、4 图、FP/FN | E2E-2、DATA-2、VIS-1 |
| Project 3 | `agent_review_report.md` | 两项目证据、一个问题、≤2 产品文件、V1/V2/V3 | REV-1 与 Git 基线 `9ad4a2d` |
| 工程提交 | `docs/engineering-constraints.md` | 无占位、测试通过、两类审计无 BLOCKED、远端可核验 | AUDIT-1 与 Git 记录 |

题目规定位置使用符号链接路由到 `docs/` 唯一正文；这同时保留最终清单文件名并避免重复文档漂移。
