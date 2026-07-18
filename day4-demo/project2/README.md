# 垃圾邮件智能过滤工具

> 基于 SpamAssassin 数据集的垃圾邮件分类工具，支持规则过滤和朴素贝叶斯两种分类方法

## 项目概述

本项目实现了一个垃圾邮件智能过滤工具，使用两种分类方法进行对比实验：
- **规则过滤器**：基于6维手工特征的加权评分分类
- **朴素贝叶斯分类器**：基于词频统计的概率分类

在 SpamAssassin 数据集（6052条邮件）上，朴素贝叶斯分类器达到 **96.78% 准确率** 和 **0.9473 F1值**，显著优于规则过滤器。

---

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd project2

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境（Windows）
.venv\Scripts\activate

# 激活虚拟环境（Linux/Mac）
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 运行方式

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

### 3. 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_utils.py -v
```

---

## 项目结构

```
project2/
├── README.md                    # 本文件
├── CLAUDE.md                    # 项目指令与技术验证记录
├── HANDOFF.md                   # 项目交接文档
├── requirements.txt             # Python 依赖清单
├── data/                        # 原始数据集（SpamAssassin）
│   ├── easy_ham/                # 正常邮件（2,501条）
│   ├── easy_ham_2/              # 正常邮件第二批（1,401条）
│   ├── hard_ham/                # 难分类正常邮件（251条）
│   ├── spam/                    # 垃圾邮件（501条）
│   └── spam_2/                  # 垃圾邮件第二批（1,398条）
├── src/                         # 源代码
│   ├── __init__.py
│   ├── utils.py                 # 数据加载模块
│   ├── text_cleaner.py          # 文本清洗模块（9步流水线）
│   ├── feature_extractor.py     # 特征提取模块（6维）
│   ├── rule_filter.py           # 规则过滤器模块
│   ├── naive_bayes.py           # 朴素贝叶斯分类器模块
│   ├── evaluator.py             # 评估与可视化模块
│   ├── lesson1.py               # Lesson 1：数据加载与清洗
│   ├── lesson2.py               # Lesson 2：特征提取与分类
│   ├── lesson3.py               # Lesson 3：评估与报告
│   └── run_all.py               # E2E 全流程脚本
├── tests/                       # 测试文件（28个用例）
│   ├── test_utils.py            # 数据加载测试（2个）
│   ├── test_text_cleaner.py     # 文本清洗测试（5个）
│   ├── test_feature_extractor.py # 特征提取测试（5个）
│   ├── test_rule_filter.py      # 规则过滤器测试（5个）
│   ├── test_naive_bayes.py      # 朴素贝叶斯测试（5个）
│   └── test_evaluator.py        # 评估模块测试（6个）
├── output/                      # 输出文件
│   ├── cleaned_data.csv         # 清洗后的数据集（6052条）
│   ├── predictions.csv          # 预测结果（含 rule_pred 和 nb_pred）
│   ├── analysis_report.md       # 分析报告（含图表引用）
│   └── charts/                  # 可视化图表
│       ├── rule_confusion_matrix.png   # 规则过滤器混淆矩阵
│       ├── nb_confusion_matrix.png     # 朴素贝叶斯混淆矩阵
│       ├── performance_comparison.png  # 性能对比柱状图
│       └── word_frequency.png          # 词频分布图
└── docs/                        # 项目文档
    ├── prd.md                   # 产品需求文档
    ├── design.md                # 技术设计文档
    ├── dev.md                   # 开发文档
    ├── test-strategy.md         # 测试策略文档
    ├── ai-log.md                # AI 协作记录
    └── 作业要求.md              # 原始作业要求
```

---

## 数据集

**数据集**：SpamAssassin 公共语料库

| 类型 | 数量 | 占比 |
|------|------|------|
| ham（正常邮件） | 4,153条 | 68.6% |
| spam（垃圾邮件） | 1,899条 | 31.4% |
| **总计** | **6,052条** | 100% |

**目录分布**：
- `easy_ham/`：2,501条（正常邮件，容易分类）
- `easy_ham_2/`：1,401条（正常邮件第二批）
- `hard_ham/`：251条（难分类正常邮件）
- `spam/`：501条（垃圾邮件）
- `spam_2/`：1,398条（垃圾邮件第二批）

---

## 核心功能

### 1. 文本清洗（9步）

1. 转小写 → 2. 去除HTML标签 → 3. 去除URL → 4. 去除邮箱 → 5. 去除电话 → 6. 去除特殊符号 → 7. 去除多余空格 → 8. 去除停用词 → 9. 过滤空消息

### 2. 特征提取（6维）

| 特征 | 说明 |
|------|------|
| length | 消息长度（字符数） |
| uppercase_ratio | 大写字母占比（从原始文本提取） |
| exclamation_count | 感叹号数量 |
| keyword_match | 垃圾关键词匹配数 |
| digit_count | 数字数量 |
| currency_symbol | 货币符号数量 |

### 3. 分类方法

- **规则过滤器**：特征加权求和，阈值判定
- **朴素贝叶斯**：CountVectorizer + MultinomialNB

---

## 模型性能

| 分类器 | 准确率 | 精确率 | 召回率 | F1值 |
|--------|--------|--------|--------|------|
| 规则过滤器 | 68.32% | 49.69% | 76.78% | 60.34% |
| **朴素贝叶斯** | **96.78%** | **97.28%** | **92.31%** | **94.73%** |

### 混淆矩阵

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

## 测试结果

### 单元测试

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

======================= 28 passed in 3.65s ========================
```

---

## 已知限制

1. **规则过滤器性能有限**：仅使用6维手工特征，难以捕捉复杂模式
2. **朴素贝叶斯假设**：特征条件独立假设在实际中不完全成立
3. **数据集年代**：SpamAssassin 数据集为 2002-2005 年，与现代垃圾邮件特征可能有差异
4. **未使用交叉验证**：当前评估基于全量数据训练和测试，可能存在过拟合

---

## 改进建议

1. **特征工程优化**
   - 引入 TF-IDF 替代简单的词频统计
   - 添加 n-gram 特征捕捉词序信息
   - 提取邮件头部特征（发件人域名、邮件路径等）

2. **算法升级**
   - 尝试 SVM（支持向量机）处理高维特征
   - 使用集成方法（随机森林、XGBoost）
   - 探索深度学习方法（LSTM、BERT）

3. **模型调优**
   - 进行超参数网格搜索
   - 使用交叉验证评估模型稳定性
   - 调整类别权重处理不平衡问题

4. **工程化改进**
   - 实现增量学习，适应新的垃圾邮件模式
   - 添加用户反馈机制，持续优化模型
   - 部署为实时过滤服务

---

## 作业要求文件对应关系

| 作业要求文件 | 实际位置 | 说明 |
|-------------|----------|------|
| `lesson1_数据探索与清洗.py` | `src/lesson1.py` | 数据加载、探索、清洗脚本 |
| `lesson2_特征提取与分类.py` | `src/lesson2.py` | 特征提取、规则过滤、朴素贝叶斯 |
| `lesson3_评估与报告.py` | `src/lesson3.py` | 评估、可视化、工具库演示 |
| `text_cleaner.py` | `src/text_cleaner.py` | 可复用的文本清洗模块 |
| `feature_extractor.py` | `src/feature_extractor.py` | 特征提取模块 |
| `rule_filter.py` | `src/rule_filter.py` | 规则过滤器模块 |
| `naive_bayes.py` | `src/naive_bayes.py` | 朴素贝叶斯分类模块 |
| `spam_filter/` 工具库 | `src/` | 整合的工具库（含所有模块） |
| `cleaned_data.csv` | `output/cleaned_data.csv` | 清洗后的数据集 |
| `charts/` | `output/charts/` | 可视化图表（6张PNG） |
| `analysis_report.md` | `output/analysis_report.md` | 分析报告 |

---

## 文档

| 文档 | 说明 |
|------|------|
| [CLAUDE.md](CLAUDE.md) | 项目指令与技术验证记录 |
| [HANDOFF.md](HANDOFF.md) | 项目交接文档 |
| [docs/prd.md](docs/prd.md) | 产品需求文档 |
| [docs/design.md](docs/design.md) | 技术设计文档 |
| [docs/dev.md](docs/dev.md) | 开发文档 |
| [docs/test-strategy.md](docs/test-strategy.md) | 测试策略文档 |
| [docs/ai-log.md](docs/ai-log.md) | AI 协作记录 |
| [output/analysis_report.md](output/analysis_report.md) | 分析报告 |

---

## 开发环境

- **Python**：3.10+
- **依赖管理**：pip + requirements.txt
- **虚拟环境**：.venv
- **测试框架**：pytest
- **核心库**：pandas、scikit-learn、matplotlib

---

## 许可证

本项目仅用于学习目的。

---

## 联系方式

如有问题，请参考：
- `CLAUDE.md`：项目技术细节和决策记录
- `docs/ai-log.md`：AI 协作过程记录
- `output/analysis_report.md`：完整分析报告

---

*文档生成时间：2026-06-25*
