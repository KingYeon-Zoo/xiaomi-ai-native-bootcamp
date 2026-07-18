import { memo, useCallback, useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import {
  Activity,
  Bot,
  BrainCircuit,
  CheckCircle2,
  ChevronRight,
  CircleDot,
  Cpu,
  Database,
  Eye,
  FileSearch,
  Gauge,
  GitCompareArrows,
  Gavel,
  Image,
  Layers3,
  Network,
  RefreshCw,
  ScanEye,
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  TimerReset,
  UserRoundSearch,
  Workflow,
  Zap,
} from "lucide-react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import metricsService from "../../services/metricsService";
import { controlCenterDemo, getControlCenterDemo } from "../../data/controlCenterDemo";
import { BorderGlow, Counter, SpotlightCard } from "../reactbits/ReactBits";
import "./operations-dashboard.css";

const MODE_OPTIONS = [
  { id: "agent", label: "Agent 方案", icon: Bot },
  { id: "ml", label: "机器学习方案", icon: Cpu },
  { id: "compare", label: "双方案对比", icon: GitCompareArrows },
];

const RANGE_OPTIONS = [
  { value: 1, label: "1 小时" },
  { value: 24, label: "24 小时" },
  { value: 168, label: "7 天" },
];

const KPI_ICONS = [Activity, ShieldCheck, ShieldAlert, UserRoundSearch];
const KPI_ACCENTS = ["#8b5cf6", "#22d3ee", "#fb5f6f", "#f6b73c"];
const compactNumber = (value) => Number(value || 0).toLocaleString("zh-CN");
const formatLatency = (value) => (
  value >= 1000 ? `${(value / 1000).toFixed(2)} s` : `${value} ms`
);

const pipelineIcons = {
  "规则预检": FileSearch,
  "文本取证": BrainCircuit,
  "视觉取证": ScanEye,
  "风险路由": Network,
  "质疑与仲裁": Gavel,
  "策略裁决": ShieldCheck,
  "文本规范化": FileSearch,
  "规则引擎": ShieldCheck,
  "文本分类": BrainCircuit,
  "图像分类": Image,
  "决策融合": CheckCircle2,
};

function ArchitectureSwitcher({
  mode,
  onModeChange,
  timeRange,
  onTimeRangeChange,
  source,
  refreshing,
  onRefresh,
}) {
  return (
    <div className="architecture-toolbar">
      <div className="architecture-tabs" role="tablist" aria-label="审核架构">
        {MODE_OPTIONS.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            role="tab"
            aria-selected={mode === id}
            className={mode === id ? "is-active" : ""}
            onClick={() => onModeChange(id)}
            data-testid={`architecture-${id}`}
          >
            <Icon />
            <span>{label}</span>
          </button>
        ))}
      </div>
      <div className="architecture-meta">
        <span className="data-source"><Database />{source === "mongodb_demo_snapshot" ? "Mongo 演示快照" : "演示数据"}</span>
        <div className="range-switcher" aria-label="时间范围">
          {RANGE_OPTIONS.map(({ value, label }) => (
            <button
              key={value}
              className={timeRange === value ? "is-active" : ""}
              onClick={() => onTimeRangeChange(value)}
            >
              {label}
            </button>
          ))}
        </div>
        <button className="refresh-control" onClick={onRefresh} aria-label="刷新指标">
          <RefreshCw className={refreshing ? "is-spinning" : ""} />
        </button>
      </div>
    </div>
  );
}

const KpiGrid = memo(function KpiGrid({ data }) {
  const cards = [
    { label: "审核总量", value: data.total, detail: "统一回放集", trend: "18.6%" },
    { label: "自动放行", value: data.allowed, detail: `${((data.allowed / data.total) * 100).toFixed(1)}%`, trend: "20.3%" },
    { label: "自动拦截", value: data.blocked, detail: `${((data.blocked / data.total) * 100).toFixed(1)}%`, trend: "12.7%" },
    { label: "待人工复核", value: data.review, detail: `${((data.review / data.total) * 100).toFixed(1)}%`, trend: "6.4%", down: true },
  ];

  return (
    <div className="operations-kpi-grid">
      {cards.map((card, index) => {
        const Icon = KPI_ICONS[index];
        const accent = KPI_ACCENTS[index];
        return (
          <SpotlightCard
            key={card.label}
            className="operations-kpi-card"
            style={{ "--accent": accent }}
            spotlightColor={`${accent}20`}
          >
            <div className="operations-kpi-card__header">
              <span><Icon /></span>
              <i />
            </div>
            <p>{card.label}</p>
            <strong><Counter value={card.value} formatter={compactNumber} /></strong>
            <div className="operations-kpi-card__footer">
              <b className={card.down ? "is-down" : ""}>{card.down ? "↓" : "↑"} {card.trend}</b>
              <small>{card.detail}</small>
              <em>
                <i /><i /><i /><i />
              </em>
            </div>
          </SpotlightCard>
        );
      })}
    </div>
  );
});

const TrendPanel = memo(function TrendPanel({ data, mode }) {
  return (
    <div className="operations-panel trend-operations-panel">
      <div className="operations-panel-heading">
        <div>
          <span>{mode === "agent" ? "AGENT DECISION STREAM" : "ML INFERENCE STREAM"}</span>
          <h2>审核趋势</h2>
          <p>最近 24 小时内容裁决变化</p>
        </div>
        <div className="operations-chart-legend">
          <span className="is-allow">放行</span>
          <span className="is-block">拦截</span>
          <span className="is-review">复核</span>
        </div>
      </div>
      <div className="operations-trend-chart">
        <ResponsiveContainer
          width="100%"
          height="100%"
          minWidth={0}
          minHeight={0}
          initialDimension={{ width: 640, height: 198 }}
        >
          <AreaChart data={data} margin={{ top: 12, right: 8, left: -24, bottom: 0 }}>
            <defs>
              <linearGradient id={`allowed-${mode}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#22d3ee" stopOpacity={0.32} />
                <stop offset="100%" stopColor="#22d3ee" stopOpacity={0} />
              </linearGradient>
              <linearGradient id={`blocked-${mode}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#8b5cf6" stopOpacity={0.2} />
                <stop offset="100%" stopColor="#8b5cf6" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid vertical={false} stroke="rgba(148,163,184,.1)" strokeDasharray="4 4" />
            <XAxis dataKey="time" interval={2} axisLine={false} tickLine={false} tick={{ fill: "#70809c", fontSize: 9 }} />
            <YAxis axisLine={false} tickLine={false} tick={{ fill: "#70809c", fontSize: 9 }} />
            <Tooltip
              contentStyle={{ background: "#080d1c", border: "1px solid rgba(139,92,246,.35)", borderRadius: 10, fontSize: 11 }}
              labelStyle={{ color: "#dbeafe" }}
            />
            <Area type="monotone" dataKey="allowed" name="放行" stroke="#22d3ee" strokeWidth={2.4} fill={`url(#allowed-${mode})`} />
            <Area type="monotone" dataKey="blocked" name="拦截" stroke="#8b5cf6" strokeWidth={2} fill={`url(#blocked-${mode})`} />
            <Area type="monotone" dataKey="review" name="复核" stroke="#f6b73c" strokeWidth={1.4} fill="transparent" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
});

const DecisionPanel = memo(function DecisionPanel({ data }) {
  const total = data.reduce((sum, item) => sum + item.value, 0);
  return (
    <BorderGlow className="operations-panel-glow decision-operations-glow" color="#7c3aed">
      <div className="operations-panel decision-operations-panel">
        <div className="operations-panel-heading">
          <div><span>REAL-TIME VERDICT</span><h2>实时裁决</h2><p>当前审核结果构成</p></div>
          <b className="operations-live"><i />实时</b>
        </div>
        <div className="decision-operations-content">
          <div className="decision-operations-chart">
            <ResponsiveContainer
              width="100%"
              height="100%"
              minWidth={0}
              minHeight={0}
              initialDimension={{ width: 170, height: 170 }}
            >
              <PieChart>
                <Pie data={data} dataKey="value" innerRadius="61%" outerRadius="88%" paddingAngle={2} stroke="transparent">
                  {data.map((entry) => <Cell key={entry.name} fill={entry.color} />)}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
            <div><strong>100%</strong><span>已裁决</span></div>
          </div>
          <div className="decision-operations-legend">
            {data.map((entry) => (
              <div key={entry.name}>
                <i style={{ background: entry.color }} />
                <strong>{Math.round((entry.value / total) * 100)}%</strong>
                <span>{entry.name}</span>
                <small>{compactNumber(entry.value)}</small>
              </div>
            ))}
          </div>
        </div>
      </div>
    </BorderGlow>
  );
});

function RiskQueue({ items, mode, setActiveTab }) {
  return (
    <BorderGlow className="operations-panel-glow risk-operations-glow" color="#7c3aed">
      <div className="operations-panel risk-operations-panel">
        <div className="operations-panel-heading">
          <div>
            <span>{mode === "agent" ? "STRUCTURED EVIDENCE QUEUE" : "MODEL SCORE QUEUE"}</span>
            <h2>高风险内容队列</h2>
            <p>{mode === "agent" ? "证据、路由和人工恢复状态" : "按分类置信度与阈值排序"}</p>
          </div>
          <button onClick={() => setActiveTab?.("moderation")}>查看全部 <ChevronRight /></button>
        </div>
        <div className="operations-risk-table">
          <div className="operations-risk-head">
            <span>内容预览</span><span>风险类型</span><span>置信度</span><span>{mode === "agent" ? "裁决路由" : "来源"}</span><span>时间</span>
          </div>
          {items.map((item, index) => (
            <button className="operations-risk-row" key={item.id} onClick={() => setActiveTab?.("moderation")}>
              <span>{item.content}</span>
              <span><b className={index === 2 ? "is-medium" : ""}>{item.risk}</b></span>
              <span><strong>{item.confidence.toFixed(1)}%</strong></span>
              <span>{mode === "agent" ? item.route : item.source}</span>
              <span>{item.time}<ChevronRight /></span>
            </button>
          ))}
        </div>
      </div>
    </BorderGlow>
  );
}

function PipelinePanel({ items, mode }) {
  return (
    <BorderGlow className="operations-panel-glow pipeline-operations-glow" color="#22d3ee">
      <div className="operations-panel pipeline-operations-panel">
        <div className="operations-panel-heading">
          <div>
            <span>{mode === "agent" ? "LANGGRAPH ORCHESTRATION" : "LOCAL MODEL PIPELINE"}</span>
            <h2>审核流水线</h2>
            <p>{mode === "agent" ? "节点状态与条件式路由" : "本地推理阶段实时状态"}</p>
          </div>
          {mode === "agent" ? <Workflow /> : <Zap />}
        </div>
        <div className="operations-pipeline-list">
          {items.map((item) => {
            const Icon = pipelineIcons[item.name] || CircleDot;
            return (
              <div key={item.name} className="operations-pipeline-row">
                <span><Icon /></span>
                <div><strong>{item.name}</strong><small>{item.agent}</small></div>
                <b className={item.status === "conditional" ? "is-conditional" : ""}><i />{item.status === "conditional" ? "按需触发" : "运行中"}</b>
                <em>{formatLatency(item.latency_ms)}</em>
              </div>
            );
          })}
        </div>
      </div>
    </BorderGlow>
  );
}

function ArchitectureDetail({ data, mode }) {
  return (
    <section className="architecture-detail-section">
      <div className="architecture-detail-copy">
        <span>{mode === "agent" ? "WHY AGENT" : "WHY MACHINE LEARNING"}</span>
        <h2>{mode === "agent" ? "深度取证，不只给分类分数" : "高速推理，适合稳定高吞吐场景"}</h2>
        <p>{data.description}</p>
        <div className="architecture-detail-stats">
          <div><TimerReset /><span>平均延迟</span><strong>{formatLatency(data.avg_latency_ms)}</strong></div>
          <div><Gauge /><span>审核精度</span><strong>{data.precision}%</strong></div>
          <div><Eye /><span>审计覆盖</span><strong>{data.audit_coverage}%</strong></div>
          <div><Layers3 /><span>峰值吞吐</span><strong>{data.throughput_per_second}/s</strong></div>
        </div>
      </div>
      <div className="architecture-route-card">
        <div className="operations-panel-heading">
          <div><span>ROUTING STRATEGY</span><h2>{mode === "agent" ? "分层裁决路径" : "固定推理路径"}</h2></div>
          <Sparkles />
        </div>
        <div className="architecture-route-list">
          {data.route_breakdown.map((route) => (
            <div key={route.name}>
              <div><strong>{route.name}</strong><span>{route.value}%</span></div>
              <i><b style={{ width: `${route.value}%` }} /></i>
              <small>{route.detail}</small>
            </div>
          ))}
        </div>
      </div>
      <div className="model-fleet-card">
        <div className="operations-panel-heading">
          <div><span>MODEL FLEET</span><h2>运行组件</h2></div>
          <BrainCircuit />
        </div>
        <div className="model-fleet-list">
          {data.models.map((model) => (
            <div key={model.name}>
              <span><Cpu /></span>
              <div><strong>{model.name}</strong><small>{model.role}</small></div>
              <b><i />在线</b>
              <em>{formatLatency(model.latency_ms)}</em>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function ComparisonView({ snapshot }) {
  const { agent, ml, comparison } = snapshot;
  const cards = [
    { label: "统一回放样本", value: comparison.same_evaluation_set, suffix: "条", icon: Database, accent: "#8b5cf6" },
    { label: "Agent 审核精度", value: agent.precision, suffix: "%", icon: Bot, accent: "#22d3ee" },
    { label: "ML 平均延迟", value: ml.avg_latency_ms, suffix: "ms", icon: Cpu, accent: "#34d399" },
    { label: "Agent 审计覆盖", value: agent.audit_coverage, suffix: "%", icon: Eye, accent: "#f6b73c" },
  ];
  return (
    <div className="comparison-view">
      <div className="comparison-kpi-grid">
        {cards.map(({ label, value, suffix, icon: Icon, accent }) => (
          <div key={label} style={{ "--accent": accent }}>
            <span><Icon /></span><p>{label}</p><strong>{compactNumber(value)}<small>{suffix}</small></strong>
          </div>
        ))}
      </div>
      <div className="comparison-main-grid">
        <div className="comparison-table-panel">
          <div className="operations-panel-heading">
            <div><span>SAME DATASET · DIFFERENT ARCHITECTURE</span><h2>双方案能力矩阵</h2><p>同一批内容回放结果，不混用口径</p></div>
            <GitCompareArrows />
          </div>
          <div className="comparison-table">
            <div><strong>比较维度</strong><strong><Bot />Agent 方案</strong><strong><Cpu />机器学习方案</strong></div>
            {comparison.dimensions.map((dimension) => (
              <div key={dimension.label}>
                <span>{dimension.label}</span>
                <b className={dimension.winner === "agent" ? "is-winner" : ""}>{dimension.agent}{dimension.winner === "agent" ? <CheckCircle2 /> : null}</b>
                <b className={dimension.winner === "ml" ? "is-winner" : ""}>{dimension.ml}{dimension.winner === "ml" ? <CheckCircle2 /> : null}</b>
              </div>
            ))}
          </div>
        </div>
        <div className="hybrid-strategy-panel">
          <span>RECOMMENDED ROUTING</span>
          <h2>混合调度策略</h2>
          <p>{comparison.recommendation}</p>
          <div>
            <span><Zap /></span>
            <div><strong>机器学习快速通道</strong><small>大规模、低风险、稳定分布</small></div>
          </div>
          <i />
          <div>
            <span><Bot /></span>
            <div><strong>Agent 深度审核通道</strong><small>图文冲突、高风险、需要证据链</small></div>
          </div>
          <i />
          <div>
            <span><UserRoundSearch /></span>
            <div><strong>人工最终裁决</strong><small>模型不可用或证据仍不一致</small></div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function ModelMetricsDashboard({ setActiveTab, timeRange, setTimeRange }) {
  const [snapshot, setSnapshot] = useState(controlCenterDemo);
  const [mode, setMode] = useState("agent");
  const [refreshing, setRefreshing] = useState(false);

  const fetchSnapshot = useCallback(async () => {
    setRefreshing(true);
    try {
      const data = await metricsService.getControlCenterMetrics(timeRange);
      setSnapshot(data);
    } catch {
      setSnapshot(getControlCenterDemo(timeRange));
    } finally {
      setRefreshing(false);
    }
  }, [timeRange]);

  useEffect(() => {
    fetchSnapshot();
  }, [fetchSnapshot]);

  const activeData = useMemo(
    () => snapshot[mode === "ml" ? "ml" : "agent"],
    [mode, snapshot],
  );

  return (
    <motion.div
      className="operations-dashboard"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.36, ease: "easeOut" }}
    >
      <ArchitectureSwitcher
        mode={mode}
        onModeChange={setMode}
        timeRange={timeRange}
        onTimeRangeChange={setTimeRange}
        source={snapshot.source}
        refreshing={refreshing}
        onRefresh={fetchSnapshot}
      />

      {mode === "compare" ? (
        <ComparisonView snapshot={snapshot} />
      ) : (
        <>
          <div className="architecture-context-line">
            <span className={mode === "agent" ? "is-agent" : "is-ml"}>
              {mode === "agent" ? <Bot /> : <Cpu />}
              {activeData.label}
            </span>
            <p>{activeData.description}</p>
            <strong><CircleDot />系统在线</strong>
          </div>
          <KpiGrid data={activeData} />
          <div className="operations-primary-grid">
            <TrendPanel data={activeData.trend} mode={mode} />
            <DecisionPanel data={activeData.decision_distribution} />
          </div>
          <div className="operations-secondary-grid">
            <RiskQueue items={activeData.queue} mode={mode} setActiveTab={setActiveTab} />
            <PipelinePanel items={activeData.pipeline} mode={mode} />
          </div>
          <ArchitectureDetail data={activeData} mode={mode} />
        </>
      )}
    </motion.div>
  );
}
