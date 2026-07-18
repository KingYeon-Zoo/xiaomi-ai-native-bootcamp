// LOOPS 技术答辩 PPT 生成器 — 小米 AI Native 训练营（个人独立开发）
const pptxgen = require("pptxgenjs");
const path = require("path");
const P = (f) => path.join(__dirname, f);
const ICON = (n) => P(`icons/${n}.png`);
const IMG = {
  bg: P("bg_dark.png"),
  hero: P("../prototype/assets/loops-hero-banner.png"),
  dashAgent: P("../prototype/assets/dashboard-agent-24h-current.png"),
  dashCompare: P("../prototype/assets/dashboard-comparison-current.png"),
};

// ── 调色板（取自真实产品深色看板）──
const C = {
  ink: "0a0e22", card: "141a35", card2: "1a2142", border: "2f3a66",
  cyan: "22d3ee", violet: "8b5cf6", gold: "f6b73c", red: "fb5f6f", green: "34d399",
  text: "e8edf7", body: "c3cde0", mute: "8b97b5", dim: "5b678a",
};
const FONT = "Calibri", FONT_L = "Calibri Light";

const pres = new pptxgen();
pres.defineLayout({ name: "W", width: 13.333, height: 7.5 });
pres.layout = "W";
const W = 13.333, H = 7.5;

// ── 复用型帮助函数 ──
function bg(s, dark = true) {
  s.background = { color: C.ink };
  s.addImage({ path: IMG.bg, x: 0, y: 0, w: W, h: H });
}
function iconCircle(s, ic, x, y, d, ring) {
  s.addShape(pres.ShapeType.ellipse, { x, y, w: d, h: d, fill: { color: C.card2 }, line: { color: ring, width: 1 } });
  const pad = d * 0.26;
  s.addImage({ path: ICON(ic), x: x + pad, y: y + pad, w: d - pad * 2, h: d - pad * 2 });
}
function eyebrow(s, txt, x, y, color) {
  s.addText(txt.toUpperCase(), { x, y, w: 8, h: 0.3, fontFace: FONT, fontSize: 11, color: color || C.cyan, bold: true, charSpacing: 3, align: "left" });
}
function pageNum(s, n, label) {
  s.addText([{ text: `${String(n).padStart(2,"0")}`, options: { color: C.cyan, bold: true } }, { text: `  /  ${label}`, options: { color: C.dim } }],
    { x: 0.6, y: H - 0.52, w: 7, h: 0.3, fontFace: FONT, fontSize: 9.5, align: "left", charSpacing: 1 });
  s.addText("LOOPS · AI SAFETY", { x: W - 3.6, y: H - 0.52, w: 3, h: 0.3, fontFace: FONT, fontSize: 9, color: C.dim, align: "right", charSpacing: 2 });
}
function card(s, x, y, w, h, opts = {}) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.09,
    fill: { color: opts.fill || C.card }, line: { color: opts.line || C.card2, width: opts.lw || 1 },
    shadow: { type: "outer", color: "000000", opacity: 0.35, blur: 8, offset: 3, angle: 90 } });
}
// 正交折线连接器（末段带箭头）
function elbow(s, pts, color, arrow = true) {
  for (let i = 0; i < pts.length - 1; i++) {
    const [x1, y1] = pts[i], [x2, y2] = pts[i + 1];
    const last = i === pts.length - 2;
    s.addShape(pres.ShapeType.line, {
      x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1),
      line: { color, width: 1.5, ...(last && arrow ? { endArrowType: "triangle" } : {}) },
      flipH: x2 < x1, flipV: y2 < y1,
    });
  }
}
// ═══════════ 幻灯片 1 · 封面 ═══════════
(() => {
  const s = pres.addSlide(); s.background = { color: C.ink };
  s.addImage({ path: IMG.bg, x: 0, y: 0, w: W, h: H });
  // hero banner 顶部半幅
  s.addImage({ path: IMG.hero, x: 1.7, y: 0.35, w: 9.93, h: 3.31, transparency: 12 });
  s.addText("LOOPS", { x: 0.9, y: 3.75, w: 8, h: 0.9, fontFace: FONT, fontSize: 60, bold: true, color: C.text, charSpacing: 2 });
  s.addText("双路线 AI 内容审核系统 · 底层实现与 AI Harness 边界", { x: 0.92, y: 4.62, w: 11.5, h: 0.5, fontFace: FONT, fontSize: 20, color: C.cyan });
  s.addText("传统 ML 高吞吐流水线   ×   LangGraph 有状态 Agent 深度审核   ×   确定性策略门最终裁决",
    { x: 0.92, y: 5.18, w: 11.5, h: 0.4, fontFace: FONT, fontSize: 13, color: C.mute });
  // 底部信息条
  const chips = [["person","个人独立开发 · 全栈"],["code","后端 13.3k 行 · 前端 6.0k 行"],["test","42 个自动化测试"],["shield","LLM 无硬权限"]];
  let cx = 0.9;
  chips.forEach(([ic, tx]) => {
    const w = 0.42 + tx.length * 0.135 + 0.5;
    card(s, cx, 6.05, w, 0.62, { fill: C.card2, line: C.border });
    s.addImage({ path: ICON(ic), x: cx + 0.16, y: 6.21, w: 0.3, h: 0.3 });
    s.addText(tx, { x: cx + 0.52, y: 6.05, w: w - 0.5, h: 0.62, fontFace: FONT, fontSize: 12, color: C.body, valign: "middle" });
    cx += w + 0.22;
  });
  s.addText("小米 AI Native 训练营 · 技术答辩", { x: W - 4.3, y: 3.95, w: 3.7, h: 0.35, fontFace: FONT, fontSize: 12.5, color: C.gold, align: "right", bold: true, charSpacing: 1 });
})();

// ═══════════ 幻灯片 2 · 问题诊断 ═══════════
(() => {
  const s = pres.addSlide(); bg(s);
  eyebrow(s, "01 · Problem Diagnosis", 0.65, 0.55);
  s.addText("不是「换一个更长的提示词」", { x: 0.6, y: 0.9, w: 12, h: 0.75, fontFace: FONT, fontSize: 33, bold: true, color: C.text });
  s.addText("项目已有一条 ML 审核流水线。真正的问题：一次性 Prompt 无法回答生产系统必须回答的五个问题。",
    { x: 0.62, y: 1.72, w: 11.8, h: 0.5, fontFace: FONT, fontSize: 15, color: C.mute });
  const qs = [
    ["tool","调用了什么工具","模型凭什么取证？证据从哪来、可否复核"],
    ["trend","为什么升级","什么条件触发深度审查而非全量辩论"],
    ["scale","冲突如何处理","文本与视觉判断矛盾时谁说了算"],
    ["refresh","失败如何恢复","模型挂了、进程重启后运行态是否可续"],
    ["lock","谁有最终权限","LLM 能否自授权限、绕过硬规则"],
  ];
  const cw = 2.32, gap = 0.19, x0 = 0.62;
  qs.forEach(([ic, t, d], i) => {
    const x = x0 + i * (cw + gap);
    card(s, x, 2.5, cw, 3.35);
    iconCircle(s, ic, x + cw/2 - 0.42, 2.85, 0.84, C.cyan);
    s.addText(`Q${i+1}`, { x, y: 3.82, w: cw, h: 0.3, fontFace: FONT, fontSize: 12, color: C.cyan, align: "center", bold: true, charSpacing: 2 });
    s.addText(t, { x: x + 0.15, y: 4.12, w: cw - 0.3, h: 0.7, fontFace: FONT, fontSize: 16, bold: true, color: C.text, align: "center" });
    s.addText(d, { x: x + 0.2, y: 4.82, w: cw - 0.4, h: 0.9, fontFace: FONT, fontSize: 11.5, color: C.mute, align: "center", valign: "top" });
  });
  card(s, 0.62, 6.1, 12.1, 0.72, { fill: C.card2, line: C.violet, lw: 1 });
  s.addImage({ path: ICON("target"), x: 0.85, y: 6.28, w: 0.36, h: 0.36 });
  s.addText([{ text: "目标：", options: { bold: true, color: C.gold } },
    { text: "把 ML 基线升级为「Agent 深度审核 + ML 快速审核」双路线系统 —— 在规则/文本/视觉/模型判断冲突时给出可追溯结论、限制 LLM 权限、证据不足时安全转人工。", options: { color: C.body } }],
    { x: 1.35, y: 6.1, w: 11.2, h: 0.72, fontFace: FONT, fontSize: 13, valign: "middle" });
  pageNum(s, 2, "问题诊断");
})();
// ═══════════ 幻灯片 3 · 从零构建的七阶段流程（阶段门禁）═══════════
(() => {
  const s = pres.addSlide(); bg(s);
  eyebrow(s, "02 · Engineering Process", 0.65, 0.55);
  s.addText("从零构建：七阶段带门禁的工程链路", { x: 0.6, y: 0.9, w: 12, h: 0.7, fontFace: FONT, fontSize: 31, bold: true, color: C.text });
  s.addText("每个阶段都有可验收的门禁与可追溯证据 —— 事实优先级：可运行代码/测试 > git diff > 已确认决策 > 文档。",
    { x: 0.62, y: 1.66, w: 12, h: 0.4, fontFace: FONT, fontSize: 14, color: C.mute });
  const steps = [
    ["search","诊断","14 问 · 3 个 P0\n用户/冲突/非目标", C.cyan],
    ["compass","澄清","P0 决定架构\n答案不同→路线变", C.cyan],
    ["grid","方案","3 条本质路线\n权重取舍矩阵", C.violet],
    ["scale","决策","选方案 C\nD01–D10 决策日志", C.violet],
    ["code","实现","架构声明→\n文件/接口/测试", C.gold],
    ["test","测试","正常/边界/失败\n/回归/端到端", C.green],
    ["book","Review","逆向审查\n发布门禁 8 项", C.red],
  ];
  const cw = 1.62, gap = 0.145, x0 = 0.62, y = 2.55;
  steps.forEach(([ic, t, d, col], i) => {
    const x = x0 + i * (cw + gap);
    card(s, x, y, cw, 3.0);
    s.addShape(pres.ShapeType.roundRect, { x: x + cw/2 - 0.5, y: y + 0.25, w: 1.0, h: 1.0, rectRadius: 0.5, fill: { color: C.card2 }, line: { color: col, width: 1.2 } });
    s.addImage({ path: ICON(ic), x: x + cw/2 - 0.27, y: y + 0.48, w: 0.54, h: 0.54 });
    s.addText(`${i+1}`, { x: x + cw - 0.5, y: y + 0.16, w: 0.4, h: 0.4, fontFace: FONT, fontSize: 15, bold: true, color: col, align: "center" });
    s.addText(t, { x, y: y + 1.32, w: cw, h: 0.4, fontFace: FONT, fontSize: 16, bold: true, color: C.text, align: "center" });
    s.addText(d, { x: x + 0.08, y: y + 1.78, w: cw - 0.16, h: 1.05, fontFace: FONT, fontSize: 10.5, color: C.mute, align: "center", valign: "top", lineSpacingMultiple: 1.05 });
    if (i < steps.length - 1) s.addImage({ path: ICON("arrow"), x: x + cw + gap/2 - 0.11, y: y + 0.62, w: 0.24, h: 0.24 });
  });
  card(s, 0.62, 5.78, 12.1, 0.95, { fill: C.card2, line: C.border });
  s.addText([{ text: "个人独立走完全链路：", options: { bold: true, color: C.cyan } },
    { text: "产品与范围 · Agent 与服务端 · Web 前端 · 数据与演示 · 验证与文档 —— 五个职责域全部由本人完成，证据映射见 ", options: { color: C.body } },
    { text: "docs/evidence-map.md（C01–C09 代码 · T01–T07 测试 · G01–G03 提交 · R01–R04 运行）", options: { color: C.gold, italic: true } }],
    { x: 0.9, y: 5.78, w: 11.6, h: 0.95, fontFace: FONT, fontSize: 12.5, valign: "middle", lineSpacingMultiple: 1.1 });
  pageNum(s, 3, "构建流程");
})();

// ═══════════ 幻灯片 4 · 三个 P0 澄清问题 ═══════════
(() => {
  const s = pres.addSlide(); bg(s);
  eyebrow(s, "03 · The Three P0 Questions", 0.65, 0.55, C.violet);
  s.addText("三个 P0 澄清问题决定了整体架构", { x: 0.6, y: 0.9, w: 12, h: 0.7, fontFace: FONT, fontSize: 31, bold: true, color: C.text });
  s.addText("在写任何代码前，先问「如果答案不同，方案会怎样变」——这三个问题的答案确定了整个系统的骨架。",
    { x: 0.62, y: 1.66, w: 12, h: 0.4, fontFace: FONT, fontSize: 14, color: C.mute });
  const p0 = [
    ["target","优先模型效果，还是可审计的 Agent 判断链？","以 Agent 判断链为主，ML 作为第二方案保留","若以效果为主 → 应把时间投入标注集、训练与离线评测", C.cyan],
    ["eye","图片必须由真实多模态模型审查吗？","必须；视觉职责交给豆包多模态，图片直送云模型","若不要求 → 可删除视觉 Agent 与缺模态转人工策略", C.violet],
    ["lock","谁拥有最终自动裁决权？","确定性策略门；LLM 只提供证据与建议","若 LLM 全权 → 代码更少，但提示注入与越权风险剧增", C.gold],
  ];
  const y0 = 2.5, ch = 1.28, gap = 0.16;
  p0.forEach(([ic, q, concl, alt, col], i) => {
    const y = y0 + i * (ch + gap);
    card(s, 0.62, y, 12.1, ch);
    iconCircle(s, ic, 0.92, y + ch/2 - 0.42, 0.84, col);
    s.addText(`P0`, { x: 1.95, y: y + 0.18, w: 1, h: 0.3, fontFace: FONT, fontSize: 11, bold: true, color: col, charSpacing: 2 });
    s.addText(q, { x: 1.95, y: y + 0.42, w: 6.3, h: 0.75, fontFace: FONT, fontSize: 16.5, bold: true, color: C.text, valign: "middle" });
    s.addShape(pres.ShapeType.line, { x: 8.45, y: y + 0.2, w: 0, h: ch - 0.4, line: { color: C.border, width: 1 } });
    s.addText([{ text: "✓ 结论  ", options: { color: C.green, bold: true } }, { text: concl, options: { color: C.body } }],
      { x: 8.65, y: y + 0.2, w: 3.95, h: 0.55, fontFace: FONT, fontSize: 11.5, valign: "middle", lineSpacingMultiple: 1.0 });
    s.addText([{ text: "↝ 反事实  ", options: { color: C.mute, bold: true } }, { text: alt, options: { color: C.mute } }],
      { x: 8.65, y: y + 0.72, w: 3.95, h: 0.5, fontFace: FONT, fontSize: 10.5, valign: "middle", italic: true, lineSpacingMultiple: 1.0 });
  });
  pageNum(s, 4, "P0 澄清");
})();
// ═══════════ 幻灯片 5 · 方案选型与权衡矩阵 ═══════════
(() => {
  const s = pres.addSlide(); bg(s);
  eyebrow(s, "04 · Solution Trade-off Matrix", 0.65, 0.55, C.gold);
  s.addText("三条本质不同的路线 · 加权取舍", { x: 0.6, y: 0.9, w: 12, h: 0.7, fontFace: FONT, fontSize: 31, bold: true, color: C.text });
  // 三方案卡片
  const opts = [
    ["cpu","方案 A · ML 流水线","规则+文本分类+图像+CLIP+融合","本地低延迟、高吞吐、复用最高","复杂图文语境、证据解释、冲突恢复弱","2.90", C.mute],
    ["brain","方案 B · 单模型提示词","单个多模态 LLM 一次返回结论","调用链最短、语义强于分类","缺工具/路由/权限隔离/恢复","2.60", C.mute],
    ["shieldcheck","方案 C · 条件式双路线","ML 快速 × LangGraph Agent 深度","效率+深度+证据链 兼顾","状态/测试/口径复杂度最高","4.85", C.cyan],
  ];
  const cw = 3.95, gap = 0.2, x0 = 0.62, y = 2.4;
  opts.forEach(([ic, t, form, pro, con, score, col], i) => {
    const x = x0 + i * (cw + gap);
    const chosen = i === 2;
    card(s, x, y, cw, 3.05, { fill: chosen ? C.card2 : C.card, line: chosen ? C.cyan : C.card2, lw: chosen ? 2 : 1 });
    s.addImage({ path: ICON(ic), x: x + 0.25, y: y + 0.25, w: 0.5, h: 0.5 });
    s.addText(score, { x: x + cw - 1.55, y: y + 0.12, w: 1.4, h: 0.6, fontFace: FONT, fontSize: 30, bold: true, color: chosen ? C.cyan : C.dim, align: "right" });
    s.addText(t, { x: x + 0.22, y: y + 0.82, w: cw - 0.44, h: 0.4, fontFace: FONT, fontSize: 15.5, bold: true, color: C.text });
    s.addText(form, { x: x + 0.22, y: y + 1.22, w: cw - 0.44, h: 0.5, fontFace: FONT, fontSize: 11, color: C.mute, italic: true });
    s.addText([{ text: "＋ ", options: { color: C.green, bold: true } }, { text: pro, options: { color: C.body } }],
      { x: x + 0.22, y: y + 1.78, w: cw - 0.44, h: 0.6, fontFace: FONT, fontSize: 11.5, valign: "top", lineSpacingMultiple: 1.0 });
    s.addText([{ text: "－ ", options: { color: C.red, bold: true } }, { text: con, options: { color: C.mute } }],
      { x: x + 0.22, y: y + 2.4, w: cw - 0.44, h: 0.55, fontFace: FONT, fontSize: 11.5, valign: "top", lineSpacingMultiple: 1.0 });
    if (chosen) s.addText("★ 最终选择", { x: x + 0.22, y: y - 0.02, w: cw, h: 0.3, fontFace: FONT, fontSize: 0.1, color: C.cyan });
  });
  // 维度权重条
  card(s, 0.62, 5.7, 12.1, 1.05, { fill: C.card, line: C.border });
  s.addText("加权维度（权重）", { x: 0.85, y: 5.8, w: 4, h: 0.3, fontFace: FONT, fontSize: 11, bold: true, color: C.gold, charSpacing: 1 });
  const dims = ["Agent 能力展示 25%","复杂图文 20%","安全兜底 20%","时延成本 15%","复用度 10%","可追溯可恢复 10%"];
  let dx = 0.85;
  dims.forEach((d) => {
    const w = 0.3 + d.length * 0.115;
    s.addShape(pres.ShapeType.roundRect, { x: dx, y: 6.18, w, h: 0.42, rectRadius: 0.06, fill: { color: C.card2 }, line: { color: C.border, width: 0.75 } });
    s.addText(d, { x: dx, y: 6.18, w, h: 0.42, fontFace: FONT, fontSize: 10.5, color: C.body, align: "center", valign: "middle" });
    dx += w + 0.18;
  });
  pageNum(s, 5, "方案权衡");
})();

// ═══════════ 幻灯片 6 · 双路线总体架构 ═══════════
(() => {
  const s = pres.addSlide(); bg(s);
  eyebrow(s, "05 · Dual-Route Architecture", 0.65, 0.55);
  s.addText("按风险分层的双路线，而非新旧替换", { x: 0.6, y: 0.9, w: 12, h: 0.7, fontFace: FONT, fontSize: 31, bold: true, color: C.text });
  s.addText("MODERATION_APPROACH 环境变量决定加载哪条路径 —— 理解代码的第一入口。ML 快、便宜、固定；Agent 深、可追溯、可恢复。",
    { x: 0.62, y: 1.66, w: 12.1, h: 0.4, fontFace: FONT, fontSize: 13.5, color: C.mute });
  // 输入
  s.addShape(pres.ShapeType.roundRect, { x: 0.62, y: 3.3, w: 1.9, h: 1.2, rectRadius: 0.09, fill: { color: C.card2 }, line: { color: C.border, width: 1 } });
  s.addImage({ path: ICON("package"), x: 1.35, y: 3.5, w: 0.44, h: 0.44 });
  s.addText("内容输入", { x: 0.62, y: 3.98, w: 1.9, h: 0.4, fontFace: FONT, fontSize: 13, bold: true, color: C.text, align: "center" });
  // 分流菱形
  s.addShape(pres.ShapeType.diamond, { x: 2.95, y: 3.25, w: 1.5, h: 1.3, fill: { color: C.card }, line: { color: C.gold, width: 1.5 } });
  s.addText("风险分流", { x: 2.95, y: 3.65, w: 1.5, h: 0.5, fontFace: FONT, fontSize: 12, bold: true, color: C.gold, align: "center" });
  s.addImage({ path: ICON("arrow"), x: 2.56, y: 3.78, w: 0.32, h: 0.32 });
  // ML 路径（上）
  card(s, 4.95, 2.28, 7.75, 1.55, { fill: C.card, line: C.violet, lw: 1.5 });
  s.addImage({ path: ICON("cpu"), x: 5.15, y: 2.5, w: 0.42, h: 0.42 });
  s.addText("ML 快速审核路径", { x: 5.65, y: 2.5, w: 4, h: 0.4, fontFace: FONT, fontSize: 15, bold: true, color: C.violet });
  s.addText("低风险 · 稳定分布 · 高吞吐", { x: 8.9, y: 2.52, w: 3.6, h: 0.4, fontFace: FONT, fontSize: 11, color: C.mute, align: "right", italic: true });
  s.addText("文本规范化 → 规则引擎 → 文本分类(RoBERTa) → 图像分类(EfficientNet·CLIP) → 决策融合", { x: 5.15, y: 3.02, w: 7.35, h: 0.7, fontFace: FONT, fontSize: 12, color: C.body, valign: "middle" });
  // Agent 路径（下）
  card(s, 4.95, 4.0, 7.75, 1.55, { fill: C.card, line: C.cyan, lw: 1.5 });
  s.addImage({ path: ICON("robot"), x: 5.15, y: 4.22, w: 0.42, h: 0.42 });
  s.addText("Agent 深度审核路径", { x: 5.65, y: 4.22, w: 4, h: 0.4, fontFace: FONT, fontSize: 15, bold: true, color: C.cyan });
  s.addText("图文 · 高风险 · 冲突 · 提示注入", { x: 8.7, y: 4.24, w: 3.8, h: 0.4, fontFace: FONT, fontSize: 11, color: C.mute, align: "right", italic: true });
  s.addText("规则预检 → 文本/视觉取证 → 风险路由 → Critic/Arbiter 仲裁 → 确定性策略门", { x: 5.15, y: 4.74, w: 7.35, h: 0.7, fontFace: FONT, fontSize: 12, color: C.body, valign: "middle" });
  // 汇合到人工
  card(s, 4.95, 5.75, 7.75, 0.95, { fill: C.card2, line: C.gold });
  s.addImage({ path: ICON("users"), x: 5.15, y: 6.0, w: 0.42, h: 0.42 });
  s.addText([{ text: "仍不确定 → 人工最终裁决  ", options: { bold: true, color: C.gold } }, { text: "证据不足、Agent 不可用、仲裁要求人审 —— 一律安全转人工，绝不静默放行", options: { color: C.body } }],
    { x: 5.7, y: 5.75, w: 6.8, h: 0.95, fontFace: FONT, fontSize: 12, valign: "middle", lineSpacingMultiple: 1.05 });
  // 左下注记
  card(s, 0.62, 5.0, 4.0, 1.7, { fill: C.card, line: C.border });
  s.addText("诚实边界", { x: 0.82, y: 5.12, w: 3, h: 0.3, fontFace: FONT, fontSize: 11, bold: true, color: C.red, charSpacing: 1 });
  s.addText("两条「能力」均已实现并各有入口；但 ML→Agent 统一在线风险路由尚未接通，列为下一步演进，不写成已完成。",
    { x: 0.82, y: 5.42, w: 3.6, h: 1.2, fontFace: FONT, fontSize: 11.5, color: C.body, valign: "top", lineSpacingMultiple: 1.1 });
  pageNum(s, 6, "双路线架构");
})();
// ═══════════ 幻灯片 7 · LangGraph 编排图（阶段化流水线）═══════════
(() => {
  const s = pres.addSlide(); bg(s);
  eyebrow(s, "06 · LangGraph Orchestration", 0.65, 0.5);
  s.addText("Agent 编排：条件路由 · 并行取证 · 中断恢复", { x: 0.6, y: 0.82, w: 12, h: 0.6, fontFace: FONT, fontSize: 28, bold: true, color: C.text });
  s.addText("app/agents/graph.py · StateGraph：assessments / trace 以 operator.add 累加，人审经 interrupt() 暂停并同 thread_id 恢复",
    { x: 0.62, y: 1.52, w: 12.3, h: 0.32, fontFace: FONT, fontSize: 11, color: C.mute });
  const node = (x, y, w, h, label, sub, col) => {
    s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.08, fill: { color: C.card2 }, line: { color: col, width: 1.4 } });
    s.addText(label, { x: x + 0.04, y: y + 0.11, w: w - 0.08, h: 0.34, fontFace: FONT, fontSize: 12.5, bold: true, color: C.text, align: "center", valign: "top" });
    s.addText(sub, { x: x + 0.04, y: y + 0.44, w: w - 0.08, h: h - 0.46, fontFace: FONT, fontSize: 9, color: C.mute, align: "center", valign: "top" });
  };
  // 主脊（中间带）y≈3.15
  const my = 3.15, nh = 0.95;
  const spine = [
    [0.62, 1.75, "precheck", "规则取证", C.gold],
    [2.72, 1.55, "dispatch", "并行分发", C.violet],
    [4.62, 1.9, "text ∥ vision", "文本·视觉取证", C.violet],
    [6.92, 1.6, "risk_route", "风险路由", C.gold],
    [8.87, 1.85, "critic·arbiter", "质疑+有界仲裁", C.red],
    [11.07, 1.66, "policy_gate", "确定性裁决", C.cyan],
  ];
  spine.forEach(([x, w, l, sb, c]) => node(x, my, w, nh, l, sb, c));
  // 脊上箭头
  for (let i = 0; i < spine.length - 1; i++) {
    const x1 = spine[i][0] + spine[i][1], x2 = spine[i + 1][0];
    elbow(s, [[x1, my + nh/2], [x2, my + nh/2]], C.dim);
  }
  // 快速路径弧：risk_route → policy_gate（跳过 critic/arbiter，下方）
  elbow(s, [[6.92 + 1.6/2, my + nh], [7.72, 4.7], [11.07 + 1.66/2, 4.7], [11.07 + 1.66/2, my + nh]], C.cyan);
  s.addText("快速路径 · 证据一致且低风险 → 跳过辩论", { x: 7.7, y: 4.72, w: 5.0, h: 0.3, fontFace: FONT, fontSize: 9.5, color: C.cyan, align: "center", italic: true });
  // critic/arbiter 触发标注（上方）
  s.addText("冲突 / 置信<0.75 / severity≥0.6 / Agent 不可用", { x: 8.6, y: 2.62, w: 4.2, h: 0.3, fontFace: FONT, fontSize: 9.5, color: C.red, align: "center", italic: true });
  elbow(s, [[6.92 + 1.6/2, my], [7.72, 2.92], [8.87 + 1.85/2, 2.92], [8.87 + 1.85/2, my]], C.red);
  // START
  s.addShape(pres.ShapeType.roundRect, { x: 0.62, y: 2.15, w: 1.75, h: 0.4, rectRadius: 0.2, fill: { color: C.card }, line: { color: C.dim, width: 1 } });
  s.addText("START", { x: 0.62, y: 2.15, w: 1.75, h: 0.4, fontFace: FONT, fontSize: 10, bold: true, color: C.mute, align: "center", valign: "middle" });
  elbow(s, [[1.5, 2.55], [1.5, my]], C.dim);
  // 硬规则短路：precheck → policy_gate（顶部长弧）
  elbow(s, [[0.62 + 1.75/2, my], [1.5, 1.95], [11.9, 1.95], [11.9, my]], C.gold);
  s.addText("命中可信硬规则(rule / attack_tool) → 直达策略门，短路全部云 Agent", { x: 2.3, y: 1.9, w: 9.4, h: 0.3, fontFace: FONT, fontSize: 10, color: C.gold, align: "center", italic: true });
  // 人审路径（底部带）y≈5.55
  const hy = 5.55, hh = 0.85;
  node(6.4, hy, 2.0, hh, "human_review", "interrupt() 暂停", C.gold);
  node(8.7, hy, 1.9, hh, "finalize_human", "同 run 恢复", C.green);
  node(10.9, hy, 1.83, hh, "END", "completed", C.green);
  elbow(s, [[11.07 + 1.66/2, my + nh], [11.9, 4.95], [6.4 + 2.0/2, 4.95], [6.4 + 2.0/2, hy]], C.gold);
  s.addText("证据不足 / 仲裁要求人审 / 建议冲突", { x: 5.9, y: 5.05, w: 4.5, h: 0.3, fontFace: FONT, fontSize: 9.5, color: C.gold, align: "center", italic: true });
  elbow(s, [[6.4 + 2.0, hy + hh/2], [8.7, hy + hh/2]], C.green);
  elbow(s, [[8.7 + 1.9, hy + hh/2], [10.9, hy + hh/2]], C.green);
  // policy_gate → END（自动完成）
  elbow(s, [[11.07 + 1.66/2, my + nh], [11.9, 5.98], [10.9 + 1.83, 5.98]], C.cyan, true);
  s.addText([{ text: "证据充分 → allow / block（自动完成）", options: { color: C.cyan } }], { x: 0.62, y: 6.55, w: 6, h: 0.3, fontFace: FONT, fontSize: 10, italic: true });
  // 图例
  const leg = [["硬规则短路", C.gold],["并行取证", C.violet],["快速路径", C.cyan],["辩论路径", C.red],["人审恢复", C.green]];
  let lx = 6.7;
  leg.forEach(([t, col]) => {
    s.addShape(pres.ShapeType.line, { x: lx, y: 6.68, w: 0.3, h: 0, line: { color: col, width: 3 } });
    const w = 0.2 + t.length * 0.135;
    s.addText(t, { x: lx + 0.36, y: 6.53, w, h: 0.3, fontFace: FONT, fontSize: 9.5, color: C.body, valign: "middle" });
    lx += 0.36 + w + 0.15;
  });
  pageNum(s, 7, "LangGraph 编排");
})();
// ═══════════ 幻灯片 8 · 权限隔离核心不变量（设计灵魂）═══════════
(() => {
  const s = pres.addSlide(); bg(s);
  eyebrow(s, "07 · The Core Invariant", 0.65, 0.55, C.cyan);
  s.addText("LLM 只产证据，确定性策略门掌握硬权限", { x: 0.6, y: 0.9, w: 12, h: 0.7, fontFace: FONT, fontSize: 30, bold: true, color: C.text });
  s.addText("本项目的设计灵魂 —— 用户内容不可信，LLM 输出也不可信。把「证据」与「政策权限」分离，让关键权限可以被单元测试。",
    { x: 0.62, y: 1.68, w: 12.1, h: 0.4, fontFace: FONT, fontSize: 14, color: C.mute });
  // 左：三条不变量
  const inv = [
    ["lock","来源可信才承认硬拦截","LLM 输出 HARD_BLOCK_* 不足以硬拦截。只有 TRUSTED_HARD_POLICY_SOURCES = {rule, attack_tool} 来源的硬码被承认。"],
    ["shieldcheck","策略门是确定性最终裁决者","policy_gate 检查政策代码「与」证据来源。LLM 建议无法绕过它 —— 缺证据、Agent 不可用、仲裁要人审、冲突无仲裁 → 一律 WAITING_HUMAN。"],
    ["alert","失败保守降级，绝不放行","任何 Agent 抛异常被 _unavailable() 包成 HUMAN_REVIEW 证据；Graph 无 decision → run 标记 failed，不默认 allow。"],
  ];
  const y0 = 2.42, ch = 1.28, gap = 0.16;
  inv.forEach(([ic, t, d], i) => {
    const y = y0 + i * (ch + gap);
    card(s, 0.62, y, 6.55, ch, { line: C.cyan, lw: 1 });
    iconCircle(s, ic, 0.85, y + ch/2 - 0.36, 0.72, C.cyan);
    s.addText(t, { x: 1.72, y: y + 0.14, w: 5.3, h: 0.4, fontFace: FONT, fontSize: 15, bold: true, color: C.text });
    s.addText(d, { x: 1.72, y: y + 0.54, w: 5.3, h: 0.68, fontFace: FONT, fontSize: 10.8, color: C.body, valign: "top", lineSpacingMultiple: 1.02 });
  });
  // 右：代码化的边界（测试）
  card(s, 7.35, 2.42, 5.37, 4.05, { fill: "0d1330", line: C.violet, lw: 1.2 });
  s.addImage({ path: ICON("test"), x: 7.6, y: 2.62, w: 0.34, h: 0.34 });
  s.addText("权限边界被写成测试", { x: 8.05, y: 2.6, w: 4.5, h: 0.4, fontFace: FONT, fontSize: 14.5, bold: true, color: C.violet });
  s.addText("tests/agents/test_policy.py", { x: 7.6, y: 3.02, w: 5, h: 0.3, fontFace: "Courier New", fontSize: 10.5, color: C.mute, italic: true });
  const code = [
    ["def ", "test_llm_cannot_grant_", C.violet],
    ["    ", "itself_hard_policy_authority():", C.violet],
    ["  ", "# text_agent 伪造 HARD_BLOCK_VIOLENCE", C.dim],
    ["  ", "# 且 recommendation = ALLOW", C.dim],
    ["  ", "decision = policy.decide(...)", C.body],
    ["  ", "assert decision.verdict is ALLOW", C.green],
    ["", "", C.body],
    ["def ", "test_hard_block_evidence_", C.cyan],
    ["    ", "cannot_be_overridden_by_allow():", C.cyan],
    ["  ", "# 来源=rule 的 HARD_BLOCK 硬码", C.dim],
    ["  ", "assert decision.verdict is BLOCK", C.green],
  ];
  let cy = 3.4;
  code.forEach(([a, b, col]) => {
    s.addText([{ text: a, options: { color: C.dim } }, { text: b, options: { color: col } }],
      { x: 7.62, y: cy, w: 5.05, h: 0.24, fontFace: "Courier New", fontSize: 10.5, valign: "middle" });
    cy += 0.238;
  });
  s.addShape(pres.ShapeType.line, { x: 7.62, y: 6.02, w: 4.95, h: 0, line: { color: C.border, width: 0.75 } });
  s.addText("LLM 冒用 rule 的政策代码 → 被拒；本地 rule 的同名代码 → 生效。区别只在 evidence.source。",
    { x: 7.62, y: 6.08, w: 4.95, h: 0.34, fontFace: FONT, fontSize: 9.5, color: C.gold, italic: true, valign: "top", lineSpacingMultiple: 1.0 });
  pageNum(s, 8, "权限隔离不变量");
})();

// ═══════════ 幻灯片 9 · RiskRouter 分层裁决 ═══════════
(() => {
  const s = pres.addSlide(); bg(s);
  eyebrow(s, "08 · Risk Router", 0.65, 0.55, C.gold);
  s.addText("RiskRouter：不为「像 Agent」而全量辩论", { x: 0.6, y: 0.9, w: 12, h: 0.7, fontFace: FONT, fontSize: 30, bold: true, color: C.text });
  s.addText("简单内容不必进入完整 critic/arbiter 辩论。只有下列任一条件成立才升级 —— 控制成本与延迟，同时保留深度审查能力。",
    { x: 0.62, y: 1.68, w: 12.1, h: 0.4, fontFace: FONT, fontSize: 14, color: C.mute });
  // 四个触发条件
  const trig = [
    ["scale","建议冲突","len(recommendations) > 1\n文本与视觉判断不一致"],
    ["trend","低置信","confidence < 0.75\n任一 Agent 置信不足阈值"],
    ["alert","高风险证据","severity ≥ 0.6\n任一证据严重度过高"],
    ["x","Agent 不可用","unavailable / error\n取证失败即触发"],
  ];
  const cw = 2.9, gap = 0.2, x0 = 0.62, y = 2.55;
  trig.forEach(([ic, t, d], i) => {
    const x = x0 + i * (cw + gap);
    card(s, x, y, cw, 2.2, { line: C.red, lw: 1 });
    iconCircle(s, ic, x + cw/2 - 0.4, y + 0.28, 0.8, C.red);
    s.addText(t, { x, y: y + 1.15, w: cw, h: 0.4, fontFace: FONT, fontSize: 16, bold: true, color: C.text, align: "center" });
    s.addText(d, { x: x + 0.15, y: y + 1.55, w: cw - 0.3, h: 0.6, fontFace: FONT, fontSize: 10.5, color: C.mute, align: "center", valign: "top", lineSpacingMultiple: 1.05 });
  });
  s.addText("↓  任一成立 = requires_debate", { x: 0.62, y: 4.9, w: 12.1, h: 0.35, fontFace: FONT, fontSize: 13, color: C.gold, align: "center", bold: true });
  // 两条出口
  card(s, 1.8, 5.4, 4.6, 1.3, { fill: C.card2, line: C.cyan });
  s.addImage({ path: ICON("zap"), x: 2.05, y: 5.62, w: 0.4, h: 0.4 });
  s.addText("快速路径 (fast_path)", { x: 2.55, y: 5.6, w: 3.7, h: 0.4, fontFace: FONT, fontSize: 15, bold: true, color: C.cyan });
  s.addText("证据一致、低风险 → 直达策略门。约 72% 流量走此路。", { x: 2.05, y: 6.02, w: 4.15, h: 0.6, fontFace: FONT, fontSize: 11.5, color: C.body, valign: "top", lineSpacingMultiple: 1.05 });
  card(s, 6.9, 5.4, 4.6, 1.3, { fill: C.card2, line: C.red });
  s.addImage({ path: ICON("gavel"), x: 7.15, y: 5.62, w: 0.4, h: 0.4 });
  s.addText("辩论路径 (debate)", { x: 7.65, y: 5.6, w: 3.7, h: 0.4, fontFace: FONT, fontSize: 15, bold: true, color: C.red });
  s.addText("Critic 反方审查 → Arbiter 有界仲裁 → 策略门。", { x: 7.15, y: 6.02, w: 4.15, h: 0.6, fontFace: FONT, fontSize: 11.5, color: C.body, valign: "top", lineSpacingMultiple: 1.05 });
  pageNum(s, 9, "风险路由");
})();
// ═══════════ 幻灯片 10 · 失败保守降级 ═══════════
(() => {
  const s = pres.addSlide(); bg(s);
  eyebrow(s, "09 · Fail-Closed by Design", 0.65, 0.55, C.red);
  s.addText("失败保守降级：模型挂了不会放过违规", { x: 0.6, y: 0.9, w: 12, h: 0.7, fontFace: FONT, fontSize: 30, bold: true, color: C.text });
  s.addText("答辩常见追问：「模型挂了会不会放过违规内容？」—— 不会。每一类失败都有明确的保守出口，从不静默 allow。",
    { x: 0.62, y: 1.68, w: 12.1, h: 0.4, fontFace: FONT, fontSize: 14, color: C.mute });
  const rows = [
    ["alert","Agent 抛异常","_unavailable() 包成 HUMAN_REVIEW 证据，severity=0.5","→ 策略门转人工"],
    ["eye","图片必需但视觉证据缺失","有图必须有 vision_agent 证据源","→ WAITING_HUMAN"],
    ["scale","仲裁要求人审 / 建议冲突无仲裁","policy_gate 拒绝自动裁决","→ WAITING_HUMAN"],
    ["x","Graph 未产生 decision","runtime 捕获异常，run 标记 failed","→ 不默认 allow"],
    ["lock","LLM 伪造 HARD_BLOCK_*","来源非 rule/attack_tool，硬码无效","→ 按普通建议处理"],
    ["refresh","进程重启，run 中断","启动时 list_recoverable() 重新入队","→ 断点续跑"],
  ];
  const cw = 6.0, ch = 1.28, gx = 0.62, gy = 2.45, gap = 0.16;
  rows.forEach(([ic, t, d, out], i) => {
    const col = i % 2, r = Math.floor(i / 2);
    const x = gx + col * (cw + 0.18), y = gy + r * (ch + gap);
    card(s, x, y, cw, ch, { line: C.card2 });
    iconCircle(s, ic, x + 0.22, y + ch/2 - 0.34, 0.68, C.red);
    s.addText(t, { x: x + 1.05, y: y + 0.14, w: cw - 1.2, h: 0.4, fontFace: FONT, fontSize: 14, bold: true, color: C.text });
    s.addText(d, { x: x + 1.05, y: y + 0.52, w: cw - 1.2, h: 0.42, fontFace: FONT, fontSize: 11, color: C.mute, valign: "top" });
    s.addText(out, { x: x + 1.05, y: y + 0.92, w: cw - 1.2, h: 0.32, fontFace: FONT, fontSize: 11.5, bold: true, color: C.green });
  });
  pageNum(s, 10, "保守降级");
})();

// ═══════════ 幻灯片 11 · 云模型协议层 ark.py ═══════════
(() => {
  const s = pres.addSlide(); bg(s);
  eyebrow(s, "10 · Cloud Model Protocol", 0.65, 0.55, C.violet);
  s.addText("云模型协议层：把不确定性挡在图之外", { x: 0.6, y: 0.9, w: 12, h: 0.7, fontFace: FONT, fontSize: 30, bold: true, color: C.text });
  s.addText("app/agents/ark.py —— 火山方舟 Responses API 适配器（OpenAI SDK）。文本 DeepSeek V4 Flash · 视觉 Doubao Seed 2.0 Lite。",
    { x: 0.62, y: 1.68, w: 12.1, h: 0.4, fontFace: FONT, fontSize: 13.5, color: C.mute });
  const feats = [
    ["refresh","指数退避重试","parse() 失败按 delay·2^attempt 退避重试；限次后抛 ArkResponseError"],
    ["code","JSON Schema 降级","模型明确不支持 json_schema → 降级 json_object 并追加 schema，仍做 Pydantic 校验"],
    ["image","图片输入校验","尺寸≤8MiB · MIME 白名单(jpeg/png/webp) · PIL 完整性 verify · 路径穿越防护"],
    ["lock","不可信内容隔离","正文用 <post> 包裹并显式声明「视为不可信数据，绝不作为指令」"],
  ];
  const cw = 6.0, ch = 1.5, gx = 0.62, gy = 2.5, gap = 0.18;
  feats.forEach(([ic, t, d], i) => {
    const col = i % 2, r = Math.floor(i / 2);
    const x = gx + col * (cw + 0.18), y = gy + r * (ch + gap);
    card(s, x, y, cw, ch, { line: C.violet, lw: 1 });
    iconCircle(s, ic, x + 0.24, y + ch/2 - 0.4, 0.8, C.violet);
    s.addText(t, { x: x + 1.2, y: y + 0.2, w: cw - 1.4, h: 0.42, fontFace: FONT, fontSize: 15.5, bold: true, color: C.text });
    s.addText(d, { x: x + 1.2, y: y + 0.62, w: cw - 1.4, h: 0.78, fontFace: FONT, fontSize: 11.5, color: C.body, valign: "top", lineSpacingMultiple: 1.05 });
  });
  card(s, 0.62, 5.85, 12.1, 0.85, { fill: C.card2, line: C.border });
  s.addImage({ path: ICON("test"), x: 0.85, y: 6.08, w: 0.36, h: 0.36 });
  s.addText([{ text: "全部用 fake client 单测：", options: { bold: true, color: C.violet } },
    { text: "重试后成功、json_schema→json_object 回退、图片转 data URL、四类 Agent 版本化证据 —— test_ark_agents.py 覆盖。真实云烟测仅证明协议可用，不声明准确率。", options: { color: C.body } }],
    { x: 1.35, y: 5.85, w: 11.2, h: 0.85, fontFace: FONT, fontSize: 12, valign: "middle", lineSpacingMultiple: 1.05 });
  pageNum(s, 11, "云模型协议");
})();
// ═══════════ 幻灯片 12 · 运行时与人审恢复 ═══════════
(() => {
  const s = pres.addSlide(); bg(s);
  eyebrow(s, "11 · Durable Runtime & HITL", 0.65, 0.55);
  s.addText("运行时：异步队列 · 持久化 · 同 run 恢复", { x: 0.6, y: 0.9, w: 12, h: 0.7, fontFace: FONT, fontSize: 30, bold: true, color: C.text });
  s.addText("app/agents/runtime.py —— 单进程异步队列 + MongoDB 持久化。run_id 即 thread_id；人工决定用同一 run 恢复，而非新建任务。",
    { x: 0.62, y: 1.68, w: 12.1, h: 0.4, fontFace: FONT, fontSize: 13.5, color: C.mute });
  // 状态机
  card(s, 0.62, 2.45, 12.1, 1.55, { fill: C.card, line: C.border });
  s.addText("运行状态机", { x: 0.85, y: 2.56, w: 3, h: 0.3, fontFace: FONT, fontSize: 12, bold: true, color: C.cyan, charSpacing: 1 });
  const st = [["queued","入队",C.mute],["running","执行图",C.violet],["waiting_human","中断暂停",C.gold],["completed","裁决完成",C.green],["failed","异常记录",C.red]];
  const sx0 = 0.95, sw = 1.95, sgap = 0.42, sy = 3.05;
  st.forEach(([n, d, col], i) => {
    const x = sx0 + i * (sw + sgap);
    s.addShape(pres.ShapeType.roundRect, { x, y: sy, w: sw, h: 0.78, rectRadius: 0.08, fill: { color: C.card2 }, line: { color: col, width: 1.3 } });
    s.addText(n, { x, y: sy + 0.1, w: sw, h: 0.34, fontFace: "Courier New", fontSize: 11.5, bold: true, color: col, align: "center" });
    s.addText(d, { x, y: sy + 0.42, w: sw, h: 0.3, fontFace: FONT, fontSize: 10.5, color: C.mute, align: "center" });
    if (i < st.length - 1) s.addImage({ path: ICON("arrow"), x: x + sw + sgap/2 - 0.14, y: sy + 0.24, w: 0.28, h: 0.28 });
  });
  s.addText("waiting_human → queued（同 run 恢复）", { x: 3.0, y: 3.85, w: 7, h: 0.3, fontFace: FONT, fontSize: 10, color: C.gold, align: "center", italic: true });
  // 三个机制卡
  const mech = [
    ["refresh","重启自愈","start() 时 list_recoverable() 把 queued/running 的 run 重新入队 —— 进程中断后断点续跑"],
    ["database","线程隔离持久化","MongoRunRepository 用 asyncio.to_thread 把同步 PyMongo 调用移出事件循环；MongoDBSaver 存 checkpoint"],
    ["users","人审恢复同一运行","resume() 校验仅 waiting_human 可恢复 → Command(resume) 注入决定 → finalize_human 用原证据/政策码收尾"],
  ];
  const cw = 3.95, gap = 0.16, x0 = 0.62, y = 4.2;
  mech.forEach(([ic, t, d], i) => {
    const x = x0 + i * (cw + gap);
    card(s, x, y, cw, 2.35, { line: C.cyan, lw: 1 });
    iconCircle(s, ic, x + cw/2 - 0.42, y + 0.28, 0.84, C.cyan);
    s.addText(t, { x, y: y + 1.2, w: cw, h: 0.4, fontFace: FONT, fontSize: 15.5, bold: true, color: C.text, align: "center" });
    s.addText(d, { x: x + 0.22, y: y + 1.62, w: cw - 0.44, h: 0.68, fontFace: FONT, fontSize: 11, color: C.body, align: "center", valign: "top", lineSpacingMultiple: 1.05 });
  });
  pageNum(s, 12, "运行时");
})();

// ═══════════ 幻灯片 13 · ML Ensemble 流水线 ═══════════
(() => {
  const s = pres.addSlide(); bg(s);
  eyebrow(s, "12 · ML Ensemble Pipeline", 0.65, 0.55, C.violet);
  s.addText("ML 快速路线：6 检测器 · 14 步 · 失败即拒", { x: 0.6, y: 0.9, w: 12, h: 0.7, fontFace: FONT, fontSize: 29, bold: true, color: C.text });
  s.addText("_moderation_service_ensemble.py —— 保留的高吞吐 ML 基线。多检测器并行取证，DecisionEngine 8 步有序裁决，全程 fail-closed（崩溃拒绝而非放行）。",
    { x: 0.62, y: 1.66, w: 12.2, h: 0.4, fontFace: FONT, fontSize: 12.5, color: C.mute });
  // 六检测器
  s.addText("六个检测器", { x: 0.65, y: 2.2, w: 4, h: 0.3, fontFace: FONT, fontSize: 12, bold: true, color: C.violet, charSpacing: 1 });
  const det = [
    ["filter","规则引擎","关键词/正则/URL/spam"],
    ["image","EfficientNet","NSFW 图像分类(ViT)"],
    ["eye","CLIP","图文相关性·余弦相似"],
    ["brain","多任务模型","toxic-bert + dehatebert"],
    ["shield","TechContextFilter","模式→零样本 二段确认"],
    ["search","IntentEntityFilter","spaCy NER + 意图分级"],
  ];
  const cw = 1.95, gap = 0.11, x0 = 0.62, y = 2.55;
  det.forEach(([ic, t, d], i) => {
    const x = x0 + i * (cw + gap);
    card(s, x, y, cw, 1.85, { line: C.card2 });
    iconCircle(s, ic, x + cw/2 - 0.36, y + 0.2, 0.72, C.violet);
    s.addText(t, { x: x + 0.06, y: y + 1.0, w: cw - 0.12, h: 0.36, fontFace: FONT, fontSize: 12, bold: true, color: C.text, align: "center" });
    s.addText(d, { x: x + 0.08, y: y + 1.36, w: cw - 0.16, h: 0.42, fontFace: FONT, fontSize: 9.5, color: C.mute, align: "center", valign: "top", lineSpacingMultiple: 1.0 });
  });
  // 决策引擎有序步骤
  card(s, 0.62, 4.65, 8.35, 2.05, { fill: "0d1330", line: C.gold });
  s.addImage({ path: ICON("scale"), x: 0.85, y: 4.82, w: 0.36, h: 0.36 });
  s.addText("DecisionEngine · 有序裁决（无快速放行捷径）", { x: 1.3, y: 4.8, w: 7.5, h: 0.4, fontFace: FONT, fontSize: 14, bold: true, color: C.gold });
  const order = "规则命中 → 可疑 URL → NSFW 图像 → 技术相关性门 → 赛博危害意图 → 内容混杂 → 图文不匹配 → ML 危害分类 → 通用兜底 → 放行";
  s.addText(order, { x: 0.9, y: 5.3, w: 7.8, h: 1.0, fontFace: FONT, fontSize: 12.5, color: C.body, valign: "top", lineSpacingMultiple: 1.35 });
  s.addText("高技术分数「绝不」跳过危害检测 —— 危害检查对所有技术帖都运行。", { x: 0.9, y: 6.32, w: 7.8, h: 0.3, fontFace: FONT, fontSize: 10, color: C.gold, italic: true });
  // 右侧：边界样本 → 人审
  card(s, 9.15, 4.65, 3.57, 2.05, { fill: C.card2, line: C.cyan });
  s.addImage({ path: ICON("users"), x: 9.38, y: 4.82, w: 0.36, h: 0.36 });
  s.addText("边界样本转人审", { x: 9.83, y: 4.8, w: 2.8, h: 0.4, fontFace: FONT, fontSize: 13.5, bold: true, color: C.cyan });
  s.addText("技术相关性落在 review 区间，或规则与毒性模型判断分歧时 → _is_borderline 标记 flag_for_human_review。",
    { x: 9.38, y: 5.3, w: 3.15, h: 1.3, fontFace: FONT, fontSize: 11, color: C.body, valign: "top", lineSpacingMultiple: 1.1 });
  pageNum(s, 13, "ML 流水线");
})();
// ═══════════ 幻灯片 14 · 反规避与多语言 ═══════════
(() => {
  const s = pres.addSlide(); bg(s);
  eyebrow(s, "13 · Anti-Evasion & Multilingual", 0.65, 0.55, C.gold);
  s.addText("规则引擎：反规避、多语言、降误报", { x: 0.6, y: 0.9, w: 12, h: 0.7, fontFace: FONT, fontSize: 30, bold: true, color: C.text });
  s.addText("rule_engine.py (1067 行) + text_normalizer.py —— 硬拦截可信来源之一。不是简单关键词表，而是归一化 + 上下文 + 混合打分。",
    { x: 0.62, y: 1.68, w: 12.1, h: 0.4, fontFace: FONT, fontSize: 13.5, color: C.mute });
  const cols = [
    ["refresh","归一化反规避", C.violet, ["leetspeak 映射 0→o @→a $→s +→t","重复字符折叠 aaaa → a","空格拆分还原 m a d a r → madar","符号剥离绕过 f*ck / f.u.c.k"]],
    ["globe","多语言检测", C.cyan, ["印地/Hinglish 高/中危词集","多词脏话短语 + 缩写 mc/bc/bsdk","置信分级 0.95 / 0.80 / 0.70","英文脏话 leet 感知正则类"]],
    ["shield","降误报机制", C.green, ["词边界 \\b：skill≠kill studied≠die","allowlist 掩码 painkiller/frontend","上下文分析 safe/harmful pattern","技术相关性混合打分 + 内容混杂惩罚"]],
  ];
  const cw = 3.95, gap = 0.16, x0 = 0.62, y = 2.5;
  cols.forEach(([ic, t, col, items], i) => {
    const x = x0 + i * (cw + gap);
    card(s, x, y, cw, 4.05, { line: col, lw: 1 });
    iconCircle(s, ic, x + 0.24, y + 0.24, 0.78, col);
    s.addText(t, { x: x + 1.15, y: y + 0.32, w: cw - 1.3, h: 0.6, fontFace: FONT, fontSize: 16, bold: true, color: C.text, valign: "middle" });
    s.addText(items.map((it, k) => ({ text: it, options: { bullet: { code: "2022", indent: 14 }, color: C.body, breakLine: true, paraSpaceAfter: k < items.length - 1 ? 10 : 0 } })),
      { x: x + 0.28, y: y + 1.22, w: cw - 0.5, h: 2.7, fontFace: FONT, fontSize: 11.5, valign: "top", lineSpacingMultiple: 1.02 });
  });
  pageNum(s, 14, "反规避多语言");
})();

// ═══════════ 幻灯片 15 · API 安全边界 ═══════════
(() => {
  const s = pres.addSlide(); bg(s);
  eyebrow(s, "14 · API Security Boundary", 0.65, 0.55, C.cyan);
  s.addText("API 安全边界：用户视图 vs 管理轨迹", { x: 0.6, y: 0.9, w: 12, h: 0.7, fontFace: FONT, fontSize: 30, bold: true, color: C.text });
  s.addText("同一个 run，两种视图。用户看不到原文与内部轨迹；管理轨迹只暴露结构化节点，绝不泄露隐藏推理。",
    { x: 0.62, y: 1.68, w: 12.1, h: 0.4, fontFace: FONT, fontSize: 14, color: C.mute });
  const ep = [
    ["person","用户安全视图", C.cyan, "GET /runs/{run_id}", "model_dump(exclude={text, trace}) —— 用户只看到状态/裁决/置信，看不到原文与执行轨迹"],
    ["eye","管理结构化轨迹", C.violet, "GET /runs/{run_id}/trace", "只返回 node/status/summary 结构化节点。Evidence 契约本身不存隐藏思维链"],
    ["users","人工决定恢复", C.gold, "POST /runs/{run_id}/human-decision", "Literal[approve, reject] 校验；仅 waiting_human 可恢复，否则 409"],
  ];
  const y0 = 2.45, ch = 1.25, gap = 0.16;
  ep.forEach(([ic, t, col, path, d], i) => {
    const y = y0 + i * (ch + gap);
    card(s, 0.62, y, 12.1, ch, { line: col, lw: 1 });
    iconCircle(s, ic, 0.9, y + ch/2 - 0.4, 0.8, col);
    s.addText(t, { x: 1.95, y: y + 0.16, w: 3.6, h: 0.44, fontFace: FONT, fontSize: 16, bold: true, color: C.text });
    s.addShape(pres.ShapeType.roundRect, { x: 1.95, y: y + 0.66, w: 4.4, h: 0.42, rectRadius: 0.06, fill: { color: "0d1330" }, line: { color: C.border, width: 0.75 } });
    s.addText(path, { x: 2.05, y: y + 0.66, w: 4.3, h: 0.42, fontFace: "Courier New", fontSize: 11.5, color: col, valign: "middle" });
    s.addText(d, { x: 6.6, y: y + 0.18, w: 5.9, h: 0.9, fontFace: FONT, fontSize: 12, color: C.body, valign: "middle", lineSpacingMultiple: 1.08 });
  });
  card(s, 0.62, 6.35, 12.1, 0.5, { fill: C.card2, line: C.border });
  s.addText([{ text: "验证：", options: { bold: true, color: C.cyan } },
    { text: "test_agent_api.py 断言用户接口 “text not in / trace not in”，管理轨迹首节点为结构化 node —— 边界被测试锁定。", options: { color: C.body } }],
    { x: 0.9, y: 6.35, w: 11.6, h: 0.5, fontFace: FONT, fontSize: 11.5, valign: "middle" });
  pageNum(s, 15, "API 安全边界");
})();
// ═══════════ 幻灯片 16 · AI Harness 接受/修改/拒绝（核心考察点）═══════════
(() => {
  const s = pres.addSlide(); bg(s);
  eyebrow(s, "15 · AI Harness · Accept / Revise / Reject", 0.65, 0.5, C.gold);
  s.addText("如何驾驭 AI：三态决策 + 明确边界", { x: 0.6, y: 0.82, w: 12, h: 0.6, fontFace: FONT, fontSize: 29, bold: true, color: C.text });
  s.addText("AI 是工具，不是项目成员。每条 AI 建议都经过代码/测试/git/命令复核后，记录为「接受 / 修改 / 拒绝」并写明人工判断。",
    { x: 0.62, y: 1.48, w: 12.2, h: 0.35, fontFace: FONT, fontSize: 12.5, color: C.mute });
  // 三列
  const groups = [
    ["check","接受", C.green, [
      ["用 LangGraph StateGraph","条件路由/并行/checkpoint/HITL 与现有栈匹配"],
      ["文本 DeepSeek、视觉豆包分工","已确认图片必须真实审查"],
      ["LLM 只产证据、策略门裁决","可防提示注入与模型自提权"],
    ]],
    ["edit","修改", C.gold, [
      ["「全部进完整辩论」→ 条件升级","全量 critic/arbiter 成本与时延过高"],
      ["「立即统一在线路由」→ 下一步","避免把设计写成已实现"],
      ["「强制 JSON Schema」→ 按需降级","部分方舟模型不支持该格式"],
    ]],
    ["x","拒绝", C.red, [
      ["LLM 输出 HARD_BLOCK_* 直接拦截","不可信模型不能自升权限 → 只信 rule/attack_tool"],
      ["旧云烟测/旧指标直接写入结果","缺本轮日志，演示值非实测 → 重跑烟测"],
      ["用 AI 同步冒充多人会议","AI 不是成员，无真实参与者证据"],
    ]],
  ];
  const cw = 3.95, gap = 0.16, x0 = 0.62, y = 2.0;
  groups.forEach(([ic, t, col, items], i) => {
    const x = x0 + i * (cw + gap);
    card(s, x, y, cw, 4.6, { line: col, lw: 1.3 });
    s.addShape(pres.ShapeType.roundRect, { x: x + 0.2, y: y + 0.22, w: cw - 0.4, h: 0.6, rectRadius: 0.08, fill: { color: C.card2 }, line: { type: "none" } });
    s.addImage({ path: ICON(ic), x: x + 0.35, y: y + 0.34, w: 0.36, h: 0.36 });
    s.addText(t, { x: x + 0.85, y: y + 0.22, w: cw - 1, h: 0.6, fontFace: FONT, fontSize: 17, bold: true, color: col, valign: "middle" });
    let iy = y + 1.02;
    items.forEach(([h, d]) => {
      s.addText(h, { x: x + 0.24, y: iy, w: cw - 0.48, h: 0.55, fontFace: FONT, fontSize: 11.8, bold: true, color: C.text, valign: "top", lineSpacingMultiple: 1.0 });
      s.addText(d, { x: x + 0.24, y: iy + 0.5, w: cw - 0.48, h: 0.62, fontFace: FONT, fontSize: 10, color: C.mute, valign: "top", lineSpacingMultiple: 1.0 });
      iy += 1.18;
    });
  });
  pageNum(s, 16, "AI Harness 三态决策");
})();

// ═══════════ 幻灯片 17 · 如何驾驭 AI：六阶段协作 + 边界 ═══════════
(() => {
  const s = pres.addSlide(); bg(s);
  eyebrow(s, "16 · Governing the AI · Six Phases", 0.65, 0.55, C.violet);
  s.addText("AI 协作被约束成六个可核验阶段", { x: 0.6, y: 0.9, w: 12, h: 0.7, fontFace: FONT, fontSize: 30, bold: true, color: C.text });
  s.addText("每阶段记录 Prompt 约束 / AI 输出 / 采纳拒绝与人工判断 / 实际影响与验证 —— 可由 diff、测试、命令相互印证。",
    { x: 0.62, y: 1.68, w: 12.1, h: 0.4, fontFace: FONT, fontSize: 13.5, color: C.mute });
  const phases = [
    ["compass","澄清","不先写代码，只列会改变架构/权限/范围的问题"],
    ["grid","方案对比","要求≥3 条本质路线，写明成本、失败面、可交付性"],
    ["target","反证","假设当前偏好是错的，找会导致误放/断链的反例"],
    ["code","实现","架构声明映射到文件/接口/测试，保留旧 ML 资产"],
    ["test","验证","执行可复现命令，保留失败，禁止 fake/快照冒充实测"],
    ["book","Review","逐文件查空模板/旧路径/强结论/密钥/缓存"],
  ];
  const cw = 3.95, gap = 0.16, x0 = 0.62, y = 2.5;
  phases.forEach(([ic, t, d], i) => {
    const col = i % 3, r = Math.floor(i / 3);
    const x = x0 + col * (cw + gap), yy = y + r * 1.28;
    card(s, x, yy, cw, 1.12);
    iconCircle(s, ic, x + 0.2, yy + 0.24, 0.64, C.violet);
    s.addText(`0${i+1} · ${t}`, { x: x + 0.95, y: yy + 0.14, w: cw - 1.1, h: 0.34, fontFace: FONT, fontSize: 14, bold: true, color: C.text });
    s.addText(d, { x: x + 0.95, y: yy + 0.48, w: cw - 1.15, h: 0.6, fontFace: FONT, fontSize: 10.5, color: C.mute, valign: "top", lineSpacingMultiple: 1.02 });
  });
  // 明确边界条
  card(s, 0.62, 5.5, 12.1, 1.2, { fill: C.card2, line: C.red, lw: 1.2 });
  s.addImage({ path: ICON("lock"), x: 0.85, y: 5.72, w: 0.4, h: 0.4 });
  s.addText("明确的 AI 使用边界（原文）", { x: 1.35, y: 5.62, w: 6, h: 0.35, fontFace: FONT, fontSize: 13, bold: true, color: C.red });
  const bnd = "AI 建议必须经代码/测试/git/命令复核 · 目标与方案选择由维护者负责 · 不把 AI 输出写成用户访谈或已验证事实 · 不回显 .env 密钥 · 单个云烟测不写成准确率 · 不提交 AI 工具缓存/令牌/会话状态";
  s.addText(bnd, { x: 1.35, y: 5.98, w: 11.15, h: 0.65, fontFace: FONT, fontSize: 11.5, color: C.body, valign: "top", lineSpacingMultiple: 1.15 });
  pageNum(s, 17, "驾驭 AI · 六阶段");
})();
// ═══════════ 幻灯片 18 · 测试与验证（诚实标注）═══════════
(() => {
  const s = pres.addSlide(); bg(s);
  eyebrow(s, "17 · Verification", 0.65, 0.55, C.green);
  s.addText("分层验证：正常/边界/失败/回归/安全/端到端", { x: 0.6, y: 0.9, w: 12.2, h: 0.7, fontFace: FONT, fontSize: 27, bold: true, color: C.text });
  s.addText("42 个自动化测试（tests/agents 31 个全通过，0.83s）。每层都有可复现命令与实际输出，计划与结果分开记录。",
    { x: 0.62, y: 1.66, w: 12.1, h: 0.4, fontFace: FONT, fontSize: 13.5, color: C.mute });
  // 左：数字卡
  const stats = [["31","Agent 测试全通过"],["7","验证层级"],["96 / 64","Posts / Agent runs"],["0","控制台 warn/error"]];
  stats.forEach(([n, l], i) => {
    const x = 0.62 + (i % 2) * 2.95, y = 2.5 + Math.floor(i / 2) * 1.42;
    card(s, x, y, 2.78, 1.25, { fill: C.card2, line: C.green });
    s.addText(n, { x: x + 0.15, y: y + 0.12, w: 2.5, h: 0.68, fontFace: FONT, fontSize: 34, bold: true, color: C.green });
    s.addText(l, { x: x + 0.18, y: y + 0.82, w: 2.45, h: 0.35, fontFace: FONT, fontSize: 11, color: C.body });
  });
  // 右：分层表 + 诚实声明
  card(s, 6.75, 2.5, 5.97, 2.67, { line: C.border });
  const layers = [["单元","规则/路由/策略门/模型适配"],["图编排","fast/hard-block/debate/interrupt"],["运行时","入队/失败/重启/人审恢复"],["API","状态隔离/轨迹/人工决定"],["数据","双方案快照/种子/Mongo 回退"],["云端","DeepSeek 文本 + 豆包图片烟测"]];
  let ly = 2.66;
  layers.forEach(([k, v], i) => {
    s.addText(k, { x: 6.95, y: ly, w: 1.5, h: 0.36, fontFace: FONT, fontSize: 12, bold: true, color: C.cyan, valign: "middle" });
    s.addText(v, { x: 8.4, y: ly, w: 4.2, h: 0.36, fontFace: FONT, fontSize: 11, color: C.body, valign: "middle" });
    ly += 0.4;
    if (i < layers.length - 1) s.addShape(pres.ShapeType.line, { x: 6.95, y: ly - 0.02, w: 5.6, h: 0, line: { color: C.card2, width: 0.5 } });
  });
  card(s, 0.62, 5.4, 12.1, 1.3, { fill: C.card2, line: C.gold, lw: 1.2 });
  s.addImage({ path: ICON("alert"), x: 0.85, y: 5.62, w: 0.4, h: 0.4 });
  s.addText("诚实的验证限制（主动声明）", { x: 1.35, y: 5.52, w: 6, h: 0.35, fontFace: FONT, fontSize: 13, bold: true, color: C.gold });
  s.addText("两个真实云烟测只证明密钥/模型名/图片传输/结构化解析可用，单样本不证明准确率 · 31 个测试集中在新增 Agent 与看板，旧 ML 全量测试未在本轮宣称全过 · 看板 97.8% / 2.84s / 326 次每秒是演示快照字段，不是这些测试测得。",
    { x: 1.35, y: 5.88, w: 11.15, h: 0.78, fontFace: FONT, fontSize: 11, color: C.body, valign: "top", lineSpacingMultiple: 1.12 });
  pageNum(s, 18, "测试验证");
})();

// ═══════════ 幻灯片 19 · 双方案看板与指标降级协议 ═══════════
(() => {
  const s = pres.addSlide(); bg(s);
  eyebrow(s, "18 · Dashboard & Honest Metrics", 0.65, 0.5, C.cyan);
  s.addText("双方案控制台：同口径对比，标注数据源", { x: 0.6, y: 0.82, w: 12.2, h: 0.6, fontFace: FONT, fontSize: 27, bold: true, color: C.text });
  s.addText("Agent / ML / 对比三视图 × 1 / 24 / 168 小时。三层数据降级协议保证演示不空白，页面始终显示「Mongo 演示快照」标签。",
    { x: 0.62, y: 1.46, w: 12.2, h: 0.35, fontFace: FONT, fontSize: 12.5, color: C.mute });
  // 截图
  s.addImage({ path: IMG.dashCompare, x: 0.62, y: 2.0, w: 7.5, h: 4.22 });
  s.addShape(pres.ShapeType.roundRect, { x: 0.62, y: 2.0, w: 7.5, h: 4.22, rectRadius: 0.05, fill: { type: "none" }, line: { color: C.border, width: 1 } });
  s.addText("真实运行截图 · /api/metrics/control-center", { x: 0.62, y: 6.26, w: 7.5, h: 0.3, fontFace: FONT, fontSize: 10, color: C.dim, align: "center", italic: true });
  // 右：三层降级协议
  card(s, 8.35, 2.0, 4.37, 2.35, { fill: C.card, line: C.cyan });
  s.addText("三层降级协议", { x: 8.6, y: 2.14, w: 4, h: 0.35, fontFace: FONT, fontSize: 14, bold: true, color: C.cyan });
  const tiers = [["database","MongoDB 快照","source = mongodb_demo_snapshot"],["server","后端确定性内置","无快照时同结构回退"],["globe","前端本地副本","接口失败时最后兜底"]];
  let ty = 2.6;
  tiers.forEach(([ic, t, d]) => {
    s.addImage({ path: ICON(ic), x: 8.6, y: ty + 0.04, w: 0.34, h: 0.34 });
    s.addText(t, { x: 9.05, y: ty, w: 3.5, h: 0.3, fontFace: FONT, fontSize: 12, bold: true, color: C.text });
    s.addText(d, { x: 9.05, y: ty + 0.3, w: 3.5, h: 0.3, fontFace: "Courier New", fontSize: 9, color: C.mute });
    ty += 0.58;
  });
  // 诚实声明
  card(s, 8.35, 4.5, 4.37, 1.72, { fill: C.card2, line: C.gold, lw: 1.2 });
  s.addImage({ path: ICON("alert"), x: 8.6, y: 4.66, w: 0.36, h: 0.36 });
  s.addText("演示快照 ≠ 生产实测", { x: 9.05, y: 4.64, w: 3.5, h: 0.35, fontFace: FONT, fontSize: 13, bold: true, color: C.gold });
  s.addText("精度、延迟、吞吐、数量均为固定随机种子(20260717)生成的演示字段，用于同口径比较架构取向，绝不解释为生产 KPI 或线上流量。",
    { x: 8.6, y: 5.04, w: 3.95, h: 1.1, fontFace: FONT, fontSize: 11, color: C.body, valign: "top", lineSpacingMultiple: 1.12 });
  pageNum(s, 19, "看板与指标口径");
})();
// ═══════════ 幻灯片 20 · 个人工作量 ═══════════
(() => {
  const s = pres.addSlide(); bg(s);
  eyebrow(s, "19 · Individual Contribution", 0.65, 0.55, C.cyan);
  s.addText("个人独立开发：五个职责域全覆盖", { x: 0.6, y: 0.9, w: 12, h: 0.7, fontFace: FONT, fontSize: 30, bold: true, color: C.text });
  s.addText("两阶段重构，从 ML 基线到 Agent/ML 双路线系统。角色集中在一人，但职责与验收证据不缺席。",
    { x: 0.62, y: 1.68, w: 12.1, h: 0.4, fontFace: FONT, fontSize: 14, color: C.mute });
  // 两阶段
  card(s, 0.62, 2.45, 6.0, 1.7, { line: C.violet });
  s.addText("阶段一 · 973ab58", { x: 0.85, y: 2.58, w: 5, h: 0.35, fontFace: FONT, fontSize: 13, bold: true, color: C.violet });
  s.addText("搭建 FastAPI + MongoDB + React 控制台，规则/文本/图像审核资产与 ML 流水线基线。",
    { x: 0.85, y: 2.96, w: 5.55, h: 1.05, fontFace: FONT, fontSize: 12, color: C.body, valign: "top", lineSpacingMultiple: 1.1 });
  card(s, 6.75, 2.45, 5.97, 1.7, { line: C.cyan });
  s.addText("阶段二 · e1bc2b7", { x: 6.98, y: 2.58, w: 5, h: 0.35, fontFace: FONT, fontSize: 13, bold: true, color: C.cyan });
  s.addText("加入结构化 Evidence、模型适配、LangGraph 编排、确定性策略门、运行记录与人工恢复。",
    { x: 6.98, y: 2.96, w: 5.5, h: 1.05, fontFace: FONT, fontSize: 12, color: C.body, valign: "top", lineSpacingMultiple: 1.1 });
  // 五职责域 + 代码量
  const roles = [["compass","产品与范围"],["server","Agent 与服务端"],["grid","Web 前端"],["database","数据与演示"],["test","验证与文档"]];
  const cw = 2.32, gap = 0.19, x0 = 0.62, y = 4.35;
  roles.forEach(([ic, t], i) => {
    const x = x0 + i * (cw + gap);
    card(s, x, y, cw, 1.15, { fill: C.card2 });
    iconCircle(s, ic, x + cw/2 - 0.34, y + 0.16, 0.68, C.cyan);
    s.addText(t, { x: x + 0.05, y: y + 0.86, w: cw - 0.1, h: 0.3, fontFace: FONT, fontSize: 11.5, bold: true, color: C.text, align: "center" });
  });
  // 代码量条
  card(s, 0.62, 5.75, 12.1, 0.98, { fill: C.card, line: C.border });
  const nums = [["13.3k","后端 Python 行"],["6.0k","前端 JS 行"],["1067","规则引擎单文件"],["42","自动化测试"],["1","git 作者"]];
  let nx = 0.9;
  nums.forEach(([n, l], i) => {
    s.addText(n, { x: nx, y: 5.86, w: 2.28, h: 0.42, fontFace: FONT, fontSize: 21, bold: true, color: C.gold, valign: "middle" });
    s.addText(l, { x: nx, y: 6.28, w: 2.28, h: 0.32, fontFace: FONT, fontSize: 11.5, color: C.body, valign: "middle" });
    if (i < nums.length - 1) s.addShape(pres.ShapeType.line, { x: nx + 2.28, y: 5.95, w: 0, h: 0.55, line: { color: C.border, width: 1 } });
    nx += 2.42;
  });
  pageNum(s, 20, "个人工作量");
})();

// ═══════════ 幻灯片 21 · 边界与下一步 ═══════════
(() => {
  const s = pres.addSlide(); bg(s);
  eyebrow(s, "20 · Boundaries & Next Steps", 0.65, 0.55, C.red);
  s.addText("已知边界与非目标：诚实划定 MVP", { x: 0.6, y: 0.9, w: 12, h: 0.7, fontFace: FONT, fontSize: 30, bold: true, color: C.text });
  s.addText("当前是演示 MVP。清楚说明「现在不能兜底什么」，比夸大能力更能体现工程判断。",
    { x: 0.62, y: 1.68, w: 12.1, h: 0.4, fontFace: FONT, fontSize: 14, color: C.mute });
  // 左：当前边界
  card(s, 0.62, 2.5, 6.0, 4.05, { line: C.red, lw: 1 });
  s.addImage({ path: ICON("alert"), x: 0.85, y: 2.68, w: 0.38, h: 0.38 });
  s.addText("当前不能兜底", { x: 1.35, y: 2.66, w: 5, h: 0.4, fontFace: FONT, fontSize: 16, bold: true, color: C.red });
  const lim = ["单进程队列：无分布式租约 / 跨实例幂等 / exactly-once","Trace 与人工接口缺管理员鉴权（RBAC）与审计签名","ML→Agent 统一在线风险路由尚未接通（当前靠配置切换）","无正式政策版本、标注集、漂移监控与生产 SLO","视频/多图/压缩炸弹/隐写/跨语言对抗样本"];
  s.addText(lim.map((t, k) => ({ text: t, options: { bullet: { code: "2022", indent: 14 }, color: C.body, breakLine: true, paraSpaceAfter: k < lim.length - 1 ? 12 : 0 } })),
    { x: 0.9, y: 3.2, w: 5.5, h: 3.2, fontFace: FONT, fontSize: 12.5, valign: "top", lineSpacingMultiple: 1.05 });
  // 右：下一步
  card(s, 6.75, 2.5, 5.97, 4.05, { line: C.green, lw: 1 });
  s.addImage({ path: ICON("trend"), x: 6.98, y: 2.68, w: 0.38, h: 0.38 });
  s.addText("下一步演进", { x: 7.48, y: 2.66, w: 5, h: 0.4, fontFace: FONT, fontSize: 16, bold: true, color: C.green });
  const next = ["统一审核入口：先跑轻量特征，再按风险升级 Agent","引入外部队列、幂等键、任务租约与多实例恢复","建立标注回放集，分测 ML / Agent / 混合路由质量","为 trace 与人工操作增加 RBAC 与审计日志","前端路由级拆包，降低首屏（当前主包 >500kB）","发布前引入独立安全审查与政策专家复核"];
  s.addText(next.map((t, k) => ({ text: t, options: { bullet: { code: "2022", indent: 14 }, color: C.body, breakLine: true, paraSpaceAfter: k < next.length - 1 ? 11 : 0 } })),
    { x: 7.05, y: 3.2, w: 5.5, h: 3.2, fontFace: FONT, fontSize: 12.5, valign: "top", lineSpacingMultiple: 1.05 });
  pageNum(s, 21, "边界与下一步");
})();

// ═══════════ 幻灯片 22 · 结语 / 追问卡 ═══════════
(() => {
  const s = pres.addSlide(); s.background = { color: C.ink };
  s.addImage({ path: IMG.bg, x: 0, y: 0, w: W, h: H });
  s.addImage({ path: IMG.hero, x: 8.4, y: 0.5, w: 4.5, h: 1.5, transparency: 30 });
  eyebrow(s, "Summary", 0.65, 0.6, C.cyan);
  s.addText("三条主线，一句话答辩", { x: 0.6, y: 0.98, w: 10, h: 0.8, fontFace: FONT, fontSize: 34, bold: true, color: C.text });
  const lines = [
    ["code","工程能力","5 道阶段门 · C01–C09 代码 / T01–T07 测试 / G·R 运行证据 —— 声明到文件/测试可定位闭环", C.violet],
    ["shieldcheck","Harness 规范性","「LLM 只产证据、策略门掌权」被写成单元测试；AI 建议接受/修改/拒绝三态可核验", C.cyan],
    ["scale","诚实边界","演示快照 ≠ 生产 KPI · AI ≠ 项目成员 · 失败被保留而非抹去", C.gold],
  ];
  const y0 = 2.15, ch = 1.05, gap = 0.18;
  lines.forEach(([ic, t, d, col], i) => {
    const y = y0 + i * (ch + gap);
    card(s, 0.62, y, 12.1, ch, { fill: C.card, line: col, lw: 1.2 });
    iconCircle(s, ic, 0.85, y + ch/2 - 0.34, 0.68, col);
    s.addText(t, { x: 1.72, y: y, w: 2.7, h: ch, fontFace: FONT, fontSize: 16.5, bold: true, color: col, valign: "middle" });
    s.addShape(pres.ShapeType.line, { x: 4.5, y: y + 0.2, w: 0, h: ch - 0.4, line: { color: C.border, width: 1 } });
    s.addText(d, { x: 4.75, y: y + 0.1, w: 7.75, h: ch - 0.2, fontFace: FONT, fontSize: 12.5, color: C.body, valign: "middle", lineSpacingMultiple: 1.05 });
  });
  // 追问卡精选
  card(s, 0.62, 5.95, 12.1, 0.98, { fill: C.card2, line: C.border });
  s.addText([{ text: "追问预案 · ", options: { bold: true, color: C.gold } },
    { text: "「为何不用一个大模型直接判？」→ 用户内容不可信，单模型把注入/格式/故障集中到黑盒；分离 Evidence 与 Policy Authority，关键权限可单测。", options: { color: C.body } }],
    { x: 0.9, y: 5.95, w: 11.5, h: 0.98, fontFace: FONT, fontSize: 12, valign: "middle", lineSpacingMultiple: 1.1 });
  s.addText("LOOPS · 双路线 AI 内容审核系统 · 个人独立开发 · 小米 AI Native 训练营", { x: 0.6, y: H - 0.5, w: 12, h: 0.3, fontFace: FONT, fontSize: 10, color: C.dim, align: "center", charSpacing: 1 });
  pageNum(s, 22, "结语");
})();
// PLACEHOLDER_SLIDES
// ═══════════ 注入答辩演讲稿（speaker notes）· 由 pptxgenjs 原生写入，避免 python-pptx 破坏结构 ═══════════
(() => {
  const NOTES = require("./notes_data.js");
  const arr = pres.slides || pres._slides;
  let n = 0;
  arr.forEach((sl, i) => {
    const txt = NOTES[i + 1];
    if (txt) { sl.addNotes(txt); n++; }
  });
  console.log("notes injected:", n, "/", arr.length);
})();
pres.writeFile({ fileName: P("LOOPS-技术答辩.pptx") }).then(f => console.log("saved", f));
