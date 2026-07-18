# Design — RAG 课程助手

## 1. 逻辑视图

### 1.1 组件职责

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐     ┌────────────────┐
│  main.py │────▶│ retrieve.py  │────▶│  answer.py   │────▶│ mock_server.py │
│ CLI 入口  │     │ 切片 + 检索   │     │ Prompt 拼接   │     │ LLM 生成回答    │
└──────────┘     └──────────────┘     └──────────────┘     └────────────────┘
```

| 组件 | 职责 | 不负责 |
|------|------|--------|
| `main.py` | CLI 入口，读取文件，串联流程，处理空输入，输出结果 | 不做检索逻辑，不做 Prompt 构建 |
| `retrieve.py` | 切片（按 `## [faq-XX]`）、关键词匹配、同义词替换、命中评分、排序 | 不调用 LLM，不生成回答 |
| `answer.py` | 拼接 Prompt（系统指令 + chunks + 用户问题），调用 LLM，解析返回结果 | 不做检索 |
| `mock_server.py` | 接收 OpenAI 格式请求，基于关键词匹配生成回答（已有实现） | 不做切片，不做检索排序 |

### 1.2 设计决策

**切片放在 retrieve.py 内部**：切片是检索的前置步骤，属于检索模块的内部实现。main.py 只传入 `course-faq.md` 的原始字符串，retrieve.py 内部完成切片和检索。这样 main.py 的职责更纯粹——只做流程编排。

**同义词表放在 retrieve.py 内部**：作为模块级常量 `SYNONYMS`，规模小（<10 条映射），不单独建文件。

---

## 2. 流程视图

### 2.0 RAG 六环节数据流（对照 faq-05）

| 环节 | 输入 | 输出 | 实现位置 |
|------|------|------|---------|
| **① 资料源** | `data/course-faq.md` 文件路径 | 原始 Markdown 字符串 | `main.py`：读取文件 |
| **② 切片** | 原始 Markdown 字符串 | `list[Chunk]`（10 个，含 id/title/content） | `retrieve.py`：按 `\n## [faq-XX]` 分割 |
| **③ 检索** | 用户问题 + chunk 列表 | top3 chunk 列表（按分数降序） | `retrieve.py`：关键词匹配 + 评分 + 排序 |
| **④ Prompt 拼接** | 系统指令 + top3 chunks + 用户问题 | 完整 Prompt（发送给 LLM） | `answer.py`：拼接 system/user message |
| **⑤ 来源引用** | retrieve 返回的 chunk id 列表 | `sources: ["[faq-02]"]` | `answer.py`：从 chunk id 直接取 |
| **⑥ 资料外拒答** | retrieve 零命中 或 mock 判断资料外 | 拒答文本 | `main.py`（零命中）/ `mock_server.py`（有命中但资料外） |

### 2.1 主流程

```
用户输入（CLI 参数）
  │
  ▼
[空输入判断]
  │
  ├── 空 ──▶ 输出"请输入您的问题" ──▶ 结束
  │
  ▼ 非空
[超长截断] 超过 200 字符 → 截断至 200 字符
  │
  ▼
[读取 data/course-faq.md]
  │
  ▼
[retrieve(question, faq_content)]
  │   内部：切片 → 关键词匹配 → 同义词替换 → 评分 → 排序 → top3
  │
  ├── 返回空列表 [] ──▶ 输出"资料中没有找到依据" ──▶ 结束
  │
  ▼ 返回 top3 chunks
[answer(question, chunks)]
  │   内部：拼接 Prompt → 调用 mock LLM → 解析返回
  │
  ▼
[输出回答 + 来源编号]
```

### 2.2 检索子流程（retrieve.py 内部）

```
输入：question（用户问题）、faq_content（原始 Markdown）
  │
  ▼
[切片] 按 \n## [faq-XX] 分割，提取 id / title / content
  │
  ▼
[同义词替换] 对 question 做子串替换（按 SYNONYMS 映射表）
  │
  ▼
[关键词分词] 对 question 按标点和空格分词，去停用词（的、是、了、什么、怎么、和、有、吗、呢）
  │
  ▼
[关键词匹配] 对每个 chunk 的 title + content 拼接文本做子串包含匹配（`in`），每命中一个关键词 +1 分
  │
  ▼
[排序] 按 score 降序，取 top3（score=0 的丢弃）
  │
  ▼
输出：list[dict] 或 []
```

### 2.3 回答子流程（answer.py 内部）

```
输入：question（用户问题）、chunks（retrieve 的返回结果）
  │
  ▼
[拼接 Prompt]
  │  system: "你是一个课程助手，只基于以下资料回答，必须注明来源编号。资料外问题请回答'资料中没有找到依据'。"
  │  user:   chunks 内容 + 用户问题
  │
  ▼
[调用 LLM] POST http://localhost:9876/v1/chat/completions
  │
  ▼
[组装返回]
  │  answer:  直接使用 mock 返回的文本（不做二次拒答判断）
  │  sources: 从 retrieve 结果中取 chunk id（不从 LLM 文本中提取）
  │
  ▼
输出：{"answer": "...", "sources": ["[faq-02]"]}
```

**拒答路径说明**：answer.py 不做额外的拒答判断，直接透传 mock 返回的内容。拒答由两条路径分别处理：
- retrieve 零命中 → main.py 直接输出拒答，不调 answer
- retrieve 有命中但 mock 判断资料外 → mock 返回拒答文本，answer.py 原样透传

**sources 来源**：sources 字段直接取 retrieve 返回结果中的 chunk id（方案 A），不依赖 mock 输出格式，保证可靠性。

### 2.4 边界场景示例

**场景 A：资料外 → 零命中拒答**

```
输入："奖学金政策是什么？"
  → retrieve: "奖学金""政策"均未命中任何 chunk → 返回 []
  → main.py: 直接输出"资料中没有找到依据"
  → 不调用 answer，不调用 mock
```

**场景 B：混淆类 → mock 自身拒答**

```
输入："说一个 Day1 没有教的内容"
  → retrieve: "Day1"命中 faq-05（RAG 原理）、faq-06（工具链）等 → 返回 top3
  → answer: 将 top3 chunks + 问题发给 mock
  → mock: 自身关键词白名单检测，判断为资料外 → 返回"资料中没有找到依据"
  → answer: 原样透传 mock 返回文本，sources 取 retrieve 的 chunk id
```

---

## 3. 接口标准

### 3.1 retrieve(question: str, chunks: str) -> list

```python
def retrieve(question: str, chunks: str) -> list:
    """
    检索相关 FAQ 条目。

    Args:
        question: 用户问题，如 "Day1要交什么？"
        chunks:   course-faq.md 的原始内容（完整字符串）

    Returns:
        list[dict]，按 score 降序，最多 3 条。每条结构：
        {
            "id":      str,   # "faq-02"
            "title":   str,   # "6 类证据文件分别是什么？"
            "content": str,   # 完整 FAQ 内容（含 Markdown）
            "score":   float  # 命中分数
        }
        零命中返回空列表 []

    边界情况：
        question 为空字符串 → 返回空列表 []
        chunks 为空字符串或空列表 → 返回空列表 []
    """
```

### 3.2 answer(question: str, chunks: list) -> dict

```python
def answer(question: str, chunks: list) -> dict:
    """
    基于检索结果生成回答。

    Args:
        question: 用户问题
        chunks:   retrieve() 返回的结果列表

    Returns:
        {
            "answer":  str,   # LLM 生成的回答文本
            "sources": list   # ["[faq-02]", "[faq-01]"]
        }

    边界情况：
        chunks 为空列表 → 返回 {"answer": "资料中没有找到依据。", "sources": []}
        question 为空字符串 → 正常调用 LLM（由 main.py 层拦截，不会走到这里）
    """
```

### 3.3 CLI 调用约定

```bash
# 正常调用
python3 src/main.py "Day1要交什么？"

# 空输入
python3 src/main.py ""
# 输出: 请输入您的问题

# 资料外
python3 src/main.py "奖学金政策？"
# 输出: 资料中没有找到依据。

# 超长输入（超过 200 字符）
python3 src/main.py "（很长的问题...）"
# 截断至 200 字符后正常处理，不报错
```

---

## 4. 数据结构

### 4.1 Chunk（切片后的 FAQ 单元）

```python
{
    "id":      "faq-01",
    "title":   "什么是"可复核交付"？",
    "content": "完整 Markdown 内容..."
}
```

### 4.2 同义词表（SYNONYMS）

```python
SYNONYMS = {
    "要交": "提交",
    "五字段": "五个字段",
    "五步": "五步法",
}
```

### 4.3 停用词表（STOP_WORDS）

```python
STOP_WORDS = {"的", "是", "了", "什么", "怎么", "和", "有", "吗", "呢"}
```

分词后过滤掉停用词，剩余词作为检索关键词。停用词表可在实现阶段根据测试结果微调。

---

## 5. 技术约束

| 约束 | 说明 |
|------|------|
| LLM 后端 | `mock_server.py`，端口 9876，兼容 OpenAI Chat Completions API |
| 外部依赖 | 仅 Python 标准库（`json`, `re`, `sys`, `os`, `urllib`） |
| 数据源 | 仅 `data/course-faq.md`，10 条 FAQ |
| 切片方式 | 按 `\n## [faq-XX]` 正则分割 |
| 检索方式 | 关键词匹配 + 手动同义词表，无向量/语义搜索 |

---

## 6. 备注：FAQ 规模扩展思考

**问题**：如果 FAQ 从 10 条增加到 100 条，当前的关键词匹配策略需要怎么调整？

| 维度 | 当前（10 条） | 扩展到 100 条后的问题 | 调整方向 |
|------|-------------|---------------------|---------|
| **切片** | 按 `##` 标题切，10 个 chunk | chunk 数量增长 10 倍，但切片逻辑不变 | 无需调整，按标题切仍然有效 |
| **检索** | 遍历所有 chunk 做关键词匹配，O(n) | 100 条遍历仍然很快（<1ms），性能不是瓶颈 | 无需调整，线性遍历足够 |
| **同义词表** | 手动维护 3 条映射 | 100 条 FAQ 覆盖更多术语，手动维护成本上升 | 考虑引入自动同义词扩展或 TF-IDF 权重 |
| **停用词** | 手动维护 9 个停用词 | 问题类型更多样，停用词表需要扩充 | 根据测试结果逐步扩充 |
| **Top-K** | 固定 top3 | 100 条中可能有更多相关 chunk，top3 可能遗漏 | 可调整为 top5 或动态 K |
| **评分** | 每命中一个关键词 +1 分（平权） | 不同关键词的区分度差异变大（"RAG" vs "的"） | 引入 TF-IDF 或 IDF 权重，稀有词权重更高 |
| **拒答** | 零命中拒答 | 可能出现"勉强命中 1 个词但不相关"的情况 | 需要引入分数阈值拒答（当前规模下不需要） |

**结论**：10 条到 100 条的扩展，切片和检索算法本身不需要重构，核心调整在**评分权重**（引入 IDF）和**拒答策略**（从零命中升级为分数阈值）。当前 MVP 阶段不做这些调整，保持关键词匹配的简单性。
