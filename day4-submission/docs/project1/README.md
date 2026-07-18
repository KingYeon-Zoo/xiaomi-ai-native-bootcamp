# Project 1：Apache 日志智能清洗与故障分析

## 环境与安装

从 `day4-submission/` 根目录执行：

```bash
python3.10 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## 运行

课程数据位于训练营工作区相邻的 `day4-data/` 时：

```bash
cd project1
../.venv/bin/python main.py --archive ../../day4-data/project1/Apache.tar.gz
```

也支持已解压日志：

```bash
../.venv/bin/python main.py --log /path/to/Apache.log
```

## 测试

```bash
cd project1
../.venv/bin/python -m pytest tests -q
```

## 输出

五个 CSV 位于 `outputs/`，三张图位于 `charts/`，结论与限制位于 `analysis_report.md`。原始数据不进入 Git；缺失时入口会给出明确参数提示。

## 限制

只支持题目规定的 Apache 格式；模块依赖固定词表；报告的故障原因是待运维证据确认的推测，不是自动根因证明。
