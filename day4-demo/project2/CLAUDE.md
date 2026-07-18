# 项目二：垃圾邮件智能过滤工具

## 项目原则

1. **作业要求是示例**：不一定要一一对应，要和用户讨论
2. **以当前数据集为准**：使用SpamAssassin数据集，指标以实际表现为准
3. **以实际出发**：有数据集，可以现场测试验证
4. **决策依据**：基于实际数据和测试结果

---

## 文件索引

### 当前结构

```
project2/
├── CLAUDE.md              # 本文件（项目原则、索引、验证记录）
├── data/                  # 原始数据（只读）
├── temp_test/             # 测试脚本（可复用）
│   └── test_email_parsing.py
└── docs/                  # 文档目录
    ├── ai-log.md          # AI协作记录
    ├── prd.md             # 产品需求文档
    ├── design.md          # 技术设计文档
    ├── dev.md             # 开发文档
    ├── test-strategy.md   # 测试策略文档
    ├── tasks.md           # 任务清单（供Agent使用）
    └── 作业要求.md        # 原始作业要求
```

### 目标结构（设计）

详见 `docs/design.md`

---

## 数据初步分析

**数据集**：SpamAssassin公共语料库

### 规模统计

| 类型 | 数量 | 占比 |
|------|------|------|
| ham（正常邮件） | 4,153条 | 68.6% |
| spam（垃圾邮件） | 1,899条 | 31.4% |
| **总计** | **6,052条** | 100% |

### 目录分布

- `easy_ham/`：2,501条（正常邮件，容易分类）
- `easy_ham_2/`：1,401条（正常邮件第二批）
- `hard_ham/`：251条（难分类正常邮件）
- `spam/`：501条（垃圾邮件）
- `spam_2/`：1,398条（垃圾邮件第二批）

### 邮件格式

- **格式**：完整电子邮件（含邮件头、MIME信息、正文）
- **编码**：主要为纯文本和HTML
- **时间范围**：2002-2005年

### 编码统计（easy_ham样本）

- 纯文本邮件：1,910条
- HTML邮件：10条
- MIME邮件：1,499条

### 编码统计（spam样本）

- 纯文本邮件：250条
- HTML邮件：257条
- MIME邮件：376条

---

## 关键决策记录

### 1. 数据集选择
- 使用SpamAssassin数据集（老师提供的唯一数据集）
- 作业要求中的SMS Spam Collection是示例

### 2. 项目架构
- Python + .venv虚拟环境管理
- CLI运行方式：3个脚本 + 1个总脚本
- 代码放src目录，结果放output目录

### 3. 评估指标
- 以当前数据集的实际表现为准
- 先运行基准模型，查看实际指标

---

## 已验证技术点

### 1. 邮件解析方案 ✅

**方案**：使用Python email库

**测试结果**：
- 可以成功解析所有类型的邮件（easy_ham、spam、hard_ham）
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

**测试脚本**：`temp_test/test_email_parsing.py`

### 2. 文本清洗方案 ✅

**方案**：9步清洗流水线

**测试结果**：
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

**测试结果**：
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

**测试结果**：
- 规则过滤器能工作
- 初步准确率：ham 66%，spam 72%
- 需要调整权重和阈值以优化效果

**默认权重**：
- length: 0.01
- uppercase_ratio: 10
- exclamation_count: 2
- keyword_match: 5
- digit_count: 0.1
- currency_symbol: 3

**默认阈值**：15

---

## 待验证技术点

1. **朴素贝叶斯参数**：平滑参数、训练/测试集划分
2. **权重和阈值优化**：根据实际效果调整
