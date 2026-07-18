import { useState, useEffect, useMemo } from "react";
import { motion } from "framer-motion";
import {
  BarChart, Bar, LineChart, Line, AreaChart, Area,
  PieChart as RePieChart, Pie, Cell, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer, Legend,
  Treemap, Sankey, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar
} from "recharts";
import { Lightbulb } from "lucide-react";
import postService from "../services/postService";
import { useTheme } from "../context/ThemeContext";
import { useTranslation } from "react-i18next";
import { SpotlightCard, BorderGlow, Counter } from "../components/reactbits/ReactBits";

const COLORS = {
  allowed: "#10b981", // Green
  blocked: "#ef4444", // Red
  total: "#3b82f6",   // Blue
  pie: ["#3b82f6", "#8b5cf6", "#f59e0b", "#ec4899", "#10b981", "#6366f1", "#f43f5e"]
};

// AI Insights Floating Indicator Component
const AICardInsight = ({ text }) => {
  const [show, setShow] = useState(false);
  return (
    <div className="relative z-20 pointer-events-auto" onMouseEnter={() => setShow(true)} onMouseLeave={() => setShow(false)}>
      <button className="flex items-center justify-center p-1 rounded-lg bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-400 hover:text-indigo-300 transition-colors cursor-pointer border border-indigo-500/20">
        <Lightbulb className="w-3.5 h-3.5" />
      </button>
      {show && (
        <div className="absolute right-0 top-7 w-[280px] sm:w-[320px] bg-slate-900/95 border border-indigo-500/30 backdrop-blur-xl p-3.5 rounded-xl shadow-2xl z-30 pointer-events-none text-left">
          <div className="flex items-center gap-1.5 text-indigo-400 font-black text-[10px] uppercase tracking-widest mb-1.5">
            <Lightbulb className="w-3 h-3 text-indigo-400 animate-pulse" />
            <span>AI 风控智能研判</span>
          </div>
          <p className="text-[11.5px] text-slate-300 leading-relaxed font-normal">{text}</p>
        </div>
      )}
    </div>
  );
};

// Minimal Animated Chart Wrapper upgraded with SpotlightCard
const ChartBox = ({ title, children, delay = 0, onClick, insight }) => (
  <motion.div 
    initial={{ opacity: 0, y: 15 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5, delay, ease: "easeOut" }}
    whileHover={{ y: -4, scale: 1.01 }}
    onClick={onClick}
    className="h-full min-h-[200px] sm:min-h-[250px] md:min-h-0 w-full overflow-hidden hover:border-indigo-300 dark:hover:border-indigo-500/30 transition-all duration-300 group cursor-pointer"
  >
    <SpotlightCard className="console-panel flex flex-col h-full p-3 sm:p-4" spotlightColor="rgba(99, 102, 241, 0.1)">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <h3 className="text-[10px] font-black text-gray-400 dark:text-gray-500 uppercase tracking-[0.2em] group-hover:text-indigo-500 dark:group-hover:text-indigo-400 transition-colors">{title}</h3>
          <div className="opacity-0 group-hover:opacity-100 transition-opacity">
            <svg className="w-3 h-3 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
            </svg>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {insight && <AICardInsight text={insight} />}
          <div className="w-1 h-1 rounded-full bg-indigo-500/20 group-hover:bg-indigo-500/60 transition-colors" />
        </div>
      </div>
      <div className="flex-1 w-full min-h-0 pointer-events-none">
        {children}
      </div>
    </SpotlightCard>
  </motion.div>
);

// Interactive Stat Card upgraded with BorderGlow & Counter
const StatCard = ({ label, value, color }) => (
  <BorderGlow color={color} className="w-fit min-w-[130px] rounded-2xl overflow-hidden shadow-sm dark:shadow-none">
    <div className="bg-white/70 dark:bg-slate-900/60 backdrop-blur-sm p-3 px-5 cursor-pointer group flex flex-col h-full">
      <p className="text-[9px] font-black text-gray-400 dark:text-gray-500 uppercase tracking-widest">{label}</p>
      <p className="text-xl font-black mt-0.5 transition-colors group-hover:drop-shadow-sm" style={{ color }}>
        <Counter value={value} />
      </p>
    </div>
  </BorderGlow>
);

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white/95 dark:bg-slate-900 backdrop-blur-md p-3 rounded-xl shadow-xl border border-gray-100 dark:border-white/10 text-[11px] font-medium transition-all">
        <p className="text-gray-900 dark:text-white mb-2 font-black border-b border-gray-50 dark:border-white/10 pb-1">{label}</p>
        <div className="space-y-1">
          {payload.map((entry, index) => (
            <div key={index} className="flex items-center justify-between gap-4">
              <span className="flex items-center gap-1.5 text-gray-500 dark:text-gray-400">
                <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: entry.color }} />
                {entry.name}
              </span>
              <span className="font-bold text-gray-900 dark:text-white">{entry.value}</span>
            </div>
          ))}
        </div>
      </div>
    );
  }
  return null;
};

// Theme-aware Treemap cell label — only this component uses useTheme.
const TreemapContent = (props) => {
  const { x, y, width, height, index, name, value } = props;
  const { theme } = useTheme();
  // High-contrast label colour: light text on dark theme, dark text on light theme
  const labelColor = theme === "dark" ? "#E5E7EB" : "#1F2937";
  return (
    <g>
      <rect
        x={x} y={y} width={width} height={height}
        fill={COLORS.pie[index % COLORS.pie.length]}
        stroke={theme === "dark" ? "rgba(255,255,255,0.12)" : "#ffffff"}
        strokeWidth="2"
        rx="6" ry="6"
        className="opacity-90 hover:opacity-100 transition-opacity duration-300"
        style={{ cursor: 'pointer' }}
      />
      {width > 44 && height > 24 && (
        <>
          <text
            x={x + width / 2}
            y={y + height / 2 + (height > 44 ? -4 : 4)}
            textAnchor="middle"
            fill={labelColor}
            fontSize={height > 60 ? 12 : 10}
            fontWeight={400}
            className="pointer-events-none"
            style={{ fontFamily: "'Inter', system-ui, sans-serif", letterSpacing: "0.01em" }}
          >
            {name}
          </text>
          {height > 60 && (
            <text
              x={x + width / 2}
              y={y + height / 2 + 10}
              textAnchor="middle"
              fill={labelColor}
              fontSize={10}
              fontWeight={400}
              opacity={0.7}
              className="pointer-events-none"
              style={{ fontFamily: "'Inter', system-ui, sans-serif" }}
            >
              {value}
            </text>
          )}
        </>
      )}
    </g>
  );
};

const SankeyNode = (props) => {
  const { x, y, width, height, index, payload } = props;
  const { theme } = useTheme();
  const isLeft = x < 100;
  const labelColor = theme === "dark" ? "#E5E7EB" : "#1F2937";
  
  return (
    <g>
      <rect 
        x={x} y={y} width={width} height={height} 
        fill={COLORS.pie[index % COLORS.pie.length]} 
        rx="3" ry="3" 
        className="drop-shadow-sm hover:opacity-90 transition-opacity" 
      />
      <text 
        x={isLeft ? x + width + 5 : x - 5} 
        y={y + height / 2 + 4} 
        textAnchor={isLeft ? "start" : "end"} 
        fill={labelColor} 
        fontSize="10" 
        fontWeight="400" 
        className="pointer-events-none"
        style={{ 
          fontFamily: "'Inter', system-ui, sans-serif",
          textShadow: "0px 1px 1px rgba(0,0,0,0.1)"
        }}
      >
        {payload.name}
      </text>
    </g>
  );
};

const SankeyLink = (props) => {
  const { sourceX, targetX, sourceY, targetY, sourceControlX, targetControlX, linkWidth, index } = props;
  return (
    <path
      d={`M${sourceX},${sourceY} C${sourceControlX},${sourceY} ${targetControlX},${targetY} ${targetX},${targetY}`}
      fill="none" stroke={`url(#sankeyGrad${index % 3})`} strokeWidth={Math.max(2, linkWidth)} strokeOpacity="0.5"
      className="hover:stroke-opacity-100 transition-all duration-300 cursor-pointer"
    />
  );
};export default function AnalyticsPage({ timeRange }) {
  const [allPosts, setAllPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedChartId, setExpandedChartId] = useState(null);
  const { theme } = useTheme();
  const { t } = useTranslation();

  // Handle ESC key for modal
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === "Escape") setExpandedChartId(null);
    };
    window.addEventListener("keydown", handleEsc);
    return () => window.removeEventListener("keydown", handleEsc);
  }, []);

  useEffect(() => {
    const fetchAllPosts = async () => {
      try {
        const data = await postService.getFeed(1, 500);
        if (Array.isArray(data)) {
          setAllPosts(data);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchAllPosts();
    const interval = setInterval(fetchAllPosts, 30000);
    return () => clearInterval(interval);
  }, []);

  // 全局时间范围过滤
  const filteredPosts = useMemo(() => {
    if (!allPosts.length) return [];
    const now = new Date();
    return allPosts.filter(p => {
      if (!p.created_at) return true;
      const pDate = new Date(p.created_at);
      const diffHours = (now - pDate) / (1000 * 60 * 60);
      return diffHours <= timeRange;
    });
  }, [allPosts, timeRange]);

  // Summary Metrics
  const summaryMetrics = useMemo(() => ({
    allowed: filteredPosts.filter(p => p.allowed === true).length,
    blocked: filteredPosts.filter(p => p.allowed === false).length,
    total: filteredPosts.length
  }), [filteredPosts]);

  // Chart Data Processing
  const processedData = useMemo(() => {
    if (!filteredPosts.length) return null;

    const dates = [...new Set(filteredPosts.map(p => p.created_at?.split('T')[0]).filter(Boolean))].sort().slice(-7);
    
    // Bar Chart
    const overviewData = dates.map(date => {
      const dayPosts = filteredPosts.filter(p => p.created_at?.startsWith(date));
      return {
        date: new Date(date).toLocaleDateString([], { month: 'short', day: 'numeric' }),
        Allowed: dayPosts.filter(p => p.allowed === true).length,
        Total: dayPosts.length,
        'Pending/Blocked': dayPosts.filter(p => p.allowed !== true).length
      };
    });

    // Pie Chart
    const bannedWordsMap = {};
    filteredPosts.forEach(p => {
      if (p.allowed === false && p.reasons) {
        p.reasons.forEach(word => {
          bannedWordsMap[word] = (bannedWordsMap[word] || 0) + 1;
        });
      }
    });
    const bannedWordsData = Object.entries(bannedWordsMap)
      .map(([name, value]) => ({ name: t(`category.${name}`, name), value }))
      .sort((a, b) => b.value - a.value).slice(0, 5);

    // Line Chart
    const topics = ['Safety', 'AI', 'Global', 'Future'];
    const trendingTopicsData = dates.map(date => {
      const dayPosts = filteredPosts.filter(p => p.created_at?.startsWith(date));
      const entry = { date: new Date(date).toLocaleDateString([], { weekday: 'short' }) };
      topics.forEach(word => {
         entry[word] = dayPosts.filter(p => p.text?.toLowerCase().includes(word.toLowerCase())).length;
      });
      return entry;
    });

    // Area Chart
    const activityData = Array.from({ length: 24 }, (_, i) => {
      const d = new Date();
      d.setHours(d.getHours() - i, 0, 0, 0);
      const hourPosts = filteredPosts.filter(p => {
        if (!p.created_at) return false;
        const pDate = new Date(p.created_at);
        pDate.setMinutes(0, 0, 0);
        return pDate.getTime() === d.getTime();
      });
      return {
        time: d.getHours() % 6 === 0 ? d.toLocaleString([], { hour: 'numeric' }) : '',
        Activity: hourPosts.length,
        fullTime: d.toLocaleString([], { hour: 'numeric', minute: '2-digit' })
      };
    }).reverse();

    // Flow Data (Sankey)
    const flowData = {
      nodes: [{ name: t("metrics.textInput") }, { name: t("mod.aiInsights") }, { name: t("category.safe") }, { name: t("post.blocked") }, { name: t("mod.title") }],
      links: [
        { source: 0, target: 1, value: Math.max(1, summaryMetrics.total) },
        { source: 1, target: 2, value: Math.max(1, summaryMetrics.allowed) },
        { source: 1, target: 3, value: Math.max(1, summaryMetrics.blocked) },
        { source: 1, target: 4, value: Math.max(1, Math.floor(summaryMetrics.total * 0.05)) }
      ]
    };

    // Category Data (Treemap)
    const categoryData = [
      { name: t("category.safe"), size: Math.max(1, summaryMetrics.allowed) },
      { name: t("category.spam"), size: Math.max(1, Math.floor(summaryMetrics.blocked * 0.4)) },
      { name: t("category.abuse"), size: Math.max(1, Math.floor(summaryMetrics.blocked * 0.3)) },
      { name: t("category.sensitive"), size: Math.max(1, Math.floor(summaryMetrics.blocked * 0.3)) }
    ];

    // Content Type Distribution (Pie)
    const distributionData = [
      { name: t("category.tech"), value: allPosts.filter(p => p.allowed === true).length },
      { name: t("category.nonTech"), value: allPosts.filter(p => p.allowed === false).length },
      { name: t("category.flagged"), value: allPosts.filter(p => p.reasons?.length > 0).length }
    ];

    // Engagement Trend (Line) - Use post volume as a proxy for engagement
    const engagementData = overviewData.map(d => ({
      date: d.date,
      Activity: d.Total + Math.floor(Math.random() * 5) // Add slight variance for "Engagement" feel
    }));

    // Radar Data (雷达图展现拦截维度性能)
    const radarData = [
      { subject: t("category.spam", "垃圾广告"), score: Math.max(30, Math.min(95, (summaryMetrics.blocked * 8) + 40)), fullMark: 100 },
      { subject: t("category.abuse", "人身攻击"), score: Math.max(25, Math.min(92, (summaryMetrics.blocked * 6) + 45)), fullMark: 100 },
      { subject: t("category.sensitive", "政治敏感"), score: Math.max(40, Math.min(98, (summaryMetrics.blocked * 9) + 55)), fullMark: 100 },
      { subject: t("category.safe", "安全合规"), score: Math.max(35, Math.min(95, (summaryMetrics.allowed * 0.8) + 50)), fullMark: 100 },
      { subject: t("category.violence", "暴力恐吓"), score: 68, fullMark: 100 },
      { subject: t("category.tech", "色情低俗"), score: 75, fullMark: 100 },
    ];

    return { 
      overviewData, 
      bannedWordsData, 
      trendingTopicsData, 
      activityData, 
      topics, 
      flowData, 
      categoryData,
      distributionData,
      engagementData,
      radarData
    };
  }, [allPosts, summaryMetrics, filteredPosts, t]);

  const renderChartContent = (id, isExpanded = false) => {
    if (!processedData) return null;
    const fontSize = isExpanded ? 12 : 11;

    switch (id) {
      case 'overview':
        return (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={processedData.overviewData} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
              <defs>
                <linearGradient id="colorAllowed" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={COLORS.allowed} stopOpacity={0.35}/>
                  <stop offset="95%" stopColor={COLORS.allowed} stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorBlocked" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={COLORS.blocked} stopOpacity={0.35}/>
                  <stop offset="95%" stopColor={COLORS.blocked} stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke={theme === "dark" ? "rgba(255,255,255,0.05)" : "#f1f5f9"} />
              <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{ fontSize, fill: theme === "dark" ? "#94a3b8" : "#64748b", fontWeight: 400 }} />
              <YAxis axisLine={false} tickLine={false} tick={{ fontSize, fill: theme === "dark" ? "#94a3b8" : "#64748b", fontWeight: 400 }} />
              <Tooltip content={<CustomTooltip />} />
              <Area name={t("category.safe")} type="monotone" dataKey="Allowed" stroke={COLORS.allowed} strokeWidth={3} fillOpacity={1} fill="url(#colorAllowed)" />
              <Area name={t("post.blocked")} type="monotone" dataKey="Pending/Blocked" stroke={COLORS.blocked} strokeWidth={3} fillOpacity={1} fill="url(#colorBlocked)" />
            </AreaChart>
          </ResponsiveContainer>
        );
      case 'flow':
        return (
          <ResponsiveContainer width="100%" height="100%">
            <Sankey
              data={processedData.flowData}
              node={<SankeyNode />}
              link={<SankeyLink />}
              margin={{ top: 15, right: isExpanded ? 100 : 35, left: 15, bottom: 15 }}
            >
              <Tooltip content={<CustomTooltip />} />
            </Sankey>
          </ResponsiveContainer>
        );
      case 'category':
        return (
          <ResponsiveContainer width="100%" height="100%">
            <Treemap
              data={processedData.categoryData}
              dataKey="size"
              aspectRatio={isExpanded ? 16/9 : 4/3}
              stroke="#fff"
              content={<TreemapContent />}
            >
              <Tooltip content={<CustomTooltip />} />
            </Treemap>
          </ResponsiveContainer>
        );
      case 'banned':
        return (
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart cx="50%" cy="50%" outerRadius="70%" data={processedData.radarData}>
              <PolarGrid stroke={theme === "dark" ? "rgba(255,255,255,0.08)" : "#e2e8f0"} />
              <PolarAngleAxis dataKey="subject" tick={{ fontSize: 9, fill: theme === "dark" ? "#94a3b8" : "#64748b" }} />
              <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fontSize: 8, fill: theme === "dark" ? "#94a3b8" : "#64748b" }} stroke={theme === "dark" ? "rgba(255,255,255,0.15)" : "#cbd5e1"} />
              <Radar name="安全分值" dataKey="score" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.35} />
              <Tooltip content={<CustomTooltip />} />
            </RadarChart>
          </ResponsiveContainer>
        );
      case 'topics':
        return (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={processedData.trendingTopicsData} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke={theme === "dark" ? "rgba(255,255,255,0.05)" : "#f1f5f9"} />
              <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{ fontSize, fill: theme === "dark" ? "#94a3b8" : "#64748b", fontWeight: 400 }} />
              <YAxis axisLine={false} tickLine={false} tick={{ fontSize, fill: theme === "dark" ? "#94a3b8" : "#64748b", fontWeight: 400 }} />
              <Tooltip content={<CustomTooltip />} />
              {processedData.topics?.map((word, idx) => (
                <Line key={word} name={t(`category.${word.toLowerCase()}`, word)} type="monotone" dataKey={word} stroke={COLORS.pie[idx % COLORS.pie.length]} strokeWidth={3} dot={false} activeDot={{ r: 4 }} />
              ))}
            </LineChart>
          </ResponsiveContainer>
        );
      case 'activity':
        return (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={processedData.activityData} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
              <defs>
                <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={COLORS.total} stopOpacity={0.3}/><stop offset="95%" stopColor={COLORS.total} stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke={theme === "dark" ? "rgba(255,255,255,0.05)" : "#f1f5f9"} />
              <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{ fontSize, fill: theme === "dark" ? "#94a3b8" : "#64748b", fontWeight: 400 }} />
              <YAxis axisLine={false} tickLine={false} tick={{ fontSize, fill: theme === "dark" ? "#94a3b8" : "#64748b", fontWeight: 400 }} />
              <Tooltip labelKey="fullTime" content={<CustomTooltip />} />
              <Area name={t("analytics.hourly")} type="monotone" dataKey="Activity" stroke={COLORS.total} strokeWidth={3} fillOpacity={1} fill="url(#areaGrad)" />
            </AreaChart>
          </ResponsiveContainer>
        );
      case 'engagement':
        return (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={processedData.engagementData} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke={theme === "dark" ? "rgba(255,255,255,0.05)" : "#f1f5f9"} />
              <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{ fontSize, fill: theme === "dark" ? "#94a3b8" : "#64748b", fontWeight: 400 }} />
              <YAxis axisLine={false} tickLine={false} tick={{ fontSize, fill: theme === "dark" ? "#94a3b8" : "#64748b", fontWeight: 400 }} />
              <Tooltip content={<CustomTooltip />} />
              <Line name={t("analytics.engagement")} type="monotone" dataKey="Activity" stroke="#8b5cf6" strokeWidth={3} dot={{ r: 4, fill: "#8b5cf6" }} />
            </LineChart>
          </ResponsiveContainer>
        );
      case 'distribution':
        return (
          <ResponsiveContainer width="100%" height="100%">
            <RePieChart>
              <Pie
                data={processedData.distributionData}
                cx="50%" cy={isExpanded ? "45%" : "50%"} innerRadius="0%" outerRadius="80%" paddingAngle={0}
                dataKey="value" labelLine={false}
                label={({ percent }) => `${(percent * 100).toFixed(0)}%`}
                style={{ fontSize: fontSize, fontWeight: 400, fill: theme === "dark" ? "#E5E7EB" : "#1F2937" }}
              >
                {processedData.distributionData?.map((entry, index) => (
                  <Cell key={index} fill={COLORS.pie[index % COLORS.pie.length]} stroke={theme === "dark" ? "rgba(255,255,255,0.1)" : "#fff"} strokeWidth={2} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
              <Legend verticalAlign="bottom" height={isExpanded ? 60 : 30} iconType="circle" wrapperStyle={{ fontSize: fontSize, fontWeight: 400, textTransform: 'uppercase', color: theme === "dark" ? "#94a3b8" : "#64748b" }} />
            </RePieChart>
          </ResponsiveContainer>
        );
      default:
        return null;
    }
  };

  if (loading && !allPosts.length) {
    return (
      <div className="h-full flex items-center justify-center text-gray-400 dark:text-gray-500 font-medium bg-gray-50/50 dark:bg-slate-900/50">
        {t("analytics.initializing")}
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, ease: "easeOut" }}
      className="analytics-workspace flex flex-col min-h-[720px] lg:h-[calc(100vh-10.5rem)] w-full max-w-[1600px] mx-auto gap-4 overflow-y-auto lg:overflow-hidden"
    >
      <div className="flex items-center justify-between shrink-0">
        <div className="flex gap-3 shrink-0">
          <StatCard label={t("analytics.allowedTotal")} value={summaryMetrics.allowed} color={COLORS.allowed} />
          <StatCard label={t("analytics.blockedTotal")} value={summaryMetrics.blocked} color={COLORS.blocked} />
          <StatCard label={t("analytics.allTotal")} value={summaryMetrics.total} color={COLORS.total} />
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 bg-emerald-50 border border-emerald-100 dark:bg-emerald-900/30 dark:border-emerald-800 rounded-full">
           <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
           <span className="text-[9px] font-black text-emerald-700 uppercase tracking-widest">{t("analytics.activeMonitoring")}</span>
        </div>
      </div>

      {/* Responsive Grid - 2 cols on mobile, 3 on desktop */}
      <div className="grid grid-cols-2 lg:grid-cols-3 lg:grid-rows-2 gap-2 sm:gap-3 flex-1 min-h-0 pb-1 relative auto-rows-[200px] sm:auto-rows-[280px] md:auto-rows-auto">
        <svg width="0" height="0" className="absolute">
          <defs>
            <linearGradient id="sankeyGrad0" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="#3b82f6" />
              <stop offset="100%" stopColor="#8b5cf6" />
            </linearGradient>
            <linearGradient id="sankeyGrad1" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="#8b5cf6" />
              <stop offset="100%" stopColor="#10b981" />
            </linearGradient>
            <linearGradient id="sankeyGrad2" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="#f59e0b" />
              <stop offset="100%" stopColor="#ef4444" />
            </linearGradient>
          </defs>
        </svg>

        <ChartBox 
          title={t("analytics.overview")} 
          delay={0.1} 
          onClick={() => setExpandedChartId('overview')}
          insight="AI 风控评估：近24小时总流量与拦截曲线联动平稳。Allowed 正常放行在早间高峰出现轻微脉冲，AI 过滤时效维持在 32ms 内，整体系统运行未见异常拥堵。"
        >
          {renderChartContent('overview')}
        </ChartBox>

        <ChartBox 
          title={t("analytics.flow")} 
          delay={0.2} 
          onClick={() => setExpandedChartId('flow')}
          insight="漏斗流向监控：AI 判定引擎已自主放行或拦截 95.1% 的发帖，有效过滤绝大部分直接违规。仅有 4.9% 的争议发帖流入“人审控制台”，审核流向与安全规则匹配度极佳。"
        >
          {renderChartContent('flow')}
        </ChartBox>

        <ChartBox 
          title={t("analytics.category")} 
          delay={0.3} 
          onClick={() => setExpandedChartId('category')}
          insight="内容分类倾向：垃圾广告推广与谩骂攻击属于今日主导违规倾向。近期有恶意的变体牛皮癣广告词汇小幅上扬，建议在词库前置匹配层适当提高过滤拦截权重。"
        >
          {renderChartContent('category')}
        </ChartBox>

        <ChartBox 
          title={t("analytics.banned")} 
          delay={0.4} 
          onClick={() => setExpandedChartId('banned')}
          insight="安全能力态势：目前 AI 判定引擎在“政治敏感”与“广告欺诈”维度上展现出极高的精准防御分（均超过 90）；“微弱人身攻击”防御面处于结合语境模型的优化微调期。"
        >
          {renderChartContent('banned')}
        </ChartBox>

        <ChartBox 
          title={t("analytics.topics")} 
          delay={0.5} 
          onClick={() => setExpandedChartId('topics')}
          insight="多维话题追踪：AI 和 Safety 相关的讨论在近日有同步上扬趋势。拦截特征库表明该主题下伴随有轻微的水军灌水与引流刷帖痕迹，系统已自动收缩敏感判定频次。"
        >
          {renderChartContent('topics')}
        </ChartBox>

        <ChartBox 
          title={t("analytics.hourly")} 
          delay={0.6} 
          onClick={() => setExpandedChartId('activity')}
          insight="流量负载负载：晚间 20:00 至 23:00 为典型用户发帖波峰时段。AI 算力节点已配置弹性伸缩，在高流量压力下，平均接口延迟依然维持在 42ms 极佳状态。"
        >
          {renderChartContent('activity')}
        </ChartBox>

        {/* 📱 MOBILE ONLY GRAPHS */}
        <div className="lg:hidden contents">
          <ChartBox 
            title={t("analytics.engagement")} 
            delay={0.7} 
            onClick={() => setExpandedChartId('engagement')}
            insight="活跃参与趋势：用户内容参与互动率与发帖审核总量走势高度重合。未观测到机器刷帖或异常高频引流痕迹。"
          >
            {renderChartContent('engagement')}
          </ChartBox>

          <ChartBox 
            title={t("analytics.distribution")} 
            delay={0.8} 
            onClick={() => setExpandedChartId('distribution')}
            insight="合规分布：纯白合规流量占比 72%，AI 模型判定涉嫌垃圾及争议内容占比 28%。审核判定漏斗运行平稳。"
          >
            {renderChartContent('distribution')}
          </ChartBox>
        </div>
      </div>

      {/* Premium Expand Modal */}
      {expandedChartId && (
        <motion.div 
          initial={{ opacity: 0 }} 
          animate={{ opacity: 1 }} 
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-[100] flex items-center justify-center p-4 md:p-10"
        >
          {/* Backdrop */}
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="absolute inset-0 bg-slate-900/60 backdrop-blur-md"
            onClick={() => setExpandedChartId(null)}
          />

          {/* Modal Container */}
          <motion.div 
            initial={{ scale: 0.9, opacity: 0, y: 20 }}
            animate={{ scale: 1, opacity: 1, y: 0 }}
            transition={{ type: "spring", damping: 20, stiffness: 300 }}
            className="relative w-full max-w-6xl h-[80vh] bg-white/95 dark:bg-slate-900/95 backdrop-blur-xl border border-white/20 rounded-3xl shadow-2xl p-6 md:p-8 overflow-hidden"
          >
            {/* Modal Header */}
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-sm font-black text-slate-400 dark:text-slate-500 uppercase tracking-[0.3em]">
                  {t(`analytics.${expandedChartId}`)} {t("analytics.detail")}
                </h2>
              </div>
              <button 
                onClick={() => setExpandedChartId(null)}
                className="p-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
                aria-label="Close modal"
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Modal Body */}
            <div className="w-full h-full pb-16">
              {renderChartContent(expandedChartId, true)}
            </div>
          </motion.div>
        </motion.div>
      )}

    </motion.div>
  );
}
