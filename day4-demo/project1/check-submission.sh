#!/bin/bash
# check-submission.sh — Apache 日志分析项目提交包完整性检查脚本
#
# 用法: bash check-submission.sh [目录路径]
# 默认检查当前目录

TARGET="${1:-.}"
PASS=0
WARN=0
BLOCKED=0

echo "========================================"
echo " Apache 日志分析项目提交包完整性检查"
echo " 目标: $TARGET"
echo "========================================"
echo ""

# ==========================================
# 辅助函数
# ==========================================

check_file() {
  local fpath="$1"
  local label="$2"
  if [ -f "$fpath" ]; then
    echo "  ✅ $label"
    PASS=$((PASS + 1))
    return 0
  else
    echo "  ❌ $label (缺失)"
    BLOCKED=$((BLOCKED + 1))
    return 1
  fi
}

check_dir() {
  local dpath="$1"
  local label="$2"
  if [ -d "$dpath" ]; then
    echo "  ✅ $label"
    PASS=$((PASS + 1))
    return 0
  else
    echo "  ❌ $label (缺失)"
    BLOCKED=$((BLOCKED + 1))
    return 1
  fi
}

check_file_lines() {
  local fpath="$1"
  local label="$2"
  local expected="$3"
  if [ -f "$fpath" ]; then
    local actual=$(wc -l < "$fpath" 2>/dev/null || echo 0)
    if [ "$actual" -ge "$expected" ]; then
      echo "  ✅ $label ($actual 行，≥$expected)"
      PASS=$((PASS + 1))
      return 0
    else
      echo "  ⚠️  $label ($actual 行，不足 $expected)"
      WARN=$((WARN + 1))
      return 1
    fi
  else
    echo "  ❌ $label (缺失)"
    BLOCKED=$((BLOCKED + 1))
    return 1
  fi
}

# ==========================================
# 1. 数据源检查
# ==========================================
echo "--- 1. 数据源 ---"

check_file "$TARGET/Apache.log" "Apache.log 数据源"
if [ -f "$TARGET/Apache.log" ]; then
  LINE_COUNT=$(wc -l < "$TARGET/Apache.log" 2>/dev/null || echo 0)
  if [ "$LINE_COUNT" -ge 50000 ]; then
    echo "  ✅ 数据源行数: $LINE_COUNT (≥50000)"
    PASS=$((PASS + 1))
  else
    echo "  ⚠️  数据源行数: $LINE_COUNT (不足50000)"
    WARN=$((WARN + 1))
  fi
fi

echo ""

# ==========================================
# 2. 交付文档检查（7 个）
# ==========================================
echo "--- 2. 交付文档 ---"

check_file "$TARGET/docs/prd.md" "产品需求文档 (prd.md)"
check_file "$TARGET/docs/design.md" "技术设计文档 (design.md)"
check_file "$TARGET/docs/作业要求.md" "原始作业要求"
check_file "$TARGET/docs/ai-log.md" "AI 协作日志 (ai-log.md)"
check_file "$TARGET/docs/dev.md" "开发文档 (dev.md)"
check_file "$TARGET/docs/test-strategy.md" "测试策略文档 (test-strategy.md)"
check_file "$TARGET/tasks.md" "任务清单 (tasks.md)"

echo ""

# ==========================================
# 3. 代码文件检查
# ==========================================
echo "--- 3. 代码文件 ---"

# Lesson 1
check_file "$TARGET/src/lesson1_日志探索与解析.py" "Lesson 1 主脚本"
check_file "$TARGET/src/log_parser.py" "日志解析模块 (log_parser.py)"

# Lesson 2
check_file "$TARGET/src/lesson2_异常识别与统计.py" "Lesson 2 主脚本"
check_file "$TARGET/src/error_filter.py" "异常筛选模块 (error_filter.py)"
check_file "$TARGET/src/statistics.py" "统计分析模块 (statistics.py)"

# Lesson 3
check_file "$TARGET/src/lesson3_可视化与报告.py" "Lesson 3 主脚本"
check_file "$TARGET/src/visualizer.py" "可视化模块 (visualizer.py)"

# 工具库
check_dir "$TARGET/log_analyzer" "工具库目录 (log_analyzer/)"
check_file "$TARGET/log_analyzer/__init__.py" "工具库 __init__.py"
check_file "$TARGET/log_analyzer/log_parser.py" "工具库 log_parser.py"
check_file "$TARGET/log_analyzer/error_filter.py" "工具库 error_filter.py"
check_file "$TARGET/log_analyzer/statistics.py" "工具库 statistics.py"
check_file "$TARGET/log_analyzer/visualizer.py" "工具库 visualizer.py"

# 依赖文件
check_file "$TARGET/requirements.txt" "依赖文件 (requirements.txt)"

echo ""

# ==========================================
# 4. 输出文件检查
# ==========================================
echo "--- 4. 输出文件 ---"

check_dir "$TARGET/output" "输出目录 (output/)"
check_file_lines "$TARGET/output/structured_logs.csv" "结构化日志 (structured_logs.csv)" 50000
check_file "$TARGET/output/error_code_reference.csv" "错误类型对照表 (error_code_reference.csv)"
check_file "$TARGET/output/analysis_report.md" "分析报告 (analysis_report.md)"

# 检查 structured_logs.csv 字段
if [ -f "$TARGET/output/structured_logs.csv" ]; then
  HAS_TIMESTAMP=$(head -1 "$TARGET/output/structured_logs.csv" | grep -q "timestamp" && echo 1 || echo 0)
  HAS_LEVEL=$(head -1 "$TARGET/output/structured_logs.csv" | grep -q "level" && echo 1 || echo 0)
  HAS_CONTENT=$(head -1 "$TARGET/output/structured_logs.csv" | grep -q "content" && echo 1 || echo 0)
  if [ "$HAS_TIMESTAMP" -eq 1 ] && [ "$HAS_LEVEL" -eq 1 ] && [ "$HAS_CONTENT" -eq 1 ]; then
    echo "  ✅ structured_logs.csv 字段完整 (timestamp/level/content)"
    PASS=$((PASS + 1))
  else
    echo "  ⚠️  structured_logs.csv 字段不完整"
    WARN=$((WARN + 1))
  fi
fi

# 检查 error_code_reference.csv 是否有至少 8 种错误类型
if [ -f "$TARGET/output/error_code_reference.csv" ]; then
  ERROR_TYPES=$(tail -n +2 "$TARGET/output/error_code_reference.csv" | wc -l 2>/dev/null || echo 0)
  if [ "$ERROR_TYPES" -ge 8 ]; then
    echo "  ✅ 错误类型数量: $ERROR_TYPES (≥8)"
    PASS=$((PASS + 1))
  else
    echo "  ⚠️  错误类型数量: $ERROR_TYPES (不足8种)"
    WARN=$((WARN + 1))
  fi
fi

# 检查 analysis_report.md 是否有至少 8 个章节
if [ -f "$TARGET/output/analysis_report.md" ]; then
  CHAPTER_COUNT=$(grep -c "^##" "$TARGET/output/analysis_report.md" 2>/dev/null || echo 0)
  if [ "$CHAPTER_COUNT" -ge 8 ]; then
    echo "  ✅ 报告章节数: $CHAPTER_COUNT (≥8)"
    PASS=$((PASS + 1))
  else
    echo "  ⚠️  报告章节数: $CHAPTER_COUNT (不足8个)"
    WARN=$((WARN + 1))
  fi
fi

# 检查图表文件
CHART_COUNT=0
check_file "$TARGET/output/charts/daily_trend.png" "时序图 (daily_trend.png)" && CHART_COUNT=$((CHART_COUNT + 1))
check_file "$TARGET/output/charts/error_types.png" "饼图 (error_types.png)" && CHART_COUNT=$((CHART_COUNT + 1))
check_file "$TARGET/output/charts/modules.png" "柱状图 (modules.png)" && CHART_COUNT=$((CHART_COUNT + 1))
if [ "$CHART_COUNT" -eq 3 ]; then
  echo "  ✅ 图表文件完整 (3张)"
  PASS=$((PASS + 1))
elif [ "$CHART_COUNT" -gt 0 ]; then
  echo "  ⚠️  图表文件不完整 ($CHART_COUNT/3)"
  WARN=$((WARN + 1))
fi

echo ""

# ==========================================
# 5. 测试文件检查
# ==========================================
echo "--- 5. 测试文件 ---"

check_file "$TARGET/src/test_log_parser.py" "日志解析测试"
check_file "$TARGET/src/test_error_filter.py" "异常筛选测试"
check_file "$TARGET/src/test_statistics.py" "统计分析测试"
check_file "$TARGET/src/test_visualizer.py" "可视化测试"

echo ""

# ==========================================
# 6. ai-log 质量检查
# ==========================================
echo "--- 6. ai-log 质量 ---"

AI_LOG="$TARGET/docs/ai-log.md"
if [ -f "$AI_LOG" ]; then
  # 五字段格式检查
  HAS_FIELDS=0
  grep -q "目的" "$AI_LOG" 2>/dev/null && HAS_FIELDS=$((HAS_FIELDS + 1))
  grep -q "输入" "$AI_LOG" 2>/dev/null && HAS_FIELDS=$((HAS_FIELDS + 1))
  grep -q "建议" "$AI_LOG" 2>/dev/null && HAS_FIELDS=$((HAS_FIELDS + 1))
  grep -q "人工判断" "$AI_LOG" 2>/dev/null && HAS_FIELDS=$((HAS_FIELDS + 1))
  grep -q "验证" "$AI_LOG" 2>/dev/null && HAS_FIELDS=$((HAS_FIELDS + 1))

  if [ "$HAS_FIELDS" -ge 4 ]; then
    echo "  ✅ 五字段格式完整 ($HAS_FIELDS/5)"
    PASS=$((PASS + 1))
  else
    echo "  ⚠️  五字段不完整 ($HAS_FIELDS/5)"
    WARN=$((WARN + 1))
  fi

  # 条目数检查
  ENTRY_COUNT=$(grep -c "^### [0-9]" "$AI_LOG" 2>/dev/null || echo 0)
  if [ "$ENTRY_COUNT" -ge 15 ]; then
    echo "  ✅ ai-log 条目数: $ENTRY_COUNT (≥15)"
    PASS=$((PASS + 1))
  elif [ "$ENTRY_COUNT" -gt 0 ]; then
    echo "  ⚠️  ai-log 条目数: $ENTRY_COUNT (不足15条)"
    WARN=$((WARN + 1))
  else
    echo "  ⚠️  无法统计 ai-log 条目数"
    WARN=$((WARN + 1))
  fi
else
  echo "  ❌ ai-log.md 不存在"
  BLOCKED=$((BLOCKED + 1))
fi

echo ""

# ==========================================
# 7. README 可复现性检查
# ==========================================
echo "--- 7. README 可复现性 ---"

README="$TARGET/README.md"
if [ -f "$README" ]; then
  HAS_ENV=0; HAS_INSTALL=0; HAS_USAGE=0; HAS_TEST=0
  grep -qiE "(python|3\.10)" "$README" 2>/dev/null && HAS_ENV=1
  grep -qiE "(pip install|requirements)" "$README" 2>/dev/null && HAS_INSTALL=1
  grep -qiE "(python.*\.py|运行)" "$README" 2>/dev/null && HAS_USAGE=1
  grep -qiE "(pytest|测试)" "$README" 2>/dev/null && HAS_TEST=1

  if [ "$HAS_ENV" -eq 1 ] && [ "$HAS_INSTALL" -eq 1 ] && [ "$HAS_USAGE" -eq 1 ]; then
    echo "  ✅ README 包含环境要求/安装命令/使用说明"
    PASS=$((PASS + 1))
  else
    echo "  ⚠️  README 缺少:"
    [ "$HAS_ENV" -eq 0 ] && echo "     - 环境要求"
    [ "$HAS_INSTALL" -eq 0 ] && echo "     - 安装命令"
    [ "$HAS_USAGE" -eq 0 ] && echo "     - 使用说明"
    WARN=$((WARN + 1))
  fi
else
  echo "  ❌ README.md 不存在"
  BLOCKED=$((BLOCKED + 1))
fi

echo ""

# ==========================================
# 8. 运行测试
# ==========================================
echo "--- 8. 运行测试 ---"

# Python 依赖检查
if [ -f "$TARGET/.venv/Scripts/python.exe" ]; then
  echo "  检查 Python 依赖..."
  DEP_OUT=$(cd "$TARGET" && .venv/Scripts/python.exe -c "import pandas; import matplotlib; print('OK')" 2>&1)
  DEP_EXIT=$?
  if [ $DEP_EXIT -eq 0 ]; then
    echo "  ✅ Python 依赖完整 (pandas, matplotlib)"
    PASS=$((PASS + 1))
  else
    echo "  ❌ Python 依赖缺失:"
    echo "$DEP_OUT" | head -5
    BLOCKED=$((BLOCKED + 1))
  fi
elif [ -f "$TARGET/.venv/bin/python" ]; then
  echo "  检查 Python 依赖..."
  DEP_OUT=$(cd "$TARGET" && .venv/bin/python -c "import pandas; import matplotlib; print('OK')" 2>&1)
  DEP_EXIT=$?
  if [ $DEP_EXIT -eq 0 ]; then
    echo "  ✅ Python 依赖完整 (pandas, matplotlib)"
    PASS=$((PASS + 1))
  else
    echo "  ❌ Python 依赖缺失:"
    echo "$DEP_OUT" | head -5
    BLOCKED=$((BLOCKED + 1))
  fi
else
  echo "  ⚠️  跳过 Python 依赖检查（.venv 不存在）"
  WARN=$((WARN + 1))
fi

# Python pytest
if [ -f "$TARGET/.venv/Scripts/python.exe" ]; then
  echo "  运行 pytest..."
  PYTEST_OUT=$(cd "$TARGET" && .venv/Scripts/python.exe -m pytest src/test_*.py -q 2>&1)
  PYTEST_EXIT=$?
  if [ $PYTEST_EXIT -eq 0 ]; then
    PYTEST_PASSED=$(echo "$PYTEST_OUT" | grep -oE "[0-9]+ passed" || echo "? passed")
    echo "  ✅ pytest: $PYTEST_PASSED"
    PASS=$((PASS + 1))
  else
    echo "  ❌ pytest 失败:"
    echo "$PYTEST_OUT" | head -10
    BLOCKED=$((BLOCKED + 1))
  fi
elif [ -f "$TARGET/.venv/bin/python" ]; then
  echo "  运行 pytest..."
  PYTEST_OUT=$(cd "$TARGET" && .venv/bin/python -m pytest src/test_*.py -q 2>&1)
  PYTEST_EXIT=$?
  if [ $PYTEST_EXIT -eq 0 ]; then
    PYTEST_PASSED=$(echo "$PYTEST_OUT" | grep -oE "[0-9]+ passed" || echo "? passed")
    echo "  ✅ pytest: $PYTEST_PASSED"
    PASS=$((PASS + 1))
  else
    echo "  ❌ pytest 失败:"
    echo "$PYTEST_OUT" | head -10
    BLOCKED=$((BLOCKED + 1))
  fi
else
  echo "  ⚠️  跳过 pytest（.venv 不存在）"
  WARN=$((WARN + 1))
fi

# 验证 structured_logs.csv 行数
if [ -f "$TARGET/output/structured_logs.csv" ]; then
  echo "  验证 structured_logs.csv 行数..."
  CSV_LINES=$(wc -l < "$TARGET/output/structured_logs.csv" 2>/dev/null || echo 0)
  if [ "$CSV_LINES" -ge 52000 ]; then
    echo "  ✅ structured_logs.csv: $CSV_LINES 行 (≥52000)"
    PASS=$((PASS + 1))
  else
    echo "  ⚠️  structured_logs.csv: $CSV_LINES 行 (不足52000)"
    WARN=$((WARN + 1))
  fi
fi

echo ""

# ==========================================
# 总评
# ==========================================
echo "========================================"
echo " 检查结果汇总"
echo "========================================"
echo "  ✅ PASS:    $PASS"
echo "  ⚠️  WARNING: $WARN"
echo "  ❌ BLOCKED: $BLOCKED"
echo "----------------------------------------"

if [ "$BLOCKED" -gt 0 ]; then
  echo " 评级: BLOCKED"
  echo " 原因: 有 $BLOCKED 项关键文件缺失或测试失败。"
elif [ "$WARN" -gt 3 ]; then
  echo " 评级: WARNING"
  echo " 原因: 有 $WARN 项需要改进。"
else
  echo " 评级: PASS"
  echo " 提交包完整，测试通过，文档齐全。"
fi
echo "========================================"

[ "$BLOCKED" -gt 0 ] && exit 2
[ "$WARN" -gt 3 ] && exit 1
exit 0
