# 贡献指南

感谢你愿意改进 LOOPS。这个项目重视小而清晰、可验证、可回滚的变更。

## 开始之前

1. 搜索现有 Issue，避免重复工作。
2. 对架构、数据模型或外部接口的较大变更，先创建 Issue 说明问题、替代方案与风险。
3. 不要在 Issue、提交、截图或日志中包含 API Key、访问令牌、真实用户内容和个人信息。

## 本地开发

```bash
cp src/backend/.env.example src/backend/.env
./start.sh
```

后端测试：

```bash
cd src/backend
.venv/bin/python -m pytest tests/agents -q
```

前端检查：

```bash
cd src/frontend
npm run lint
npm run build
```

## Pull Request 要求

- 说明解决的问题、核心选择和未覆盖范围。
- 行为变化必须补充或更新测试。
- 界面变化请附截图；涉及失败处理时同时提供失败场景证据。
- 更新与实现直接相关的 README 或 `docs/`。
- 不把演示数据写成生产指标，不把计划写成已完成事实。
- 保持提交聚焦，不混入构建产物、依赖目录和本地工具缓存。

## 提交信息

推荐使用清晰的动词前缀，例如：

```text
feat: 增加审核运行恢复接口
fix: 阻止不可信 Evidence 触发硬拦截
docs: 补充人工复核边界
test: 覆盖视觉证据缺失场景
```
