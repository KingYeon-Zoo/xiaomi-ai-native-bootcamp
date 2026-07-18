# CLAUDE.md — 项目指南

## 任务概述

**项目名称**：Apache HTTP 服务器日志智能清洗与故障分析

**角色**：运维工程师

**目标**：从 Apache 错误日志中自动识别故障原因，完成日志解析 → 异常识别 → 统计分析 → 可视化 → 报告输出全流程。

**技术栈**：Python 3.10+ / pandas / re / matplotlib

**时间约束**：3 课时（约 3 小时）

---

## 文件索引（按优先级）

### 第一优先级：任务要求与数据源

| 文件 | 说明 |
|------|------|
| `作业要求.md` | **最重要** — 完整的作业要求、提交文件清单、评分标准 |
| `Apache.log` | **数据源** — 56,482 行 Apache 错误日志（2005-06-09 ~ 2006-02-28） |

### 第二优先级：产出文档

| 文件 | 说明 |
|------|------|
| `docs/prd.md` | ✅ 产品需求文档 — 项目背景、目标/非目标、功能需求、验收标准 |
| `docs/design.md` | ✅ 技术设计文档 — 架构设计、模块划分、正则设计、数据流、错误分类规则 |
| `docs/作业要求.md` | ✅ 原始作业要求 |
| `docs/ai-log.md` | ✅ AI 协作日志（24 条记录） |
| `docs/dev.md` | ✅ 开发文档 — 环境搭建、代码结构、模块接口、开发计划 |
| `docs/test-strategy.md` | ✅ 测试策略文档 — 测试用例、验证标准、pytest 集成 |
| `tasks.md` | ✅ 任务清单 — 6 个独立可验证任务，供 Agent 执行 |
| `ai-log/ai-log模板.md` | AI 协作记录模板 |
| `ai-log/ai-log定义.txt` | AI 协作记录定义 |

### 第三优先级：代码文件（待创建）

| 文件 | 说明 |
|------|------|
| `lesson1_日志探索与解析.py` | Lesson 1 主脚本 |
| `log_parser.py` | 日志解析模块 |
| `structured_logs.csv` | 结构化输出（52,004 行） |
| `lesson2_异常识别与统计.py` | Lesson 2 主脚本 |
| `error_filter.py` | 异常筛选模块 |
| `statistics.py` | 统计分析模块 |
| `error_code_reference.csv` | 错误类型含义对照表 |
| `lesson3_可视化与报告.py` | Lesson 3 主脚本 |
| `log_analyzer/` | 工具库目录 |
| `charts/` | 可视化图表 |
| `analysis_report.md` | 分析报告 |

---

## 关键数据（必须了解）

### 数据规模

| 维度 | 值 |
|------|-----|
| 总行数 | 56,482 |
| 格式完整 | 52,004 行 |
| 格式异常 | 4,478 行（仅有 `script not found or unable to stat`，无时间戳和级别） |

### 日志级别分布

| 级别 | 数量 | 占比 |
|------|------|------|
| error | 38,081 | 67.6% |
| notice | 13,755 | 24.5% |
| warn | 168 | 0.3% |

### 主要错误类型

| 错误模式 | 出现次数 | 含义 |
|----------|----------|------|
| `mod_jk child workerEnv in error state` | 4,349 | mod_jk worker 连接后端 Tomcat 失败 |
| `mod_jk child init 1 -2` | 971 | mod_jk 子进程初始化失败 |
| `File does not exist` | 大量 | 404 文件不存在 |
| `Directory index forbidden by rule` | 大量 | 目录列表被禁止 |
| `env.createBean2(): Factory error` | 各 45 | JNI/VM 通道创建失败 |
| `config.update(): Can't create` | 各 45 | 配置更新失败 |

---

## 重要约定

### 1. 代码文件要求是灵活的

作业要求中给出的 3 个阶段的代码文件只是**基本示例要求**，不一定要完全一一对应：
- 可以多一个 `.py` 文件
- 可以根据实际需要调整模块划分
- 核心原则是功能完整，而非文件名完全匹配

### 2. 目标与非目标

**目标**：
- 结构化解析完整（CSV = 52,004 行）
- 字段提取准确（timestamp / level / content 无缺失）
- 异常识别覆盖（至少 8 种错误类型）
- 可视化有效（3 张图表清晰展示）
- 报告完整（8 个章节）

**非目标**：
- 不分析 notice / warn 级别
- 不做实时监控、AI/ML 检测
- 不做通用日志框架
- 不处理格式异常行（4,478 行）

### 3. 性能参考

5 万行日志正则解析耗时约 0.038 秒，无需过度优化。

---

## 三阶段任务概览

### Lesson 1：日志探索与解析
- 数据探索：统计总行数、各级别数量、时间范围
- 正则解析：提取 timestamp / level / content
- 输出：`structured_logs.csv`（52,004 行）

### Lesson 2：异常识别与统计分析
- 三维度筛选：按级别、关键字、模块
- 多维度统计：时间、类型、模块
- 输出：`error_code_reference.csv`（至少 8 种错误类型）

### Lesson 3：可视化展示与报告
- 3 种图表：时序图、饼图、柱状图
- 工具库封装：`log_analyzer/` 包
- 输出：`analysis_report.md`（8 个章节）
