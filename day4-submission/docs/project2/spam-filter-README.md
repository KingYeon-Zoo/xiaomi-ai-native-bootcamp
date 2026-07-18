# `spam_filter` 包

`raw_message` 固定为 Subject + 正文，保留大小写、标点、数字和货币符号；`cleaned_message` 只供关键词与词袋模型使用。六类人工特征通过同时传入两种文本提取，从接口上阻止“从清洗文本计算大写率”的常见错误。

`NaiveBayesClassifier.fit()` 仅由训练集调用，并记录 `fit_sample_count` 供测试检查数据泄漏。
