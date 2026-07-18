# Day 1 测试与审计记录

## 1. 执行环境

- 日期：2026-07-15
- 系统：macOS
- Python：3.9.6
- 第三方依赖：无
- 工作目录：`day1-submission/`

## 2. Bug 修复回归

命令：`python3 bug-fix-lab/test.py`

| 类别 | 输入 | 预期 | 实际结果 | 结果 |
|---|---|---|---|---|
| 正常 | 添加优先级 1、5、3 的任务 | 按 5、3、1 排序 | 高→中→低 | PASS |
| 边界 | 空字符串标题 | 抛出包含 `title` 的错误 | 抛出 `ValueError` | PASS |
| 边界 | 纯空格标题 | 去空格后拒绝 | 抛出 `ValueError` | PASS |
| 异常 | `high/low` 字符串优先级 | 转为整数，不保留字符串 | 映射为 5/1 | PASS |
| 回归 | 列表副本与最低优先级筛选 | 保持原行为 | 两项断言通过 | PASS |

实际汇总：7 条断言通过、0 条失败。修复前失败、双假设和最小修复见 `docs/bugs/`。

## 3. RAG 工程骨架

命令：`python3 rag-assistant/tests/test_basic.py`

| 检查 | 预期 | 实际结果 | 结果 |
|---|---|---|---|
| 核心文件 | FAQ、retrieve、answer、main 存在 | 4 项存在 | PASS |
| 模块加载 | retrieve、answer 可调用 | 2 项可调用 | PASS |
| 接口结构 | retrieve 返回列表；answer 返回 answer/sources | 类型与字段符合 | PASS |
| FAQ 编号 | 至少 8 个 `[faq-XX]` | 检出 12 次编号 | PASS |

实际汇总：9 条检查通过、0 条失败。

## 4. RAG 行为与边界

命令：`python3 rag-assistant/tests/test_rag.py`

| 类型 | 输入示例 | 预期 | 实际结果 | 结果 |
|---|---|---|---|---|
| 正确匹配 | “Day1要交什么？” | 内容命中且含 `[faq-02]` | 命中关键词与来源 | PASS |
| 正确匹配 | “什么是可复核交付？” | 含 `[faq-01]` | 命中关键词与来源 | PASS |
| 跨段落 | Spec 非目标与 AI 过度设计 | 命中相关 FAQ 之一 | 命中 faq-04/faq-10 | PASS |
| 资料外 | 奖学金、午饭 | 固定拒答 | 均输出无依据 | PASS |
| 混淆 | 未教授内容、RAG 其他检索方式 | 不扩展回答 | 均固定拒答 | PASS |
| 空输入 | 空字符串 | 提示输入问题 | 输出提示 | PASS |
| 超长输入 | 超过 200 字 | 不崩溃、无超时 | 有正常输出 | PASS |
| 纯停用词 | “的是了什么怎么” | 固定拒答 | 输出无依据 | PASS |

实际汇总：13 条用例通过、0 条失败；Mock 服务成功自动启动和关闭。

## 5. 提交审计

| 命令 | 预期 | 实际结果 | 结果 |
|---|---|---|---|
| `bash ../day1/check-submission.sh .` | 无 BLOCKED | 27 PASS、0 WARNING、0 BLOCKED | PASS |
| `bash ../.agents/skills/xiaomi-ai-bootcamp/scripts/audit-xiaomi-project.sh . personal` | 无 BLOCKED | 39 PASS、0 WARNING、0 BLOCKED | PASS |

## 6. 未执行与残留风险

- 未接入真实大模型，不宣称真实模型回答质量。
- 未做 Windows 环境验证。
- 未做并发请求、端口冲突恢复或超大 FAQ 性能测试。
