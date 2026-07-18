# Task 计划 — RAG 课程助手

> 每个 task 独立可验证，完成后更新 test-record.md，有决策点时更新 ai-log.md。

---

## Phase 1：测试用例开发

### Task 1：编写自动化测试脚本 test_rag.py

**目标**：创建 `tests/test_rag.py`，覆盖 questions.json 的全部 13 个测试用例。

**具体内容**：
- 加载 `tests/questions.json`
- 自动启动 `llm-mock/mock_server.py`（subprocess），等待端口就绪
- 对每个测试用例，执行 `python src/main.py "<question>"`，捕获 stdout
- 根据 `expected_type` 验证：
  - `answer_with_source`：stdout 包含 `expected_keywords` 中的至少一个，且包含 `expected_source`
  - `refuse`：stdout 包含 `expected_keywords` 中的"资料中没有找到依据"
  - `refuse_or_handle`：stdout 包含"资料中没有找到依据"
  - `prompt_input`：stdout 包含"请输入您的问题"
- 对用例 11（超长输入）：验证不报错，stdout 非空
- 对用例 12（纯停用词）：验证 stdout 包含"资料中没有找到依据"
- 测试结束后自动关闭 mock server
- 输出每条用例的 ✅/❌ 结果和汇总

**验证标准**：
- `python tests/test_rag.py` 可运行（即使全部 FAIL，脚本本身不报错）
- 输出 13 条测试结果 + 汇总行

**前置依赖**：无
**后续依赖**：Task 5（集成测试时才能全部 PASS）

---

## Phase 2：框架搭建

### Task 2：创建 src/ 骨架文件

**目标**：创建 `src/retrieve.py`、`src/answer.py`、`src/main.py`，实现空签名。

**具体内容**：
- `src/retrieve.py`：
  ```python
  def retrieve(question, chunks):
      return []
  ```
- `src/answer.py`：
  ```python
  def answer(question, chunks):
      return {"answer": "", "sources": []}
  ```
- `src/main.py`：
  ```python
  import sys
  def main():
      print("Hello from RAG assistant")
  if __name__ == "__main__":
      main()
  ```

**验证命令**：
```bash
python tests/test_basic.py
```

**预期输出**：
```
1. 项目文件检查
  ✅ course-faq.md 存在
  ✅ retrieve.py 存在
  ✅ answer.py 存在
  ✅ main.py 存在

2. 模块加载检查
  ✅ retrieve 模块可加载
  ✅ answer 模块可加载

3. 接口契约检查
  ✅ retrieve() 返回列表
  ✅ answer() 返回 {answer, sources}

4. FAQ 数据检查
    (找到 10 个 FAQ 编号)
  ✅ FAQ 文件包含至少 8 个 [faq-XX] 编号

========================================
结果: 9 通过, 0 失败
========================================
```

**前置依赖**：无
**后续依赖**：Task 3

---

## Phase 3：功能开发（按开发流程：实现 → 验证 → 下一个）

### Task 3：实现 retrieve.py + 验证

**目标**：完成检索模块，能从 course-faq.md 中检索出相关 chunk。

**具体内容**：
- 切片：按 `\n## [faq-XX]` 正则分割，提取 id/title/content
- 同义词表（SYNONYMS）：`{"要交": "提交", "五字段": "五个字段", "五步": "五步法"}`
- 停用词表（STOP_WORDS）：`{"的", "是", "了", "什么", "怎么", "和", "有", "吗", "呢"}`
- 分词：按标点和空格分词，去停用词
- 匹配：对每个 chunk 的 title+content 做子串包含匹配（`in`），每命中 +1 分
- 排序：按 score 降序，取 top3，score=0 丢弃

**验证命令**：
```bash
python -c "
import sys; sys.path.insert(0, '.')
from src.retrieve import retrieve
with open('data/course-faq.md', 'r', encoding='utf-8') as f:
    faq = f.read()

# 用例 1：正确匹配
r = retrieve('Day1要交什么？', faq)
assert len(r) > 0 and r[0]['id'] == 'faq-02', f'Expected faq-02, got {r[0][\"id\"] if r else \"empty\"}'
print('✅ Day1要交什么？ → faq-02')

# 用例 2：正确匹配
r = retrieve('什么是可复核交付？', faq)
assert len(r) > 0 and r[0]['id'] == 'faq-01', f'Expected faq-01, got {r[0][\"id\"] if r else \"empty\"}'
print('✅ 什么是可复核交付？ → faq-01')

# 用例 3：资料外 → 空列表
r = retrieve('奖学金政策？', faq)
assert r == [], f'Expected [], got {r}'
print('✅ 奖学金政策？ → []')

# 用例 4：空输入 → 空列表
r = retrieve('', faq)
assert r == [], f'Expected [], got {r}'
print('✅ 空输入 → []')

# 用例 5：同义词映射
r = retrieve('ai-log的五字段是什么？', faq)
assert len(r) > 0 and r[0]['id'] == 'faq-03', f'Expected faq-03, got {r[0][\"id\"] if r else \"empty\"}'
print('✅ 五字段 → faq-03 (同义词映射生效)')

# 用例 6：纯停用词 → 空列表
r = retrieve('的是了什么怎么', faq)
assert r == [], f'Expected [], got {r}'
print('✅ 纯停用词 → []')

# 用例 7：返回结构
r = retrieve('什么是RAG？', faq)
assert len(r) > 0, 'Expected non-empty result'
assert 'id' in r[0] and 'title' in r[0] and 'content' in r[0] and 'score' in r[0], 'Missing keys'
print('✅ 返回结构包含 id/title/content/score')

print(f'\n全部 7 个 retrieve 验证通过')
"
```

**预期输出**：
```
✅ Day1要交什么？ → faq-02
✅ 什么是可复核交付？ → faq-01
✅ 奖学金政策？ → []
✅ 空输入 → []
✅ 五字段 → faq-03 (同义词映射生效)
✅ 纯停用词 → []
✅ 返回结构包含 id/title/content/score

全部 7 个 retrieve 验证通过
```

**前置依赖**：Task 2
**后续依赖**：Task 4

---

### Task 4：实现 answer.py + 验证

**目标**：完成回答模块，能调用 mock LLM 并组装返回。

**具体内容**：
- 拼接 Prompt：system 指令 + chunks 内容 + 用户问题
- 调用 mock：`POST http://localhost:9876/v1/chat/completions`（用 urllib）
- sources：直接取 retrieve 返回的 chunk id 列表（加 `[faq-XX]` 格式）
- chunks 为空时返回 `{"answer": "资料中没有找到依据。", "sources": []}`

**验证命令**（需先启动 mock server）：
```bash
# 终端 1：启动 mock
python llm-mock/mock_server.py

# 终端 2：运行验证
python -c "
import sys; sys.path.insert(0, '.')
from src.answer import answer

# 用例 1：正常回答
chunks = [{'id': 'faq-02', 'title': '6类证据文件', 'content': 'Day1最终提交包必须包含6类标准文件', 'score': 3.0}]
r = answer('Day1要交什么？', chunks)
assert isinstance(r, dict), f'Expected dict, got {type(r)}'
assert 'answer' in r and 'sources' in r, f'Missing keys: {r}'
assert len(r['answer']) > 0, 'answer is empty'
assert '[faq-02]' in r['sources'], f'Expected [faq-02] in sources, got {r[\"sources\"]}'
print('✅ 正常回答 → answer 非空, sources 含 [faq-02]')

# 用例 2：空 chunks → 拒答
r = answer('test', [])
assert r['answer'] == '资料中没有找到依据。', f'Expected 拒答, got {r[\"answer\"]}'
assert r['sources'] == [], f'Expected [], got {r[\"sources\"]}'
print('✅ 空 chunks → 拒答, sources 为空')

print(f'\n全部 2 个 answer 验证通过')
"
```

**预期输出**：
```
✅ 正常回答 → answer 非空, sources 含 [faq-02]
✅ 空 chunks → 拒答, sources 为空

全部 2 个 answer 验证通过
```

**前置依赖**：Task 3
**后续依赖**：Task 5

---

### Task 5：实现 main.py + 端到端验证

**目标**：完成 CLI 入口，串联 retrieve → answer → 输出。

**具体内容**：
- 空输入判断：`sys.argv[1]` 为空 → 输出"请输入您的问题"
- 超长截断：超过 200 字符 → 截断至 200 字符
- 读取 `data/course-faq.md`
- 调用 retrieve → 零命中则输出"资料中没有找到依据"
- 调用 answer → 输出 answer 文本 + sources
- 输出格式：先输出 answer，再输出 `来源: [faq-XX], [faq-XX]`

**验证命令**（需先启动 mock server）：
```bash
# 终端 1：启动 mock
python llm-mock/mock_server.py

# 终端 2：运行验证
python src/main.py "Day1要交什么？"
python src/main.py ""
python src/main.py "奖学金政策？"
```

**预期输出**：
```
$ python src/main.py "Day1要交什么？"
（输出包含"spec""design""证据"等关键词，末尾含 来源: [faq-02]）

$ python src/main.py ""
请输入您的问题

$ python src/main.py "奖学金政策？"
资料中没有找到依据。
```

**前置依赖**：Task 3 + Task 4
**后续依赖**：Task 6

---

## Phase 4：集成测试

### Task 6：运行全部自动化测试

**目标**：运行 test_basic.py + test_rag.py，全部通过。

**具体内容**：
- 先运行 `python tests/test_basic.py`
- 再运行 `python tests/test_rag.py`
- 如有 FAIL，定位问题并修复（遵循 bug 修复五步法：复现→定位→假设→最小修复→验证）
- 修复后重跑直到全部 PASS

**验证命令**：
```bash
python tests/test_basic.py
python tests/test_rag.py
```

**预期输出**：
```
$ python tests/test_basic.py
结果: 9 通过, 0 失败

$ python tests/test_rag.py
（13 条用例全部 ✅）
结果: 13 通过, 0 失败
```

**前置依赖**：Task 5
**后续依赖**：Task 7

---

## Phase 5：整体验收

### Task 7：生成 test-record.md

**目标**：汇总所有测试结果到 `docs/test-record.md`。

**具体内容**：
- test_basic.py 结果（9 项检查）
- test_rag.py 结果（13 个测试用例）
- Task 3/4/5 手动验证结果
- 三栏格式：输入 | 预期输出 | 实际输出
- 标 ✅ PASS / ❌ FAIL

**验证标准**：
- `docs/test-record.md` 存在且内容完整
- 所有用例有实际输出记录

**前置依赖**：Task 6
**后续依赖**：Task 8

### Task 8：最终检查清单

**目标**：对照 faq-08 提交前检查清单，逐项核对。

**具体内容**：
1. **目录齐全**：`src/`、`data/`、`docs/`、`tests/` 存在且非空
2. **README 可复现**：包含运行命令、测试命令，照做能跑通
3. **AI log 有判断**：每条 ai-log 的"人工判断"字段非空、非"AI 说的都对"
4. **产物完整**：
   - `docs/spec.md` ✅
   - `docs/design.md` ✅
   - `docs/ai-log.md` ✅
   - `docs/test-record.md` ✅
   - `docs/reflection.md` — 待补充
   - `README.md` ✅
5. **Git 提交**：commit message 有意义，不是 "update"

**验证标准**：
- 检查清单 5 项全部通过
- 补充 `docs/reflection.md`（如尚未创建）

**前置依赖**：Task 7
**后续依赖**：无（项目完成）

---

## 任务总览

```
Task 1  编写 test_rag.py              Phase 1 测试用例开发
Task 2  创建 src/ 骨架                 Phase 2 框架搭建
Task 3  实现 retrieve.py + 验证        Phase 3 功能开发（实现→验证）
Task 4  实现 answer.py + 验证          Phase 3 功能开发（实现→验证）
Task 5  实现 main.py + 端到端验证      Phase 3 功能开发（实现→验证）
Task 6  集成测试 + 修复                Phase 4 集成测试
Task 7  生成 test-record.md            Phase 5 整体验收
Task 8  最终检查清单 + reflection      Phase 5 整体验收
```

## 文档更新规则

| 文档 | 更新时机 |
|------|---------|
| `test-record.md` | Task 3/4/5 验证后记录，Task 7 汇总 |
| `ai-log.md` | 仅在有明确决策点时更新（拒绝/修改 AI 建议） |
| `reflection.md` | Task 8 最终复盘时编写 |
