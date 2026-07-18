"""
Lesson 2：特征提取与分类实现

实现特征提取、规则过滤和朴素贝叶斯分类
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from src.feature_extractor import extract_features_batch
from src.rule_filter import RuleFilter
from src.naive_bayes import NaiveBayesClassifier


def calc_uppercase_ratio(text: str) -> float:
    """计算大写字母占比（从原始文本）"""
    if not text or not isinstance(text, str):
        return 0.0
    upper_count = sum(1 for c in text if c.isupper())
    total_alpha = sum(1 for c in text if c.isalpha())
    return upper_count / total_alpha if total_alpha > 0 else 0.0


def main():
    """主函数"""
    print("=" * 60)
    print("Lesson 2：特征提取与分类实现")
    print("=" * 60)

    # 1. 加载清洗后的数据
    print("\n[1/4] 加载清洗后的数据...")
    df = pd.read_csv('output/cleaned_data.csv')
    print(f"加载完成：共 {len(df)} 条记录")

    # 2. 提取特征
    print("\n[2/4] 提取特征...")
    # 填充NaN值为空字符串
    df['cleaned_text'] = df['cleaned_text'].fillna('')
    df['body'] = df['body'].fillna('')
    features_df = extract_features_batch(df['cleaned_text'].tolist())

    # 从原始正文计算大写字母占比（因为清洗后已转小写）
    features_df['uppercase_ratio'] = df['body'].apply(calc_uppercase_ratio)

    # 显示特征统计
    print("\n特征统计:")
    print(features_df.describe())

    # 3. 规则过滤预测
    print("\n[3/4] 规则过滤预测...")
    rule_filter = RuleFilter()
    df['rule_pred'] = rule_filter.predict_batch(features_df)

    # 统计预测结果
    rule_pred_counts = df['rule_pred'].value_counts()
    print(f"\n规则过滤预测结果:")
    print(rule_pred_counts)

    # 计算准确率
    correct = (df['label'] == df['rule_pred']).sum()
    accuracy = correct / len(df)
    print(f"\n规则过滤准确率: {accuracy:.4f} ({correct}/{len(df)})")

    # 4. 朴素贝叶斯预测
    print("\n[4/6] 训练朴素贝叶斯分类器...")
    nb_classifier = NaiveBayesClassifier()
    nb_classifier.train(df['cleaned_text'].tolist(), df['label'].tolist())
    print("训练完成！")

    print("\n[5/6] 朴素贝叶斯预测...")
    df['nb_pred'] = nb_classifier.predict_batch(df['cleaned_text'].tolist())

    # 统计预测结果
    nb_pred_counts = df['nb_pred'].value_counts()
    print(f"\n朴素贝叶斯预测结果:")
    print(nb_pred_counts)

    # 计算准确率
    nb_correct = (df['label'] == df['nb_pred']).sum()
    nb_accuracy = nb_correct / len(df)
    print(f"\n朴素贝叶斯准确率: {nb_accuracy:.4f} ({nb_correct}/{len(df)})")

    # 5. 保存结果
    print("\n[6/6] 保存结果...")
    df.to_csv('output/predictions.csv', index=False)
    print(f"✓ 预测结果已保存到 output/predictions.csv")

    # 显示样例
    print("\n" + "=" * 60)
    print("预测样例（前5条）:")
    print("=" * 60)
    for i, row in df.head(5).iterrows():
        print(f"\n[{i+1}] 标签: {row['label']}, 规则预测: {row['rule_pred']}, NB预测: {row['nb_pred']}")
        print(f"    清洗后（前80字符）: {row['cleaned_text'][:80]}...")

    # 显示两种方法对比
    print("\n" + "=" * 60)
    print("分类方法对比:")
    print("=" * 60)
    print(f"规则过滤准确率: {accuracy:.4f}")
    print(f"朴素贝叶斯准确率: {nb_accuracy:.4f}")

    print("\n" + "=" * 60)
    print("Lesson 2 完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
