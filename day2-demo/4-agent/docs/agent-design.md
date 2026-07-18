# Agent Design — 训练营助教 AGENT

## 一、架构图

```
用户输入
    │
    ▼
┌─────────┐
│  Agent  │  ← CLAUDE.md 编排（路由 + 结果校验 + 失败处理）
└────┬────┘
     │
     ▼
┌──────────┐
│  Router  │  LLM 根据用户意图 + 工具描述，自行决定调用哪个工具
└────┬────┘
     │
     ├──→ RAG 检索 ──→ 结果校验 ──→ 生成回答
     │
     ├──→ 学习管理 ──→ 结果校验 ──→ 返回状态
     │
     └──→ 提交校验 ──→ 结果校验 ──→ 返回报告
```

---

## 二、工具定义

### 2.1 RAG 检索工具

从课程知识文件中检索相关信息，拼入 prompt 生成回答。

**输入：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `query` | string | 用户问题 |

**输出：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `answer` | string | 基于检索结果的回答 |
| `sources` | string[] | 命中的知识条目编号（如 `[faq-02]`） |

**失败处理：**

| 场景 | 处理 |
|------|------|
| 关键词零命中 | 拒绝回答，输出"资料中没有找到依据" |
| query 为空 | 输出"请输入您的问题" |
| query 超长（>200 字符） | 截断至 200 字符后继续处理 |

**边界：**

- 不做语义检索，仅关键词匹配
- 知识库固定为 `course-faq.md` 的 10 条 FAQ
- 不接真实 LLM，回答基于检索到的 chunk 拼接

---

### 2.2 学习管理工具

管理 Day2 学习任务清单，支持查看、提交、检查。

**命令：**

| 命令 | 输入 | 输出 |
|------|------|------|
| `today` | 无 | 返回 Day2 任务列表（5 个文件名 + 描述） |
| `submit <文件名>` | 文件名 | 确认该文件已标记为已提交 |
| `check` | 无 | 返回尚未提交的文件清单 |

**失败处理：**

| 场景 | 处理 |
|------|------|
| submit 不在任务列表中的文件 | 提示"该文件不在任务清单中" |
| submit 已提交过的文件 | 提示"该文件已提交过" |
| status.json 不存在 | 自动初始化，所有文件标记为未提交 |
| status.json 损坏 | 提示错误并重新初始化 |
| check 时全部提交 | 提示"全部完成！" |

**边界：**

- 任务列表固定（spec.md / plan.md / tasks.md / README.md / ai-log.md），不支持增删改
- 单用户设计，不支持团队协作
- 不记录历史，只显示当前状态

---

### 2.3 提交校验工具

检查 Day2 作业的提交完整性，校验文件存在性和内容质量。

**输入：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `project_dir` | string | 待检查项目目录 |

**输出：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | PASS / WARNING / BLOCKED |
| `missing_files` | string[] | 缺失的必需文件 |
| `warnings` | string[] | 轻量质量警告 |
| `details` | object | 各项检查的详细结果 |

**检查项：**

| 文件 | 检查内容 |
|------|----------|
| README.md | 文件存在 + 包含安装/运行/测试相关文本 |
| agent-design.md | 文件存在 + 包含架构图、工具定义、测试用例 |
| ai-log.md | 文件存在 + 包含"目的""输入""建议""人工判断""验证"五个标签 |
| 测试文件 | 文件存在 + pytest 可运行 |

**状态判定：**

| 条件 | 状态 |
|------|------|
| 全部文件存在，内容检查通过 | PASS |
| 全部文件存在，但有内容质量警告 | WARNING |
| 任一文件缺失或不可读 | BLOCKED |

**失败处理：**

| 场景 | 处理 |
|------|------|
| 项目目录不存在 | BLOCKED，提示"项目目录不存在" |
| 文件缺失 | BLOCKED，在 missing_files 中列出 |
| pytest 运行失败 | BLOCKED，记录错误输出 |
| README 内容不足 | WARNING，提示补充 |

---

## 三、结果校验流程

工具调用后，Agent 不能直接使用返回值，必须先执行结果校验：

```
工具返回结果
    │
    ▼
┌──────────────┐
│ 结果是否为空？ │──→ 是 → 返回兜底话术
└──────┬───────┘
       │ 否
       ▼
┌──────────────┐
│ 是否包含错误？ │──→ 是 → 转译为人话，不展示堆栈
└──────┬───────┘
       │ 否
       ▼
┌──────────────┐
│ 结果是否完整？ │──→ 否 → 提示信息不足，建议补充
└──────┬───────┘
       │ 是
       ▼
   使用结果生成回答
```

**校验规则：**

| 工具 | 空结果处理 | 错误处理 | 完整性检查 |
|------|-----------|----------|-----------|
| RAG 检索 | "资料中没有找到依据" | 不适用（无外部调用） | 结果必须包含至少一个来源编号 |
| 学习管理 | "未获取到任务信息" | 转译错误为人话 | today 必须返回文件列表，check 必须返回状态 |
| 提交校验 | "无法完成校验" | 记录错误详情 | status 必须是 PASS/WARNING/BLOCKED 之一 |

---

## 四、路由规则

CLAUDE.md 定义工具描述，LLM 根据用户意图自行决策调用哪个工具。

**工具描述（写入 CLAUDE.md）：**

| 工具 | 描述 | 典型触发意图 |
|------|------|-------------|
| RAG 检索 | 从课程 FAQ 中检索信息回答问题 | "Day1 要交什么？""什么是可复核交付？" |
| 学习管理 | 管理 Day2 任务清单 | "今天要做什么？""提交 spec.md""还剩什么？" |
| 提交校验 | 检查作业提交完整性 | "帮我检查一下作业""可以提交了吗？" |

**范围外拒答：**

| 请求类型 | 拒答话术 |
|----------|----------|
| 非训练营相关问题 | "我是训练营助教，只处理课程相关请求" |
| 编辑/删除任务列表 | "本工具只支持查看和提交，不支持编辑任务列表" |
| 查询奖学金/政策 | "资料中没有找到依据" |

---

## 五、CLAUDE.md 编排设计

CLAUDE.md 包含以下内容：

```markdown
# 训练营助教 AGENT

## 人设
你是训练营助教 AGENT，帮助学生管理 Day2 学习任务、检索课程资料、校验作业提交。

## 可用工具

### RAG 检索
- 用途：从课程 FAQ 中检索信息
- 输入：用户问题
- 输出：回答 + 来源编号
- 边界：仅关键词匹配，无关问题拒答

### 学习管理
- 用途：管理 Day2 任务清单
- 命令：today / submit <文件名> / check
- 边界：任务列表固定，不支持编辑

### 提交校验
- 用途：检查作业提交完整性
- 检查项：README、agent-design、ai-log、测试文件
- 输出：PASS / WARNING / BLOCKED

## 工具调用流程
1. 理解用户意图
2. 选择合适的工具
3. 调用工具获取结果
4. **结果校验**（必选）：
   - 结果是否为空？→ 返回兜底话术
   - 是否包含错误？→ 转译为人话
   - 结果是否完整？→ 提示补充
5. 使用校验通过的结果生成回答

## 范围外拒答
- 非训练营相关 → "我是训练营助教，只处理课程相关请求"
- 编辑任务列表 → "本工具只支持查看和提交"
- 课程资料无关 → "资料中没有找到依据"

## 工具失败处理
- 工具不存在或调用失败 → "工具暂时不可用，请稍后重试"
- 未知命令 → "请使用 today / submit / check 命令"
```

---

## 六、测试用例

### 6.1 正确回答

| # | 用户输入 | 期望工具 | 期望输出 |
|---|---------|----------|----------|
| 1 | "Day1 要交什么？" | RAG 检索 | 包含 6 类证据文件描述，来源 [faq-02] |
| 2 | "什么是可复核交付？" | RAG 检索 | 包含"助教""独立判断""证据"，来源 [faq-01] |
| 3 | "今天要做什么？" | 学习管理 | 输出 5 个文件名及描述 |
| 4 | "提交 spec.md" | 学习管理 | 提示"spec.md 已提交" |
| 5 | "还剩什么没交？" | 学习管理 | 列出未提交文件 |
| 6 | "帮我检查作业" | 提交校验 | 输出 PASS/WARNING/BLOCKED 状态 |

### 6.2 范围外拒答

| # | 用户输入 | 期望输出 |
|---|---------|----------|
| 7 | "奖学金政策是什么？" | "资料中没有找到依据" |
| 8 | "帮我删掉任务列表里的文件" | "本工具只支持查看和提交，不支持编辑任务列表" |
| 9 | "今天天气怎么样？" | "我是训练营助教，只处理课程相关请求" |

### 6.3 工具失败 / 边界

| # | 用户输入 | 场景 | 期望输出 |
|---|---------|------|----------|
| 10 | ""（空输入） | RAG 空查询 | "请输入您的问题" |
| 11 | 提交 fake.txt | 文件不在列表 | "该文件不在任务清单中" |
| 12 | 重复提交 spec.md | 已提交过 | "该文件已提交过" |
| 13 | 超长输入（>200 字符） | RAG 超长 query | 截断后正常处理，不报错 |

### 6.4 pytest 测试文件

```python
# test_tools.py
import pytest
import json
import os

# === RAG 工具测试 ===

def test_rag_normal_query():
    """正常查询应返回回答和来源"""
    result = rag_search("Day1要交什么？")
    assert result["success"] is True
    assert "faq-" in str(result["sources"])

def test_rag_empty_query():
    """空查询应返回提示"""
    result = rag_search("")
    assert "请输入" in result["answer"]

def test_rag_no_match():
    """无关查询应拒答"""
    result = rag_search("奖学金政策")
    assert "没有找到依据" in result["answer"]

def test_rag_long_query():
    """超长查询应截断处理"""
    long_query = "a" * 300
    result = rag_search(long_query)
    assert result["success"] is True

# === 学习管理工具测试 ===

def test_task_today(cleanup_status):
    """today 应返回任务列表"""
    result = task_today()
    assert result["success"] is True
    assert len(result["tasks"]) == 5

def test_task_submit_normal(cleanup_status):
    """正常提交应成功"""
    result = task_submit("spec.md")
    assert result["success"] is True
    assert "已提交" in result["message"]

def test_task_submit_not_in_list(cleanup_status):
    """提交不在列表中的文件应失败"""
    result = task_submit("fake.txt")
    assert result["success"] is False
    assert "不在任务清单" in result["message"]

def test_task_submit_duplicate(cleanup_status):
    """重复提交应提示已提交过"""
    task_submit("spec.md")
    result = task_submit("spec.md")
    assert "已提交过" in result["message"]

def test_task_check_all_done(cleanup_status):
    """全部提交后应提示完成"""
    for f in ["spec.md", "plan.md", "tasks.md", "README.md", "ai-log.md"]:
        task_submit(f)
    result = task_check()
    assert "全部完成" in result["message"]

# === 提交校验工具测试 ===

def test_validate_missing_files():
    """缺失文件应返回 BLOCKED"""
    result = validate_submission("/nonexistent")
    assert result["status"] == "BLOCKED"

def test_validate_complete_project(tmp_path):
    """完整项目应返回 PASS 或 WARNING"""
    # 创建必要文件
    (tmp_path / "README.md").write_text("# 项目说明\n安装\n运行\n测试")
    (tmp_path / "agent-design.md").write_text("# Agent Design\n架构图\n工具定义\n测试用例")
    (tmp_path / "ai-log.md").write_text("# AI Log\n目的\n输入\n建议\n人工判断\n验证")
    (tmp_path / "test_tools.py").write_text("def test_pass(): assert True")
    result = validate_submission(str(tmp_path))
    assert result["status"] in ["PASS", "WARNING"]
```

---

## 七、项目结构

```
4-agent/
├── agent-design.md          # 本文件（架构 + 工具定义 + 测试用例）
├── tools/
│   ├── __init__.py
│   ├── rag.py               # RAG 检索工具
│   ├── task_manager.py      # 学习管理工具
│   └── validator.py         # 提交校验工具
├── data/
│   └── course-faq.md        # 课程知识库（沿用 day1）
├── tests/
│   └── test_tools.py        # pytest 测试
└── CLAUDE.md                # Agent 编排配置
```
