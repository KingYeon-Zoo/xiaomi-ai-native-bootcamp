"""
Lesson 3：测试评估与报告总结

实现评估、可视化和报告生成
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from src.evaluator import (
    calculate_metrics,
    plot_confusion_matrix,
    plot_performance_comparison,
    plot_word_frequency,
    generate_report
)


def main():
    """主函数"""
    print("=" * 60)
    print("Lesson 3：测试评估与报告总结")
    print("=" * 60)

    # 1. 加载预测结果
    print("\n[1/5] 加载预测结果...")
    df = pd.read_csv('output/predictions.csv')
    print(f"加载完成：共 {len(df)} 条记录")

    # 2. 计算评估指标
    print("\n[2/5] 计算评估指标...")
    rule_metrics = calculate_metrics(df['label'].tolist(), df['rule_pred'].tolist())
    nb_metrics = calculate_metrics(df['label'].tolist(), df['nb_pred'].tolist())

    print("\n规则过滤器指标:")
    print(f"  准确率: {rule_metrics['accuracy']:.4f}")
    print(f"  精确率: {rule_metrics['precision']:.4f}")
    print(f"  召回率: {rule_metrics['recall']:.4f}")
    print(f"  F1值: {rule_metrics['f1']:.4f}")

    print("\n朴素贝叶斯指标:")
    print(f"  准确率: {nb_metrics['accuracy']:.4f}")
    print(f"  精确率: {nb_metrics['precision']:.4f}")
    print(f"  召回率: {nb_metrics['recall']:.4f}")
    print(f"  F1值: {nb_metrics['f1']:.4f}")

    # 3. 生成图表
    print("\n[3/5] 生成图表...")

    # 混淆矩阵
    plot_confusion_matrix(
        df['label'].tolist(),
        df['rule_pred'].tolist(),
        'output/charts/rule_confusion_matrix.png',
        title='规则过滤器 - 混淆矩阵'
    )
    print("  ✓ 规则过滤器混淆矩阵")

    plot_confusion_matrix(
        df['label'].tolist(),
        df['nb_pred'].tolist(),
        'output/charts/nb_confusion_matrix.png',
        title='朴素贝叶斯 - 混淆矩阵'
    )
    print("  ✓ 朴素贝叶斯混淆矩阵")

    # 性能对比
    plot_performance_comparison(
        rule_metrics,
        nb_metrics,
        'output/charts/performance_comparison.png'
    )
    print("  ✓ 性能对比图")

    # 词频分布
    plot_word_frequency(
        df['cleaned_text'].tolist(),
        df['label'].tolist(),
        'output/charts/word_frequency.png'
    )
    print("  ✓ 词频分布图")

    # 4. 生成报告
    print("\n[4/5] 生成分析报告...")
    generate_report(df, rule_metrics, nb_metrics, 'output/analysis_report.md')
    print("  ✓ 分析报告已生成")

    # 5. 显示误判样本
    print("\n[5/5] 误判样本分析...")

    # 规则过滤器误判
    rule_fp = df[(df['label'] == 'ham') & (df['rule_pred'] == 'spam')]
    rule_fn = df[(df['label'] == 'spam') & (df['rule_pred'] == 'ham')]

    print(f"\n规则过滤器误判:")
    print(f"  假阳性（ham误判为spam）: {len(rule_fp)} 条")
    print(f"  假阴性（spam误判为ham）: {len(rule_fn)} 条")

    if len(rule_fp) > 0:
        print(f"\n假阳性样例（前3条）:")
        for i, (_, row) in enumerate(rule_fp.head(3).iterrows()):
            print(f"  [{i+1}] {row['cleaned_text'][:80]}...")

    # 朴素贝叶斯误判
    nb_fp = df[(df['label'] == 'ham') & (df['nb_pred'] == 'spam')]
    nb_fn = df[(df['label'] == 'spam') & (df['nb_pred'] == 'ham')]

    print(f"\n朴素贝叶斯误判:")
    print(f"  假阳性（ham误判为spam）: {len(nb_fp)} 条")
    print(f"  假阴性（spam误判为ham）: {len(nb_fn)} 条")

    if len(nb_fn) > 0:
        print(f"\n假阴性样例（前3条）:")
        for i, (_, row) in enumerate(nb_fn.head(3).iterrows()):
            print(f"  [{i+1}] {row['cleaned_text'][:80]}...")

    print("\n" + "=" * 60)
    print("Lesson 3 完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
