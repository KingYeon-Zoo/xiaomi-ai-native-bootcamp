# 产品需求文档（PRD）

## Apache HTTP 服务器日志智能清洗与故障分析工具

---

## 1. 项目概述

### 1.1 项目名称

Apache HTTP 服务器日志智能清洗与故障分析工具

### 1.2 项目背景

运维工程师在日常工作中需要面对大量的 Apache 错误日志，人工排查效率低、容易遗漏关键信息。当 Web 服务器出现故障时，快速定位问题根因是保障服务可用性的关键。

本项目借助 AI 辅助开发，构建一套自动化故障排查工具，实现从日志解析到故障定位的全流程自动化，提升运维效率。

### 1.3 项目目标

| 目标 | 衡量标准 |
|------|----------|
| 结构化解析完整 | CSV 行数 = 格式完整的原始日志行数（52,004 行） |
| 字段提取准确 | timestamp / level / content 三个字段无缺失 |
| 异常识别覆盖 | 覆盖 error 级别的主要错误类型（至少识别 8 种） |
| 可视化有效 | 3 张图表能清晰展示时间趋势、错误分布、模块对比 |
| 报告完整 | 包含 8 个章节的分析报告，有故障根因分析和优化建议 |

### 1.4 非目标（明确不做什么）

| 非目标 | 原因 |
|--------|------|
| 不分析 notice / warn 级别 | 聚焦 error 故障排查 |
| 不做实时日志监控 | 3 小时内不现实，本次只处理静态文件 |
| 不做机器学习/AI 异常检测 | 用规则匹配即可 |
| 不做跨服务器日志聚合 | 单文件分析 |
| 不做通用日志解析框架 | 聚焦 Apache，不考虑 Nginx 等 |
| 不做深度的性能优化 | 数据量 5 万行，正则解析仅需 0.038 秒 |
| 不深究每种错误的详细根因 | 报告指出 top 错误类型和大类原因即可 |
| 不处理格式异常行 | 4,478 行缺少时间戳和级别，无法结构化 |

### 1.5 技术栈

- Python 3.10+
- pandas — 数据处理与分析
- re — 正则表达式解析
- matplotlib — 数据可视化

### 1.6 约束条件

- 总课时：3 课时（约 3 小时）
- 聚焦当前任务目标，不做过度的可复用性和可扩展性设计

---

## 2. 数据说明

### 2.1 数据来源

- 来源：GitHub [logpai/loghub](https://github.com/logpai/loghub/tree/master/Apache)
- 背景：Apache HTTP Server 运行时的错误日志（2005-06-09 ~ 2006-02-28）
- 文件：`Apache.log`

### 2.2 数据规模

| 维度 | 值 |
|------|-----|
| 总行数 | 56,482 |
| 格式完整（可解析） | 52,004 行 |
| 格式异常（无法解析） | 4,478 行 |

### 2.3 日志格式

标准格式：`[时间戳] [日志级别] 日志内容`

```
[Thu Jun 09 06:07:04 2005] [notice] LDAP: Built with OpenLDAP LDAP SDK
[Thu Jun 09 06:07:05 2005] [error] env.createBean2(): Factory error creating channel.jni:jni
[Thu Jun 09 07:11:21 2005] [error] [client 204.100.200.22] Directory index forbidden by rule: /var/www/html/
```

格式异常行（仅有内容，无时间戳和级别）：
```
script not found or unable to stat
```

### 2.4 日志级别分布

| 级别 | 数量 | 占比 |
|------|------|------|
| error | 38,081 | 67.6% |
| notice | 13,755 | 24.5% |
| warn | 168 | 0.3% |

### 2.5 主要错误类型（真实数据）

| 错误模式 | 出现次数 | 错误类型 | 含义 |
|----------|----------|----------|------|
| `mod_jk child workerEnv in error state` | 4,349 | MODJK_WORKER_ERROR | mod_jk worker 连接后端 Tomcat 失败 |
| `mod_jk child init 1 -2` | 971 | MODJK_INIT_FAIL | mod_jk 子进程初始化失败 |
| `mod_jk child init 1 0` | 288 | MODJK_INIT | mod_jk 子进程初始化 |
| `env.createBean2(): Factory error` | 各 45 | BEAN_CREATE_ERROR | JNI/VM 通道创建失败 |
| `config.update(): Can't create` | 各 45 | CONFIG_ERROR | 配置更新失败 |
| `File does not exist` | 大量 | FILE_NOT_FOUND | 404 文件不存在 |
| `Directory index forbidden by rule` | 大量 | DIR_INDEX_FORBIDDEN | 目录列表被禁止 |
| `Invalid method in request` | 若干 | INVALID_METHOD | 无效 HTTP 方法（可能是攻击） |
| `jk2_init() Can't find child` | 若干 | JK2_CHILD_NOT_FOUND | 找不到子进程 |
| `uriMap.mapUri() uri must start with` | 27 | URIMAP_ERROR | URI 映射配置错误 |

---

## 3. 功能需求

### 3.1 Lesson 1：日志探索与解析

**目标**：将原始日志文件解析为结构化的 CSV 数据

| 功能点 | 说明 | 优先级 |
|--------|------|:------:|
| 数据加载 | 读取 Apache.log 日志文件 | P0 |
| 数据探索 | 统计总行数（56,482）、各级别日志数量、时间范围、格式异常行数（4,478） | P0 |
| 正则解析 | 编写正则表达式，从格式完整的日志中提取 timestamp、level、content 三个字段 | P0 |
| 结构化输出 | 将解析结果保存为 structured_logs.csv（52,004 行） | P0 |
| 大文件处理 | 了解分块读取的思路（本次 5 万行 0.038 秒，了解即可） | P1 |

**输入**：Apache.log 原始日志文件

**输出**：
- `src/lesson1_日志探索与解析.py` — 数据探索 + 解析流程脚本
- `src/log_parser.py` — 可复用的日志解析模块
- `output/structured_logs.csv` — 解析后的结构化数据

### 3.2 Lesson 2：异常识别与统计分析

**目标**：从结构化数据中识别异常，进行多维度统计分析

| 功能点 | 说明 | 优先级 |
|--------|------|:------:|
| 级别筛选 | 按日志级别（error）筛选异常日志 | P0 |
| 关键字筛选 | 按错误码/关键字筛选异常日志 | P0 |
| 模块筛选 | 按模块（mod_jk、config、env 等）筛选异常日志 | P0 |
| 时间维度统计 | 每日 Error 数量趋势 | P0 |
| 类型维度统计 | 各错误码出现次数与占比 | P0 |
| 模块维度统计 | 各模块异常率对比 | P0 |
| 异常导出 | 将筛选出的异常日志单独保存 | P1 |
| 错误类型对照 | 生成错误类型含义对照表（覆盖上述 10 种错误类型） | P0 |

**输入**：output/structured_logs.csv

**输出**：
- `src/lesson2_异常识别与统计.py` — 异常识别 + 统计脚本
- `src/error_filter.py` — 异常筛选模块
- `src/statistics.py` — 统计分析模块
- `output/error_code_reference.csv` — 错误类型含义对照表

### 3.3 Lesson 3：可视化展示与报告总结

**目标**：生成可视化图表，封装工具库，撰写分析报告

| 功能点 | 说明 | 优先级 |
|--------|------|:------:|
| 时序图 | 每日 Error 数量变化趋势 | P0 |
| 饼图 | 各错误类型占比分布 | P0 |
| 柱状图 | 各模块 Error 数量对比 | P0 |
| 工具库封装 | 整合为 log_analyzer/ 包，含 __init__.py 和 README.md | P1 |
| 分析报告 | 撰写含 8 个章节的 analysis_report.md | P0 |

**输入**：output/structured_logs.csv、统计数据

**输出**：
- `src/lesson3_可视化与报告.py` — 可视化 + 工具库演示脚本
- `log_analyzer/` — 工具库目录
- `output/charts/` — 可视化图表 PNG 文件
- `output/analysis_report.md` — 分析报告

---

## 4. 验收标准

### 4.1 Lesson 1 验收标准

| 文件 | 验收标准 |
|------|----------|
| `src/lesson1_日志探索与解析.py` | 能正常运行，输出总行数（56,482）、各级别数量、时间范围（2005-06-09 ~ 2006-02-28）、格式异常行数（4,478） |
| `src/log_parser.py` | 可作为独立模块导入，正则表达式能正确提取 timestamp、level、content 三个字段 |
| `output/structured_logs.csv` | 包含 52,004 行数据，有 timestamp、level、content 三个字段，无缺失值 |

### 4.2 Lesson 2 验收标准

| 文件 | 验收标准 |
|------|----------|
| `src/lesson2_异常识别与统计.py` | 能正常运行，输出三个维度的统计结果 |
| `src/error_filter.py` | 支持按级别、关键字、模块三种方式筛选 |
| `src/statistics.py` | 支持时间、类型、模块三个维度的统计 |
| `output/error_code_reference.csv` | 包含 12 种错误类型的错误码、含义说明、所属模块 |

### 4.3 Lesson 3 验收标准

| 文件 | 验收标准 |
|------|----------|
| `src/lesson3_可视化与报告.py` | 能正常运行，生成 3 种图表，演示工具库功能 |
| `log_analyzer/` | 包结构完整，含 __init__.py、log_parser.py、error_filter.py、statistics.py、visualizer.py、utils.py、README.md |
| `output/charts/` | 包含 3 张 PNG 图表（时序图、饼图、柱状图），图表清晰可读 |
| `output/analysis_report.md` | 包含项目概述、数据探索、日志解析方法、异常识别结果、统计分析结果、可视化分析、故障根因分析、总结与优化建议共 8 个章节 |

### 4.4 全流程文档验收标准

| 文件 | 验收标准 |
|------|----------|
| `prd.md` | 本文档，包含项目背景、功能需求、验收标准 |
| `design.md` | 包含架构设计、模块划分、正则设计、数据流 |
| `dev.md` | 包含环境搭建、代码结构、接口说明、开发日志 |
| `test-strategy.md` | 包含测试方案、测试用例、验证标准 |
| `ai-log.md` | 至少 3 条 AI 协作记录，每条含目的、输入、建议、人工判断、验证五个字段 |

---

## 5. 项目计划

| 阶段 | 课时 | 主要任务 | 产出物 |
|:----:|:----:|----------|--------|
| Lesson 1 | 第 1 课时 | 日志探索与解析 | 解析脚本 + 结构化 CSV |
| Lesson 2 | 第 2 课时 | 异常识别与统计 | 统计脚本 + 错误类型表 |
| Lesson 3 | 第 3 课时 | 可视化与报告 | 图表 + 工具库 + 分析报告 |
