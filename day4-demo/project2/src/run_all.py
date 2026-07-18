"""
E2E脚本

运行所有Lesson，完成全流程
"""

import subprocess
import sys
import os


def main():
    """主函数"""
    print("=" * 60)
    print("垃圾邮件智能过滤工具 - E2E测试")
    print("=" * 60)

    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)

    # 1. 运行Lesson 1
    print("\n[1/3] 运行Lesson 1: 数据加载与清洗...")
    try:
        result = subprocess.run(
            [sys.executable, 'src/lesson1.py'],
            capture_output=True,
            text=True,
            check=True
        )
        print("  ✓ Lesson 1 完成")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Lesson 1 失败: {e}")
        print(f"  错误输出: {e.stderr}")
        return False

    # 2. 运行Lesson 2
    print("\n[2/3] 运行Lesson 2: 特征提取与分类...")
    try:
        result = subprocess.run(
            [sys.executable, 'src/lesson2.py'],
            capture_output=True,
            text=True,
            check=True
        )
        print("  ✓ Lesson 2 完成")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Lesson 2 失败: {e}")
        print(f"  错误输出: {e.stderr}")
        return False

    # 3. 运行Lesson 3
    print("\n[3/3] 运行Lesson 3: 评估与报告...")
    try:
        result = subprocess.run(
            [sys.executable, 'src/lesson3.py'],
            capture_output=True,
            text=True,
            check=True
        )
        print("  ✓ Lesson 3 完成")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Lesson 3 失败: {e}")
        print(f"  错误输出: {e.stderr}")
        return False

    print("\n" + "=" * 60)
    print("E2E测试完成！")
    print("=" * 60)

    # 检查输出文件
    print("\n输出文件:")
    output_files = [
        'output/cleaned_data.csv',
        'output/predictions.csv',
        'output/analysis_report.md',
        'output/charts/rule_confusion_matrix.png',
        'output/charts/nb_confusion_matrix.png',
        'output/charts/performance_comparison.png',
        'output/charts/word_frequency.png'
    ]

    for filepath in output_files:
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"  ✓ {filepath} ({size:,} bytes)")
        else:
            print(f"  ✗ {filepath} 未生成")

    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
