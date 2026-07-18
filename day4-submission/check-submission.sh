#!/usr/bin/env bash
set -u

ROOT="${1:-.}"
blocked=0

need_file() {
  if [[ -s "$ROOT/$1" ]]; then
    printf 'PASS  %s\n' "$1"
  else
    printf 'BLOCKED  %s 缺失或为空\n' "$1"
    blocked=$((blocked + 1))
  fi
}

for path in README.md AGENTS.md requirements.txt agent_review_report.md docs/engineering-constraints.md docs/test-record.md docs/reflection.md; do
  need_file "$path"
done

for project in project1 project2; do
  for path in spec.md test-strategy.md AI-log.md README.md main.py analysis_report.md; do
    need_file "$project/$path"
  done
done

for path in \
  project1/outputs/structured_logs.csv \
  project1/outputs/error_level_logs.csv \
  project1/outputs/error_state_logs.csv \
  project1/outputs/keyword_logs.csv \
  project1/outputs/error_code_reference.csv \
  project1/charts/daily_error_trend.png \
  project1/charts/error_type_distribution.png \
  project1/charts/module_error_comparison.png \
  project2/outputs/cleaned_data.csv \
  project2/charts/rule_confusion_matrix.png \
  project2/charts/nb_confusion_matrix.png \
  project2/charts/model_metrics_comparison.png \
  project2/charts/word_frequency_comparison.png; do
  need_file "$path"
done

if rg -n '【填写|待执行初次测试|状态：Draft' "$ROOT" --glob '*.md' >/dev/null; then
  printf 'BLOCKED  发现占位或未完成状态\n'
  blocked=$((blocked + 1))
fi

if [[ "$blocked" -gt 0 ]]; then
  printf '总评：BLOCKED（%d 项）\n' "$blocked"
  exit 2
fi

printf '总评：PASS\n'

