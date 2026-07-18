# 数据集说明

本目录包含两个课程项目所需的数据集，按项目分文件夹存放。

---

## 目录结构

```
data/
├── README.md                 # 本文件
├── project1/                 # 项目一：Apache 系统日志分析
│   ├── Apache.tar.gz         # Apache HTTP Server 错误日志（解压后 Apache.log，约 56,481 行）
│   └── Linux.tar.gz          # Linux syslog 格式日志（解压后 Linux.log，约 25,567 行，可选扩展）
└── project2/                 # 项目二：垃圾邮件智能过滤
    ├── 20030228_easy_ham.tar.bz2
    ├── 20030228_easy_ham_2.tar.bz2
    ├── 20030228_hard_ham.tar.bz2
    ├── 20030228_spam.tar.bz2
    ├── 20030228_spam_2.tar.bz2
    └── 20050311_spam_2.tar.bz2
```

---

## 项目一：Apache 系统日志数据集

### 数据来源

- **仓库地址**：https://github.com/logpai/loghub
- **论文引用**：Jieming Zhu, Shilin He, Pinjia He, Jinyang Liu, Michael R. Lyu. *Loghub: A Large Collection of System Log Datasets for AI-driven Log Analytics*. IEEE International Symposium on Software Reliability Engineering (ISSRE), 2023.

### Apache.log（主数据）

| 属性 | 说明 |
|------|------|
| **来源系统** | Apache HTTP Server（Fedora） |
| **日志类型** | 错误日志（error log） |
| **压缩包** | `Apache.tar.gz` |
| **行数** | 约 56,481 行 |
| **日志级别** | error（约 38,081）、notice（约 13,755）、warn（约 168） |

**日志格式**：
```
[Thu Jun 09 06:07:04 2005] [notice] LDAP: Built with OpenLDAP LDAP SDK
[Thu Jun 09 06:07:20 2005] [error] mod_jk child init 1 0
[Wed Sep 28 09:08:45 2005] [warn] child process 18801 still did not exit, sending a SIGTERM
```

**字段说明**：
1. `timestamp` — 第一个方括号中的时间（格式：`DDD MMM DD HH:MM:SS YYYY`）
2. `level` — 第二个方括号中的日志级别（error / notice / warn）
3. `content` — 日志级别之后的完整文本

**可选字段**（由教案定义提取规则）：
- `module`：从教师给定的模块词表中识别（如 `mod_jk`、`mod_jk2`、`workerEnv`、`jk2_init`、`mod_security`、`mod_python`、`LDAP`、`env`、`config`、`uriMap` 等）
- `error_code`：仅提取 `error state N` 中的数字 N（日志中约 4,349 处，N 范围 1-10）

### Linux.log（可选扩展数据）

| 属性 | 说明 |
|------|------|
| **来源系统** | Linux（combo 服务器） |
| **日志类型** | 系统日志（syslog 格式） |
| **压缩包** | `Linux.tar.gz` |
| **行数** | 约 25,567 行 |

**日志格式**：
```
Jun  9 06:06:20 combo syslogd 1.4.1: restart.
Jun 14 15:16:01 combo sshd(pam_unix)[19939]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4
```

**字段说明**：
1. `timestamp` — 时间戳（格式：`MMM DD HH:MM:SS`）
2. `hostname` — 主机名
3. `process` — 进程名（含PID）
4. `content` — 日志内容

> 注意：Linux.log 使用 syslog 格式，字段结构与 Apache.log 不同。可作为扩展/对比分析使用。

---

## 项目二：垃圾邮件数据集

### 数据来源

- **数据集名称**：Apache SpamAssassin Public Corpus
- **官方地址**：https://spamassassin.apache.org/old/publiccorpus/
- **维护者**：Apache SpamAssassin 项目
- **许可证**：Apache License 2.0

### 数据集概述

Apache SpamAssassin 公开语料库是垃圾邮件过滤研究的经典数据集，包含大量真实邮件，按类型分为 **正常邮件（ham）** 和 **垃圾邮件（spam）** 两类。

### 文件列表

| 文件名 | 类型 | 日期 | 说明 |
|--------|------|------|------|
| `20030228_easy_ham.tar.bz2` | Ham（正常邮件） | 2003-02-28 | 容易识别的正常邮件，2,501 封 |
| `20030228_easy_ham_2.tar.bz2` | Ham（正常邮件） | 2003-02-28 | 第二批容易识别的正常邮件，1,401 封 |
| `20030228_hard_ham.tar.bz2` | Ham（困难邮件） | 2003-02-28 | 难以区分的正常邮件（含特殊格式），251 封 |
| `20030228_spam.tar.bz2` | Spam（垃圾邮件） | 2003-02-28 | 垃圾邮件样本，501 封 |
| `20030228_spam_2.tar.bz2` | Spam（垃圾邮件） | 2003-02-28 | 第二批垃圾邮件样本，1,398 封 |
| `20050311_spam_2.tar.bz2` | Spam（垃圾邮件） | 2005-03-11 | 更新的垃圾邮件样本，1,397 封 |

### 数据格式

- **压缩格式**：`.tar.bz2`（需用 `tar -xjf` 解压）
- **邮件格式**：标准 RFC 2822 邮件格式（含邮件头 + 正文）
- **编码**：每封邮件为独立文件，文件名为邮件的 SHA1 哈希值

**解压命令**：
```bash
# 解压单个文件
tar -xjf 20030228_easy_ham.tar.bz2

# 解压所有文件
for f in *.tar.bz2; do tar -xjf "$f"; done
```

### 邮件结构示例

```
From: sender@example.com
To: recipient@example.com
Subject: Special offer just for you!
Date: Mon, 28 Feb 2003 10:15:00 -0500
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8

Congratulations! You have been selected to receive a FREE gift card...
```

**邮件头字段说明**：
| 字段 | 说明 |
|------|------|
| `From` | 发件人地址 |
| `To` | 收件人地址 |
| `Subject` | 邮件主题 |
| `Date` | 发送时间 |
| `MIME-Version` | MIME 版本 |
| `Content-Type` | 内容类型和编码 |

### easy_ham vs hard_ham 的区别

| 类型 | 特点 | 示例 |
|------|------|------|
| **easy_ham** | 格式规范、特征明显，容易与spam区分 | 正常的工作邮件、通知邮件 |
| **hard_ham** | 含特殊格式（HTML、附件、转发），容易被误判为spam | 邮件列表、自动通知、含链接的邮件 |

### 使用建议

1. **数据合并**：将所有 ham 合并为一类，所有 spam 合并为一类
2. **训练/测试分割**：建议 80% 训练、20% 测试（`random_state=42`）
3. **类别平衡**：ham 4,153 / spam 3,296，spam 约占 44%，类别较平衡
4. **文本清洗**：需要去除邮件头（可保留 Subject 行）、HTML 标签、特殊编码

**Python 加载示例**：
```python
import os
import email

def load_emails(directory):
    """加载目录中的所有邮件"""
    emails = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                msg = email.message_from_string(f.read())
                emails.append({
                    'subject': msg['Subject'] or '',
                    'from': msg['From'] or '',
                    'body': get_body(msg),
                    'label': 'spam' if 'spam' in directory else 'ham'
                })
    return emails
```

---

## 课程交付物清单一致性要求

本 `data/README.md` 主要说明数据集，但学生最终提交作业时，**交付物清单必须与 `project1/`、`project2/` 中的作业要求文件和课件保持一致**：

- 项目一以 `data/project1/项目一_Apache日志分析_作业要求与评分标准_精简版.md` 和 S4 课件“完整交付物清单”为准；
- 项目二以 `data/project2/项目二_垃圾邮件过滤_作业要求与评分标准_精简版.md` 和 S7 课件“完整交付物清单”为准；
- 不要自行新增、删除或重命名必交文件；
- 不再单独提交 `prd.md`、`design.md`、`dev.md`，相关需求、设计、任务和变更记录应合并到 `spec.md`；
- `spec.md` 与 `test-strategy.md` 最终状态应更新为 **Final Approved**；
- `analysis_report.md` 中的数字、图表和结论必须来自实际输出；
- `AI-log.md` 至少记录 3 条关键 AI 协作 Session，每课时至少 1 条，且必须包含人工判断和验证证据。

### Project 1 最终交付目录

项目一最终提交应组织为如下结构，与 `project1/` 作业要求和 S4 课件保持一致：

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

Project 1 的交付重点：

| 类别 | 必交内容 |
|------|----------|
| 代码与测试 | `log_analyzer/`、`tests/`、`main.py`、3 个 lesson 脚本 |
| 数据与结果 | `outputs/structured_logs.csv`、三类异常筛选 CSV、`error_code_reference.csv` |
| 图表 | `charts/daily_error_trend.png`、`charts/error_type_distribution.png`、`charts/module_error_comparison.png` |
| 文档 | `spec.md`、`test-strategy.md`、`AI-log.md`、`README.md`、`analysis_report.md` |

### Project 2 最终交付目录

项目二最终提交应组织为如下结构，与 `project2/` 作业要求和 S7 课件保持一致：

```text
project2/
├── spec.md
├── test-strategy.md
├── AI-log.md
├── README.md
├── main.py
├── example.py
├── lesson1_数据探索与清洗.py
├── lesson2_特征提取与分类.py
├── lesson3_评估与报告.py
├── outputs/
│   └── cleaned_data.csv
├── spam_filter/
│   ├── __init__.py
│   ├── text_cleaner.py
│   ├── feature_extractor.py
│   ├── rule_filter.py
│   ├── naive_bayes.py
│   ├── evaluator.py
│   ├── utils.py
│   └── README.md
├── tests/
│   ├── test_text_cleaner.py
│   ├── test_feature_extractor.py
│   ├── test_rule_filter.py
│   ├── test_evaluator.py
│   └── test_integration.py
├── charts/
│   ├── rule_confusion_matrix.png
│   ├── nb_confusion_matrix.png
│   ├── model_metrics_comparison.png
│   └── word_frequency_comparison.png
└── analysis_report.md
```

Project 2 的交付重点：

| 类别 | 必交内容 |
|------|----------|
| 代码与测试 | `spam_filter/`、`tests/`、`main.py`、`example.py`、3 个 lesson 脚本 |
| 数据与结果 | `outputs/cleaned_data.csv`，必须保留 `raw_message` 与 `cleaned_message` |
| 图表 | `charts/rule_confusion_matrix.png`、`charts/nb_confusion_matrix.png`、`charts/model_metrics_comparison.png`、`charts/word_frequency_comparison.png` |
| 文档 | `spec.md`、`test-strategy.md`、`AI-log.md`、`README.md`、`analysis_report.md` |

### 一致性检查建议

提交前请逐项核对：

1. `project1/`、`project2/` 根目录是否均包含 `spec.md`、`test-strategy.md`、`AI-log.md`、`README.md`、`main.py` 和 `analysis_report.md`；
2. 代码包目录是否分别为 `log_analyzer/` 与 `spam_filter/`，不要混用命名；
3. 测试文件是否与课件中的测试清单一致；
4. 输出文件是否放入 `outputs/`，图表是否放入 `charts/`；
5. 报告中的数据是否能从 `outputs/` 和 `charts/` 追溯；
6. `spec.md`、`test-strategy.md`、课堂 PPT、`project1/` 和 `project2/` 的交付物命名是否一致。

---

## 参考链接

| 资源 | 链接 |
|------|------|
| LogHub 日志数据集仓库 | https://github.com/logpai/loghub |
| Apache 日志 | https://github.com/logpai/loghub/tree/master/Apache |
| Linux 系统日志 | https://github.com/logpai/loghub/tree/master/Linux |
| SpamAssassin 公开语料库 | https://spamassassin.apache.org/old/publiccorpus/ |
| SpamAssassin 项目主页 | https://spamassassin.apache.org/ |
| LogHub 论文（arXiv） | https://arxiv.org/abs/2008.06448 |
