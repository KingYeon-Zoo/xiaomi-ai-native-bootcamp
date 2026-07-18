#!/bin/bash
# check-submission.sh — 垃圾邮件智能过滤工具提交包检查脚本
#
# 用法: bash check-submission.sh [目录路径]
# 默认检查当前目录

TARGET="${1:-.}"
PASS=0
WARN=0
BLOCKED=0

echo "========================================"
echo " 垃圾邮件智能过滤工具提交包检查"
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
# 1. 文档检查（5个核心文档）
# ==========================================
echo "--- 1. 核心文档检查 ---"

check_file_lines "$TARGET/docs/prd.md" "产品需求文档 (prd.md)" 50
check_file_lines "$TARGET/docs/design.md" "技术设计文档 (design.md)" 50
check_file_lines "$TARGET/docs/dev.md" "开发文档 (dev.md)" 30
check_file_lines "$TARGET/docs/test-strategy.md" "测试策略文档 (test-strategy.md)" 50
check_file_lines "$TARGET/docs/ai-log.md" "AI协作日志 (ai-log.md)" 50

echo ""

# ==========================================
# 2. 运行测试
# ==========================================
echo "--- 2. 运行测试 ---"

# Python 依赖检查
if [ -f "$TARGET/.venv/Scripts/python.exe" ]; then
  PYTHON_CMD=".venv/Scripts/python.exe"
elif [ -f "$TARGET/.venv/bin/python" ]; then
  PYTHON_CMD=".venv/bin/python"
else
  echo "  ❌ Python 虚拟环境不存在"
  BLOCKED=$((BLOCKED + 1))
  PYTHON_CMD=""
fi

if [ -n "$PYTHON_CMD" ]; then
  echo "  检查 Python 依赖..."
  DEP_OUT=$(cd "$TARGET" && $PYTHON_CMD -c "import email; import re; print('OK')" 2>&1)
  DEP_EXIT=$?
  if [ $DEP_EXIT -eq 0 ]; then
    echo "  ✅ Python 依赖完整"
    PASS=$((PASS + 1))
  else
    echo "  ❌ Python 依赖缺失:"
    echo "$DEP_OUT" | head -5
    BLOCKED=$((BLOCKED + 1))
  fi

  # 运行 pytest
  echo "  运行 pytest..."
  PYTEST_OUT=$(cd "$TARGET" && $PYTHON_CMD -m pytest tests/ -q 2>&1)
  PYTEST_EXIT=$?
  if [ $PYTEST_EXIT -eq 0 ]; then
    PYTEST_PASSED=$(echo "$PYTEST_OUT" | grep -oE "[0-9]+ passed" || echo "? passed")
    echo "  ✅ pytest: $PYTEST_PASSED"
    PASS=$((PASS + 1))
  else
    echo "  ❌ pytest 失败:"
    echo "$PYTEST_OUT" | head -15
    BLOCKED=$((BLOCKED + 1))
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
  echo " 原因: 有 $BLOCKED 项关键检查失败。"
elif [ "$WARN" -gt 2 ]; then
  echo " 评级: WARNING"
  echo " 原因: 有 $WARN 项需要改进。"
else
  echo " 评级: PASS"
  echo " 文档齐全，测试通过。"
fi
echo "========================================"

[ "$BLOCKED" -gt 0 ] && exit 2
[ "$WARN" -gt 2 ] && exit 1
exit 0
