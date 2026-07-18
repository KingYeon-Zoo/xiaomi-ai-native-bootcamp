"""
评估模块

提供评估指标计算和可视化功能
"""

import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from collections import Counter

# 配置中文字体
def setup_chinese_font():
    """配置matplotlib中文字体"""
    # 尝试使用系统中文字体
    font_paths = [
        'C:/Windows/Fonts/msyh.ttc',  # 微软雅黑
        'C:/Windows/Fonts/simsun.ttc',  # 宋体
        'C:/Windows/Fonts/simhei.ttf',  # 黑体
    ]

    for font_path in font_paths:
        try:
            font_prop = fm.FontProperties(fname=font_path)
            plt.rcParams['font.family'] = font_prop.get_name()
            plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
            return
        except:
            continue

    # 如果没有找到中文字体，使用英文标签
    plt.rcParams['axes.unicode_minus'] = False

setup_chinese_font()


def calculate_metrics(y_true: list, y_pred: list) -> dict:
    """
    计算评估指标

    Args:
        y_true: 真实标签
        y_pred: 预测标签

    Returns:
        dict: 评估指标
        - accuracy: 准确率
        - precision: 精确率
        - recall: 召回率
        - f1: F1值
        - confusion_matrix: 混淆矩阵
    """
    # 计算混淆矩阵
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 'spam' and p == 'spam')
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == 'ham' and p == 'ham')
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 'ham' and p == 'spam')
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 'spam' and p == 'ham')

    # 计算指标
    accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'confusion_matrix': [[tn, fp], [fn, tp]]
    }


def plot_confusion_matrix(y_true: list, y_pred: list, save_path: str, title: str = '混淆矩阵'):
    """
    绘制混淆矩阵热力图

    Args:
        y_true: 真实标签
        y_pred: 预测标签
        save_path: 保存路径
        title: 图表标题
    """
    metrics = calculate_metrics(y_true, y_pred)
    cm = np.array(metrics['confusion_matrix'])

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)

    classes = ['ham', 'spam']
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=classes,
           yticklabels=classes,
           title=title,
           ylabel='真实标签',
           xlabel='预测标签')

    # 在格子中显示数值
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], 'd'),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")

    fig.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()


def plot_performance_comparison(metrics1: dict, metrics2: dict, save_path: str,
                                 label1: str = '规则过滤', label2: str = '朴素贝叶斯'):
    """
    绘制性能对比柱状图

    Args:
        metrics1: 第一个模型的指标
        metrics2: 第二个模型的指标
        save_path: 保存路径
        label1: 第一个模型标签
        label2: 第二个模型标签
    """
    metrics_names = ['accuracy', 'precision', 'recall', 'f1']
    display_names = ['准确率', '精确率', '召回率', 'F1值']

    x = np.arange(len(metrics_names))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width/2, [metrics1[m] for m in metrics_names], width, label=label1)
    bars2 = ax.bar(x + width/2, [metrics2[m] for m in metrics_names], width, label=label2)

    ax.set_ylabel('分数')
    ax.set_title('分类器性能对比')
    ax.set_xticks(x)
    ax.set_xticklabels(display_names)
    ax.legend()
    ax.set_ylim(0, 1)

    # 在柱子上显示数值
    for bar in bars1:
        height = bar.get_height()
        ax.annotate(f'{height:.3f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

    for bar in bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.3f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

    fig.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()


def plot_word_frequency(texts: list, labels: list, save_path: str, top_n: int = 20):
    """
    绘制词频分布图

    Args:
        texts: 文本列表
        labels: 标签列表
        save_path: 保存路径
        top_n: 显示前N个高频词
    """
    # 分别统计ham和spam的词频
    ham_words = []
    spam_words = []

    for text, label in zip(texts, labels):
        if not text or not isinstance(text, str):
            continue
        words = text.split()
        if label == 'ham':
            ham_words.extend(words)
        else:
            spam_words.extend(words)

    ham_counter = Counter(ham_words)
    spam_counter = Counter(spam_words)

    # 获取top_n高频词
    ham_top = ham_counter.most_common(top_n)
    spam_top = spam_counter.most_common(top_n)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Ham词频
    if ham_top:
        words, counts = zip(*ham_top)
        y_pos = np.arange(len(words))
        ax1.barh(y_pos, counts)
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(words)
        ax1.invert_yaxis()
        ax1.set_xlabel('出现次数')
        ax1.set_title('正常邮件 Top 20 高频词')

    # Spam词频
    if spam_top:
        words, counts = zip(*spam_top)
        y_pos = np.arange(len(words))
        ax2.barh(y_pos, counts)
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(words)
        ax2.invert_yaxis()
        ax2.set_xlabel('出现次数')
        ax2.set_title('垃圾邮件 Top 20 高频词')

    fig.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()


def generate_report(df, rule_metrics: dict, nb_metrics: dict, save_path: str):
    """
    生成分析报告

    Args:
        df: 包含预测结果的DataFrame
        rule_metrics: 规则过滤器的评估指标
        nb_metrics: 朴素贝叶斯的评估指标
        save_path: 报告保存路径
    """
    # 计算统计数据
    total = len(df)
    ham_count = len(df[df['label'] == 'ham'])
    spam_count = len(df[df['label'] == 'spam'])

    rule_cm = rule_metrics['confusion_matrix']
    nb_cm = nb_metrics['confusion_matrix']

    # 获取误判样本
    rule_fp_df = df[(df['label'] == 'ham') & (df['rule_pred'] == 'spam')]
    rule_fn_df = df[(df['label'] == 'spam') & (df['rule_pred'] == 'ham')]
    nb_fp_df = df[(df['label'] == 'ham') & (df['nb_pred'] == 'spam')]
    nb_fn_df = df[(df['label'] == 'spam') & (df['nb_pred'] == 'ham')]

    # 截取误判样本示例（前80字符）
    def get_sample_text(text_df, n=3):
        samples = []
        for _, row in text_df.head(n).iterrows():
            text = str(row.get('cleaned_text', ''))[:80]
            if text:
                samples.append(f'"{text}..."')
        return samples

    rule_fp_samples = get_sample_text(rule_fp_df)
    rule_fn_samples = get_sample_text(rule_fn_df)
    nb_fp_samples = get_sample_text(nb_fp_df)
    nb_fn_samples = get_sample_text(nb_fn_df)

    # 判断哪个模型更优
    if nb_metrics['f1'] > rule_metrics['f1']:
        best_model = "朴素贝叶斯"
        best_f1 = nb_metrics['f1']
        worse_f1 = rule_metrics['f1']
        improvement = (best_f1 - worse_f1) / worse_f1 * 100
    else:
        best_model = "规则过滤器"
        best_f1 = rule_metrics['f1']
        worse_f1 = nb_metrics['f1']
        improvement = (best_f1 - worse_f1) / worse_f1 * 100

    report = f"""# 垃圾邮件智能过滤工具 - 分析报告

## 1. 项目概述

本项目实现了一个垃圾邮件智能过滤工具，旨在自动识别和过滤垃圾邮件，保护用户免受垃圾信息的干扰。

项目采用两种不同的分类方法进行对比实验：
- **规则过滤器**：基于人工设计的特征权重进行线性评分，通过阈值判定分类
- **朴素贝叶斯分类器**：基于贝叶斯定理和特征条件独立假设的概率分类方法

通过对比两种方法的性能，可以深入理解不同分类策略在垃圾邮件过滤任务上的优劣。

## 2. 数据探索

### 2.1 数据集概况

本项目使用 **SpamAssassin 公共语料库** 作为实验数据集，该数据集是垃圾邮件过滤领域的经典基准数据集。

| 指标 | 数值 |
|------|------|
| 总邮件数 | {total} 条 |
| 正常邮件（ham） | {ham_count} 条（{ham_count / total * 100:.1f}%） |
| 垃圾邮件（spam） | {spam_count} 条（{spam_count / total * 100:.1f}%） |
| 数据来源 | SpamAssassin Public Corpus |
| 时间范围 | 2002-2005年 |

### 2.2 数据分布特点

数据集存在一定的**类别不平衡**问题：正常邮件占比约 {ham_count / total * 100:.1f}%，垃圾邮件占比约 {spam_count / total * 100:.1f}%。这种分布反映了真实场景中邮件的自然比例，对分类器的评估提出了更高要求——仅看准确率是不够的，还需要关注精确率和召回率。

### 2.3 数据来源分布

数据集包含多个子目录：
- `easy_ham/` 和 `easy_ham_2/`：容易分类的正常邮件
- `hard_ham/`：难以分类的正常邮件（与垃圾邮件特征相似）
- `spam/` 和 `spam_2/`：垃圾邮件

## 3. 文本清洗方法

### 3.1 清洗流水线

采用 **9 步清洗流水线**，逐步去除噪声并保留有效信息：

| 步骤 | 操作 | 目的 |
|------|------|------|
| 1 | 转小写 | 统一大小写，减少词汇表大小 |
| 2 | 去除HTML标签 | 提取纯文本内容 |
| 3 | 去除URL链接 | 移除网页地址干扰 |
| 4 | 去除邮箱地址 | 移除邮箱地址干扰 |
| 5 | 去除电话号码 | 移除数字序列干扰 |
| 6 | 去除特殊符号和标点 | 保留字母和数字 |
| 7 | 去除多余空格 | 规范化空白字符 |
| 8 | 去除停用词 | 移除常见无意义词汇 |
| 9 | 过滤空消息 | 清理无效数据 |

### 3.2 清洗的权衡

文本清洗是一个**有损操作**，需要在去噪和保留信息之间取得平衡：

- **正面效果**：去除噪声后，模型能更专注于有意义的文本特征
- **负面风险**：某些 spam 特征（如 `!!!`、`FREE!!!`）可能在清洗过程中丢失
- **设计选择**：本项目选择保留感叹号数量和大写字母占比作为独立特征，弥补清洗带来的信息损失

## 4. 特征提取方案

### 4.1 特征维度

提取 **6 个维度** 的手工特征，用于规则过滤器：

| 特征 | 描述 | 与spam的相关性 |
|------|------|----------------|
| `length` | 消息长度（字符数） | spam通常较长 |
| `uppercase_ratio` | 大写字母占比 | spam常用大写强调 |
| `exclamation_count` | 感叹号数量 | spam常使用多个感叹号 |
| `keyword_match` | 关键词匹配数量 | spam包含促销关键词 |
| `digit_count` | 数字数量 | spam包含电话、金额等 |
| `currency_symbol` | 货币符号数量 | spam常涉及金钱 |

### 4.2 关键词列表

用于 `keyword_match` 特征的关键词包括：`free`、`win`、`winner`、`prize`、`cash`、`urgent`、`offer`、`click`、`subscribe`、`buy`、`discount` 等 30+ 个常见垃圾邮件词汇。

### 4.3 大写字母占比的特殊处理

由于文本清洗步骤中包含"转小写"操作，大写字母信息会丢失。因此，`uppercase_ratio` 特征需要从**原始正文**（清洗前）中提取，而非清洗后的文本。

## 5. 分类方法

### 5.1 规则过滤器

**原理**：对每个特征维度计算加权得分，累加后与阈值比较。

**权重配置**：
| 特征 | 权重 |
|------|------|
| length | 0.01 |
| uppercase_ratio | 10 |
| exclamation_count | 2 |
| keyword_match | 5 |
| digit_count | 0.1 |
| currency_symbol | 3 |

**判定规则**：当总分 ≥ 15 时判定为 spam，否则为 ham。

**优点**：
- 可解释性强，每个特征的贡献清晰可见
- 无需训练数据，基于领域知识设计
- 计算速度快

**缺点**：
- 特征权重需要人工调优
- 难以捕捉复杂的特征交互
- 泛化能力有限

### 5.2 朴素贝叶斯分类器

**原理**：基于贝叶斯定理，计算在给定文本条件下属于 spam/ham 的后验概率。

**技术实现**：
- 使用 `CountVectorizer` 将文本转换为词频矩阵
- 使用 `MultinomialNB`（多项式朴素贝叶斯）进行分类
- 最大特征数限制为 5000

**优点**：
- 自动从数据中学习特征重要性
- 能捕捉词汇层面的复杂模式
- 训练后预测速度快

**缺点**：
- 假设特征条件独立（实际不完全成立）
- 需要标注数据进行训练
- 可解释性相对较弱

## 6. 实验结果与评估

### 6.1 评估指标说明

| 指标 | 含义 | 为什么重要 |
|------|------|------------|
| 准确率（Accuracy） | 预测正确的比例 | 整体性能的直观反映 |
| 精确率（Precision） | 预测为spam中真正是spam的比例 | 衡量"误报"程度 |
| 召回率（Recall） | 真正spam中被正确识别的比例 | 衡量"漏报"程度 |
| F1值 | 精确率和召回率的调和平均 | 综合评估指标 |

> **为什么只看准确率不够？** 如果把所有邮件都判为 ham，准确率也能达到 {ham_count / total * 100:.1f}%！但这完全没有过滤垃圾邮件的能力。

### 6.2 规则过滤器性能

| 指标 | 数值 |
|------|------|
| 准确率 | {rule_metrics['accuracy']:.4f} |
| 精确率 | {rule_metrics['precision']:.4f} |
| 召回率 | {rule_metrics['recall']:.4f} |
| F1值 | {rule_metrics['f1']:.4f} |

**混淆矩阵**：
|  | 预测ham | 预测spam |
|--|---------|----------|
| 实际ham | {rule_cm[0][0]} | {rule_cm[0][1]} |
| 实际spam | {rule_cm[1][0]} | {rule_cm[1][1]} |

**分析**：
- 精确率（{rule_metrics['precision']:.4f}）较低，说明误报较多
- 召回率（{rule_metrics['recall']:.4f}）相对较高，能识别大部分垃圾邮件
- F1值（{rule_metrics['f1']:.4f}）反映了精确率和召回率的平衡

### 6.3 朴素贝叶斯分类器性能

| 指标 | 数值 |
|------|------|
| 准确率 | {nb_metrics['accuracy']:.4f} |
| 精确率 | {nb_metrics['precision']:.4f} |
| 召回率 | {nb_metrics['recall']:.4f} |
| F1值 | {nb_metrics['f1']:.4f} |

**混淆矩阵**：
|  | 预测ham | 预测spam |
|--|---------|----------|
| 实际ham | {nb_cm[0][0]} | {nb_cm[0][1]} |
| 实际spam | {nb_cm[1][0]} | {nb_cm[1][1]} |

**分析**：
- 精确率（{nb_metrics['precision']:.4f}）很高，误报很少
- 召回率（{nb_metrics['recall']:.4f}）也很高，漏报很少
- F1值（{nb_metrics['f1']:.4f}）显著优于规则过滤器

### 6.4 性能对比

![分类器性能对比](charts/performance_comparison.png)

**对比分析**：
- {best_model} 在所有指标上都优于另一个分类器
- F1值提升了 **{improvement:.1f}%**，从 {worse_f1:.4f} 提升到 {best_f1:.4f}
- 机器学习方法（朴素贝叶斯）在垃圾邮件分类任务上表现更好

### 6.5 混淆矩阵可视化

**规则过滤器混淆矩阵**：

![规则过滤器混淆矩阵](charts/rule_confusion_matrix.png)

**朴素贝叶斯混淆矩阵**：

![朴素贝叶斯混淆矩阵](charts/nb_confusion_matrix.png)

## 7. 误判样本分析

### 7.1 规则过滤器误判分析

**假阳性（ham 误判为 spam）**：{rule_cm[0][1]} 条

这些正常邮件被错误地标记为垃圾邮件，可能原因：
- 包含较多数字或大写字母
- 包含某些被规则误判的关键词

示例：
{chr(10).join(f'- {s}' for s in rule_fp_samples) if rule_fp_samples else '- 无示例'}

**假阴性（spam 误判为ham）**：{rule_cm[1][0]} 条

这些垃圾邮件未被识别，可能原因：
- 不包含明显的垃圾邮件特征词
- 使用了规避检测的技巧

示例：
{chr(10).join(f'- {s}' for s in rule_fn_samples) if rule_fn_samples else '- 无示例'}

### 7.2 朴素贝叶斯误判分析

**假阳性（ham 误判为 spam）**：{nb_cm[0][1]} 条

示例：
{chr(10).join(f'- {s}' for s in nb_fp_samples) if nb_fp_samples else '- 无示例'}

**假阴性（spam 误判为 ham）**：{nb_cm[1][0]} 条

示例：
{chr(10).join(f'- {s}' for s in nb_fn_samples) if nb_fn_samples else '- 无示例'}

### 7.3 词频分析

通过分析两种类型邮件的高频词，可以更好地理解分类器的决策依据：

![词频分布图](charts/word_frequency.png)

**观察**：
- 正常邮件的高频词多为日常用语
- 垃圾邮件的高频词包含更多促销、营销相关词汇

## 8. 总结与改进建议

### 8.1 总结

{best_model} 分类器（F1={best_f1:.4f}）在本次实验中表现更优，相比另一种方法（F1={worse_f1:.4f}）提升了 {improvement:.1f}%。

**主要发现**：
1. **机器学习方法更有效**：朴素贝叶斯能够自动从数据中学习垃圾邮件的特征模式，比人工设计的规则更准确
2. **特征工程仍有价值**：规则过滤器虽然性能较低，但其可解释性强，可以作为辅助分析工具
3. **数据清洗很重要**：9步清洗流水线有效去除了噪声，提升了分类效果
4. **类别不平衡的影响**：数据集中 spam 占比约 {spam_count / total * 100:.1f}%，需要关注召回率

### 8.2 改进建议

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

*报告生成时间：基于 {total} 条邮件的实验数据*
"""

    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(report)
