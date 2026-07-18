import {
  Activity,
  AlertTriangle,
  Bell,
  CalendarDays,
  ChartNoAxesCombined,
  Infinity as InfinityIcon,
  Languages,
  LayoutDashboard,
  Menu,
  Moon,
  Sun,
  UsersRound,
  X,
} from "lucide-react";
import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { AnimatePresence, motion } from "framer-motion";
import { useTheme } from "../context/ThemeContext";
import { SpotlightCard, Aurora } from "./reactbits/ReactBits";
import Toast from "./Toast";
import postService from "../services/postService";

const pageMeta = {
  feed: {
    title: "发帖广场",
    subtitle: "提交内容并查看 AI 审核结果",
    eyebrow: "CONTENT OPERATIONS",
  },
  analytics: {
    title: "统计分析",
    subtitle: "实时内容流与风险趋势监控",
    eyebrow: "LIVE ANALYTICS",
  },
  metrics: {
    title: "内容审核控制台",
    subtitle: "实时监控 · 风险识别 · 人工复核",
    eyebrow: "AI SAFETY OPERATIONS",
  },
  moderation: {
    title: "人工审核",
    subtitle: "复核 AI 标记内容并完成最终裁决",
    eyebrow: "HUMAN IN THE LOOP",
  },
};

const RANGE_OPTIONS = [
  { value: 1, label: "最近 1 小时" },
  { value: 24, label: "最近 24 小时" },
  { value: 168, label: "最近 7 天" }
];

export default function AppShell({ 
  activeTab, 
  setActiveTab, 
  currentUser, 
  setCurrentUser,
  onLogout,
  timeRange,
  setTimeRange,
  children 
}) {
  const { theme, toggleTheme } = useTheme();
  const { t, i18n } = useTranslation();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [toast, setToast] = useState({ show: false, message: "", type: "success" });
  
  const isNormalUser = currentUser?.role === "user";
  
  // 交互菜单状态
  const [showTimeDropdown, setShowTimeDropdown] = useState(false);
  const [showUserDropdown, setShowUserDropdown] = useState(false);
  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [hasUnread, setHasUnread] = useState(true);
  const [unreadCount, setUnreadCount] = useState(0);

  // 轮询未读消息数
  useEffect(() => {
    if (isNormalUser) return;
    const checkUnread = async () => {
      try {
        const data = await postService.getFeed(1, 50);
        if (Array.isArray(data)) {
          const readIds = JSON.parse(localStorage.getItem("loops_read_notifications") || "[]");
          const mappedIds = data.map((post, idx) => {
            const postId = post.id || post._id || `post_${idx}`;
            return post.allowed === false ? `alert_${postId}` : (post.allowed === null || post.allowed === undefined ? `review_${postId}` : `allowed_${postId}`);
          });
          const systemLogIds = ["sys_log_1", "sys_log_2", "sys_log_3"];
          const allIds = [...mappedIds, ...systemLogIds];
          const unread = allIds.filter(id => !readIds.includes(id)).length;
          setUnreadCount(unread);
          setHasUnread(unread > 0);
        }
      } catch (err) {
        console.error("Failed to check unread notifications:", err);
      }
    };

    checkUnread();
    const interval = setInterval(checkUnread, 15000);
    return () => clearInterval(interval);
  }, [currentUser, activeTab, isNormalUser]);

  // 密码修改表单状态
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [modalError, setModalError] = useState("");

  const pageMetaWithNotify = {
    ...pageMeta,
    notifications: {
      title: "安全事件通知中心",
      subtitle: "实时监控全局 AI 内容防线事件与审核日志",
      eyebrow: "SECURITY ALERTS",
    }
  };

  const meta = pageMetaWithNotify[activeTab] || pageMeta.metrics;

  const showToast = (message, type = "success") => {
    setToast({ show: true, message, type });
  };

  // 根据角色进行导航控制
  const navItems = isNormalUser 
    ? [{ id: "feed", label: t("nav.feed"), icon: LayoutDashboard }]
    : [
        { id: "feed", label: t("nav.feed"), icon: LayoutDashboard },
        { id: "analytics", label: t("nav.analytics"), icon: ChartNoAxesCombined },
        { id: "metrics", label: t("nav.metrics"), icon: Activity },
        { id: "moderation", label: t("nav.moderation"), icon: UsersRound },
      ];

  const chooseTab = (id) => {
    setActiveTab(id);
    setMobileOpen(false);
    if (id === "notifications") {
      setHasUnread(false);
      setUnreadCount(0);
    }
  };

  // 修改密码逻辑
  const handlePasswordChange = (e) => {
    e.preventDefault();
    setModalError("");

    if (!oldPassword || !newPassword || !confirmPassword) {
      setModalError("请填写所有字段");
      return;
    }

    if (newPassword !== confirmPassword) {
      setModalError("两次输入的新密码不一致");
      return;
    }

    if (newPassword.length < 3) {
      setModalError("新密码长度不能少于 3 位");
      return;
    }

    // 从 localStorage 中查找并更新用户密码
    const savedUsers = JSON.parse(localStorage.getItem("loops_users") || "[]");
    const userIndex = savedUsers.findIndex(u => u.username === currentUser.username);

    if (userIndex === -1) {
      // 如果没有记录（异常情况），使用默认密码比对
      if (oldPassword !== "123") {
        setModalError("旧密码验证不通过");
        return;
      }
    } else {
      const dbUser = savedUsers[userIndex];
      if (dbUser.password !== oldPassword) {
        setModalError("旧密码输入错误");
        return;
      }
    }

    // 更新密码
    const updatedUser = { ...currentUser, password: newPassword };
    if (userIndex !== -1) {
      savedUsers[userIndex] = updatedUser;
    } else {
      savedUsers.push(updatedUser);
    }
    localStorage.setItem("loops_users", JSON.stringify(savedUsers));
    localStorage.setItem("loops_current_user", JSON.stringify(updatedUser));
    setCurrentUser(updatedUser);

    showToast("密码修改成功，新密码已生效", "success");
    // 关闭 Modal 并重设输入
    setShowPasswordModal(false);
    setOldPassword("");
    setNewPassword("");
    setConfirmPassword("");
  };

  const handleTimeSelect = (value) => {
    setTimeRange(value);
    setShowTimeDropdown(false);
    const label = RANGE_OPTIONS.find(o => o.value === value)?.label || "最近 24 小时";
    showToast(`已成功同步时间跨度至: ${label}`);
  };

  const selectedRangeLabel = RANGE_OPTIONS.find(o => o.value === timeRange)?.label || "最近 24 小时";

  const sidebar = (
    <div className="app-sidebar-inner">
      <button className="brand-lockup" onClick={() => chooseTab(isNormalUser ? "feed" : "metrics")} aria-label="LOOPS 指标看板">
        <span className="brand-mark"><InfinityIcon /></span>
        <span>
          <strong>LOOPS</strong>
          <small>AI SAFETY</small>
        </span>
      </button>

      <nav className="app-nav" aria-label="主导航">
        {navItems.map(({ id, label, icon: Icon }) => {
          const selected = activeTab === id;
          return (
            <SpotlightCard
              as="button"
              key={id}
              onClick={() => chooseTab(id)}
              className={`app-nav-item ${selected ? "app-nav-item-active" : ""}`}
              spotlightColor="rgba(124, 58, 237, 0.2)"
              aria-current={selected ? "page" : undefined}
            >
              <Icon />
              <span>{label}</span>
              {selected && <i />}
            </SpotlightCard>
          );
        })}
      </nav>

      <div className="sidebar-actions">
        <button onClick={toggleTheme}>
          {theme === "dark" ? <Sun /> : <Moon />}
          <span>{theme === "dark" ? t("nav.lightMode") : t("nav.darkMode")}</span>
        </button>
        <button onClick={() => i18n.changeLanguage(i18n.language === "zh" ? "en" : "zh")}>
          <Languages />
          <span>{i18n.language === "zh" ? "简体中文" : "English"}</span>
        </button>
        <div className="engine-status">
          <span />
          <strong>{t("nav.engineOnline")}</strong>
        </div>
      </div>
    </div>
  );

  return (
    <div className="app-shell">
      <aside className="app-sidebar">{sidebar}</aside>

      <AnimatePresence>
        {mobileOpen && (
          <>
            <motion.button
              className="mobile-sidebar-backdrop"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setMobileOpen(false)}
              aria-label="关闭导航"
            />
            <motion.aside
              className="mobile-sidebar"
              initial={{ x: "-100%" }}
              animate={{ x: 0 }}
              exit={{ x: "-100%" }}
              transition={{ duration: 0.22 }}
            >
              <button className="mobile-close" onClick={() => setMobileOpen(false)} aria-label="关闭导航"><X /></button>
              {sidebar}
            </motion.aside>
          </>
        )}
      </AnimatePresence>

      <div className="app-workspace">
        <header className="app-topbar relative">
          {/* 顶部右侧流体极光效果 */}
          <div className="absolute top-0 right-0 w-[55%] h-full pointer-events-none opacity-30 z-0 overflow-hidden select-none" style={{ maskImage: "linear-gradient(to left, rgba(0,0,0,0.85) 30%, rgba(0,0,0,0))", WebkitMaskImage: "linear-gradient(to left, rgba(0,0,0,0.85) 30%, rgba(0,0,0,0))" }}>
            <Aurora colorStops={["#7C3AED", "#2563EB", "#10B981"]} speed={0.35} />
          </div>

          <button className="mobile-menu z-10" onClick={() => setMobileOpen(true)} aria-label="打开导航"><Menu /></button>
          <div className="page-heading z-10">
            <span>{meta.eyebrow}</span>
            <h1>{meta.title}</h1>
            <p>{meta.subtitle}</p>
          </div>
          
          <div className="topbar-actions z-10">
            {/* 时间切换下拉框：仅管理员可用 */}
            {!isNormalUser && (
              <div className="relative">
                <button 
                  className="date-control" 
                  onClick={() => {
                    setShowTimeDropdown(!showTimeDropdown);
                    setShowUserDropdown(false);
                  }}
                >
                  <CalendarDays />
                  <span>{selectedRangeLabel}</span>
                </button>
                
                <AnimatePresence>
                  {showTimeDropdown && (
                    <motion.div 
                      initial={{ opacity: 0, y: 10, scale: 0.95 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, y: 5, scale: 0.95 }}
                      className="dropdown-menu"
                    >
                      {RANGE_OPTIONS.map(opt => (
                        <button
                          key={opt.value}
                          onClick={() => handleTimeSelect(opt.value)}
                          className={`dropdown-item ${timeRange === opt.value ? "is-active" : ""}`}
                        >
                          {opt.label}
                        </button>
                      ))}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            )}

            {/* 消息通知铃铛：仅管理员可用 */}
            {!isNormalUser && (
              <button 
                className="icon-control" 
                aria-label="通知" 
                onClick={() => {
                  setActiveTab("notifications");
                  setHasUnread(false);
                  setUnreadCount(0);
                  setShowTimeDropdown(false);
                  setShowUserDropdown(false);
                }}
              >
                <Bell />
                {hasUnread && unreadCount > 0 && (
                  <span className="unread-badge">
                    {unreadCount > 99 ? "99+" : unreadCount}
                  </span>
                )}
              </button>
            )}

            {/* 操作员头像下拉菜单：所有角色可用 */}
            <div className="relative">
              <button 
                className="operator-avatar" 
                aria-label="当前操作员" 
                onClick={() => {
                  setShowUserDropdown(!showUserDropdown);
                  setShowTimeDropdown(false);
                }}
              >
                {currentUser?.avatar || "L"}
              </button>

              <AnimatePresence>
                {showUserDropdown && (
                  <motion.div 
                    initial={{ opacity: 0, y: 10, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: 5, scale: 0.95 }}
                    className="dropdown-menu user-dropdown"
                  >
                    <div className="dropdown-user-info">
                      <strong>{currentUser?.name || "操作员 L"}</strong>
                      <small>{currentUser?.role === "admin" ? "安全管理员" : "发帖运营员"}</small>
                    </div>
                    <div className="dropdown-divider" />
                    <button
                      onClick={() => {
                        setShowUserDropdown(false);
                        setShowPasswordModal(true);
                      }}
                      className="dropdown-item"
                    >
                      修改密码
                    </button>
                    <button
                      onClick={() => {
                        setShowUserDropdown(false);
                        onLogout();
                      }}
                      className="dropdown-item text-red-500 hover:bg-rose-500/10"
                    >
                      退出登录
                    </button>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>
        </header>
        <main className="app-main">{children}</main>
      </div>

      {/* 修改密码 Modal 弹窗 */}
      <AnimatePresence>
        {showPasswordModal && (
          <div className="modal-backdrop">
            <motion.div 
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9, y: 15 }}
              className="modal-content"
            >
              <div className="modal-header">
                <h3>安全密码变更</h3>
                <button className="modal-close" onClick={() => setShowPasswordModal(false)}><X className="w-5 h-5" /></button>
              </div>

              <form onSubmit={handlePasswordChange} className="modal-form">
                <div className="modal-input-group">
                  <label>旧密码验证</label>
                  <input
                    type="password"
                    placeholder="请输入当前所用旧密码"
                    value={oldPassword}
                    onChange={(e) => setOldPassword(e.target.value)}
                  />
                </div>

                <div className="modal-input-group">
                  <label>新安全密码</label>
                  <input
                    type="password"
                    placeholder="请输入新设定的密码 (至少 3 位)"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                  />
                </div>

                <div className="modal-input-group">
                  <label>确认新密码</label>
                  <input
                    type="password"
                    placeholder="请再次确认输入以防笔误"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                  />
                </div>

                {modalError && (
                  <div className="modal-error-msg">
                    <AlertTriangle className="w-4 h-4 shrink-0" />
                    <span>{modalError}</span>
                  </div>
                )}

                <div className="modal-actions">
                  <button type="button" className="modal-cancel-btn" onClick={() => setShowPasswordModal(false)}>取消</button>
                  <button type="submit" className="modal-submit-btn">保存新密码</button>
                </div>
              </form>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      {toast.show && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast({ ...toast, show: false })}
        />
      )}
    </div>
  );
}
