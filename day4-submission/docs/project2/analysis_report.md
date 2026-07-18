# 垃圾邮件智能过滤分析报告

## 1. 项目概述

本项目用同一测试集比较可解释规则与 `CountVectorizer + MultinomialNB`。报告数字由 `python main.py` 基于真实语料生成。

## 2. 数据探索

- 总邮件：7,449；ham：4,153；spam：3,296。
- 解析告警：49；清洗后空文本：160。

## 3. 文本清洗

依次执行小写、HTML 文本化、URL、邮箱、电话、标点、空白、停用词和空文本处理。空文本保留为空字符串，不删除样本或改标签。

## 4. 数据契约

`raw_message` 是 Subject + 正文，不含其余邮件头；`cleaned_message` 是模型输入。大写率、感叹号、数字和货币符号只从 raw 提取，关键词只从 cleaned 提取。

## 5. 特征提取

六类特征为消息长度、大写字母占比、感叹号数量、关键词命中、数字数量和货币符号数量。规则对计数设置上限，避免单一长邮件让得分无限增长。

## 6. 规则过滤

规则阈值固定为 5.0，没有使用最终测试集反复调参。测试集结果：accuracy=0.7799 | precision=0.8702 | recall=0.5903 | f1=0.7034；混淆矩阵（行真实、列预测，ham/spam）：`[[773, 58], [270, 389]]`。

## 7. 朴素贝叶斯

使用最多 12,000 个 unigram/bigram 特征与 `MultinomialNB(alpha=0.5)`。测试集结果：accuracy=0.9564 | precision=0.9885 | recall=0.9120 | f1=0.9487；混淆矩阵：`[[824, 7], [58, 601]]`。

## 8. 实验协议

使用 `train_test_split(test_size=0.2, random_state=42, stratify=y)`；训练 5,959 封、测试 1,490 封，两种方法共享完全相同的测试行。

## 9. 模型指标

朴素贝叶斯验收门槛为 Accuracy≥95%、spam Precision≥90%、spam Recall≥85%。是否达标由上述实际数字判断，不修改标签或测试集迎合门槛。

## 10. 混淆矩阵

四张图均由本次测试标签和预测直接生成；矩阵标签顺序固定为 `[ham, spam]`，避免类别排序导致 TP/FP 解释反转。

## 11. False Positive 分析

- 规则样例：`["Save an extra $50 of Compaq's powerful iPaq H3835! (CNET SHOPPER) Shopper Newsletter: Alerts 1 Canon PowerShot S40 2 Canon PowerShot G2 3 Ga", "Back to School with Buy4Now <http://www.buy4now.ie> It's Back to School at Buy4Now, but don't feel down because we have lots of special offe", 'Announcing the New Netscape 7.0 - The Fastest Netscape Browser Ever Netscape Valued Customer: Announcing the NEW Netscape 7.0 Browser! Downl']`
- 朴素贝叶斯样例：`["Back to School with Buy4Now <http://www.buy4now.ie> It's Back to School at Buy4Now, but don't feel down because we have lots of special offe", 'Announcing the New Netscape 7.0 - The Fastest Netscape Browser Ever Netscape Valued Customer: Announcing the NEW Netscape 7.0 Browser! Downl', "Astrology.com: daily horoscope ----------------------------------------------------------------- Back to school! Find out what's in store fo"]`

正常邮件可能因营销词、金额或强烈标点被误判；这说明“像垃圾邮件”不等同于真实标签。

## 12. False Negative 分析

- 规则样例：`['Slim Factors - A totally new approach to weight loss Slim Factors This e-mail is intended to be a benefit to the recipient. If you would lik', 'Adult Ads Married But Lonely ENTER THE WORLD FAMOUS Married But Lonely ! A worldwide non-profit organization founded and managed exclusively', ':: Fast Acting Viagra FAST ACTING VIAGRA!!! AT LAST (FAST ACTING VIAGRA) Removal Instructions: You have received this advertisement because ']`
- 朴素贝叶斯样例：`[':: Fast Acting Viagra FAST ACTING VIAGRA!!! AT LAST (FAST ACTING VIAGRA) Removal Instructions: You have received this advertisement because ', 'The Hotel Show LAST CHANCE TO EXHIBIT AT The Hotel Show 2002 20-22 May, 2002, Airport Expo Dubai, UAE With over 200 luxury hotels and resort', 'Find Peace, Harmony, Tranquility, And Happiness Right Now!']`

隐晦表达、图片型内容或清洗后信息稀少会漏判。降低阈值虽能提高召回，但也可能增加正常邮件拦截成本。

## 13. 数据泄漏检查

Vectorizer 仅在训练集 `fit`，之后对测试集 `transform`；代码和集成测试检查 `fit_sample_count == train_size`。词频图只作离线说明，不参与模型训练。

## 14. 改进建议

下一步应使用独立验证集选择规则阈值与超参数，并按 `hard_ham`、时间批次分层报告，以观察分布漂移，而不是继续消费最终测试集。

## 15. 已知限制

语料来自 2003—2005 年，不能代表当代钓鱼与多语言邮件；附件和图片内容未做 OCR；随机分层切分不能替代跨时间外部验证。
