# 开发文档

## 环境搭建

### 1. 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境（Windows）
.venv\Scripts\activate

# 激活虚拟环境（Linux/Mac）
source .venv/bin/activate
```

### 2. 安装依赖

```bash
# 安装依赖
pip install -r requirements.txt
```

**依赖清单**（requirements.txt）：
- pandas==3.0.3
- scikit-learn==1.9.0
- matplotlib==3.11.0
- pytest==9.1.1
- numpy==2.5.0
- scipy==1.18.0

### 3. 目录结构

```
project2/
├── src/                         # 源代码
│   ├── __init__.py
│   ├── utils.py                 # 数据加载模块
│   ├── text_cleaner.py          # 文本清洗模块
│   ├── feature_extractor.py     # 特征提取模块
│   ├── rule_filter.py           # 规则过滤器模块
│   ├── naive_bayes.py           # 朴素贝叶斯模块
│   ├── evaluator.py             # 评估模块
│   ├── lesson1.py               # Lesson 1 脚本
│   ├── lesson2.py               # Lesson 2 脚本
│   ├── lesson3.py               # Lesson 3 脚本
│   └── run_all.py               # E2E 脚本
├── tests/                       # 测试文件
├── output/                      # 输出目录
└── data/                        # 原始数据
```

---

## 代码规范

### 1. 命名规范
- **文件名**：小写字母 + 下划线（如 `text_cleaner.py`）
- **函数名**：小写字母 + 下划线（如 `clean_text()`）
- **类名**：大驼峰（如 `RuleFilter`）
- **常量**：大写字母 + 下划线（如 `MAX_LENGTH`）

### 2. 注释规范
- **模块注释**：文件顶部，说明模块功能
- **函数注释**：使用docstring，说明参数和返回值
- **关键代码**：必要时添加行内注释

### 3. 代码风格
- 遵循PEP 8规范
- 每行不超过79字符
- 使用4个空格缩进

---

## 开发流程

### 测试驱动开发（TDD）

每个模块开发流程：

1. **编写测试用例**（先写测试）
2. **运行测试**（预期失败）
3. **编写实现代码**
4. **运行测试**（预期通过）
5. **重构代码**
6. **再次运行测试**

### 阶段性验证

每个Lesson完成后需要验证：

| 阶段 | 验证内容 | 验证方式 |
|------|----------|----------|
| Lesson 1 | 数据清洗效果 | pytest + 人工检查 |
| Lesson 2 | 特征提取和分类 | pytest + 指标检查 |
| Lesson 3 | 评估和可视化 | pytest + 人工检查 |

---

## 模块开发顺序

### Lesson 1：数据探索与清洗

**开发顺序**：
1. `src/utils.py` - 工具函数（数据加载）
2. `src/text_cleaner.py` - 文本清洗模块
3. `src/lesson1.py` - 主脚本

**依赖关系**：
```
lesson1.py → text_cleaner.py → utils.py
```

### Lesson 2：特征提取与分类

**开发顺序**：
1. `src/feature_extractor.py` - 特征提取模块
2. `src/rule_filter.py` - 规则过滤器
3. `src/naive_bayes.py` - 朴素贝叶斯
4. `src/lesson2.py` - 主脚本

**依赖关系**：
```
lesson2.py → feature_extractor.py
lesson2.py → rule_filter.py
lesson2.py → naive_bayes.py
```

### Lesson 3：评估与报告

**开发顺序**：
1. `src/evaluator.py` - 评估模块
2. `src/lesson3.py` - 主脚本
3. `src/run_all.py` - E2E脚本

**依赖关系**：
```
lesson3.py → evaluator.py
run_all.py → lesson1.py, lesson2.py, lesson3.py
```

---

## 已验证技术方案

### 1. 邮件解析方案 ✅

**方案**：使用Python email库

**验证结果**：
- 可以解析所有类型的邮件（easy_ham、spam、hard_ham）
- 可以提取邮件头信息（From、Subject等）
- 可以提取正文（纯文本或HTML）
- HTML邮件可以用HTMLParser转换为纯文本

**实现方式**：
```python
from email import policy
from email.parser import BytesParser

with open(filepath, 'rb') as f:
    msg = BytesParser(policy=policy.default).parse(f)

# 提取邮件头
from_addr = msg['From']
subject = msg['Subject']

# 提取正文
body = msg.get_body(preferencelist=('plain', 'html'))
text = body.get_content()
```

### 2. 文本清洗方案 ✅

**方案**：9步清洗流水线

**验证结果**：
- 转小写 ✅
- 去除HTML标签 ✅
- 去除URL链接 ✅
- 去除邮箱地址 ✅
- 去除电话号码 ✅
- 去除特殊符号和标点 ✅
- 去除多余空格 ✅
- 去除停用词 ✅
- 过滤空消息 ✅

**停用词表**：使用简化版停用词列表（约100个常见英文停用词）

### 3. 特征提取方案 ✅

**方案**：6个维度的特征

**验证结果**：
- 消息长度（字符数） ✅
- 大写字母占比 ✅
- 感叹号数量 ✅
- 关键词匹配 ✅
- 数字数量 ✅
- 货币符号 ✅

**特征分布**（基于样本分析）：
- ham平均长度：783字符，关键词匹配：0.84
- spam平均长度：1133字符，关键词匹配：2.40
- ham和spam的特征分布有明显差异

### 4. 规则过滤器方案 ✅

**方案**：基于特征权重的规则过滤

**验证结果**：
- 规则过滤器能工作
- 准确率：68.32%
- 精确率：49.69%
- 召回率：76.78%
- F1值：60.34%

**默认权重**：
- length: 0.01
- uppercase_ratio: 10
- exclamation_count: 2
- keyword_match: 5
- digit_count: 0.1
- currency_symbol: 3

**默认阈值**：15

### 5. 朴素贝叶斯方案 ✅

**方案**：CountVectorizer + MultinomialNB

**验证结果**：
- 准确率：96.78%
- 精确率：97.28%
- 召回率：92.31%
- F1值：94.73%

**参数**：
- 最大特征数：5000
- 平滑参数：1.0（默认）

---

## 开发日志

### 2026-06-25

**阶段一：项目初始化** ✅
- 确定数据集：SpamAssassin（6052条）
- 确定架构：CLI + src目录
- 确定开发原则：以实际数据为准

**阶段二：需求与设计** ✅
- 完成PRD文档
- 完成技术设计文档
- 验证4个技术方案

**阶段三：测试与任务** ✅
- 完成测试策略文档
- 设计5个开发任务
- 创建28个测试用例

**阶段四：开发与验证** ✅
- 完成Lesson 1：数据加载与清洗
- 完成Lesson 2：特征提取与分类
- 完成Lesson 3：评估与报告
- 完成E2E全流程脚本

**阶段五：验收与交付** ✅
- 28个测试全部通过
- E2E脚本运行成功
- 朴素贝叶斯准确率96.78%（>95%）
- 生成4张可视化图表
- 生成完整分析报告

---

## 运行指南

### 运行完整流程（推荐）

```bash
# 激活虚拟环境
.venv\Scripts\activate

# 运行E2E全流程
python src/run_all.py
```

### 分步运行

```bash
# Step 1: 数据加载与清洗
python src/lesson1.py

# Step 2: 特征提取与分类
python src/lesson2.py

# Step 3: 评估与报告
python src/lesson3.py
```

### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_utils.py -v
```

---

## 常见问题

### 1. 邮件解析失败怎么办？

**可能原因**：
- 邮件格式异常
- 编码问题

**解决方案**：
- 添加异常处理
- 记录失败的邮件
- 跳过无法解析的邮件

### 2. HTML解析不完整怎么办？

**可能原因**：
- HTML结构复杂
- 特殊标签处理

**解决方案**：
- 使用HTMLParser
- 添加更多解析规则
- 手动处理特殊案例

### 3. 特征提取效果不好怎么办？

**可能原因**：
- 特征选择不当
- 权重设计不合理

**解决方案**：
- 分析spam/ham的特征差异
- 调整特征权重
- 添加新的特征维度

### 4. 朴素贝叶斯准确率低怎么办？

**可能原因**：
- 数据质量问题
- 特征数量不足

**解决方案**：
- 优化文本清洗
- 增加最大特征数
- 调整平滑参数
