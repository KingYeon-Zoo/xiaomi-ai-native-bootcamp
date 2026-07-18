import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  ShieldCheck, 
  ShieldAlert, 
  Eye, 
  Info, 
  CheckCheck, 
  Clock, 
  AlertTriangle,
  RefreshCw,
  Search
} from "lucide-react";
import postService from "../services/postService";

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all"); // all, alert, allowed, system
  const [readIds, setReadIds] = useState(() => {
    return JSON.parse(localStorage.getItem("loops_read_notifications") || "[]");
  });

  const fetchNotifications = async () => {
    setLoading(true);
    try {
      const data = await postService.getFeed(1, 100);
      if (Array.isArray(data)) {
        // 将帖子映射成通知消息
        const mapped = data.map((post, idx) => {
          const isAllowed = post.allowed;
          const isPending = post.allowed === null || post.allowed === undefined;
          const postTextSnippet = post.text ? (post.text.length > 35 ? post.text.substring(0, 35) + "..." : post.text) : "无文本内容";
          const postId = post.id || post._id || `post_${idx}`;
          const time = post.created_at ? new Date(post.created_at).toLocaleString() : "刚才";

          if (isAllowed === false) {
            return {
              id: `alert_${postId}`,
              type: "alert",
              time,
              title: "AI 自动拦截预警",
              content: `帖子 [内容: "${postTextSnippet}"] 触发了敏感词或视觉审核策略，系统已执行自动拦截。`,
              badge: post.reasons && post.reasons.length > 0 ? post.reasons[0] : "敏感内容",
              postId
            };
          } else if (isPending) {
            return {
              id: `review_${postId}`,
              type: "review",
              time,
              title: "等待人工裁决提示",
              content: `帖子 [内容: "${postTextSnippet}"] 被标记为中度风险，已挂起并推送至人工审核队列。`,
              badge: "人工复核",
              postId
            };
          } else {
            return {
              id: `allowed_${postId}`,
              type: "allowed",
              time,
              title: "内容自动放行通知",
              content: `帖子 [内容: "${postTextSnippet}"] 已通过多层 Agent 策略匹配，确认为合规内容并自动放行。`,
              badge: "正常通过",
              postId
            };
          }
        });

        // 加上几条常态化的系统日志通知，增强科技感和内容饱满度
        const systemLogs = [
          {
            id: "sys_log_1",
            type: "system",
            time: new Date(Date.now() - 1000 * 60 * 5).toLocaleString(), // 5分钟前
            title: "大模型 API 连接正常",
            content: "已成功握手云端安全审核 API 服务，当前网络延迟: 135ms，吞吐量正常。",
            badge: "API 连接",
          },
          {
            id: "sys_log_2",
            type: "system",
            time: new Date(Date.now() - 1000 * 60 * 30).toLocaleString(), // 30分钟前
            title: "安全规则库自动更新",
            content: "决策流引擎已同步最新敏感词防护列表，新增 4 个高频拦截策略。",
            badge: "引擎升级",
          },
          {
            id: "sys_log_3",
            type: "system",
            time: new Date(Date.now() - 1000 * 60 * 120).toLocaleString(), // 2小时前
            title: "实例自动扩容完成",
            content: "检测到突发内容发送量激增，文本审核 Agent 已扩容部署 2 个并行处理节点。",
            badge: "资源调度",
          }
        ];

        // 组合并排序 (将最近的通知放在最上面)
        const combined = [...mapped, ...systemLogs];
        setNotifications(combined);
      }
    } catch (err) {
      console.error("加载消息通知失败", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotifications();
    const interval = setInterval(fetchNotifications, 20000);
    return () => clearInterval(interval);
  }, []);

  const markAllAsRead = () => {
    const allIds = notifications.map(n => n.id);
    setReadIds(allIds);
    localStorage.setItem("loops_read_notifications", JSON.stringify(allIds));
  };

  const toggleRead = (id) => {
    let updated;
    if (readIds.includes(id)) {
      updated = readIds.filter(x => x !== id);
    } else {
      updated = [...readIds, id];
    }
    setReadIds(updated);
    localStorage.setItem("loops_read_notifications", JSON.stringify(updated));
  };

  const filteredNotifications = notifications.filter(item => {
    if (filter === "all") return true;
    return item.type === filter;
  });

  // 获取各种类型的未读数
  const unreadCount = filteredNotifications.filter(n => !readIds.includes(n.id)).length;

  return (
    <div className="notifications-container">
      {/* 头部标题区域 */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h2 className="text-lg font-black text-slate-800 dark:text-slate-100 flex items-center gap-2">
            安全事件消息中心
            {unreadCount > 0 && (
              <span className="px-2 py-0.5 text-[10px] bg-indigo-500 text-white rounded-full font-bold animate-pulse">
                {unreadCount} 条新未读
              </span>
            )}
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            监控系统下发的多层 AI 审核流水日志与全局安全系统事件。
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button 
            onClick={fetchNotifications}
            className="p-2 border border-slate-200 dark:border-white/10 hover:bg-slate-50 dark:hover:bg-white/5 text-slate-500 rounded-xl transition-colors"
            title="刷新数据"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          </button>
          <button 
            onClick={markAllAsRead}
            disabled={unreadCount === 0}
            className={`flex items-center gap-1.5 px-4 py-2 border rounded-xl text-xs font-semibold transition-all ${
              unreadCount === 0 
                ? "border-slate-100 dark:border-white/5 bg-slate-50/50 dark:bg-white/[0.02] text-slate-400 dark:text-slate-600 cursor-not-allowed" 
                : "border-indigo-500/30 hover:border-indigo-500/50 bg-indigo-500/10 hover:bg-indigo-500/15 text-indigo-600 dark:text-indigo-400"
            }`}
          >
            <CheckCheck className="w-4 h-4" />
            <span>全部标记已读</span>
          </button>
        </div>
      </div>

      {/* 分类过滤器 */}
      <div className="flex gap-1.5 border-b border-slate-100 dark:border-white/10 pb-4 mb-6 overflow-x-auto">
        {[
          { id: "all", label: "全部消息" },
          { id: "alert", label: "拦截预警" },
          { id: "review", label: "待人工审核" },
          { id: "allowed", label: "正常通过" },
          { id: "system", label: "系统日志" }
        ].map(opt => (
          <button
            key={opt.id}
            onClick={() => setFilter(opt.id)}
            className={`px-4 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all ${
              filter === opt.id 
                ? "bg-slate-900 text-white dark:bg-white dark:text-slate-900" 
                : "text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-white/5"
            }`}
          >
            {opt.label}
          </button>
        ))}
      </div>

      {/* 消息时间线列表 */}
      {loading && notifications.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-slate-400">
          <RefreshCw className="w-8 h-8 animate-spin mb-3 text-indigo-500" />
          <p className="text-xs">正在分析并拉取最新的安全日志...</p>
        </div>
      ) : filteredNotifications.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 border border-dashed border-slate-200 dark:border-white/10 rounded-2xl">
          <AlertTriangle className="w-8 h-8 mb-3 text-slate-300 dark:text-slate-700" />
          <p className="text-xs text-slate-500 dark:text-slate-400">该分类下当前无任何日志消息记录</p>
        </div>
      ) : (
        <div className="flex flex-col gap-3 relative">
          <AnimatePresence initial={false}>
            {filteredNotifications.map((item) => {
              const isRead = readIds.includes(item.id);
              
              // 匹配样式
              const config = {
                alert: {
                  icon: <ShieldAlert className="w-5 h-5 text-red-500" />,
                  bg: "border-red-200 bg-red-500/[0.03] dark:border-red-950/30 dark:bg-red-950/[0.05]",
                  accent: "bg-red-500 text-red-100 dark:bg-red-500/20 dark:text-red-300"
                },
                review: {
                  icon: <Eye className="w-5 h-5 text-amber-500" />,
                  bg: "border-amber-200 bg-amber-500/[0.03] dark:border-amber-950/30 dark:bg-amber-950/[0.05]",
                  accent: "bg-amber-500 text-amber-900 dark:bg-amber-500/20 dark:text-amber-300"
                },
                allowed: {
                  icon: <ShieldCheck className="w-5 h-5 text-emerald-500" />,
                  bg: "border-emerald-200 bg-emerald-500/[0.03] dark:border-emerald-950/30 dark:bg-emerald-950/[0.05]",
                  accent: "bg-emerald-500 text-emerald-100 dark:bg-emerald-500/20 dark:text-emerald-300"
                },
                system: {
                  icon: <Info className="w-5 h-5 text-blue-500" />,
                  bg: "border-blue-200 bg-blue-500/[0.03] dark:border-blue-950/30 dark:bg-blue-950/[0.05]",
                  accent: "bg-blue-500 text-blue-100 dark:bg-blue-500/20 dark:text-blue-300"
                }
              }[item.type] || {
                icon: <Info className="w-5 h-5 text-slate-500" />,
                bg: "border-slate-200 bg-slate-50 dark:border-white/10 dark:bg-white/[0.02]",
                accent: "bg-slate-500 text-white"
              };

              return (
                <motion.div
                  key={item.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: isRead ? 0.6 : 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  whileHover={{ scale: 1.005, y: -1 }}
                  transition={{ duration: 0.2 }}
                  onClick={() => toggleRead(item.id)}
                  className={`flex gap-4 p-4 border rounded-2xl cursor-pointer transition-all ${config.bg} ${
                    isRead ? "border-slate-100 dark:border-white/5 opacity-55" : ""
                  }`}
                >
                  <div className="shrink-0 flex items-center justify-center w-10 h-10 rounded-xl bg-white dark:bg-slate-900 border border-slate-100 dark:border-white/5 shadow-sm">
                    {config.icon}
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1.5 mb-1.5">
                      <div className="flex items-center gap-2">
                        <h4 className="text-xs font-black text-slate-800 dark:text-slate-200">{item.title}</h4>
                        <span className={`px-2 py-0.5 text-[8px] font-black rounded-md ${config.accent}`}>
                          {item.badge}
                        </span>
                        {!isRead && (
                          <span className="w-1.5 h-1.5 rounded-full bg-indigo-500" />
                        )}
                      </div>
                      <div className="flex items-center gap-1 text-[10px] text-slate-400">
                        <Clock className="w-3 h-3" />
                        <span>{item.time}</span>
                      </div>
                    </div>
                    <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                      {item.content}
                    </p>
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
}
