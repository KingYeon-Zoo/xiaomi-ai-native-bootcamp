# 开发任务清单

> 供Agent按部就班执行。每个任务独立可验证，完成验证后才能继续下一个。
> 遇到重大决策问题、环境问题等阻塞问题时，立刻停下来和用户讨论。

---

## 任务总览

| 任务 | 名称 | 状态 | 验证方式 |
|------|------|------|----------|
| 1 | 环境搭建与项目结构 | ✅ | 环境可用，目录正确 |
| 2 | 数据加载与文本清洗 | ✅ | cleaned_data.csv生成 |
| 3 | 特征提取与规则过滤 | ✅ | 规则过滤器能预测 |
| 4 | 朴素贝叶斯与评估 | ✅ | 两种分类器都能工作 |
| 5 | E2E整合与报告 | ✅ | 全流程运行成功 |

---

## 任务 1：环境搭建与项目结构

**目标**：搭建开发环境，创建项目目录结构

**状态**：✅ 已完成

**步骤**：
1. 创建虚拟环境
   ```bash
   python -m venv .venv
   ```

2. 激活虚拟环境
   ```bash
   # Windows
   .venv\Scripts\activate
   ```

3. 安装依赖
   ```bash
   pip install pandas scikit-learn matplotlib pytest
   ```

4. 创建目录结构
   ```bash
   mkdir -p src
   mkdir -p output/charts
   mkdir -p tests
   ```

5. 生成requirements.txt
   ```bash
   pip freeze > requirements.txt
   ```

6. 创建 `src/__init__.py`

**验证结果**：
- [x] 虚拟环境可用
- [x] 依赖安装成功
- [x] 目录结构正确
- [x] requirements.txt生成

---

## 任务 2：数据加载与文本清洗

**目标**：实现数据加载、邮件解析、文本清洗，生成 cleaned_data.csv

**状态**：✅ 已完成

**步骤**：

### 2.1 创建 `src/utils.py`

实现数据加载功能：
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

### 2.2 创建 `src/text_cleaner.py`

实现邮件解析和文本清洗：
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

### 2.3 创建 `src/lesson1.py`

实现完整流程：
```python
def main():
    # 1. 加载所有邮件
    df = load_emails('data')

    # 2. 解析邮件正文
    df['body'] = df['raw_email'].apply(parse_email_from_raw)

    # 3. 清洗文本
    df['cleaned_text'] = df['body'].apply(clean_text)

    # 4. 保存到CSV
    df[['label', 'source', 'body', 'cleaned_text']].to_csv('output/cleaned_data.csv', index=False)
```

### 2.4 创建测试文件

创建 `tests/test_utils.py` 和 `tests/test_text_cleaner.py`

**验证结果**：
- [x] 所有测试通过（7个测试）
- [x] `output/cleaned_data.csv` 生成
- [x] CSV格式正确（label, source, body, cleaned_text）
- [x] 数据数量正确（6,052条）
- [x] 无异常错误

---

## 任务 3：特征提取与规则过滤

**目标**：实现特征提取和规则过滤器，能预测spam/ham

**状态**：✅ 已完成

**步骤**：

### 3.1 创建 `src/feature_extractor.py`

实现特征提取：
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
    """批量提取特征"""
    pass
```

### 3.2 创建 `src/rule_filter.py`

实现规则过滤器：
```python
class RuleFilter:
    def __init__(self, weights=None, threshold=None):
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

### 3.3 创建测试文件

创建 `tests/test_feature_extractor.py` 和 `tests/test_rule_filter.py`

**验证结果**：
- [x] 所有测试通过（10个测试）
- [x] 特征提取正确
- [x] 规则过滤器能预测
- [x] 规则过滤器准确率：68.32%

---

## 任务 4：朴素贝叶斯与评估

**目标**：实现朴素贝叶斯分类器和评估模块

**状态**：✅ 已完成

**步骤**：

### 4.1 创建 `src/naive_bayes.py`

实现朴素贝叶斯分类器：
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

### 4.2 创建 `src/evaluator.py`

实现评估功能：
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

### 4.3 创建测试文件

创建 `tests/test_naive_bayes.py` 和 `tests/test_evaluator.py`

**验证结果**：
- [x] 所有测试通过（11个测试）
- [x] 朴素贝叶斯能训练和预测
- [x] 评估指标能计算
- [x] 朴素贝叶斯准确率：96.78%（>95%）

---

## 任务 5：E2E整合与报告

**目标**：实现Lesson 3、E2E脚本，生成图表和报告

**状态**：✅ 已完成

**步骤**：

### 5.1 创建 `src/lesson3.py`

实现评估和可视化：
```python
def main():
    # 1. 加载预测结果
    df = pd.read_csv('output/predictions.csv')

    # 2. 计算评估指标
    rule_metrics = calculate_metrics(df['label'], df['rule_pred'])
    nb_metrics = calculate_metrics(df['label'], df['nb_pred'])

    # 3. 生成图表
    plot_confusion_matrix(df['label'], df['rule_pred'], 'output/charts/rule_confusion_matrix.png')
    plot_confusion_matrix(df['label'], df['nb_pred'], 'output/charts/nb_confusion_matrix.png')
    plot_performance_comparison(rule_metrics, nb_metrics, 'output/charts/performance_comparison.png')
    plot_word_frequency(df['cleaned_text'], df['label'], 'output/charts/word_frequency.png')

    # 4. 生成报告
    generate_report(df, rule_metrics, nb_metrics, 'output/analysis_report.md')
```

### 5.2 创建 `src/run_all.py`

实现E2E脚本：
```python
def main():
    print("=== 开始E2E测试 ===")

    # 1. 运行Lesson 1
    print("运行Lesson 1: 数据加载与清洗...")
    subprocess.run(['python', 'src/lesson1.py'], check=True)

    # 2. 运行Lesson 2
    print("运行Lesson 2: 特征提取与分类...")
    subprocess.run(['python', 'src/lesson2.py'], check=True)

    # 3. 运行Lesson 3
    print("运行Lesson 3: 评估与报告...")
    subprocess.run(['python', 'src/lesson3.py'], check=True)

    print("=== E2E测试完成 ===")
```

### 5.3 运行所有测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行E2E
python src/run_all.py
```

**验证结果**：
- [x] 所有测试通过（28个测试）
- [x] E2E脚本运行成功
- [x] 4张图表生成成功
- [x] 分析报告生成成功
- [x] 图表可读性良好
- [x] 报告内容完整（8个章节）

---

## 任务依赖关系

```
任务1 (环境搭建) ✅
    ↓
任务2 (数据加载与清洗) ✅
    ↓
任务3 (特征提取与规则过滤) ✅
    ↓
任务4 (朴素贝叶斯与评估) ✅
    ↓
任务5 (E2E整合与报告) ✅
```

---

## 决策记录

### 决策1：数据集选择

**决策**：使用SpamAssassin数据集

**原因**：
- 老师提供的唯一数据集
- 数据量更大（6052 vs 5574）
- 更接近真实邮件场景

### 决策2：评估指标

**决策**：不做硬性数字指标，流程跑通即可

**原因**：
- 作业要求是示例，不一定要一一对应
- 以当前数据集的实际表现为准
- 先运行基准模型，查看实际指标

### 决策3：验证标准

**决策**：流程跑通优先，人工检查图表和报告质量

**原因**：
- 图表质量、报告质量难以量化
- 人工检查更直观
- 先保证功能正确，再优化质量

### 决策4：任务粒度

**决策**：5个任务，每个任务独立可验证

**原因**：
- 任务太多会增加管理成本
- 任务太少会增加单个任务复杂度
- 5个任务是合理的平衡点

---

## 最终验收结果

### 代码功能
- [x] 能正确加载data目录中的所有邮件（6,052条）
- [x] 能提取邮件正文（去除邮件头）
- [x] 实现9步文本清洗流水线
- [x] 实现6个维度的特征提取
- [x] 实现规则过滤器，能分类spam/ham
- [x] 实现朴素贝叶斯分类器，能分类spam/ham
- [x] 计算混淆矩阵和评估指标
- [x] 生成4张可视化图表
- [x] 撰写完整的分析报告

### 模型性能
- [x] 规则过滤器准确率：68.32%
- [x] 朴素贝叶斯准确率：96.78%（>95%）
- [x] 朴素贝叶斯F1值：94.73%

### 测试结果
- [x] 28个单元测试全部通过
- [x] E2E脚本运行成功
- [x] 所有输出文件生成

### 文档完整性
- [x] `docs/prd.md` - 产品需求文档
- [x] `docs/design.md` - 技术设计文档
- [x] `docs/dev.md` - 开发文档
- [x] `docs/test-strategy.md` - 测试策略文档
- [x] `docs/ai-log.md` - AI协作记录
- [x] `README.md` - 项目说明文档
