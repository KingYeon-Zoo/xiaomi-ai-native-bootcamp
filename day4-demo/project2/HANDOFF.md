# 垃圾邮件智能过滤工具 - 项目交接文档

> **项目名称**：垃圾邮件智能过滤工具
> **交付日期**：2026-06-25
> **开发环境**：Python 3.12.10 + pandas + scikit-learn + matplotlib

---

## 1. 项目概述

本项目实现了一个垃圾邮件智能过滤工具，使用两种分类方法进行对比实验：
- **规则过滤器**：基于6维手工特征的加权评分分类
- **朴素贝叶斯分类器**：基于词频统计的概率分类

在 SpamAssassin 数据集（6052条邮件）上，朴素贝叶斯分类器达到 **96.78% 准确率** 和 **0.9473 F1值**，显著优于规则过滤器。

---

## 2. 交付物清单

### 2.1 源代码

| 文件 | 说明 | 行数 |
|------|------|------|
| `src/utils.py` | 数据加载模块 | ~60行 |
| `src/text_cleaner.py` | 邮件解析与文本清洗模块 | ~150行 |
| `src/feature_extractor.py` | 特征提取模块（6维） | ~90行 |
| `src/rule_filter.py` | 规则过滤器模块 | ~80行 |
| `src/naive_bayes.py` | 朴素贝叶斯分类器模块 | ~100行 |
| `src/evaluator.py` | 评估与可视化模块 | ~300行 |
| `src/lesson1.py` | Lesson 1：数据加载与清洗 | ~80行 |
| `src/lesson2.py` | Lesson 2：特征提取与分类 | ~100行 |
| `src/lesson3.py` | Lesson 3：评估与报告 | ~120行 |
| `src/run_all.py` | E2E 全流程脚本 | ~80行 |

### 2.2 测试文件

| 文件 | 测试用例数 | 说明 |
|------|-----------|------|
| `tests/test_utils.py` | 2 | 数据加载测试 |
| `tests/test_text_cleaner.py` | 5 | 文本清洗测试 |
| `tests/test_feature_extractor.py` | 5 | 特征提取测试 |
| `tests/test_rule_filter.py` | 5 | 规则过滤器测试 |
| `tests/test_naive_bayes.py` | 5 | 朴素贝叶斯测试 |
| `tests/test_evaluator.py` | 6 | 评估模块测试 |
| **合计** | **28** | **全部通过** |

### 2.3 输出文件

| 文件 | 说明 |
|------|------|
| `output/cleaned_data.csv` | 清洗后的数据集（6052条） |
| `output/predictions.csv` | 预测结果（含规则和NB预测） |
| `output/analysis_report.md` | 分析报告（含图表引用） |
| `output/charts/performance_comparison.png` | 性能对比柱状图 |
| `output/charts/rule_confusion_matrix.png` | 规则过滤器混淆矩阵 |
| `output/charts/nb_confusion_matrix.png` | 朴素贝叶斯混淆矩阵 |
| `output/charts/word_frequency.png` | 词频分布图 |

### 2.4 文档

| 文件 | 说明 |
|------|------|
| `CLAUDE.md` | 项目指令与技术验证记录 |
| `requirements.txt` | Python 依赖清单 |
| `docs/prd.md` | 产品需求文档 |
| `docs/design.md` | 技术设计文档 |
| `docs/dev.md` | 开发文档 |
| `docs/test-strategy.md` | 测试策略文档 |
| `docs/tasks.md` | 任务清单 |
| `docs/ai-log.md` | AI 协作记录 |

---

## 3. 快速开始

### 3.1 环境准备

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境（Windows）
.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 3.2 运行方式

**方式一：运行完整流程（推荐）**

```bash
python src/run_all.py
```

**方式二：分步运行**

```bash
# Step 1: 数据加载与清洗
python src/lesson1.py

# Step 2: 特征提取与分类
python src/lesson2.py

# Step 3: 评估与报告
python src/lesson3.py
```

### 3.3 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_utils.py -v
```

---

## 4. 测试结果

### 4.1 单元测试

```
============================= test session starts =============================
platform win32 -- Python 3.12.10

tests/test_evaluator.py::test_calculate_metrics PASSED
tests/test_evaluator.py::test_calculate_metrics_perfect PASSED
tests/test_evaluator.py::test_calculate_metrics_all_ham PASSED
tests/test_evaluator.py::test_plot_confusion_matrix PASSED
tests/test_evaluator.py::test_plot_performance_comparison PASSED
tests/test_evaluator.py::test_confusion_matrix_structure PASSED
tests/test_feature_extractor.py::test_extract_features PASSED
tests/test_feature_extractor.py::test_extract_features_empty PASSED
tests/test_feature_extractor.py::test_extract_features_batch PASSED
tests/test_feature_extractor.py::test_extract_features_ham PASSED
tests/test_feature_extractor.py::test_extract_features_spam PASSED
tests/test_naive_bayes.py::test_naive_bayes_train PASSED
tests/test_naive_bayes.py::test_naive_bayes_predict PASSED
tests/test_naive_bayes.py::test_naive_bayes_predict_batch PASSED
tests/test_naive_bayes.py::test_naive_bayes_not_trained PASSED
tests/test_naive_bayes.py::test_naive_bayes_feature_importance PASSED
tests/test_rule_filter.py::test_rule_filter_predict PASSED
tests/test_rule_filter.py::test_rule_filter_threshold PASSED
tests/test_rule_filter.py::test_rule_filter_weights PASSED
tests/test_rule_filter.py::test_rule_filter_batch PASSED
tests/test_rule_filter.py::test_rule_filter_score PASSED
tests/test_text_cleaner.py::test_parse_email PASSED
tests/test_text_cleaner.py::test_parse_email_from_raw PASSED
tests/test_text_cleaner.py::test_clean_text PASSED
tests/test_text_cleaner.py::test_clean_text_empty PASSED
tests/test_text_cleaner.py::test_html_to_text PASSED
tests/test_utils.py::test_load_emails PASSED
tests/test_utils.py::test_load_emails_content PASSED

======================= 28 passed in 4.90s ========================
```

### 4.2 模型性能

| 分类器 | 准确率 | 精确率 | 召回率 | F1值 |
|--------|--------|--------|--------|------|
| 规则过滤器 | 68.32% | 49.69% | 76.78% | 60.34% |
| 朴素贝叶斯 | **96.78%** | **97.28%** | **92.31%** | **94.73%** |

### 4.3 混淆矩阵

**规则过滤器**：
|  | 预测ham | 预测spam |
|--|---------|----------|
| 实际ham | 2677 | 1476 |
| 实际spam | 441 | 1458 |

**朴素贝叶斯**：
|  | 预测ham | 预测spam |
|--|---------|----------|
| 实际ham | 4104 | 49 |
| 实际spam | 146 | 1753 |

---

## 5. 项目结构

```
project2/
├── src/                        # 源代码
│   ├── __init__.py
│   ├── utils.py               # 数据加载
│   ├── text_cleaner.py        # 文本清洗（9步流水线）
│   ├── feature_extractor.py   # 特征提取（6维）
│   ├── rule_filter.py         # 规则过滤器
│   ├── naive_bayes.py         # 朴素贝叶斯
│   ├── evaluator.py           # 评估与可视化
│   ├── lesson1.py             # Lesson 1 脚本
│   ├── lesson2.py             # Lesson 2 脚本
│   ├── lesson3.py             # Lesson 3 脚本
│   └── run_all.py             # E2E 脚本
├── tests/                      # 测试文件（28个用例）
├── output/                     # 输出文件
│   ├── cleaned_data.csv       # 清洗后数据
│   ├── predictions.csv        # 预测结果
│   ├── analysis_report.md     # 分析报告
│   └── charts/                # 可视化图表
├── data/                       # 原始数据集
├── docs/                       # 项目文档
├── requirements.txt            # 依赖清单
├── CLAUDE.md                   # 项目指令
└── HANDOFF.md                  # 本文件
```

---

## 6. 核心功能说明

### 6.1 文本清洗（9步）

1. 转小写 → 2. 去除HTML标签 → 3. 去除URL → 4. 去除邮箱 → 5. 去除电话 → 6. 去除特殊符号 → 7. 去除多余空格 → 8. 去除停用词 → 9. 过滤空消息

### 6.2 特征提取（6维）

| 特征 | 说明 |
|------|------|
| length | 消息长度 |
| uppercase_ratio | 大写字母占比（从原始文本提取） |
| exclamation_count | 感叹号数量 |
| keyword_match | 垃圾关键词匹配数 |
| digit_count | 数字数量 |
| currency_symbol | 货币符号数量 |

### 6.3 分类方法

- **规则过滤器**：特征加权求和，阈值判定
- **朴素贝叶斯**：CountVectorizer + MultinomialNB

---

## 7. 已知限制

1. **规则过滤器性能有限**：仅使用6维手工特征，难以捕捉复杂模式
2. **朴素贝叶斯假设**：特征条件独立假设在实际中不完全成立
3. **数据集年代**：SpamAssassin 数据集为 2002-2005 年，与现代垃圾邮件特征可能有差异
4. **未使用交叉验证**：当前评估基于全量数据训练和测试，可能存在过拟合

---

## 8. 验收检查清单

- [x] 环境可正常搭建（`pip install -r requirements.txt`）
- [x] E2E 脚本可正常运行（`python src/run_all.py`）
- [x] 所有测试通过（`pytest tests/ -v`，28/28）
- [x] `cleaned_data.csv` 生成（6052条）
- [x] `predictions.csv` 生成（含 rule_pred 和 nb_pred）
- [x] 4张图表生成（混淆矩阵×2、性能对比、词频）
- [x] `analysis_report.md` 生成（含图表引用）
- [x] 两种分类器均可工作
- [x] 朴素贝叶斯准确率 > 95%
- [x] 报告内容完整（8个章节）

---

## 9. 联系方式

如有问题，请参考：
- `CLAUDE.md`：项目技术细节和决策记录
- `docs/ai-log.md`：AI 协作过程记录
- `output/analysis_report.md`：完整分析报告

---

*文档生成时间：2026-06-25*
