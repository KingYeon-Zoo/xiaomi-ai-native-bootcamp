# 项目一：Apache HTTP 服务器日志智能清洗与故障分析

> **难度等级**：Lv.2 入门级 | **总课时**：3 课时（每课时 45 分钟）  
> **技术栈**：Python 3.10+ · pandas · re · matplotlib · pytest  
> **数据文件**：`Apache.tar.gz`（解压后得到 `Apache.log`，约 56,481 行 Apache HTTP Server 错误日志）

---

## 项目目标

你是运维工程师，Web 服务器报错，需要分析 Apache 错误日志并定位主要故障现象。

借助 AI 完成全流程：

**日志探索 → 结构化解析 → 异常识别 → 统计分析 → 可视化 → 报告输出**

核心能力：

**正则表达式 · 数据解析 · TDD · 故障分析 · Agent 结果审查**

---

## 数据集

- **来源**：GitHub `logpai/loghub`
- **背景**：Apache HTTP Server 运行时错误日志
- **课堂数据**：`Apache.tar.gz`
- **日志格式**：`[时间戳] [日志级别] 日志内容`

```text
[Sun Dec 04 04:47:44 2005] [notice] workerEnv.init() ok /etc/httpd/conf/workers2.properties
[Sun Dec 04 04:47:44 2005] [error] mod_jk child workerEnv in error state 6
```

项目统一提取以下字段：

- `timestamp`
- `level`
- `module`
- `error_code`
- `content`

---

## Lesson 1：规格、测试与日志解析

### 你要做什么

1. 解压并读取 Apache 日志；
2. 统计日志总量、日志级别和时间范围；
3. 使用 `spec_template.md` 生成并审查 `spec.md`；
4. 使用 `test_strategy_template.md` 生成并审查 `test-strategy.md`；
5. 编写日志解析测试；
6. 使用 Red–Green–Refactor 实现日志解析；
7. 生成 `structured_logs.csv`。

### 阶段提交文件

| 文件 | 说明 |
|---|---|
| `spec.md` | 项目规格，状态应为 Approved |
| `test-strategy.md` | 测试策略，状态应为 Approved |
| `lesson1_日志探索与解析.py` | 数据探索与解析脚本 |
| `log_parser.py` | 日志解析模块 |
| `tests/test_log_parser.py` | 日志解析测试 |
| `outputs/structured_logs.csv` | 结构化日志 |
| `AI-log.md` | 本课至少记录 1 条关键 AI 协作 Session |

---

## Lesson 2：异常识别与统计分析

### 你要做什么

1. 检查 Spec、测试和解析代码是否一致；
2. 实现三类异常筛选：
   - 按日志级别筛选；
   - 按 `error state` 筛选；
   - 按关键字筛选；
3. 实现以下统计：
   - 每日 Error 数量；
   - 错误类型数量与占比；
   - 模块 Error 数量；
   - 模块 Error 率；
4. 使用小型固定数据编写统计测试；
5. 完成解析、筛选和统计的集成验证。

模块 Error 率定义：

```text
模块 Error 率
=
该模块 Error 日志数
÷
该模块全部日志数
```

### 阶段提交文件

| 文件 | 说明 |
|---|---|
| `lesson2_异常识别与统计.py` | 异常识别和统计脚本 |
| `error_filter.py` | 异常筛选模块 |
| `statistics.py` | 统计分析模块 |
| `tests/test_error_filter.py` | 异常筛选测试 |
| `tests/test_statistics.py` | 统计分析测试 |
| `tests/test_integration.py` | 集成测试 |
| `outputs/error_level_logs.csv` | 按日志级别筛选结果 |
| `outputs/error_state_logs.csv` | 按错误状态筛选结果 |
| `outputs/keyword_logs.csv` | 按关键字筛选结果 |
| `outputs/error_code_reference.csv` | 错误类型对照表 |
| `AI-log.md` | 累计至少 2 条关键 AI 协作 Session |

---

## Lesson 3：可视化、验收与报告

### 你要做什么

1. 生成三张图：
   - 每日 Error 趋势图；
   - 错误类型分布图；
   - 模块 Error 数量对比图；
2. 将模块封装为 `log_analyzer/` 包；
3. 执行单元测试、集成测试和 Smoke Test；
4. 撰写 `analysis_report.md`；
5. 更新 `spec.md` 和 `test-strategy.md` 为 Final Approved；
6. 完成最终提交。

### 分析报告要求

报告至少包含：

1. 项目概述；
2. 数据探索；
3. 日志解析规则；
4. 异常识别结果；
5. 统计分析结果；
6. 可视化分析；
7. 故障原因推测；
8. 优化建议；
9. 已知限制。

报告中的数字必须来自实际输出。故障原因需要区分事实、推测和限制。

---

## 最终提交目录

```text
project1/
├── spec.md
├── test-strategy.md
├── AI-log.md
├── README.md
├── main.py
├── lesson1_日志探索与解析.py
├── lesson2_异常识别与统计.py
├── lesson3_可视化与报告.py
├── log_analyzer/
│   ├── __init__.py
│   ├── log_parser.py
│   ├── error_filter.py
│   ├── statistics.py
│   ├── visualizer.py
│   ├── utils.py
│   └── README.md
├── tests/
│   ├── test_log_parser.py
│   ├── test_error_filter.py
│   ├── test_statistics.py
│   └── test_integration.py
├── outputs/
│   ├── structured_logs.csv
│   ├── error_level_logs.csv
│   ├── error_state_logs.csv
│   ├── keyword_logs.csv
│   └── error_code_reference.csv
├── charts/
│   ├── daily_error_trend.png
│   ├── error_type_distribution.png
│   └── module_error_comparison.png
└── analysis_report.md
```

---

## AI-log.md 要求

至少记录 **3 条关键 AI 协作 Session**，每课时至少 1 条。

建议主题：

| 课时 | 建议记录内容 |
|---|---|
| Lesson 1 | 字段规则、正则解析、测试 Expected Result |
| Lesson 2 | 筛选规则、统计口径、模块 Error 率 |
| Lesson 3 | 验收结果、图表核对、故障分析 |

每条记录格式：

```markdown
## Session 1：日志解析规则确认

| 字段 | 内容 |
|---|---|
| 目的 | 本次希望 AI 协助完成什么 |
| 输入 | 提供给 AI 的文件、规则和约束 |
| AI 建议 | AI 给出的主要方案 |
| 人工判断 | 采纳、修改或拒绝了什么，为什么 |
| 验证 | 使用什么测试、命令或输出进行确认 |
```

以下记录无效：

- 只写“AI 说得对”；
- 只粘贴聊天截图；
- 没有人工判断；
- 没有验证方法或实际结果。

---

## 评分标准

总分 100 分。

| 评分维度 | 分值 | 评分重点 |
|---|---:|---|
| Spec 与测试策略 | 15 | 需求明确、字段规则一致、测试可验证 |
| 日志解析 | 20 | 五字段正确、非法行处理可靠 |
| 异常筛选与统计 | 25 | 三类筛选正确、统计口径正确 |
| 测试与运行证据 | 15 | 测试真实有效、完整流程可运行 |
| 图表与分析报告 | 15 | 图表与数据一致、分析有证据 |
| 工程结构与 AI-log | 10 | 目录完整、包可导入、人工判断有效 |

### 好的提交

- 可以通过 `pytest -q`；
- 可以通过 `python main.py` 重新生成输出；
- `spec.md`、测试和代码一致；
- 非法日志不会导致批量处理停止；
- 模块 Error 率计算正确；
- 图表和报告数字可以复现；
- `AI-log.md` 能体现学生真实的采纳、修改和拒绝判断。

### 不好的提交

- 只提交代码，没有 Spec、测试或 AI-log；
- 测试只检查“结果非空”；
- 直接复制参考 CSV；
- 为通过测试修改 Expected Result；
- 图表数据与输出文件不一致；
- 报告包含无法复现的数字；
- `AI-log.md` 只有聊天截图或“AI 说得对”。

---

## 最终验收命令

```bash
pytest -q
python main.py
```
