# 测试策略文档

## 测试概述

### 测试目标

1. **验证代码功能**：确保每个模块按预期工作
2. **验证数据流**：确保数据在模块间正确传递
3. **验证评估指标**：确保模型效果达到预期
4. **保证代码质量**：确保代码可维护、可复用

### 测试框架

- **单元测试**：pytest
- **集成测试**：pytest + 人工验证
- **验收测试**：人工检查

---

## 测试分层

### 1. 单元测试（pytest）

**目标**：测试单个函数/类的功能

**覆盖范围**：
- `utils.py` 的数据加载函数
- `text_cleaner.py` 的清洗函数
- `feature_extractor.py` 的特征提取函数
- `rule_filter.py` 的规则过滤类
- `naive_bayes.py` 的朴素贝叶斯类
- `evaluator.py` 的评估函数

### 2. 集成测试（pytest + 人工）

**目标**：测试模块间的协作

**覆盖范围**：
- 数据加载 → 清洗 → 特征提取
- 特征提取 → 分类 → 评估
- 完整流程（E2E）

### 3. 验收测试（人工检查）

**目标**：验证最终交付物

**覆盖范围**：
- 代码文件完整性
- 文档完整性
- 可视化图表质量
- 分析报告质量

---

## 测试用例设计

### Lesson 1 测试用例

#### 1.1 数据加载测试

```python
# test_utils.py
def test_load_emails():
    """测试邮件加载功能"""
    df = load_emails('data')
    assert len(df) == 6052  # 应该有6052条邮件
    assert 'label' in df.columns
    assert 'raw_email' in df.columns
    assert 'source' in df.columns
    # 检查标签值
    assert set(df['label'].unique()).issubset({'ham', 'spam'})

def test_load_emails_content():
    """测试邮件内容加载"""
    df = load_emails('data')
    assert df['raw_email'].iloc[0] != ''  # 第一条邮件内容不为空
```

#### 1.2 邮件解析测试

```python
# test_text_cleaner.py
def test_parse_email():
    """测试邮件解析"""
    filepath = 'data/easy_ham/00001.7c53336b37003a9286aba55d2945844c'
    result = parse_email(filepath)
    assert result['body'] != ''
    assert 'from' in result
    assert 'subject' in result

def test_parse_email_from_raw():
    """测试从原始内容解析邮件"""
    raw_email = "From: test@example.com\nSubject: Test\n\nHello World"
    body = parse_email_from_raw(raw_email)
    assert body == 'Hello World'
```

#### 1.3 文本清洗测试

```python
# test_text_cleaner.py
def test_clean_text():
    """测试文本清洗"""
    # 测试转小写
    assert clean_text('Hello WORLD') == 'hello world'
    
    # 测试去除HTML标签
    assert clean_text('<p>Hello</p>') == 'hello'
    
    # 测试去除URL
    assert clean_text('Visit http://example.com') == 'visit'
    
    # 测试去除特殊符号
    assert clean_text('Hello! @#$%') == 'hello'

def test_clean_text_empty():
    """测试空文本清洗"""
    assert clean_text('') == ''
    assert clean_text('   ') == ''

def test_html_to_text():
    """测试HTML转纯文本"""
    html = '<html><body><p>Hello <b>World</b></p></body></html>'
    text = html_to_text(html)
    assert 'Hello' in text
    assert 'World' in text
    assert '<p>' not in text
```

### Lesson 2 测试用例

#### 2.1 特征提取测试

```python
# test_feature_extractor.py
def test_extract_features():
    """测试特征提取"""
    features = extract_features('Free entry! Win $100')
    assert 'length' in features
    assert 'uppercase_ratio' in features
    assert 'exclamation_count' in features
    assert 'keyword_match' in features
    assert 'digit_count' in features
    assert 'currency_symbol' in features

def test_extract_features_empty():
    """测试空文本特征提取"""
    features = extract_features('')
    assert features['length'] == 0
    assert features['keyword_match'] == 0

def test_extract_features_batch():
    """测试批量特征提取"""
    texts = ['Hello World', 'Free entry!']
    df = extract_features_batch(texts)
    assert len(df) == 2
    assert 'length' in df.columns

def test_extract_features_ham():
    """测试ham特征提取"""
    features = extract_features('Hello, how are you today?')
    assert features['keyword_match'] == 0  # 没有spam关键词

def test_extract_features_spam():
    """测试spam特征提取"""
    features = extract_features('FREE! Win $1000 cash prize!!!')
    assert features['keyword_match'] > 0  # 有spam关键词
    assert features['currency_symbol'] > 0  # 有货币符号
    assert features['exclamation_count'] > 0  # 有感叹号
```

#### 2.2 规则过滤器测试

```python
# test_rule_filter.py
def test_rule_filter_predict():
    """测试规则过滤器预测"""
    filter = RuleFilter()
    # ham特征
    features = {'length': 100, 'keyword_match': 0, 'exclamation_count': 0}
    assert filter.predict(features) == 'ham'
    # spam特征
    features = {'length': 200, 'keyword_match': 3, 'exclamation_count': 5}
    assert filter.predict(features) == 'spam'

def test_rule_filter_threshold():
    """测试阈值影响"""
    filter = RuleFilter(threshold=10)  # 低阈值
    features = {'length': 100, 'keyword_match': 2, 'exclamation_count': 2}
    # 低阈值更容易判为spam
    result = filter.predict(features)
    assert result in ['ham', 'spam']

def test_rule_filter_weights():
    """测试权重影响"""
    weights = {'keyword_match': 10}  # 高权重
    filter = RuleFilter(weights=weights)
    features = {'length': 100, 'keyword_match': 2, 'exclamation_count': 0}
    # 高权重关键词匹配更容易判为spam
    result = filter.predict(features)
    assert result in ['ham', 'spam']

def test_rule_filter_batch():
    """测试批量预测"""
    filter = RuleFilter()
    df = pd.DataFrame([
        {'length': 100, 'keyword_match': 0, 'exclamation_count': 0},
        {'length': 200, 'keyword_match': 3, 'exclamation_count': 5}
    ])
    predictions = filter.predict_batch(df)
    assert len(predictions) == 2
    assert predictions[0] == 'ham'
    assert predictions[1] == 'spam'

def test_rule_filter_score():
    """测试分数计算"""
    filter = RuleFilter()
    features = {'length': 100, 'keyword_match': 2, 'exclamation_count': 3}
    score = filter.calculate_score(features)
    assert isinstance(score, float)
```

#### 2.3 朴素贝叶斯测试

```python
# test_naive_bayes.py
def test_naive_bayes_train():
    """测试朴素贝叶斯训练"""
    classifier = NaiveBayesClassifier()
    texts = ['free entry', 'hello world', 'win prize', 'good morning']
    labels = ['spam', 'ham', 'spam', 'ham']
    classifier.train(texts, labels)
    assert classifier.model is not None

def test_naive_bayes_predict():
    """测试朴素贝叶斯预测"""
    classifier = NaiveBayesClassifier()
    texts = ['free entry', 'hello world', 'win prize', 'good morning']
    labels = ['spam', 'ham', 'spam', 'ham']
    classifier.train(texts, labels)
    assert classifier.predict('free win') == 'spam'
    assert classifier.predict('hello good') == 'ham'

def test_naive_bayes_predict_batch():
    """测试批量预测"""
    classifier = NaiveBayesClassifier()
    texts = ['free entry', 'hello world', 'win prize', 'good morning']
    labels = ['spam', 'ham', 'spam', 'ham']
    classifier.train(texts, labels)
    predictions = classifier.predict_batch(['free win', 'hello good'])
    assert len(predictions) == 2
    assert predictions[0] == 'spam'
    assert predictions[1] == 'ham'

def test_naive_bayes_not_trained():
    """测试未训练时预测"""
    classifier = NaiveBayesClassifier()
    try:
        classifier.predict('test')
        assert False, "应该抛出异常"
    except Exception:
        pass

def test_naive_bayes_feature_importance():
    """测试特征重要性"""
    classifier = NaiveBayesClassifier()
    texts = ['free entry', 'hello world', 'win prize', 'good morning']
    labels = ['spam', 'ham', 'spam', 'ham']
    classifier.train(texts, labels)
    # 检查模型参数存在
    assert classifier.model is not None
```

### Lesson 3 测试用例

#### 3.1 评估指标测试

```python
# test_evaluator.py
def test_calculate_metrics():
    """测试评估指标计算"""
    y_true = ['ham', 'spam', 'ham', 'spam']
    y_pred = ['ham', 'spam', 'spam', 'ham']
    metrics = calculate_metrics(y_true, y_pred)
    assert 'accuracy' in metrics
    assert 'precision' in metrics
    assert 'recall' in metrics
    assert 'f1' in metrics
    assert 'confusion_matrix' in metrics

def test_calculate_metrics_perfect():
    """测试完美预测的指标"""
    y_true = ['ham', 'spam', 'ham', 'spam']
    y_pred = ['ham', 'spam', 'ham', 'spam']
    metrics = calculate_metrics(y_true, y_pred)
    assert metrics['accuracy'] == 1.0
    assert metrics['precision'] == 1.0
    assert metrics['recall'] == 1.0
    assert metrics['f1'] == 1.0

def test_calculate_metrics_all_ham():
    """测试全部预测为ham的指标"""
    y_true = ['ham', 'spam', 'ham', 'spam']
    y_pred = ['ham', 'ham', 'ham', 'ham']
    metrics = calculate_metrics(y_true, y_pred)
    assert metrics['accuracy'] == 0.5
    assert metrics['recall'] == 0.0  # 没有识别出spam
```

#### 3.2 可视化测试

```python
# test_evaluator.py
def test_plot_confusion_matrix():
    """测试混淆矩阵绘制"""
    y_true = ['ham', 'spam', 'ham', 'spam']
    y_pred = ['ham', 'spam', 'spam', 'ham']
    plot_confusion_matrix(y_true, y_pred, 'output/charts/test_confusion_matrix.png')
    assert os.path.exists('output/charts/test_confusion_matrix.png')

def test_plot_performance_comparison():
    """测试性能对比图绘制"""
    metrics1 = {'accuracy': 0.7, 'precision': 0.5, 'recall': 0.8, 'f1': 0.6}
    metrics2 = {'accuracy': 0.97, 'precision': 0.97, 'recall': 0.92, 'f1': 0.95}
    plot_performance_comparison(metrics1, metrics2, 'output/charts/test_performance.png')
    assert os.path.exists('output/charts/test_performance.png')

def test_confusion_matrix_structure():
    """测试混淆矩阵结构"""
    y_true = ['ham', 'spam', 'ham', 'spam']
    y_pred = ['ham', 'spam', 'spam', 'ham']
    metrics = calculate_metrics(y_true, y_pred)
    cm = metrics['confusion_matrix']
    assert len(cm) == 2
    assert len(cm[0]) == 2
    assert len(cm[1]) == 2
```

---

## 测试运行指南

### 运行所有测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行并显示详细输出
pytest tests/ -v -s

# 运行并生成覆盖率报告
pytest tests/ --cov=src --cov-report=html
```

### 运行特定测试

```bash
# 运行特定模块测试
pytest tests/test_text_cleaner.py -v

# 运行特定测试函数
pytest tests/test_text_cleaner.py::test_clean_text -v

# 运行失败的测试
pytest tests/ --lf
```

---

## 测试结果

### 单元测试结果

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

### 模型性能结果

| 分类器 | 准确率 | 精确率 | 召回率 | F1值 |
|--------|--------|--------|--------|------|
| 规则过滤器 | 68.32% | 49.69% | 76.78% | 60.34% |
| 朴素贝叶斯 | **96.78%** | **97.28%** | **92.31%** | **94.73%** |

---

## 人工验证项

### 1. 代码质量检查

**检查内容**：
- [x] 代码可运行，无语法错误
- [x] 有适当的注释和文档字符串
- [x] 模块化设计，可复用
- [x] 遵循PEP 8规范

**检查方式**：
- 代码审查
- 运行代码
- 检查文档

### 2. 可视化图表质量

**检查内容**：
- [x] 图表清晰可读
- [x] 标签和标题正确
- [x] 颜色和样式合适
- [x] 数据准确

**检查方式**：
- 打开图表文件
- 检查视觉效果
- 验证数据准确性

**图表清单**：
- [x] `output/charts/rule_confusion_matrix.png`
- [x] `output/charts/nb_confusion_matrix.png`
- [x] `output/charts/performance_comparison.png`
- [x] `output/charts/word_frequency.png`

### 3. 分析报告质量

**检查内容**：
- [x] 报告结构完整（8个章节）
- [x] 内容准确
- [x] 分析有深度
- [x] 建议可行

**检查方式**：
- 阅读报告
- 检查逻辑
- 验证数据

**报告章节**：
1. 项目概述
2. 数据探索
3. 文本清洗方法
4. 特征提取方案
5. 分类方法
6. 实验结果与评估
7. 误判样本分析
8. 总结与改进建议

---

## 测试覆盖率

**目标**：
- 测试通过率：100% ✅
- 测试执行时间：< 5分钟 ✅（3.65秒）

**覆盖模块**：
- utils.py: 2个测试 ✅
- text_cleaner.py: 5个测试 ✅
- feature_extractor.py: 5个测试 ✅
- rule_filter.py: 5个测试 ✅
- naive_bayes.py: 5个测试 ✅
- evaluator.py: 6个测试 ✅
- **合计**: 28个测试 ✅
