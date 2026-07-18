# 技术设计文档

## 架构概述

### 技术栈

- **语言**：Python 3.10+
- **虚拟环境**：.venv
- **核心库**：pandas、scikit-learn、matplotlib
- **测试框架**：pytest
- **运行方式**：CLI脚本

### 运行方式

采用CLI脚本运行，支持两种模式：

1. **分步运行**：3个脚本对应3个Lesson
   - `python src/lesson1.py` - 数据探索与清洗
   - `python src/lesson2.py` - 特征提取与分类
   - `python src/lesson3.py` - 评估与报告

2. **一键运行**：1个总脚本顺序执行3个步骤
   - `python src/run_all.py` - E2E全流程

---

## 目录结构

```
project2/
├── README.md                    # 项目说明文档
├── CLAUDE.md                    # 项目指令与技术验证记录
├── HANDOFF.md                   # 项目交接文档
├── requirements.txt             # Python 依赖清单
├── .venv/                       # 虚拟环境
├── data/                        # 原始数据（只读）
│   ├── easy_ham/                # 正常邮件（2,501条）
│   ├── easy_ham_2/              # 正常邮件第二批（1,401条）
│   ├── hard_ham/                # 难分类正常邮件（251条）
│   ├── spam/                    # 垃圾邮件（501条）
│   └── spam_2/                  # 垃圾邮件第二批（1,398条）
├── src/                         # 源代码
│   ├── __init__.py
│   ├── lesson1.py               # Lesson 1：数据探索与清洗
│   ├── lesson2.py               # Lesson 2：特征提取与分类
│   ├── lesson3.py               # Lesson 3：评估与报告
│   ├── run_all.py               # E2E全流程脚本
│   ├── text_cleaner.py          # 文本清洗模块
│   ├── feature_extractor.py     # 特征提取模块
│   ├── rule_filter.py           # 规则过滤器模块
│   ├── naive_bayes.py           # 朴素贝叶斯模块
│   ├── evaluator.py             # 评估模块
│   └── utils.py                 # 工具函数
├── tests/                       # 测试文件（28个用例）
│   ├── test_utils.py            # 数据加载测试（2个）
│   ├── test_text_cleaner.py     # 文本清洗测试（5个）
│   ├── test_feature_extractor.py # 特征提取测试（5个）
│   ├── test_rule_filter.py      # 规则过滤器测试（5个）
│   ├── test_naive_bayes.py      # 朴素贝叶斯测试（5个）
│   └── test_evaluator.py        # 评估模块测试（6个）
├── output/                      # 输出目录
│   ├── cleaned_data.csv         # 清洗后的数据（6052条）
│   ├── predictions.csv          # 预测结果
│   ├── analysis_report.md       # 分析报告
│   └── charts/                  # 可视化图表
│       ├── rule_confusion_matrix.png
│       ├── nb_confusion_matrix.png
│       ├── performance_comparison.png
│       └── word_frequency.png
└── docs/                        # 文档目录
    ├── ai-log.md                # AI协作记录
    ├── prd.md                   # 产品需求文档
    ├── design.md                # 技术设计文档
    ├── dev.md                   # 开发文档
    ├── test-strategy.md         # 测试策略文档
    └── 作业要求.md              # 原始作业要求
```

---

## 模块设计

### 1. utils.py - 工具函数模块

**职责**：提供通用工具函数

**接口**：
```python
def load_emails(data_dir: str) -> pd.DataFrame:
    """
    加载所有邮件

    返回DataFrame，包含列：
    - label: ham/spam
    - raw_email: 原始邮件内容
    - source: 来源目录
    """
    pass
```

### 2. text_cleaner.py - 文本清洗模块

**职责**：提供可复用的文本清洗功能

**接口**：
```python
def parse_email(filepath: str) -> dict:
    """
    从文件路径解析邮件（用于测试）

    返回dict：
    - from: 发件人
    - subject: 主题
    - body: 正文
    - content_type: 内容类型
    """
    pass

def parse_email_from_raw(raw_email: str) -> str:
    """
    从原始邮件内容提取正文（用于数据流）

    Args:
        raw_email: 原始邮件内容（含邮件头）

    Returns:
        str: 邮件正文
    """
    pass

def clean_text(text: str) -> str:
    """
    清洗文本（9步）

    1. 转小写
    2. 去除HTML标签
    3. 去除URL链接
    4. 去除邮箱地址
    5. 去除电话号码
    6. 去除特殊符号和标点
    7. 去除多余空格
    8. 去除停用词
    9. 过滤空消息
    """
    pass
```

### 3. feature_extractor.py - 特征提取模块

**职责**：从清洗文本中提取特征

**接口**：
```python
def extract_features(text: str) -> dict:
    """
    提取6个维度的特征

    特征：
    1. length: 消息长度（字符数）
    2. uppercase_ratio: 大写字母占比
    3. exclamation_count: 感叹号数量
    4. keyword_match: 关键词匹配数量
    5. digit_count: 数字数量
    6. currency_symbol: 货币符号数量
    """
    pass

def extract_features_batch(texts: list) -> pd.DataFrame:
    """批量提取特征，返回DataFrame"""
    pass
```

### 4. rule_filter.py - 规则过滤器模块

**职责**：基于规则判断spam/ham

**接口**：
```python
class RuleFilter:
    def __init__(self, weights: dict = None, threshold: float = None):
        """
        初始化规则过滤器

        默认权重：
        - length: 0.01
        - uppercase_ratio: 10
        - exclamation_count: 2
        - keyword_match: 5
        - digit_count: 0.1
        - currency_symbol: 3

        默认阈值：15
        """
        pass

    def predict(self, features: dict) -> str:
        """预测单个样本，返回 'ham' 或 'spam'"""
        pass

    def predict_batch(self, features_df: pd.DataFrame) -> list:
        """批量预测"""
        pass
```

### 5. naive_bayes.py - 朴素贝叶斯模块

**职责**：使用朴素贝叶斯分类

**接口**：
```python
class NaiveBayesClassifier:
    def __init__(self):
        """初始化分类器，使用CountVectorizer + MultinomialNB"""
        pass

    def train(self, texts: list, labels: list):
        """训练模型"""
        pass

    def predict(self, text: str) -> str:
        """预测单个样本"""
        pass

    def predict_batch(self, texts: list) -> list:
        """批量预测"""
        pass
```

### 6. evaluator.py - 评估模块

**职责**：计算评估指标和生成报告

**接口**：
```python
def calculate_metrics(y_true: list, y_pred: list) -> dict:
    """
    计算评估指标

    返回：
    - accuracy: 准确率
    - precision: 精确率
    - recall: 召回率
    - f1: F1值
    - confusion_matrix: 混淆矩阵
    """
    pass

def plot_confusion_matrix(y_true: list, y_pred: list, save_path: str):
    """绘制混淆矩阵热力图"""
    pass

def plot_performance_comparison(metrics1: dict, metrics2: dict, save_path: str):
    """绘制性能对比柱状图"""
    pass

def plot_word_frequency(texts: list, labels: list, save_path: str):
    """绘制词频分布图"""
    pass

def generate_report(df: pd.DataFrame, rule_metrics: dict, nb_metrics: dict, save_path: str):
    """
    生成分析报告

    Args:
        df: 包含预测结果的DataFrame
        rule_metrics: 规则过滤器的评估指标
        nb_metrics: 朴素贝叶斯的评估指标
        save_path: 报告保存路径
    """
    pass
```

---

## 数据流设计

### Lesson 1 数据流

```
data/ (原始邮件)
    ↓
load_emails() → DataFrame[label, raw_email, source]
    ↓
parse_email_from_raw() → DataFrame[label, raw_email, source, body]
    ↓
clean_text() → DataFrame[label, raw_email, source, body, cleaned_text]
    ↓
save → output/cleaned_data.csv
```

### Lesson 2 数据流

```
output/cleaned_data.csv
    ↓
extract_features_batch() → DataFrame[label, feature1, feature2, ..., feature6]
    ↓
RuleFilter.predict_batch() → DataFrame[label, features..., rule_pred]
    ↓
NaiveBayesClassifier.predict_batch() → DataFrame[label, features..., rule_pred, nb_pred]
    ↓
save → output/predictions.csv
```

### Lesson 3 数据流

```
output/predictions.csv
    ↓
calculate_metrics() → metrics_dict
    ↓
plot_*() → output/charts/*.png
    ↓
generate_report() → output/analysis_report.md
```

---

## 接口契约

### 输入格式

**原始邮件**：完整电子邮件格式（含邮件头）

**清洗后数据**：CSV格式
```csv
label,source,body,cleaned_text
ham,easy_ham,"Go until jurong point...","go jurong point crazy available bugis n great world la e buffet"
spam,spam,"Free entry in 2 a wkly comp...","free entry 2 wkly comp win fa cup final tkts 21st may 2005"
```

**特征数据**：CSV格式
```csv
label,source,body,cleaned_text,rule_pred,nb_pred
ham,easy_ham,"Go until jurong point...","go jurong point...",ham,ham
spam,spam,"Free entry...","free entry...",spam,spam
```

### 输出格式

**评估指标**：字典格式
```python
{
    "accuracy": 0.9678,
    "precision": 0.9728,
    "recall": 0.9231,
    "f1": 0.9473,
    "confusion_matrix": [[4104, 49], [146, 1753]]
}
```

---

## 错误处理策略

### 1. 邮件解析异常
- **策略**：跳过无法解析的邮件，记录日志
- **原因**：少数邮件格式异常不影响整体结果

### 2. 特征提取异常
- **策略**：使用默认值（0或空）
- **原因**：保证特征矩阵完整性

### 3. 分类器训练异常
- **策略**：检查数据格式，抛出明确错误
- **原因**：训练数据必须符合要求

---

## 技术选型说明

### 1. 为什么用CLI而不是Web界面？
- CLI最简洁，便于验收
- 无需额外依赖（Flask、FastAPI等）
- 便于脚本化和自动化

### 2. 为什么分3个脚本 + 1个总脚本？
- 分步运行便于调试和验证
- 总脚本便于一键运行和演示
- 符合作业要求的3个Lesson结构

### 3. 为什么用.venv而不是conda？
- Python原生支持，无需额外安装
- 轻量级，适合小型项目
- 便于依赖管理

### 4. 为什么代码放src目录？
- 包管理清晰，代码不散落
- 便于import和测试
- 符合Python项目最佳实践

### 5. 为什么用SpamAssassin而不是SMS Spam Collection？
- 老师提供的唯一数据集
- 数据量更大（6052 vs 5574）
- 更接近真实邮件场景

---

## 性能指标

### 模型性能

| 分类器 | 准确率 | 精确率 | 召回率 | F1值 |
|--------|--------|--------|--------|------|
| 规则过滤器 | 68.32% | 49.69% | 76.78% | 60.34% |
| 朴素贝叶斯 | **96.78%** | **97.28%** | **92.31%** | **94.73%** |

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
