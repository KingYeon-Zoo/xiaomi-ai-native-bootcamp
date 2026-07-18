"""
测试评估模块
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.evaluator import calculate_metrics, plot_confusion_matrix, plot_performance_comparison


def test_calculate_metrics():
    """测试评估指标计算"""
    y_true = ['ham', 'spam', 'ham', 'spam']
    y_pred = ['ham', 'spam', 'spam', 'ham']

    metrics = calculate_metrics(y_true, y_pred)

    assert 'accuracy' in metrics, "缺少accuracy"
    assert 'precision' in metrics, "缺少precision"
    assert 'recall' in metrics, "缺少recall"
    assert 'f1' in metrics, "缺少f1"
    assert 'confusion_matrix' in metrics, "缺少confusion_matrix"

    # 检查值范围
    assert 0 <= metrics['accuracy'] <= 1, f"accuracy应在0-1之间，实际{metrics['accuracy']}"
    assert 0 <= metrics['precision'] <= 1, f"precision应在0-1之间，实际{metrics['precision']}"
    assert 0 <= metrics['recall'] <= 1, f"recall应在0-1之间，实际{metrics['recall']}"
    assert 0 <= metrics['f1'] <= 1, f"f1应在0-1之间，实际{metrics['f1']}"


def test_calculate_metrics_perfect():
    """测试完美预测的指标"""
    y_true = ['ham', 'spam', 'ham', 'spam']
    y_pred = ['ham', 'spam', 'ham', 'spam']

    metrics = calculate_metrics(y_true, y_pred)

    assert metrics['accuracy'] == 1.0, f"完美预测准确率应为1.0，实际{metrics['accuracy']}"
    assert metrics['precision'] == 1.0, f"完美预测精确率应为1.0，实际{metrics['precision']}"
    assert metrics['recall'] == 1.0, f"完美预测召回率应为1.0，实际{metrics['recall']}"
    assert metrics['f1'] == 1.0, f"完美预测F1应为1.0，实际{metrics['f1']}"


def test_calculate_metrics_all_ham():
    """测试全预测为ham的情况"""
    y_true = ['ham', 'spam', 'ham', 'spam']
    y_pred = ['ham', 'ham', 'ham', 'ham']

    metrics = calculate_metrics(y_true, y_pred)

    assert metrics['accuracy'] == 0.5, f"准确率应为0.5，实际{metrics['accuracy']}"
    assert metrics['precision'] == 0.0, f"精确率应为0.0，实际{metrics['precision']}"
    assert metrics['recall'] == 0.0, f"召回率应为0.0，实际{metrics['recall']}"


def test_plot_confusion_matrix():
    """测试混淆矩阵绘图"""
    y_true = ['ham', 'spam', 'ham', 'spam']
    y_pred = ['ham', 'spam', 'spam', 'ham']

    save_path = 'output/charts/test_confusion_matrix.png'
    plot_confusion_matrix(y_true, y_pred, save_path)

    assert os.path.exists(save_path), f"图表文件未生成: {save_path}"


def test_plot_performance_comparison():
    """测试性能对比图"""
    metrics1 = {
        'accuracy': 0.8,
        'precision': 0.7,
        'recall': 0.6,
        'f1': 0.65
    }
    metrics2 = {
        'accuracy': 0.9,
        'precision': 0.85,
        'recall': 0.75,
        'f1': 0.8
    }

    save_path = 'output/charts/test_performance_comparison.png'
    plot_performance_comparison(metrics1, metrics2, save_path)

    assert os.path.exists(save_path), f"图表文件未生成: {save_path}"


def test_confusion_matrix_structure():
    """测试混淆矩阵结构"""
    y_true = ['ham', 'spam', 'ham', 'spam']
    y_pred = ['ham', 'spam', 'spam', 'ham']

    metrics = calculate_metrics(y_true, y_pred)
    cm = metrics['confusion_matrix']

    assert len(cm) == 2, f"混淆矩阵应有2行，实际{len(cm)}"
    assert len(cm[0]) == 2, f"混淆矩阵每行应有2列，实际{len(cm[0])}"
    assert len(cm[1]) == 2, f"混淆矩阵每行应有2列，实际{len(cm[1])}"
