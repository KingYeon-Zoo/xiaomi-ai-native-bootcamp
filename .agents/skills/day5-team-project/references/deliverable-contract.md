# Day5 交付合同

## 核心目录

```text
README.md
src/
prototype/
  prototype-readme.md
  screenshots-or-video.md
docs/
  diagnosis/
    problem-diagnosis.md
    clarifying-questions.md
    assumptions-and-non-goals.md
  design/
    end-to-end-system-design.md
  options/
    solution-options.md
    tradeoff-matrix.md
    rejected-options.md
  decision/
    decision-memo.md
    final-recommendation.md
  validation/
    validation-plan.md
    cases-and-results.md
    risk-and-edge-cases.md
    review-record.md
  ai/
    ai-collaboration-log.md
    accepted-and-rejected-ai-advice.md
  collaboration/
    role-division.md
    meeting-minutes.md
    decision-log.md
    issue-log.md
  reflection/
    team-retrospective.md
    individual-contributions.md
  defense/
    defense-outline.md
```

## 文件责任

| 文件 | 必须证明 |
|---|---|
| `README.md` | 项目、真正问题、运行、Demo、验证、限制、设计和 AI 概览 |
| `problem-diagnosis.md` | 用户、利益相关方、冲突、约束、信息缺口和成功标准 |
| `clarifying-questions.md` | 10 个问题、3 个 P0，以及不同答案的方案影响 |
| `assumptions-and-non-goals.md` | 未确认假设、两天范围和主动放弃 |
| `solution-options.md` | 3 条本质不同路线 |
| `tradeoff-matrix.md` | 权重、评分、证据、成本和风险 |
| `rejected-options.md` | 被拒路线或 AI 建议及人工判断 |
| `decision-memo.md` | 最终选择、放弃原因、代价、风险和验证责任 |
| `end-to-end-system-design.md` | 技术端、角色、数据流、AI 边界、复核、日志和失败处理 |
| `prototype-readme.md` | 原型能证明什么、不能证明什么、主路径和失败演示 |
| `screenshots-or-video.md` | 主路径和至少一个边界/失败场景的兜底证据 |
| `validation-plan.md` | 正常、边界、失败、回归、端到端计划 |
| `cases-and-results.md` | 实际执行环境、输入、预期、实际、结果和修复 |
| `risk-and-edge-cases.md` | 当前能兜住、兜不住和残留风险 |
| `review-record.md` | 人工 Review、AI Review 和修正 |
| `ai-collaboration-log.md` | AI 六类协作中的至少五类，含 Prompt 与人工判断 |
| `accepted-and-rejected-ai-advice.md` | 至少两条真实拒绝或明显修改 |
| `role-division.md` | 成员、职责、主备负责人、交付物和证据 |
| `meeting-minutes.md` | 四个真实节点的结论、分歧和行动项 |
| `decision-log.md` | 关键决策的备选、理由、代价和验证 |
| `issue-log.md` | 阻塞、冲突、风险与处理；没有也需说明 |
| `team-retrospective.md` | 具体事件、风险和可沉淀经验 |
| `individual-contributions.md` | 每人关键判断、AI 判断、验证和至少三类证据 |
| `final-recommendation.md` | 800 字以内的评委向建议 |
| `defense-outline.md` | 6+6 分钟脚本、证据、追问卡和 Demo 兜底 |

## 一致性检查

每个关键判断至少能沿以下链路追踪：

```text
题面/评分项
→ 诊断和 P0 澄清
→ 方案与人工取舍
→ 端到端设计
→ 负责人和实现文件
→ 用例与实际结果
→ AI/人工 Review
→ README、最终建议和答辩说法
```

检查同一概念在不同文件中的名称、范围、数字和状态是否一致，尤其是：

- 端和角色；
- MVP 功能与非目标；
- AI 自动决策和人工复核边界；
- 测试计划与实际结果；
- 已修复问题与残留风险；
- 成员角色与提交、会议、AI、测试证据；
- README 命令与真实项目结构。

空表、模板示例、占位文字、不可执行命令和只有预期没有实际结果均不算证据。
