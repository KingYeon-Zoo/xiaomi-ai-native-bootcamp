# Test Record — 训练营助教 Agent

## 环境与命令

- Python 3.9.6，标准库实现
- 日期：2026-07-13
- 命令：`python3 -m unittest discover -s 04-training-agent/tests -v`

## 结果

| 类别 | 输入 | 预期 | 实际 | 结果 |
|------|------|------|------|------|
| RAG 正常 | 可复核交付 | 回答 + faq-01 | 返回定义与 faq-01 | ✅ PASS |
| RAG 资料外 | 奖学金 | 固定拒答、无来源 | 固定拒答、空列表 | ✅ PASS |
| RAG 失败 | 缺失 FAQ | success=false | 加载失败提示 | ✅ PASS |
| RAG 边界 | 空查询 | 明确提示 | “请输入课程问题” | ✅ PASS |
| 任务正常 | today/submit/check | 五项并持久化 | 符合预期 | ✅ PASS |
| 任务异常 | 重复/未知文件 | success=false | 人类可读提示 | ✅ PASS |
| 校验正常 | 四文件完整 | PASS | PASS | ✅ PASS |
| 校验警告 | README 线索不足 | WARNING | WARNING | ✅ PASS |
| 校验阻塞 | 目录/文件缺失 | BLOCKED | BLOCKED | ✅ PASS |
| 安全边界 | allowed_root 外目录 | BLOCKED | BLOCKED | ✅ PASS |

```text
Ran 13 tests in 0.007s
OK
```

所有正常、资料外、工具失败和路径边界均有自动测试；下一步在真实 Agent Runtime 中增加 Router 自然语言分类评估。
