# 小米 AI Native 训练营 Day4 提交

本提交包含两个完整数据项目和一次 Agent 代码可信审查。实现没有沿用老师 Demo 的旧目录；文件名以 `day4-data/README.md` 的最终清单为准。

## 目录

```text
day4-submission/
├── project1/                 # Apache 日志分析
├── project2/                 # 垃圾邮件过滤
├── agent_review_report.md    # Project 3 唯一报告
├── docs/                     # 跨项目约束、任务、测试证据与反思
├── AGENTS.md
├── requirements.txt
└── pytest.ini
```

## 一次安装

要求 Python 3.10+。在本目录执行：

```bash
python3.10 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## 测试

```bash
.venv/bin/python -m pytest -q
```

## 运行与全量复现

原始课程数据不复制进提交仓库。若本仓库仍位于训练营工作区的 `day4-submission/`，执行：

```bash
(cd project1 && ../.venv/bin/python main.py --archive ../../day4-data/project1/Apache.tar.gz)
(cd project2 && ../.venv/bin/python main.py --data-dir ../../day4-data/project2)
```

若单独克隆本仓库，请下载题目 README 所列公开数据，并通过 `--archive` / `--data-dir` 指向本地路径。

## 证据导航

- 范围、设计、任务和变更：`project1/spec.md`、`project2/spec.md`
- 每课时 AI/人工判断：两个项目的 `AI-log.md`
- 测试实际结果：`docs/test-record.md`
- Agent 三维审查：`agent_review_report.md`
- 个人深度反思：`docs/reflection.md`
- 工程执行合同：`docs/engineering-constraints.md`

## 已知边界

Project 1 不覆盖可选 Linux.log；Project 2 不处理附件图像与现代分布漂移。报告严格区分实际数字、推测与限制。
