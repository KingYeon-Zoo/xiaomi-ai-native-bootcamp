#!/usr/bin/env bash
# 审计脚本回归测试：合规个人项目应通过，docs 外过程 Markdown 应阻断。

set -u

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
AUDIT="$SCRIPT_DIR/audit-xiaomi-project.sh"
FIXTURE="$(mktemp -d "${TMPDIR:-/tmp}/xiaomi-audit-test.XXXXXX")"
trap 'rm -rf "$FIXTURE"' EXIT

write_md() {
  local path="$1"
  local content="$2"
  mkdir -p "$(dirname "$path")"
  printf '%s\n' "$content" > "$path"
}

write_md "$FIXTURE/README.md" '# 测试项目

## 安装
pip install -r requirements.txt

## 运行
python3 src/main.py

## 测试
pytest'

write_md "$FIXTURE/AGENTS.md" '# 项目入口

开始工作前必须读取 docs/engineering-constraints.md。'

write_md "$FIXTURE/docs/engineering-constraints.md" '# 项目工程约束

## 文档目录规范
过程 Markdown 全部放入 docs。

## 资料优先级
题目优先。

## 目标与非目标
目标可验证，非目标主动收窄。

## 阶段门禁
先文档后代码。

## 运行与验证命令
使用 README 命令。

## 验收证据映射
验收映射到测试记录。

## AI 协作
记录人工判断。

## 完成定义
PASS 表示命令和证据全部通过。'

write_md "$FIXTURE/docs/prd.md" '# PRD

## 目标
完成主路径。

## 非目标
不做登录。

## 验收标准
输入示例得到预期输出。

## 边界条件
处理空输入。'

write_md "$FIXTURE/docs/design.md" '# Design

## 数据流
输入到处理再到输出。

## 模块与接口
主模块提供命令行接口。

## 取舍
选择最小方案，因为两天内可验证。

## 失败与风险
空输入返回错误。'

write_md "$FIXTURE/docs/ai-log.md" '# AI Log

| 目的 | 输入 | 建议 | 人工判断 | 验证 |
|---|---|---|---|---|
| 审查范围 | PRD | 增加登录 | 拒绝，超出非目标 | 检查 PRD |'

write_md "$FIXTURE/docs/test-record.md" '# 测试记录

| 输入 | 预期输出 | 实际输出 | 结果 |
|---|---|---|---|
| 示例 | 成功 | 成功 | 通过 |'

write_md "$FIXTURE/docs/tasks.md" '# 任务拆分

- [x] 主路径；验证：pytest'

write_md "$FIXTURE/docs/reflection.md" '# 个人复盘

拒绝登录功能，因为它超出两天 MVP 范围。'

set +e
output="$(bash "$AUDIT" "$FIXTURE" personal 2>&1)"
audit_rc=$?
set -e
if [[ "$audit_rc" -ne 0 ]]; then
  printf '%s\n' "$output"
  echo "测试失败：合规个人项目应返回 PASS（退出码 0），实际退出码为 $audit_rc"
  exit 1
fi

write_md "$FIXTURE/tasks.md" '# 错误位置的任务拆分'
set +e
output="$(bash "$AUDIT" "$FIXTURE" personal 2>&1)"
audit_rc=$?
set -e
if [[ "$audit_rc" -ne 2 ]]; then
  printf '%s\n' "$output"
  echo "测试失败：docs 外过程 Markdown 应返回 BLOCKED（退出码 2），实际退出码为 $audit_rc"
  exit 1
fi

echo "审计脚本回归测试通过"
