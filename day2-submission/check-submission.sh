#!/usr/bin/env bash
set -u

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
PASS=0
BLOCKED=0

pass() { printf '✅ %s\n' "$1"; PASS=$((PASS + 1)); }
block() { printf '❌ %s\n' "$1"; BLOCKED=$((BLOCKED + 1)); }

check_file() {
  if [ -f "$1" ]; then pass "$1"; else block "缺少文件：$1"; fi
}

check_terms() {
  local file="$1"
  shift
  local missing=""
  for term in "$@"; do
    grep -q "$term" "$file" 2>/dev/null || missing="$missing $term"
  done
  if [ -z "$missing" ]; then pass "$file 内容字段"; else block "$file 缺少:$missing"; fi
}

run_test() {
  local label="$1"
  shift
  if "$@"; then pass "$label"; else block "$label"; fi
}

printf '=== Day2 mission 文件检查 ===\n'
for file in \
  README.md ai-log.md reflection.md \
  01-submission-workflow/ai-workflow.md \
  02-task-assistant/spec.md 02-task-assistant/plan.md 02-task-assistant/tasks.md \
  02-task-assistant/AGENTS.md 02-task-assistant/cli.py \
  02-task-assistant/eval-cases.json 02-task-assistant/test-record.md \
  02-task-assistant/context-pack.md \
  03-learning-demo/learning-record.md 03-learning-demo/demo.py \
  03-learning-demo/test-record.md 03-learning-demo/peer-review.md \
  04-training-agent/agent-design.md 04-training-agent/review-checklist.md; do
  check_file "$file"
done

printf '\n=== 课程规范检查 ===\n'
check_terms README.md 安装 运行 测试 环境要求 项目结构 约束 故障排查
check_terms ai-log.md 目的 输入 建议 人工判断 验证
check_terms reflection.md 今天最大的认知变化 今天最困难的地方 如果再学一遍
check_terms 02-task-assistant/AGENTS.md 可调用命令 何时 范围外 工具失败
check_terms 04-training-agent/agent-design.md 数据流 工具定义 校验规则 测试用例

if [ "$(grep -c '^## 第' ai-log.md)" -ge 7 ]; then pass "根 AI 日志不少于 7 条"; else block "根 AI 日志不足 7 条"; fi
if [ "$(grep -Ec '^\| [1-6] \|' 04-training-agent/review-checklist.md)" -ge 6 ]; then pass "代码审查覆盖六类风险"; else block "代码审查 finding 不足"; fi
if python3 -m json.tool 02-task-assistant/eval-cases.json >/dev/null; then pass "eval-cases.json 语法"; else block "eval-cases.json 非法"; fi
for type in 正确回答 范围外拒答 工具失败; do
  grep -q "$type" 02-task-assistant/eval-cases.json && pass "Eval 类型：$type" || block "Eval 缺少类型：$type"
done

printf '\n=== 自动测试 ===\n'
run_test "工作流测试（5 条）" python3 -m unittest discover -s 01-submission-workflow/tests -v
run_test "任务助手测试（8 条）" python3 -m unittest discover -s 02-task-assistant/tests -v
if [ -x .venv/bin/python ]; then
  run_test "LangChain Demo 测试（4 条）" .venv/bin/python -m unittest discover -s 03-learning-demo/tests -v
else
  block "缺少 .venv；请先按 README 安装 Demo 依赖"
fi
run_test "训练营 Agent 工具测试（13 条）" python3 -m unittest discover -s 04-training-agent/tests -v

printf '\n=== 提交卫生 ===\n'
if git ls-files | grep -Eq '(^|/)(\.env|\.DS_Store|__pycache__)(/|$)|\.pyc$'; then
  block "Git 跟踪了敏感或缓存文件"
else
  pass "未跟踪 .env/.DS_Store/缓存"
fi
if git grep -En 'sk-[A-Za-z0-9]{16,}|PRIVATE KEY|ACCESS_TOKEN=' -- ':!docs/superpowers/**' ':!check-submission.sh' >/dev/null 2>&1; then
  block "发现疑似真实凭证模式"
else
  pass "未发现真实凭证模式"
fi
if git grep -En '待定|待填写|以后补' -- ':!docs/superpowers/**' ':!check-submission.sh' >/dev/null 2>&1; then
  block "发现未完成占位内容"
else
  pass "无未完成占位内容"
fi

printf '\n=== 汇总 ===\n'
if [ "$BLOCKED" -gt 0 ]; then
  printf '评级: BLOCKED（%d 项阻塞，%d 项通过）\n' "$BLOCKED" "$PASS"
  exit 2
fi
printf '评级: PASS（%d 项通过，0 项阻塞）\n' "$PASS"
