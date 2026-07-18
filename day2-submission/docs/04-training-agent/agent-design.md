# Agent Design：训练营助教

## 1. 数据流

```text
User
  ↓ 请求
Router（课程问答 / 任务管理 / 提交检查 / 范围外）
  ↓
RAG Tool 或 Task Tool 或 Submission Tool
  ↓ 结构化结果
Validator（success、空结果、来源、状态、路径边界）
  ↓
Answer（带来源回答 / 人类可读失败 / 固定拒答）
```

Router 只选择工具，不生成事实；工具只返回结构化结果；Validator 是宣布成功前的必经节点；Answer 不补写工具结果中不存在的内容。

## 2. 工具定义

### RAG 检索 `rag_search`

| 项 | 定义 |
|----|------|
| 输入 | `query: str`（非空，最多处理前 200 字）；`faq_path: Path` 可选 |
| 输出 | `{success: bool, answer: str, sources: list[str]}` |
| 正常 | 关键词 bigram/trigram 匹配，最多返回 3 个 FAQ 和来源 |
| 边界 | 空输入失败；无匹配成功返回固定拒答和空来源；不做语义检索 |
| 失败 | 知识库不存在/无合法切片时 `success=false`，提示加载失败 |

### 学习管理 `task_today/task_submit/task_check`

| 项 | 定义 |
|----|------|
| 输入 | today/check 无输入；submit 输入固定任务文件名，大小写不敏感 |
| 输出 | 始终包含 `success`；列表或 `message/remaining` 随命令返回 |
| 正常 | 五个任务的查看、提交和剩余清单 |
| 边界 | 不支持动态清单、历史、团队；重复提交不是新成功 |
| 失败 | 未知文件 `success=false`；损坏状态按五个未提交重新加载 |

### 提交校验 `validate_submission`

| 项 | 定义 |
|----|------|
| 输入 | `project_dir: Path`、`allowed_root: Path` |
| 输出 | `{status, missing_files, warnings, details}` |
| 正常 | 检查 README、agent-design、ai-log 和测试文件及内容线索 |
| 边界 | resolve 后必须位于 allowed_root；只读取固定相对路径 |
| 失败 | 越界、目录不存在或缺文件为 BLOCKED；内容线索不足为 WARNING |

## 3. 校验规则

1. RAG `success=true` 但 `sources=[]` 时只能输出固定拒答，不能说“根据资料”。
2. 任一工具 `success=false` 时不得输出成功，应转译 `answer/message`，不展示堆栈。
3. 提交校验存在 `missing_files` 或路径越界时必须为 BLOCKED，不能降级。
4. task submit 只有 `success=true` 才能告诉用户“已提交”；重复提交要准确说明旧状态。
5. 回答中的来源必须来自工具 `sources`，禁止生成不存在的 FAQ 编号。

## 4. 测试用例

| 类型 | 输入 | 工具结果 | Validator 期望 | 最终回答 |
|------|------|----------|----------------|----------|
| 正常 | “什么是可复核交付？” | success=true，sources 含 faq-01 | 来源非空，通过 | 回答定义并标 `[faq-01]` |
| 资料外 | “奖学金怎么申请？” | success=true，sources=[] | 触发拒答 | “资料中没有找到依据” |
| 工具失败 | FAQ 路径不存在 | success=false | 不输出回答，不展示堆栈 | “课程资料加载失败，请检查 course-faq.md” |
| 正常 | 提交 `spec.md` | success=true | 通过 | “spec.md 已提交” |
| 范围外 | 提交 `secret.txt` | success=false | 不宣布提交 | “不在任务清单中” |
| 安全边界 | 检查 allowed_root 外目录 | status=BLOCKED | 阻塞 | “项目目录超出允许范围” |

## 5. 组件边界与错误策略

工具不返回自然语言之外的堆栈；Validator 不修改工具数据；Answer 不读取磁盘。开发日志应保留异常类型，但用户回复只提供可操作下一步。路径校验在任何文件读取之前完成。
