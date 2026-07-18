# Project 1 规格：Apache 日志智能清洗与故障分析

- 状态：Final Approved（2026-07-15 全量验收通过）
- 数据：`Apache.tar.gz` 中的 `Apache.log`
- Python：3.10+

## 1. 问题与目标

运维工程师需要把 Apache 错误日志转换为可复核的数据集，并区分事实统计与故障推测。目标限定为：五字段解析、三类异常筛选、四种统计口径、三张图和一份由实际输出驱动的报告。

## 2. 非目标

- 不支持可选 Linux.log：其 syslog 格式需要独立解析器，超出必交范围。
- 不做实时采集、告警服务、数据库、Web UI 或根因自动修复。
- 不把词表未命中的 `unknown` 写成“日志没有模块”。
- 不用 PID、端口或普通数字填充 `error_code`。

## 3. 数据契约

| 字段 | 类型 | 规则 |
|---|---|---|
| timestamp | datetime | 必须通过 `%a %b %d %H:%M:%S %Y` 解析 |
| level | string | 第二组方括号，统一小写 |
| module | string | 固定词表、长词优先、忽略大小写；未命中为 `unknown` |
| error_code | nullable int | 仅匹配 `error state N` 的 N |
| content | string | 级别后的完整非空内容 |

非法行返回 `None` 并累计数量，不中断文件处理，也不伪造默认字段。

## 4. 行为规格与验收

| AC | 行为 | 可执行验收 |
|---|---|---|
| P1-AC1 | 正常行准确提取五字段；错误时间戳/格式被跳过 | `tests/test_log_parser.py` |
| P1-AC2 | error 级别、error state、关键词三类筛选口径独立 | `tests/test_error_filter.py` |
| P1-AC3 | 每日 Error、错误类型数量/占比、模块 Error 数和模块 Error 率正确 | `tests/test_statistics.py` |
| P1-AC4 | `python main.py` 从真实压缩包生成清单规定的 5 CSV、3 PNG 与报告 | 全量入口 + `tests/test_integration.py` |
| P1-AC5 | 报告数字可从输出复算，事实/推测/限制明确分开 | 输出审计 + 人工 Review |

模块 Error 率严格定义为：该模块 `level=error` 数 / 该模块全部级别日志数。`unknown` 也可统计，但报告不会把它解释成真实业务模块。

## 5. 方案比较与选择

### 方案 A：一次正则完成全部语义

优点是代码短；风险是模块词表和 error state 规则绑死在一个复杂正则中，非法时间戳也可能被接受。适合演示，不利于定位错误。

### 方案 B：结构正则 + 时间校验 + 独立语义提取（选择）

先验证三段结构，再用 `datetime.strptime` 校验时间，最后分别提取模块和 error_code。多几步，但每条契约可单测，异常行处理更清楚。

### 方案 C：引入日志解析框架

扩展性强，但新增依赖和配置不能在课堂范围内证明收益，拒绝。

## 6. 模块、数据流与失败处理

```text
Apache.tar.gz -> 临时安全提取 -> parse_log_file
-> structured_logs.csv
-> 三类 filter CSV
-> 统一 statistics 表 -> 3 张图 + analysis_report.md
```

- `log_parser.py`：结构与字段契约。
- `error_filter.py`：只筛选，不重新解释字段。
- `statistics.py`：所有分母集中定义。
- `visualizer.py`：只消费统计表，不在图内重复聚合。
- `main.py`：编排与输出清单。

压缩包缺文件、有效记录为空时明确失败；单行异常只计数。输出目录可重复覆盖，保证相同输入得到同口径结果。

## 7. 可执行任务与变更边界

1. 固定样本验证 parser 正常/边界/非法。
2. 固定数据验证三个 filter 和统计分母。
3. 小型集成输入验证全部输出文件。
4. 全量运行并用 CSV 复算报告关键数字。
5. 只在 Project 3 选定问题后做最小变更，禁止顺手重构。

## 8. 风险

模块词表可能漏识别；内容分类把未含 error state 的 error 归入 `other_error`；只有 error log 无法提供请求量分母；故障原因只能作为待验证推测。
