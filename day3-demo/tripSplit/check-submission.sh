#!/bin/bash
# check-submission.sh — TripSplit 提交包完整性检查脚本
#
# 用法: bash check-submission.sh [目录路径]
# 默认检查当前目录

TARGET="${1:-.}"
PASS=0
WARN=0
BLOCKED=0

echo "========================================"
echo " TripSplit 提交包完整性检查"
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

# ==========================================
# 1. 目录结构检查
# ==========================================
echo "--- 1. 目录结构 ---"

check_dir "$TARGET/backend" "backend/"
check_dir "$TARGET/backend/routes" "  routes/"
check_dir "$TARGET/backend/services" "  services/"
check_dir "$TARGET/backend/tests" "  tests/"
check_dir "$TARGET/backend/data" "  data/"
check_dir "$TARGET/frontend" "frontend/"
check_dir "$TARGET/frontend/src" "  src/"
check_dir "$TARGET/frontend/src/pages" "    pages/"
check_dir "$TARGET/frontend/src/components" "    components/"
check_dir "$TARGET/frontend/src/api" "    api/"
check_dir "$TARGET/docs" "docs/"
check_dir "$TARGET/docs/交付文档" "  交付文档/"

echo ""

# ==========================================
# 2. 交付文档检查（8 个）
# ==========================================
echo "--- 2. 交付文档 ---"

check_file "$TARGET/docs/交付文档/product-prd.md" "PRD"
check_file "$TARGET/docs/交付文档/design-options.md" "方案取舍"
check_file "$TARGET/docs/交付文档/dev-workflow.md" "开发计划"
check_file "$TARGET/docs/交付文档/test-strategy.md" "测试矩阵"
check_file "$TARGET/docs/交付文档/qa-gates.md" "质量关卡"
check_file "$TARGET/docs/交付文档/skill-mcp-harness.md" "自动化三件套"
check_file "$TARGET/docs/交付文档/token-strategy.md" "资料索引"
check_file "$TARGET/docs/交付文档/project-flow-map.md" "产物流转图"

echo ""

# ==========================================
# 3. 开发文档检查
# ==========================================
echo "--- 3. 开发文档 ---"

check_file "$TARGET/docs/ai-log.md" "AI 协作日志"
check_file "$TARGET/docs/plan.md" "实现计划"
check_file "$TARGET/docs/tasks.md" "任务清单"
check_file "$TARGET/docs/tests.md" "测试用例"
check_file "$TARGET/README.md" "README"

echo ""

# ==========================================
# 4. 后端核心文件检查
# ==========================================
echo "--- 4. 后端核心文件 ---"

check_file "$TARGET/backend/main.py" "main.py"
check_file "$TARGET/backend/models.py" "models.py"
check_file "$TARGET/backend/requirements.txt" "requirements.txt"
check_file "$TARGET/backend/routes/trips.py" "routes/trips.py"
check_file "$TARGET/backend/services/storage.py" "services/storage.py"
check_file "$TARGET/backend/services/settle.py" "services/settle.py"
check_file "$TARGET/backend/data/trips.json" "data/trips.json"

echo ""

# ==========================================
# 5. 前端核心文件检查
# ==========================================
echo "--- 5. 前端核心文件 ---"

check_file "$TARGET/frontend/package.json" "package.json"
check_file "$TARGET/frontend/vite.config.js" "vite.config.js"
check_file "$TARGET/frontend/index.html" "index.html"
check_file "$TARGET/frontend/src/main.jsx" "main.jsx"
check_file "$TARGET/frontend/src/App.jsx" "App.jsx"
check_file "$TARGET/frontend/src/api/trips.js" "api/trips.js"
check_file "$TARGET/frontend/src/pages/TripList.jsx" "pages/TripList.jsx"
check_file "$TARGET/frontend/src/pages/TripDetail.jsx" "pages/TripDetail.jsx"
check_file "$TARGET/frontend/src/components/TripForm.jsx" "components/TripForm.jsx"
check_file "$TARGET/frontend/src/components/MemberForm.jsx" "components/MemberForm.jsx"
check_file "$TARGET/frontend/src/components/ExpenseForm.jsx" "components/ExpenseForm.jsx"
check_file "$TARGET/frontend/src/components/ExpenseList.jsx" "components/ExpenseList.jsx"
check_file "$TARGET/frontend/src/components/MemberStats.jsx" "components/MemberStats.jsx"
check_file "$TARGET/frontend/src/components/Settlement.jsx" "components/Settlement.jsx"
check_file "$TARGET/frontend/src/components/EmptyState.jsx" "components/EmptyState.jsx"

echo ""

# ==========================================
# 6. 测试文件检查
# ==========================================
echo "--- 6. 测试文件 ---"

check_file "$TARGET/backend/tests/conftest.py" "conftest.py"
check_file "$TARGET/backend/tests/test_trips.py" "test_trips.py"
check_file "$TARGET/backend/tests/test_members.py" "test_members.py"
check_file "$TARGET/backend/tests/test_expenses.py" "test_expenses.py"
check_file "$TARGET/backend/tests/test_settle.py" "test_settle.py"
check_file "$TARGET/frontend/src/components/TripForm.test.jsx" "TripForm.test.jsx"
check_file "$TARGET/frontend/src/components/MemberForm.test.jsx" "MemberForm.test.jsx"
check_file "$TARGET/frontend/src/components/ExpenseForm.test.jsx" "ExpenseForm.test.jsx"
check_file "$TARGET/frontend/src/components/ExpenseList.test.jsx" "ExpenseList.test.jsx"
check_file "$TARGET/frontend/src/components/Settlement.test.jsx" "Settlement.test.jsx"

echo ""

# ==========================================
# 7. ai-log 质量检查
# ==========================================
echo "--- 7. ai-log 质量 ---"

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
  ENTRY_COUNT=$(grep -c "^### 记录" "$AI_LOG" 2>/dev/null || echo 0)
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

  # 决策标记检查
  REJECT_COUNT=$(grep -c "🔴" "$AI_LOG" 2>/dev/null || echo 0)
  MODIFY_COUNT=$(grep -c "🟡" "$AI_LOG" 2>/dev/null || echo 0)
  ADOPT_COUNT=$(grep -c "🟢" "$AI_LOG" 2>/dev/null || echo 0)
  TOTAL_DECISIONS=$((REJECT_COUNT + MODIFY_COUNT + ADOPT_COUNT))
  if [ "$TOTAL_DECISIONS" -gt 0 ]; then
    echo "  ✅ 决策标记: 🔴×$REJECT_COUNT 🟡×$MODIFY_COUNT 🟢×$ADOPT_COUNT"
    PASS=$((PASS + 1))
  else
    echo "  ⚠️  未找到决策标记"
    WARN=$((WARN + 1))
  fi
else
  echo "  ❌ ai-log.md 不存在"
  BLOCKED=$((BLOCKED + 1))
fi

echo ""

# ==========================================
# 8. README 可复现性检查
# ==========================================
echo "--- 8. README 可复现性 ---"

README="$TARGET/README.md"
if [ -f "$README" ]; then
  HAS_BACKEND=0; HAS_FRONTEND=0; HAS_TEST=0; HAS_ENV=0
  grep -qiE "(uvicorn|pip install|requirements)" "$README" 2>/dev/null && HAS_BACKEND=1
  grep -qiE "(npm install|npm run dev)" "$README" 2>/dev/null && HAS_FRONTEND=1
  grep -qiE "(pytest|vitest|npm test)" "$README" 2>/dev/null && HAS_TEST=1
  grep -qiE "(node.js|python)" "$README" 2>/dev/null && HAS_ENV=1

  if [ "$HAS_BACKEND" -eq 1 ] && [ "$HAS_FRONTEND" -eq 1 ] && [ "$HAS_TEST" -eq 1 ] && [ "$HAS_ENV" -eq 1 ]; then
    echo "  ✅ README 包含环境要求/后端启动/前端启动/测试命令"
    PASS=$((PASS + 1))
  else
    echo "  ⚠️  README 缺少:"
    [ "$HAS_ENV" -eq 0 ] && echo "     - 环境要求"
    [ "$HAS_BACKEND" -eq 0 ] && echo "     - 后端启动命令"
    [ "$HAS_FRONTEND" -eq 0 ] && echo "     - 前端启动命令"
    [ "$HAS_TEST" -eq 0 ] && echo "     - 测试命令"
    WARN=$((WARN + 1))
  fi
else
  echo "  ❌ README.md 不存在"
  BLOCKED=$((BLOCKED + 1))
fi

echo ""

# ==========================================
# 9. 运行测试
# ==========================================
echo "--- 9. 运行测试 ---"

# 后端 pytest
if [ -f "$TARGET/backend/.venv/Scripts/python.exe" ]; then
  echo "  运行 pytest..."
  PYTEST_OUT=$(cd "$TARGET/backend" && .venv/Scripts/python.exe -m pytest tests/ -q 2>&1)
  PYTEST_EXIT=$?
  if [ $PYTEST_EXIT -eq 0 ]; then
    PYTEST_PASSED=$(echo "$PYTEST_OUT" | grep -oE "[0-9]+ passed" || echo "? passed")
    echo "  ✅ pytest: $PYTEST_PASSED"
    PASS=$((PASS + 1))
  else
    echo "  ❌ pytest 失败:"
    echo "$PYTEST_OUT" | head -5
    BLOCKED=$((BLOCKED + 1))
  fi
else
  echo "  ⚠️  跳过 pytest（.venv 不存在）"
  WARN=$((WARN + 1))
fi

# 前端 vitest
if [ -d "$TARGET/frontend/node_modules" ]; then
  echo "  运行 vitest..."
  VITEST_OUT=$(cd "$TARGET/frontend" && npx vitest --run 2>&1)
  VITEST_EXIT=$?
  if [ $VITEST_EXIT -eq 0 ]; then
    VITEST_PASSED=$(echo "$VITEST_OUT" | grep -oE "[0-9]+ passed" || echo "? passed")
    echo "  ✅ vitest: $VITEST_PASSED"
    PASS=$((PASS + 1))
  else
    echo "  ❌ vitest 失败:"
    echo "$VITEST_OUT" | head -5
    BLOCKED=$((BLOCKED + 1))
  fi
else
  echo "  ⚠️  跳过 vitest（node_modules 不存在）"
  WARN=$((WARN + 1))
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
