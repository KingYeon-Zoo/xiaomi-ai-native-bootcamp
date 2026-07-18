#!/usr/bin/env bash
# 小米训练营项目证据审计。只读检查，不修改被审计项目。

set -u

TARGET="${1:-}"
MODE="${2:-}"
PASS=0
WARN=0
BLOCKED=0

usage() {
  echo "用法：bash audit-xiaomi-project.sh <项目目录> <personal|team>"
}

if [[ -z "$TARGET" || ( "$MODE" != "personal" && "$MODE" != "team" ) ]]; then
  usage
  exit 64
fi

if [[ "$TARGET" != "/" ]]; then
  TARGET="${TARGET%/}"
fi

if [[ ! -d "$TARGET" ]]; then
  echo "❌ BLOCKED：项目目录不存在：$TARGET"
  exit 2
fi

ok() { echo "✅ $1"; PASS=$((PASS + 1)); }
warn() { echo "⚠️  $1"; WARN=$((WARN + 1)); }
blocked() { echo "❌ $1"; BLOCKED=$((BLOCKED + 1)); }

check_nonempty() {
  local path="$1"
  local label="$2"
  if [[ -s "$path" ]]; then
    ok "${label}：${path}"
  else
    blocked "${label}缺失或为空：${path}"
  fi
}

find_first_nonempty() {
  local candidate
  for candidate in "$@"; do
    if [[ -s "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  return 1
}

contains_pattern() {
  local pattern="$1"
  shift
  if command -v rg >/dev/null 2>&1; then
    rg -n -i "$pattern" "$@" >/dev/null 2>&1
  else
    grep -R -n -i -E "$pattern" "$@" >/dev/null 2>&1
  fi
}

echo "========================================"
echo "小米训练营项目证据审计"
echo "目录：$TARGET"
echo "模式：$MODE"
echo "========================================"

echo
echo "--- 1. docs 目录与 Markdown 路径规范 ---"
if [[ -d "$TARGET/docs" ]]; then
  ok "找到过程文档目录：$TARGET/docs"
else
  blocked "缺少 docs/；所有开发过程 Markdown 必须写入该目录"
fi

DOC_VIOLATIONS=()
while IFS= read -r markdown; do
  case "$markdown" in
    "$TARGET/README.md"|"$TARGET/AGENTS.md"|"$TARGET/CLAUDE.md")
      ;;
    "$TARGET/docs/"*|*/.agents/*|*/.git/*|*/.venv/*|*/node_modules/*|*/vendor/*|*/skills/*|*/templates/*|*/materials/*|*/reference/*|*/references/*|*/input/*|*/素材/*|*/材料/*|*/day*材料/*)
      ;;
    *)
      DOC_VIOLATIONS+=("$markdown")
      ;;
  esac
done < <(find "$TARGET" -type f -name '*.md' 2>/dev/null)

if (( ${#DOC_VIOLATIONS[@]} == 0 )); then
  ok "除根目录入口和 README 外，Markdown 全部位于 docs/"
else
  blocked "发现 docs/ 外的过程 Markdown"
  for markdown in "${DOC_VIOLATIONS[@]}"; do
    echo "   - $markdown"
  done
fi

echo
echo "--- 2. 工程约束入口与正文 ---"
check_nonempty "$TARGET/AGENTS.md" "Codex 根目录入口 AGENTS.md"
ENGINEERING_GUIDANCE="$TARGET/docs/engineering-constraints.md"
check_nonempty "$ENGINEERING_GUIDANCE" "工程约束正文"

if [[ -s "$TARGET/AGENTS.md" ]] && contains_pattern 'docs/engineering-constraints\.md' "$TARGET/AGENTS.md"; then
  ok "AGENTS.md 已路由到 docs/engineering-constraints.md"
else
  blocked "AGENTS.md 未明确要求读取 docs/engineering-constraints.md"
fi

if [[ -s "$TARGET/CLAUDE.md" ]]; then
  if contains_pattern 'docs/engineering-constraints\.md' "$TARGET/CLAUDE.md"; then
    ok "CLAUDE.md 已路由到 docs/engineering-constraints.md"
  else
    warn "CLAUDE.md 存在但未路由到 docs/engineering-constraints.md"
  fi
fi

if [[ -s "$ENGINEERING_GUIDANCE" ]]; then
  for heading in "文档目录规范" "资料优先级" "目标与非目标" "阶段门禁" "运行与验证命令" "验收证据映射" "AI 协作" "完成定义"; do
    if contains_pattern "$heading" "$ENGINEERING_GUIDANCE"; then
      ok "工程约束正文包含：$heading"
    else
      warn "工程约束正文缺少章节：$heading"
    fi
  done
fi

echo
echo "--- 3. 模板占位符 ---"
SCAN_PATHS=("$TARGET/README.md" "$TARGET/AGENTS.md")
[[ -s "$TARGET/CLAUDE.md" ]] && SCAN_PATHS+=("$TARGET/CLAUDE.md")
[[ -d "$TARGET/docs" ]] && SCAN_PATHS+=("$TARGET/docs")
if contains_pattern '【填写|\[TODO|\[TBD|\[项目名称\]|\[补全\]' "${SCAN_PATHS[@]}"; then
  blocked "发现未替换模板占位符"
else
  ok "未发现常见模板占位符"
fi

echo
echo "--- 4. 核心可复核证据 ---"
check_nonempty "$TARGET/README.md" "README"

if [[ -s "$TARGET/README.md" ]]; then
  for clue in "安装|依赖|pip install|npm install|pnpm install" "运行|启动|python3 |npm run|pnpm " "测试|pytest|unittest|playwright|npm test"; do
    if contains_pattern "$clue" "$TARGET/README.md"; then
      ok "README 包含复现线索：$clue"
    else
      warn "README 缺少复现线索：$clue"
    fi
  done
fi

SPEC="$(find_first_nonempty "$TARGET/docs/spec.md" "$TARGET/docs/prd.md" "$TARGET/docs/diagnosis/problem-diagnosis.md" 2>/dev/null || true)"
DESIGN="$(find_first_nonempty "$TARGET/docs/design.md" "$TARGET/docs/design/end-to-end-system-design.md" 2>/dev/null || true)"
AI_LOG="$(find_first_nonempty "$TARGET/docs/ai-log.md" "$TARGET/docs/ai/ai-collaboration-log.md" 2>/dev/null || true)"
TEST_RECORD="$(find_first_nonempty "$TARGET/docs/test-record.md" "$TARGET/docs/test-strategy.md" "$TARGET/docs/validation/cases-and-results.md" 2>/dev/null || true)"

[[ -n "$SPEC" ]] && ok "找到范围/验收证据：$SPEC" || blocked "docs/ 中缺少 spec.md、prd.md 或问题诊断等范围证据"
[[ -n "$DESIGN" ]] && ok "找到设计证据：$DESIGN" || blocked "docs/ 中缺少 design.md 或端到端设计证据"
[[ -n "$AI_LOG" ]] && ok "找到 AI 协作证据：$AI_LOG" || blocked "docs/ 中缺少 AI 协作日志"
[[ -n "$TEST_RECORD" ]] && ok "找到测试实际结果：$TEST_RECORD" || blocked "docs/ 中缺少测试记录或执行结果"

if [[ -n "$SPEC" ]]; then
  for section in "目标" "非目标" "验收|成功标准" "边界|失败"; do
    if contains_pattern "$section" "$SPEC"; then
      ok "范围证据包含：$section"
    else
      warn "范围证据可能缺少：$section"
    fi
  done
fi

if [[ -n "$DESIGN" ]]; then
  for section in "数据流|流程" "模块|接口" "取舍|选择|为什么" "失败|异常|风险"; do
    if contains_pattern "$section" "$DESIGN"; then
      ok "设计证据包含：$section"
    else
      warn "设计证据可能缺少：$section"
    fi
  done
fi

if [[ -n "$AI_LOG" ]]; then
  for field in "目的|AI 目标" "输入|输入材料" "建议|AI 输出" "人工判断" "验证|实际影响|影响"; do
    if contains_pattern "$field" "$AI_LOG"; then
      ok "AI 日志包含字段：$field"
    else
      warn "AI 日志可能缺少字段：$field"
    fi
  done
fi

echo
echo "--- 5. 模式专属证据 ---"
if [[ "$MODE" == "personal" ]]; then
  TASKS="$(find_first_nonempty "$TARGET/docs/tasks.md" 2>/dev/null || true)"
  REFLECTION="$(find_first_nonempty "$TARGET/docs/reflection.md" "$TARGET/docs/reflection/individual-reflection.md" 2>/dev/null || true)"
  [[ -n "$TASKS" ]] && ok "找到任务拆分：$TASKS" || warn "docs/ 中缺少 tasks.md；如题目未要求，需在工程约束中说明替代文件"
  [[ -n "$REFLECTION" ]] && ok "找到个人复盘：$REFLECTION" || warn "docs/ 中缺少 reflection.md；如题目未要求，需说明"
else
  TEAM_FILES=(
    "docs/diagnosis/problem-diagnosis.md"
    "docs/diagnosis/clarifying-questions.md"
    "docs/diagnosis/assumptions-and-non-goals.md"
    "docs/options/solution-options.md"
    "docs/options/tradeoff-matrix.md"
    "docs/options/rejected-options.md"
    "docs/ai/ai-collaboration-log.md"
    "docs/ai/accepted-and-rejected-ai-advice.md"
    "docs/collaboration/role-division.md"
    "docs/collaboration/meeting-minutes.md"
    "docs/collaboration/decision-log.md"
    "docs/collaboration/issue-log.md"
    "docs/decision/decision-memo.md"
    "docs/decision/final-recommendation.md"
    "docs/design/end-to-end-system-design.md"
    "docs/validation/validation-plan.md"
    "docs/validation/cases-and-results.md"
    "docs/validation/review-record.md"
    "docs/validation/risk-and-edge-cases.md"
    "docs/reflection/individual-contributions.md"
    "docs/reflection/team-retrospective.md"
    "docs/defense/defense-outline.md"
    "docs/prototype/prototype-readme.md"
    "docs/prototype/screenshots-or-video.md"
  )
  for rel in "${TEAM_FILES[@]}"; do
    if [[ -s "$TARGET/$rel" ]]; then
      ok "团队证据：$rel"
    else
      blocked "团队证据缺失或为空：$rel"
    fi
  done
fi

echo
echo "--- 6. 结果真实性提示 ---"
if [[ -n "$TEST_RECORD" ]] && contains_pattern '实际输出|实际结果|执行结果' "$TEST_RECORD"; then
  ok "测试证据包含实际结果字段"
else
  warn "测试证据可能只有计划，没有实际结果字段"
fi

if [[ -n "$TEST_RECORD" ]] && contains_pattern '全部通过' "$TEST_RECORD" && ! contains_pattern '实际输出|实际结果|执行结果' "$TEST_RECORD"; then
  warn "测试记录只声明全部通过，但缺少实际结果字段"
else
  ok "通过声明未替代测试实际结果"
fi

echo
echo "========================================"
echo "汇总：PASS=$PASS WARNING=$WARN BLOCKED=$BLOCKED"
if (( BLOCKED > 0 )); then
  echo "评级：BLOCKED"
  exit 2
elif (( WARN > 0 )); then
  echo "评级：WARNING"
  exit 1
else
  echo "评级：PASS"
  exit 0
fi
