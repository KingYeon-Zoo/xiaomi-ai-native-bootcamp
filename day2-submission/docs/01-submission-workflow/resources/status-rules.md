# 状态规则

优先级：`BLOCKED > WARNING > PASS`。

1. 项目目录不存在、任一文件缺失、任一测试失败/超时/无法执行：BLOCKED。
2. 无阻塞项，但 README 缺安装/运行/测试线索或 AI 日志缺五字段：WARNING。
3. 无阻塞项和警告：PASS。
