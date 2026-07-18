# Project 2 测试策略

- 状态：Final Approved（2026-07-15 全量验收通过）
- 核心：数据契约、泄漏边界和误判成本优先于单一 Accuracy

## 1. 分层与边界

| 层级 | 正常 | 边界/失败 |
|---|---|---|
| 邮件解析 | Subject + text/plain | HTML、普通头排除、附件排除、坏编码 |
| 清洗 | URL/邮箱/电话/符号 | None、空白、全停用词、script/style |
| 特征 | 六类精确值 | 无字母、大长文、`carefree` 不误中 `free` |
| 规则 | 明显 spam/ham | 长度单项不支配、阈值边界 |
| NB | fit/predict Smoke | 未 fit 抛错、fit 样本数等于训练集 |
| 指标 | 四指标与矩阵 | 无正预测时不除零、正类固定 spam |
| 全量 | 7,449 样本 | parse warning、空 cleaned、门槛与 FP/FN |

## 2. 验收映射

| AC | 证据 |
|---|---|
| P2-AC1/2 | `tests/test_text_cleaner.py` + 全量总数/列检查 |
| P2-AC3 | `tests/test_feature_extractor.py`、`test_rule_filter.py` |
| P2-AC4 | `tests/test_integration.py` 与报告训练/测试数量 |
| P2-AC5 | `tests/test_evaluator.py` + CSV/报告复算 |
| P2-AC6 | 最终文件清单与图像可读性检查 |

## 3. 固定实验协议

先切分行索引，再仅对训练 cleaned 文本 fit Vectorizer；测试标签不进入特征或训练。规则与 NB 使用同一 `test_indices`。最终测试集只运行验收，不按结果反复调整参数。

## 4. 命令

```bash
../.venv/bin/python -m pytest tests -q
../.venv/bin/python main.py --data-dir ../../day4-data/project2
../.venv/bin/python example.py
```

实际样本数、指标、失败与复测写入仓库 `docs/test-record.md`。
