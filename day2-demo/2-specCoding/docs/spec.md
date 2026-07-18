# Spec — Day2 学习任务清单助手

## 一、目标

| 命令 | 输入 | 输出 |
|------|------|------|
| `python cli.py today` | 无 | 返回 Day2 任务列表（5 个文件名 + 简要描述） |
| `python cli.py submit <文件名>` | 文件名（如 README.md） | 确认该文件已标记为已提交 |
| `python cli.py check` | 无 | 返回尚未提交的文件清单 |

**任务清单**（固定）：
- `spec.md` — 需求规格
- `plan.md` — 技术设计
- `tasks.md` — 任务拆解
- `README.md` — 项目说明
- `ai-log.md` — AI 协作日志

**存储方式**：本地 JSON 文件（`status.json`），记录每个文件的提交状态

---

## 二、非目标

1. **不做 GUI** —— 纯命令行工具
2. **不做远程存储** —— 数据存在本地，不联网
3. **不做任务编辑** —— 任务列表固定，不支持增删改

---

## 三、边界条件

| 场景 | 处理方式 |
|------|----------|
| `submit` 一个不在任务列表中的文件 | 提示"该文件不在任务清单中" |
| `submit` 一个已经提交过的文件 | 提示"该文件已提交"，不重复标记 |
| `check` 时所有文件都已提交 | 提示"全部完成！" |
| 首次运行（`status.json` 不存在） | 自动初始化，所有文件标记为未提交 |
| `status.json` 文件损坏 | 提示错误并重新初始化 |

---

## 四、验收标准

| # | 命令 | 期望结果 |
|---|------|----------|
| 1 | `python cli.py today` | 输出 5 个文件名及描述 |
| 2 | `python cli.py submit spec.md` | 提示"spec.md 已提交" |
| 3 | `python cli.py check` | 列出剩余 4 个未提交文件 |
| 4 | `python cli.py submit spec.md`（重复） | 提示"spec.md 已提交过" |
| 5 | `python cli.py submit fake.txt` | 提示"fake.txt 不在任务清单中" |
| 6 | 全部提交后 `python cli.py check` | 提示"全部完成！" |
