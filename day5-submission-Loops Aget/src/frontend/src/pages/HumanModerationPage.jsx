import { useState, useEffect, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  ShieldAlert, CheckCircle2, XCircle, PenLine,
  ChevronRight, AlertTriangle, Zap, Tag, Clock,
  User, Image as ImageIcon, FileText, Inbox,
  SkipForward, RefreshCw, Bot
} from "lucide-react";
import postService from "../services/postService";
import { useTranslation } from "react-i18next";

// ─── Helpers ────────────────────────────────────────────────────────────────

const AVATARS = [
  "https://api.dicebear.com/7.x/bottts/svg?seed=alpha",
  "https://api.dicebear.com/7.x/bottts/svg?seed=beta",
  "https://api.dicebear.com/7.x/bottts/svg?seed=gamma",
  "https://api.dicebear.com/7.x/bottts/svg?seed=delta",
  "https://api.dicebear.com/7.x/bottts/svg?seed=epsilon",
];

const derivePriority = (post) => {
  const conf = post._aiConfidence ?? 0;
  if (conf < 40) return "high";
  if (conf < 65) return "medium";
  return "low";
};

const deriveCategory = (post) => {
  if (post.allowed === false) return "non-tech";
  if (post.allowed === true) return "tech";
  return "uncertain";
};

const deriveFlags = (post) => {
  const flags = [];
  if (post.reasons?.length) flags.push("Flagged");
  if (post._aiConfidence < 40) flags.push("Suspicious");
  if (post.text?.length < 20) flags.push("Low Quality");
  if (!flags.length) flags.push("Uncertain");
  return flags;
};

// ─── Circular Progress ───────────────────────────────────────────────────────

const CircularProgress = ({ value, size = 110, stroke = 10 }) => {
  const r = (size - stroke) / 2;
  const circ = 2 * Math.PI * r;
  const offset = circ - (value / 100) * circ;
  const color = value >= 70 ? "#10b981" : value >= 45 ? "#f59e0b" : "#ef4444";
  const { t } = useTranslation();

  return (
    <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={r} fill="none"
          stroke="rgba(0,0,0,0.05)" strokeWidth={stroke} className="dark:stroke-white/10" />
        <motion.circle
          cx={size / 2} cy={size / 2} r={r} fill="none"
          stroke={color} strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={circ}
          initial={{ strokeDashoffset: circ }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1.2, ease: "easeOut" }}
          style={{ filter: `drop-shadow(0 0 6px ${color})` }}
        />
      </svg>
      <div className="absolute flex flex-col items-center">
        <span className="text-xl font-black text-slate-900 dark:text-white tabular-nums">{value}%</span>
        <span className="text-[9px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-widest">{t("mod.confidence")}</span>
      </div>
    </div>
  );
};

// ─── Skeleton Card ───────────────────────────────────────────────────────────

const SkeletonShimmer = () => (
  <div className="animate-pulse space-y-3 p-4">
    <div className="h-3 bg-slate-200 dark:bg-white/10 rounded-full w-3/4" />
    <div className="h-3 bg-slate-200 dark:bg-white/10 rounded-full w-full" />
    <div className="h-3 bg-slate-200 dark:bg-white/10 rounded-full w-5/6" />
    <div className="h-3 bg-slate-200 dark:bg-white/10 rounded-full w-2/3" />
  </div>
);

// ─── Priority Badge ──────────────────────────────────────────────────────────

const PriorityBadge = ({ level }) => {
  const { t } = useTranslation();
  const cfg = {
    high:   { label: t("category.high"), color: "#ef4444", bg: "rgba(239,68,68,0.15)",   shadow: "rgba(239,68,68,0.4)",   dot: "bg-red-500"    },
    medium: { label: t("category.medium"),    color: "#f59e0b", bg: "rgba(245,158,11,0.15)",  shadow: "rgba(245,158,11,0.4)",  dot: "bg-amber-400"  },
    low:    { label: t("category.low"),  color: "#10b981", bg: "rgba(16,185,129,0.15)",  shadow: "rgba(16,185,129,0.4)",  dot: "bg-emerald-500" },
  }[level];

  return (
    <div
      className="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-widest"
      style={{ background: cfg.bg, color: cfg.color, border: `1px solid ${cfg.color}40` }}
    >
      <span className={`w-1.5 h-1.5 rounded-full ${cfg.dot} animate-pulse`} />
      {cfg.label}
    </div>
  );
};

// ─── Category Badge ──────────────────────────────────────────────────────────

const CategoryBadge = ({ cat }) => {
  const { t } = useTranslation();
  const cfg = {
    tech:      { label: t("category.tech"),      color: "#10b981", bg: "rgba(16,185,129,0.12)"  },
    "non-tech":{ label: t("category.nonTech"),  color: "#ef4444", bg: "rgba(239,68,68,0.12)"   },
    uncertain: { label: t("category.uncertain"), color: "#f59e0b", bg: "rgba(245,158,11,0.12)"  },
  }[cat] ?? { label: t(`category.${cat}`, cat), color: "#94a3b8", bg: "rgba(148,163,184,0.1)" };

  return (
    <span
      className="px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-widest"
      style={{ background: cfg.bg, color: cfg.color, border: `1px solid ${cfg.color}30` }}
    >
      {cfg.label}
    </span>
  );
};

// ─── Ripple Button ───────────────────────────────────────────────────────────

const RippleBtn = ({ onClick, children, className = "", id, disabled = false }) => {
  const [ripples, setRipples] = useState([]);
  const ref = useRef(null);

  const handleClick = (e) => {
    if (disabled) return;
    const rect = ref.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const id = Date.now();
    setRipples(r => [...r, { x, y, id }]);
    setTimeout(() => setRipples(r => r.filter(rp => rp.id !== id)), 600);
    onClick?.(e);
  };

  return (
    <motion.button
      id={id}
      ref={ref}
      onClick={handleClick}
      whileHover={!disabled ? { scale: 1.04, y: -1 } : {}}
      whileTap={!disabled ? { scale: 0.96 } : {}}
      disabled={disabled}
      className={`relative overflow-hidden ${className} ${disabled ? "opacity-40 cursor-not-allowed" : "cursor-pointer"}`}
    >
      {ripples.map(rp => (
        <motion.span
          key={rp.id}
          initial={{ width: 0, height: 0, opacity: 0.5, x: rp.x, y: rp.y }}
          animate={{ width: 200, height: 200, opacity: 0, x: rp.x - 100, y: rp.y - 100 }}
          transition={{ duration: 0.55, ease: "easeOut" }}
          className="absolute rounded-full bg-white/30 pointer-events-none"
          style={{ transform: `translate(${rp.x - 100}px, ${rp.y - 100}px)` }}
        />
      ))}
      {children}
    </motion.button>
  );
};

// ─── Queue Preview Card ──────────────────────────────────────────────────────

const QueueCard = ({ post, isActive, onClick, index }) => {
  const priority = derivePriority(post);
  const dotColor = { high: "bg-red-500", medium: "bg-amber-400", low: "bg-emerald-500" }[priority];
  const { t } = useTranslation();

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
      whileHover={{ y: -2 }}
      onClick={onClick}
      className={`shrink-0 w-44 cursor-pointer rounded-xl p-3 border transition-all duration-200 ${
        isActive
          ? "border-indigo-500 bg-indigo-500/10 shadow-lg shadow-indigo-500/20"
          : "border-slate-200 dark:border-white/10 bg-white dark:bg-white/5 hover:border-indigo-400 dark:hover:border-white/20 shadow-sm dark:shadow-none"
      }`}
    >
      <div className="flex items-center gap-2 mb-2">
        <img src={AVATARS[index % AVATARS.length]} alt="" className="w-6 h-6 rounded-full bg-slate-100 dark:bg-slate-700" />
        <span className={`w-2 h-2 rounded-full ${dotColor} shadow-sm`} />
      </div>
      <p className="text-[10px] text-slate-700 dark:text-slate-300 line-clamp-2 leading-relaxed font-medium">{post.text || t("mod.noText")}</p>
      <p className="text-[9px] text-slate-500 dark:text-slate-500 mt-1.5 font-bold uppercase tracking-wider">{post._aiConfidence ?? "—"}% {t("mod.confidence")}</p>
    </motion.div>
  );
};

// ─── MAIN PAGE ───────────────────────────────────────────────────────────────

export default function HumanModerationPage() {
  const [queue, setQueue]           = useState([]);
  const [activeIdx, setActiveIdx]   = useState(0);
  const [loading, setLoading]       = useState(true);
  const [action, setAction]         = useState(null);      // "approve"|"reject"|"edit"
  const [showReason, setShowReason] = useState(false);
  const [reason, setReason]         = useState("");
  const [otherText, setOtherText]   = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [transitioning, setTrans]   = useState(false);
  const [toast, setToast]           = useState(null);
  const [agentTrace, setAgentTrace] = useState(null);
  const { t } = useTranslation();

  // ── Fetch flagged posts ──────────────────────────────────────────────────

  const loadQueue = useCallback(async () => {
    setLoading(true);
    try {
      const data = await postService.getFeed(1, 200);
      const flagged = (Array.isArray(data) ? data : [])
        .filter(p => p.allowed !== true || p.reasons?.length)
        .map((p, i) => ({
          ...p,
          _aiConfidence: Math.max(10, Math.min(99,
            typeof p.confidence_score === "number"
              ? Math.round(p.confidence_score * 100)
              : 30 + Math.floor(Math.random() * 50)
          )),
          _avatarSeed: AVATARS[i % AVATARS.length],
        }));
      setQueue(flagged);
      setActiveIdx(0);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  // ── Active post ──────────────────────────────────────────────────────────

  const current = queue[activeIdx] ?? null;
  const priority = current ? derivePriority(current) : "low";
  const category = current ? deriveCategory(current) : "uncertain";
  const flags    = current ? deriveFlags(current)    : [];

  useEffect(() => { loadQueue(); }, [loadQueue]);

  useEffect(() => {
    let active = true;
    setAgentTrace(null);
    if (!current?.moderation_run_id) return () => { active = false; };
    postService.getModerationTrace(current.moderation_run_id)
      .then((data) => {
        if (active) setAgentTrace(data);
      })
      .catch(() => {
        if (active) setAgentTrace(null);
      });
    return () => { active = false; };
  }, [current?.moderation_run_id]);

  // ── Action handlers ──────────────────────────────────────────────────────

  const selectAction = (type) => {
    setAction(type);
    setShowReason(type === "reject" || type === "edit");
    setReason("");
    setOtherText("");
  };

  const showToast = (msg, ok = true) => {
    setToast({ msg, ok });
    setTimeout(() => setToast(null), 3000);
  };

  const confirmAction = async () => {
    if (!current) return;
    setSubmitting(true);
    try {
      if (
        current.moderation_run_id &&
        (action === "approve" || action === "reject")
      ) {
        const selectedReason =
          action === "approve"
            ? "人工确认内容可放行"
            : otherText || reason || "人工确认内容违规";
        await postService.submitHumanDecision(
          current.moderation_run_id,
          {
            decision: action,
            reviewer_id: "training-camp-admin",
            reason: selectedReason,
          }
        );
        showToast(
          action === "approve" ? t("mod.postApproved") : t("mod.postRejected")
        );
      } else if (action === "reject") {
        await postService.deletePost(current.id);
        showToast(t("mod.postRejected"));
      } else if (action === "approve") {
        showToast(t("mod.postApproved"));
      } else {
        showToast(t("mod.postEditNotify"));
      }
      // advance queue
      setTrans(true);
      setTimeout(() => {
        setQueue(q => q.filter((_, i) => i !== activeIdx));
        setActiveIdx(i => Math.max(0, i - (i > 0 ? 1 : 0)));
        setAction(null);
        setShowReason(false);
        setTrans(false);
        setSubmitting(false);
      }, 350);
    } catch {
      showToast(t("mod.errorAction"), false);
      setSubmitting(false);
    }
  };

  const switchPost = (idx) => {
    if (idx === activeIdx) return;
    setTrans(true);
    setTimeout(() => {
      setActiveIdx(idx);
      setAction(null);
      setShowReason(false);
      setTrans(false);
    }, 280);
  };

  const skipPost = () => {
    if (queue.length > 1) switchPost((activeIdx + 1) % queue.length);
  };

  // ── UI ───────────────────────────────────────────────────────────────────

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="moderation-page flex flex-col min-h-[700px] lg:h-[calc(100vh-10.5rem)] w-full max-w-[1600px] mx-auto overflow-hidden gap-3"
    >
      {/* ── HEADER ─────────────────────────────────────────────────────────── */}
      <div className="flex items-center justify-end shrink-0 px-1">
        <div className="flex items-center gap-2">
          {/* Pending counter */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-violet-500/10 border border-violet-500/30">
            <Inbox className="w-3.5 h-3.5 text-violet-600 dark:text-violet-400" />
            <span className="text-xs font-black text-violet-700 dark:text-violet-300">
              {loading ? "…" : t("mod.postsPending", { count: queue.length })}
            </span>
          </div>

          {/* Refresh */}
          <motion.button
            onClick={loadQueue}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.9, rotate: 180 }}
            className="w-8 h-8 rounded-full flex items-center justify-center bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 hover:border-indigo-400 dark:hover:border-white/20 text-slate-500 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-white transition-colors shadow-sm dark:shadow-none"
            title={t("mod.refresh")}
          >
            <RefreshCw className="w-3.5 h-3.5" />
          </motion.button>
        </div>
      </div>

      {/* thin divider */}
      <div className="h-px bg-slate-100 dark:bg-white/10 shrink-0" />

      {/* ── BODY ────────────────────────────────────────────────────────────── */}
      {loading ? (
        <div className="flex-1 grid grid-cols-5 gap-3 min-h-0">
          <div className="col-span-3 rounded-2xl border border-slate-200 dark:border-white/10 bg-white dark:bg-white/[0.04] backdrop-blur-sm"><SkeletonShimmer /></div>
          <div className="col-span-2 rounded-2xl border border-slate-200 dark:border-white/10 bg-white dark:bg-white/[0.04] backdrop-blur-sm"><SkeletonShimmer /></div>
        </div>
      ) : queue.length === 0 ? (
        <div className="flex-1 flex flex-col items-center justify-center gap-3 text-slate-400 dark:text-slate-500">
          <CheckCircle2 className="w-10 h-10 text-emerald-500/60" />
          <p className="text-sm font-bold">{t("mod.allCaughtUp")}</p>
          <button onClick={loadQueue} className="text-xs text-indigo-500 hover:text-indigo-400 underline font-black uppercase tracking-widest">{t("mod.reload")}</button>
        </div>
      ) : (
        <div className="moderation-workspace-grid flex-1 min-h-0">

          <aside className="moderation-queue-column">
            <div className="moderation-column-heading">
              <Inbox />
              <span>待审队列</span>
              <strong>{queue.length}</strong>
            </div>
            <div className="moderation-queue-list custom-scroll">
              {queue.map((p, i) => (
                <QueueCard
                  key={p.id ?? i}
                  post={p}
                  index={i}
                  isActive={i === activeIdx}
                  onClick={() => switchPost(i)}
                />
              ))}
            </div>
          </aside>

          {/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ CENTER ━━━━━━━━━━━━━ */}
          <div className="moderation-content-column flex flex-col gap-3 min-h-0">

            {/* POST REVIEW CARD */}
            <motion.div
              layout
              className="flex-1 min-h-0 rounded-2xl border border-slate-200 dark:border-white/10 bg-white dark:bg-white/[0.04] backdrop-blur-xl shadow-xl dark:shadow-2xl shadow-slate-200 dark:shadow-black/20 flex flex-col overflow-hidden relative"
            >
              {/* Priority badge — top right */}
              <div className="absolute top-3 right-3 z-10">
                <PriorityBadge level={priority} />
              </div>

              {/* User / meta strip */}
              <div className="flex items-center gap-3 pl-4 pr-20 pt-4 pb-2 shrink-0 border-b border-slate-100 dark:border-white/[0.06]">
                <AnimatePresence mode="wait">
                  <motion.img
                    key={current?.id}
                    initial={{ opacity: 0, scale: 0.85 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.25 }}
                    src={current?._avatarSeed}
                    alt="avatar"
                    className="w-9 h-9 rounded-full bg-slate-100 dark:bg-slate-700 ring-2 ring-indigo-500/40 shrink-0"
                  />
                </AnimatePresence>
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-black text-slate-900 dark:text-slate-200 truncate">
                    {current?.username ?? `User-${current?.id?.slice(-5) ?? t("category.uncertain")}`}
                  </p>
                  <p className="text-[9px] text-slate-500 font-mono truncate">
                    ID: {current?.id ?? "—"}
                  </p>
                </div>
                <div className="flex items-center gap-1 text-[9px] text-slate-500">
                  <Clock className="w-3 h-3" />
                  {current?.created_at
                    ? new Date(current.created_at).toLocaleString([], { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" })
                    : t("category.uncertain")}
                </div>
              </div>

              {/* Post body — scrollable */}
              <AnimatePresence mode="wait">
                <motion.div
                  key={current?.id + "-body"}
                  initial={{ opacity: 0, x: transitioning ? -20 : 20 }}
                  animate={{ opacity: transitioning ? 0 : 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                  className="flex-1 min-h-0 overflow-y-auto px-4 py-3 space-y-3 custom-scroll"
                >
                  {/* Text */}
                  {current?.text && (
                    <div className="flex gap-2">
                      <FileText className="w-4 h-4 text-indigo-500 dark:text-indigo-400 shrink-0 mt-0.5" />
                      <p className="text-sm text-slate-800 dark:text-slate-200 leading-relaxed font-medium">
                        {current.text}
                      </p>
                    </div>
                  )}

                  {/* Media preview */}
                  {current?.image_url && (
                    <div className="relative rounded-xl overflow-hidden border border-slate-100 dark:border-white/10 mt-1">
                      <img
                        src={current.image_url}
                        alt="Post media"
                        className="w-full max-h-44 object-cover"
                        onError={e => { e.target.style.display = "none"; }}
                      />
                      <div className="absolute top-2 left-2 flex items-center gap-1 px-2 py-0.5 rounded-md bg-black/60 text-[9px] text-slate-300 font-bold">
                        <ImageIcon className="w-3 h-3" /> {t("mod.media")}
                      </div>
                    </div>
                  )}

                  {/* Reasons/flags from AI */}
                  {current?.reasons?.length > 0 && (
                    <div className="rounded-lg bg-amber-500/8 border border-amber-500/20 p-2.5">
                      <p className="text-[9px] font-black text-amber-600 dark:text-amber-400 uppercase tracking-widest mb-1.5 flex items-center gap-1">
                        <AlertTriangle className="w-3 h-3" /> {t("mod.aiFlaggedReasons")}
                      </p>
                      <div className="flex flex-wrap gap-1.5">
                        {current.reasons.map((r, i) => (
                          <span key={i} className="px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-800 dark:text-amber-300 text-[10px] font-bold border border-amber-500/20">
                            {t(`category.${r}`, r)}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </motion.div>
              </AnimatePresence>

              {/* Skip */}
              <div className="shrink-0 px-4 py-2 border-t border-slate-100 dark:border-white/[0.06] flex justify-between items-center bg-slate-50/50 dark:bg-transparent">
                <span className="text-[9px] text-slate-500 dark:text-slate-600 font-bold uppercase tracking-widest">
                  {t("mod.queueProgress", { current: activeIdx + 1, total: queue.length })}
                </span>
                <button
                  onClick={skipPost}
                  className="flex items-center gap-1 text-[10px] text-slate-400 dark:text-slate-500 hover:text-indigo-600 dark:hover:text-slate-300 transition-colors font-black uppercase tracking-widest group"
                >
                  {t("mod.skip")} <SkipForward className="w-3 h-3 group-hover:translate-x-0.5 transition-transform" />
                </button>
              </div>
            </motion.div>

          </div>

          {/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ RIGHT ━━━━━━━━━━━━━ */}
          <div className="moderation-insights-column flex flex-col gap-3 min-h-0 overflow-y-auto pr-0.5 custom-scroll">

            {/* AI INSIGHTS CARD */}
            <div className="rounded-2xl border border-slate-200 dark:border-white/10 bg-white dark:bg-white/[0.04] backdrop-blur-xl shadow-lg dark:shadow-xl shadow-slate-200 dark:shadow-black/10 p-4 flex flex-col gap-4">
              {/* Header */}
              <div className="flex items-center gap-2">
                <Bot className="w-4 h-4 text-indigo-500 dark:text-indigo-400" />
                <span className="text-[10px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-[0.2em]">{t("mod.aiInsights")}</span>
              </div>

              {/* Confidence + Category row */}
              <div className="flex items-center gap-4">
                <AnimatePresence mode="wait">
                  <motion.div key={current?._aiConfidence}
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.4 }}>
                    <CircularProgress value={current?._aiConfidence ?? 0} />
                  </motion.div>
                </AnimatePresence>
                <div className="flex flex-col gap-2">
                  <div>
                    <p className="text-[9px] text-slate-500 font-bold uppercase tracking-widest mb-1">{t("mod.category")}</p>
                    <CategoryBadge cat={category} />
                  </div>
                  <div>
                    <p className="text-[9px] text-slate-500 font-bold uppercase tracking-widest mb-1">{t("mod.priority")}</p>
                    <PriorityBadge level={priority} />
                  </div>
                </div>
              </div>

              {/* Flags */}
              <div>
                <div className="flex items-center gap-1.5 mb-2">
                  <Tag className="w-3.5 h-3.5 text-slate-400 dark:text-slate-500" />
                  <p className="text-[9px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-widest">{t("mod.detectionFlags")}</p>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {flags.map(f => {
                    const flagLabels = {
                      "Flagged": t("category.flagged"),
                      "Suspicious": t("category.suspicious"),
                      "Low Quality": t("category.lowQuality"),
                      "Uncertain": t("category.uncertain")
                    };
                    return (
                      <span key={f}
                        className="px-2.5 py-1 rounded-full text-[10px] font-black border border-slate-100 dark:border-white/10 bg-slate-50 dark:bg-white/5 text-slate-600 dark:text-slate-300 hover:border-indigo-500/40 hover:text-indigo-600 dark:hover:text-indigo-300 transition-colors cursor-default">
                        {flagLabels[f] || f}
                      </span>
                    );
                  })}
                </div>
              </div>

              {agentTrace?.trace?.length > 0 && (
                <div className="rounded-xl border border-indigo-500/20 bg-indigo-500/5 p-3">
                  <p className="text-[9px] font-black text-indigo-600 dark:text-indigo-300 uppercase tracking-widest mb-2">
                    Agent 结构化执行轨迹
                  </p>
                  <div className="space-y-1.5">
                    {agentTrace.trace.map((item, index) => (
                      <div key={`${item.node}-${index}`} className="flex items-start gap-2 text-[10px]">
                        <span className="mt-1 w-1.5 h-1.5 rounded-full bg-indigo-500 shrink-0" />
                        <div className="min-w-0">
                          <strong className="text-slate-700 dark:text-slate-200">{item.node}</strong>
                          <span className="text-slate-500 dark:text-slate-400"> · {item.summary || item.status}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* ACTION CONTROLS */}
            <div className="rounded-2xl border border-slate-200 dark:border-white/10 bg-white dark:bg-white/[0.04] backdrop-blur-xl shadow-lg dark:shadow-xl shadow-slate-200 dark:shadow-black/10 p-4 flex flex-col gap-3">
              <div className="flex items-center gap-2 mb-1">
                <Zap className="w-4 h-4 text-yellow-500 dark:text-yellow-400" />
                <span className="text-[10px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-[0.2em]">{t("mod.actionControls")}</span>
              </div>

              {/* Three action buttons */}
              <div className="grid grid-cols-3 gap-2">
                {/* Approve */}
                <RippleBtn
                  id="mod-approve-btn"
                  onClick={() => selectAction("approve")}
                  className={`flex flex-col items-center gap-1.5 py-3 rounded-xl border text-[10px] font-black uppercase tracking-wider transition-all
                    ${action === "approve"
                      ? "border-emerald-500/60 bg-emerald-500/20 text-emerald-600 dark:text-emerald-300 shadow-lg shadow-emerald-500/20"
                      : "border-slate-100 dark:border-white/10 bg-slate-50 dark:bg-white/5 text-slate-400 dark:text-slate-400 hover:border-emerald-500/40 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-emerald-500/10"}`}
                >
                  <CheckCircle2 className="w-5 h-5" />
                  {t("mod.approve")}
                </RippleBtn>

                {/* Reject */}
                <RippleBtn
                  id="mod-reject-btn"
                  onClick={() => selectAction("reject")}
                  className={`flex flex-col items-center gap-1.5 py-3 rounded-xl border text-[10px] font-black uppercase tracking-wider transition-all group
                    ${action === "reject"
                      ? "border-red-500/60 bg-red-500/20 text-red-600 dark:text-red-300 shadow-lg shadow-red-500/20"
                      : "border-slate-100 dark:border-white/10 bg-slate-50 dark:bg-white/5 text-slate-400 dark:text-slate-400 hover:border-red-500/40 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-500/10 hover:animate-[wiggle_0.3s_ease-in-out]"}`}
                >
                  <XCircle className="w-5 h-5" />
                  {t("mod.reject")}
                </RippleBtn>

                {/* Send for Edit */}
                <RippleBtn
                  id="mod-edit-btn"
                  onClick={() => selectAction("edit")}
                  className={`flex flex-col items-center gap-1.5 py-3 rounded-xl border text-[10px] font-black uppercase tracking-wider transition-all
                    ${action === "edit"
                      ? "border-amber-500/60 bg-amber-500/20 text-amber-700 dark:text-amber-300 shadow-lg shadow-amber-500/20"
                      : "border-slate-100 dark:border-white/10 bg-slate-50 dark:bg-white/5 text-slate-400 dark:text-slate-400 hover:border-amber-500/40 hover:text-amber-600 dark:hover:text-amber-400 hover:bg-amber-500/10"}`}
                >
                  <PenLine className="w-5 h-5" />
                  {t("mod.edit")}
                </RippleBtn>
              </div>

              {/* Reason input — slide in */}
              <AnimatePresence>
                {showReason && (
                  <motion.div
                    initial={{ opacity: 0, height: 0, y: -8 }}
                    animate={{ opacity: 1, height: "auto", y: 0 }}
                    exit={{ opacity: 0, height: 0, y: -8 }}
                    transition={{ duration: 0.3, ease: "easeOut" }}
                    className="overflow-hidden"
                  >
                    <div className="rounded-xl border border-slate-100 dark:border-white/10 bg-slate-50/50 dark:bg-white/5 p-3 space-y-2 mt-1">
                      <p className="text-[9px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-widest">{t("mod.selectReason")}</p>
                      <select
                        id="mod-reason-select"
                        value={reason}
                        onChange={e => setReason(e.target.value)}
                        className="w-full rounded-lg bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 text-xs text-slate-900 dark:text-slate-200 px-3 py-2 outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/30 transition-all appearance-none shadow-sm dark:shadow-none"
                      >
                        <option value="" disabled>{t("mod.chooseReason")}</option>
                        <option value="not-tech">{t("category.nonTech")}</option>
                        <option value="spam">{t("category.spam")}</option>
                        <option value="low-quality">{t("category.lowQuality")}</option>
                        <option value="inappropriate">{t("category.sensitive")}</option>
                        <option value="other">{t("category.uncertain")}</option>
                      </select>

                      <AnimatePresence>
                        {reason === "other" && (
                          <motion.input
                            id="mod-other-input"
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: "auto" }}
                            exit={{ opacity: 0, height: 0 }}
                            placeholder={t("mod.otherReason")}
                            value={otherText}
                            onChange={e => setOtherText(e.target.value)}
                            className="w-full rounded-lg bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 text-xs text-slate-900 dark:text-slate-200 px-3 py-2 outline-none focus:border-indigo-500/50 placeholder-slate-400 dark:placeholder-slate-600 transition-all shadow-sm dark:shadow-none"
                          />
                        )}
                      </AnimatePresence>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Confirm button */}
              <AnimatePresence>
                {action && (
                  <motion.div
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 8 }}
                    transition={{ duration: 0.25 }}
                  >
                    <RippleBtn
                      id="mod-confirm-btn"
                      onClick={confirmAction}
                      disabled={submitting || (showReason && !reason)}
                      className={`w-full py-2.5 rounded-xl text-xs font-black uppercase tracking-wider flex items-center justify-center gap-2 transition-all
                        ${action === "approve"
                          ? "bg-gradient-to-r from-emerald-600 to-emerald-500 text-white shadow-lg shadow-emerald-500/30 hover:shadow-emerald-500/50"
                          : action === "reject"
                          ? "bg-gradient-to-r from-red-600 to-red-500 text-white shadow-lg shadow-red-500/30 hover:shadow-red-500/50"
                          : "bg-gradient-to-r from-amber-600 to-orange-500 text-white shadow-lg shadow-amber-500/30 hover:shadow-amber-500/50"
                        }`}
                    >
                      {submitting ? (
                        <RefreshCw className="w-4 h-4 animate-spin" />
                      ) : (
                        <>
                          <ChevronRight className="w-4 h-4" />
                          {action === "approve" ? t("mod.confirmApprove") : action === "reject" ? t("mod.confirmReject") : t("mod.sendEdit")}
                        </>
                      )}
                    </RippleBtn>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

          </div>{/* end right */}
        </div>
      )}

      {/* ── TOAST ──────────────────────────────────────────────────────────── */}
      <AnimatePresence>
        {toast && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.9 }}
            className={`fixed bottom-6 left-1/2 -translate-x-1/2 z-[100] flex items-center gap-2 px-5 py-3 rounded-2xl shadow-2xl text-sm font-bold
              ${toast.ok
                ? "bg-emerald-600 text-white shadow-emerald-500/30"
                : "bg-red-600 text-white shadow-red-500/30"
              }`}
          >
            {toast.ok ? <CheckCircle2 className="w-4 h-4" /> : <AlertTriangle className="w-4 h-4" />}
            {toast.msg}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
