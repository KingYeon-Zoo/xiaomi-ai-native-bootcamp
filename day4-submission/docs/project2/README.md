# Project 2：垃圾邮件智能过滤工具

## 环境与安装

从 `day4-submission/` 根目录执行：

```bash
python3.10 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## 运行

```bash
cd project2
../.venv/bin/python main.py --data-dir ../../day4-data/project2
```

程序要求目录中恰有六个课程 `tar.bz2`；直接从压缩包读取，不需要预先解压。最小规则示例：

```bash
../.venv/bin/python example.py
```

## 测试

```bash
cd project2
../.venv/bin/python -m pytest tests -q
```

## 输出

- `outputs/cleaned_data.csv`：保留 label、source、message_id、raw_message、cleaned_message、split。
- `charts/`：规则/NB 混淆矩阵、指标对比、高频词对比。
- `analysis_report.md`：真实指标、FP/FN、泄漏检查和限制。

## 限制

语料年代较早；不解析附件图像；随机切分不能证明跨时间泛化。规则是可解释基线，不以测试集调参追求门槛。
