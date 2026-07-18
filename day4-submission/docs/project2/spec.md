# Project 2 规格：垃圾邮件智能过滤工具

- 状态：Final Approved（2026-07-15 全量验收通过）
- 数据：SpamAssassin Public Corpus 六个 `tar.bz2`
- 固定协议：`test_size=0.2`、`random_state=42`、`stratify=y`、正类 `spam`

## 1. 目标

建立可复核的邮件加载与清洗契约，用同一测试集比较可解释规则过滤器和 `CountVectorizer + MultinomialNB`，输出四项指标、混淆矩阵、四张图与真实 FP/FN 分析。

## 2. 非目标

- 不处理附件内容、图片 OCR、多语言分词或线上邮件收发。
- 不引入外部停用词下载，避免运行时网络依赖。
- 不使用最终测试集循环调规则阈值或模型超参数。
- 不因清洗后空文本而删除样本或更改标签。
- 不把高 Accuracy 等同于可部署结论。

## 3. 数据契约

| 字段 | 定义 |
|---|---|
| label | 由压缩包名确定：含 ham 为 `ham`，其余课程 spam 包为 `spam` |
| raw_message | 解码后的 Subject + 正文；排除 From/To 等头和附件 |
| cleaned_message | raw 依次经小写、HTML、URL、邮箱、电话、标点、空格、停用词、空文本处理 |
| source/message_id | 追溯压缩包与 member，不参与分类 |
| split | 固定为 train/test，证明实验边界 |

六类人工特征的数据源：长度、大写率、感叹号、数字、货币符号来自 raw；spam 关键词来自 cleaned；CountVectorizer 只使用 cleaned。

## 4. 验收标准

| AC | 行为 | 验收 |
|---|---|---|
| P2-AC1 | 六包共加载 7,449 封，raw 不含普通邮件头且保留 Subject/正文 | 全量入口 + `test_text_cleaner.py` |
| P2-AC2 | 九步清洗覆盖 HTML/URL/邮箱/电话/符号/空文本 | `test_text_cleaner.py` |
| P2-AC3 | 六类特征使用正确文本源，长邮件不能单独支配规则 | feature/rule 单测 |
| P2-AC4 | Vectorizer 只在训练集 fit；两模型共享测试集 | `test_integration.py` + `fit_sample_count` |
| P2-AC5 | 报告 Accuracy/Precision/Recall/F1、矩阵、FP/FN 与实际预测一致 | 全量运行与复算 |
| P2-AC6 | 生成 cleaned_data.csv、四张指定图和 analysis_report.md | 清单审计 |

建议门槛：NB Accuracy≥95%、spam Precision≥90%、spam Recall≥85%。未达标时记录原因，不改变实验协议。

## 5. 方案比较

### 数据加载

- 全部解压到同一目录：简单，但不同压缩包含同名 `spam/` 等目录，存在覆盖和样本来源丢失风险。
- 逐 tar member 读取（选择）：无中间副本、保留 source、避免路径覆盖；单封异常可记录。

### 特征接口

- 只传 cleaned：调用简单，却无法正确计算大写、标点和货币特征。
- 同时传 raw/cleaned（选择）：接口更明确，直接暴露数据契约。

### 模型

- 手写朴素贝叶斯：教学价值高但边界多，题目已指定 scikit-learn。
- CountVectorizer + MultinomialNB（选择）：与题目一致、可检查只在训练集 fit。
- 深度学习：指标可能更高，但成本、解释与时间不匹配，拒绝。

## 6. 数据流与失败处理

```text
6 tar.bz2 -> RFC/MIME 解析 -> raw_message -> clean_text -> cleaned_message
-> 固定分层切分
-> raw+cleaned -> 六特征 -> RuleFilter ------┐
-> train cleaned fit Vectorizer+NB -> test ---┼-> 同一测试集指标/图/FP-FN 报告
```

单封 MIME 异常记录告警并保留空 raw；压缩包数量非 6 时主入口失败；模型未 fit 时预测明确抛错；指标正类与矩阵顺序显式固定。

## 7. 可执行任务

1. 用合成邮件验证 Subject/正文与头、附件边界。
2. 验证九步清洗和空文本。
3. 用 raw/cleaned 反例验证六特征来源。
4. 固定小数据 Smoke Test 训练/预测及 fit 样本数。
5. 全量运行，检查 7,449、类别分布、指标门槛、四图和 FP/FN。

## 8. 风险

旧语料分布与现代邮件不同；随机切分可能高估跨时间泛化；部分 MIME 编码损坏；规则阈值仅为固定基线；停用词表较小但确定、离线可复现。
