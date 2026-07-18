import {
  Activity,
  CheckCircle2,
  FileSearch,
  Gauge,
  ShieldAlert,
  ShieldCheck,
  UserRoundSearch,
  Zap,
} from "lucide-react";
import {
  Area,
  AreaChart,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { BorderGlow, Counter, SpotlightCard } from "../reactbits/ReactBits";

const fallbackTrend = [
  { time: "00:00", allowed: 420, blocked: 118 },
  { time: "03:00", allowed: 560, blocked: 142 },
  { time: "06:00", allowed: 980, blocked: 236 },
  { time: "09:00", allowed: 720, blocked: 198 },
  { time: "12:00", allowed: 910, blocked: 244 },
  { time: "15:00", allowed: 760, blocked: 180 },
  { time: "18:00", allowed: 490, blocked: 156 },
  { time: "21:00", allowed: 1060, blocked: 278 },
  { time: "24:00", allowed: 840, blocked: 214 },
];

const pipeline = [
  { label: "文本规范化", latency: "23 ms", icon: FileSearch, color: "#22D3EE" },
  { label: "规则引擎", latency: "45 ms", icon: ShieldCheck, color: "#8B5CF6" },
  { label: "LLM 分析", latency: "382 ms", icon: Gauge, color: "#22D3EE" },
  { label: "决策引擎", latency: "18 ms", icon: CheckCircle2, color: "#34D399" },
];

const compactNumber = (value) => {
  return value.toLocaleString();
};

export default function MetricsHeroOverview({ advancedMetrics, recentPredictions, systemHealth }) {
  const outcomes = advancedMetrics?.outcomes || {};
  const total = outcomes.total || advancedMetrics?.prediction_volume?.last_24h || 12847;
  const allowed = outcomes.allowed || Math.round(total * 0.75);
  const blocked = outcomes.blocked || Math.round(total * 0.23);
  const review = Math.max(0, total - allowed - blocked) || 274;
  const allowedPct = total ? Math.round((allowed / total) * 100) : 75;
  const blockedPct = total ? Math.round((blocked / total) * 100) : 23;
  const reviewPct = Math.max(0, 100 - allowedPct - blockedPct);

  const metrics = [
    { label: "审核总量", value: total, trend: "18.6%", icon: Activity, accent: "#8B5CF6" },
    { label: "自动放行", value: allowed, trend: "20.3%", icon: ShieldCheck, accent: "#22D3EE" },
    { label: "已拦截", value: blocked, trend: "12.7%", icon: ShieldAlert, accent: "#FB7185" },
    { label: "待人工复核", value: review, trend: "6.4%", icon: UserRoundSearch, accent: "#FBBF24", down: true },
  ];
  const outcomeData = [
    { name: "放行", value: allowed, color: "#22D3EE", pct: allowedPct },
    { name: "拦截", value: blocked, color: "#FB7185", pct: blockedPct },
    { name: "复核", value: review, color: "#FBBF24", pct: reviewPct },
  ];
  const queue = (recentPredictions || []).filter((item) => item.category !== "safe").slice(0, 3);
  const queueRows = queue.length ? queue : [
    { content: "免费领取加密货币，点击链接立即参与…", category: "spam", confidence: 0.987, input_type: "用户评论" },
    { content: "这条内容包含潜在攻击性表达，需要人工复核…", category: "abuse", confidence: 0.961, input_type: "用户帖子" },
    { content: "下载破解软件并永久激活，来源未经验证…", category: "suspicious", confidence: 0.883, input_type: "私信消息" },
  ];
  const healthOk = !systemHealth || systemHealth.api_status === "operational";

  return (
    <section className="metrics-hero-overview" aria-label="审核指标总览">
      <div className="metrics-kpi-grid">
        {metrics.map(({ label, value, trend, icon: Icon, accent, down }) => (
          <SpotlightCard
            key={label}
            className="metric-hero-card"
            spotlightColor={`${accent}1f`}
            style={{ "--metric-accent": accent }}
          >
            <div className="metric-hero-top">
              <span className="metric-icon"><Icon /></span>
              <span className="metric-status-dot" />
            </div>
            <p>{label}</p>
            <strong><Counter value={value} formatter={compactNumber} /></strong>
            <div className="metric-hero-footer">
              <span className={down ? "metric-trend-down" : ""}>{down ? "↓" : "↑"} {trend}</span>
              <small>较昨日</small>
              <i />
            </div>
          </SpotlightCard>
        ))}
      </div>

      <div className="metrics-primary-grid">
        <div className="console-panel trend-panel">
          <div className="panel-heading">
            <div><h2>审核趋势</h2><p>最近 24 小时内容裁决变化</p></div>
            <div className="chart-legend"><span className="legend-allowed">放行</span><span className="legend-blocked">拦截</span></div>
          </div>
          <div className="trend-chart">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={fallbackTrend} margin={{ top: 12, right: 8, left: -22, bottom: 0 }}>
                <defs>
                  <linearGradient id="heroAllowed" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#22D3EE" stopOpacity={0.32} />
                    <stop offset="100%" stopColor="#22D3EE" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="heroBlocked" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#8B5CF6" stopOpacity={0.2} />
                    <stop offset="100%" stopColor="#8B5CF6" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{ fill: "#64748b", fontSize: 9 }} />
                <YAxis axisLine={false} tickLine={false} tick={{ fill: "#64748b", fontSize: 9 }} />
                <Tooltip contentStyle={{ background: "#0B1020", border: "1px solid rgba(148,163,184,.18)", borderRadius: 10, fontSize: 11 }} />
                <Area type="monotone" dataKey="allowed" name="放行" stroke="#22D3EE" strokeWidth={2.4} fill="url(#heroAllowed)" />
                <Area type="monotone" dataKey="blocked" name="拦截" stroke="#8B5CF6" strokeWidth={2} fill="url(#heroBlocked)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <BorderGlow className="decision-panel-wrap" color="#7C3AED">
          <div className="decision-panel">
            <div className="panel-heading">
              <div><h2>实时裁决</h2><p>当前审核结果构成</p></div>
              <span className={`live-chip ${healthOk ? "" : "live-chip-warn"}`}><i />{healthOk ? "实时" : "受限"}</span>
            </div>
            <div className="decision-content">
              <div className="decision-chart">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={outcomeData} dataKey="value" innerRadius="62%" outerRadius="88%" paddingAngle={2} stroke="transparent">
                      {outcomeData.map((entry) => <Cell key={entry.name} fill={entry.color} />)}
                    </Pie>
                  </PieChart>
                </ResponsiveContainer>
                <div><strong>{total ? 100 : 0}%</strong><span>已裁决</span></div>
              </div>
              <div className="decision-legend">
                {outcomeData.map((entry) => (
                  <div key={entry.name}>
                    <i style={{ background: entry.color }} />
                    <strong>{entry.pct}%</strong>
                    <span>{entry.name}</span>
                    <small>{entry.value.toLocaleString()}</small>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </BorderGlow>
      </div>

      <div className="metrics-secondary-grid">
        <BorderGlow className="risk-queue-wrap" color="#7C3AED">
          <div className="risk-queue">
            <div className="panel-heading">
              <div><h2>高风险内容队列</h2><p>按置信度与风险等级排序</p></div>
              <button>查看全部队列</button>
            </div>
            <div className="risk-table">
              <div className="risk-table-head">
                <span>内容预览</span><span>风险类型</span><span>置信度</span><span>来源</span><span>操作</span>
              </div>
              {queueRows.map((item, index) => {
                const confidence = item.confidence > 1 ? item.confidence : item.confidence * 100;
                return (
                  <div className="risk-table-row" key={item.id || item._id || index}>
                    <span>{item.content || item.text || "内容等待人工复核…"}</span>
                    <span><b className={index === 2 ? "risk-medium" : ""}>{index === 2 ? "中风险" : "高风险"}</b></span>
                    <span><strong>{confidence.toFixed(1)}%</strong></span>
                    <span>{item.input_type || "用户内容"}</span>
                    <span><button>查看详情</button></span>
                  </div>
                );
              })}
            </div>
          </div>
        </BorderGlow>

        <BorderGlow className="pipeline-panel-wrap" color="#22D3EE">
          <div className="pipeline-panel">
            <div className="panel-heading">
              <div><h2>审核流水线</h2><p>端到端实时运行状态</p></div>
              <Zap />
            </div>
            <div className="pipeline-list">
              {pipeline.map(({ label, latency, icon: Icon, color }) => (
                <div key={label} className="pipeline-row">
                  <span className="pipeline-node" style={{ "--node-color": color }}><Icon /></span>
                  <strong>{label}</strong>
                  <span className="pipeline-running"><i />运行中</span>
                  <small>{latency}</small>
                </div>
              ))}
            </div>
          </div>
        </BorderGlow>
      </div>
    </section>
  );
}
