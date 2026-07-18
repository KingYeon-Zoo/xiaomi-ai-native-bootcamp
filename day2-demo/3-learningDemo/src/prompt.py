"""Prompt 模板和建议备选项定义"""

from langchain_core.prompts import PromptTemplate

# 建议备选项
SUGGESTIONS = {
    "product": ["小米SU7", "iPhone 15", "戴森吹风机", "元气森林", "兰蔻小黑瓶"],
    "target_user": ["大学生", "白领", "宝妈", "程序员", "健身人群", "学生党"],
    "style": ["种草安利", "测评干货", "情绪共鸣"],
}

# Prompt 模板
PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["product", "target_user", "style"],
    template="""你是一个专业的小红书文案写手。请根据以下信息生成一篇小红书笔记。

【产品信息】
- 产品名称: {product}
- 目标用户: {target_user}
- 风格要求: {style}

【输出要求】
请生成以下内容：

1. **标题**（15-20字，带 emoji，吸引眼球）
2. **正文**（300-500字，包含：
   - 开头 hook（引发共鸣或好奇）
   - 产品介绍（自然融入，不要太硬广）
   - 使用体验/卖点展开
   - 结尾号召（引导互动）
3. **标签**（5-8个，#开头，热门+长尾组合）

【风格要求】
- 语气: 亲切、真实、像朋友推荐
- 多用 emoji，但不要过度
- 适当用小红书流行语（姐妹们、绝绝子、真的会谢 等）
- 分段清晰，多用短句""",
)
