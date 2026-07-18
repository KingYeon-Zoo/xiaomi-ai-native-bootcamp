import { useState, useEffect } from "react";
import AnalyticsPage from "./pages/AnalyticsPage";
import FeedPage from "./pages/FeedPage";
import MetricsDashboardPage from "./pages/MetricsDashboardPage";
import HumanModerationPage from "./pages/HumanModerationPage";
import NotificationsPage from "./pages/NotificationsPage";
import usePosts from "./hooks/usePosts";
import AppShell from "./components/AppShell";
import LoginPage from "./components/LoginPage";
import AmbientBackground from "./components/AmbientBackground";

import { motion, AnimatePresence } from "framer-motion";

function App() {
  const [currentUser, setCurrentUser] = useState(() => {
    const saved = localStorage.getItem("loops_current_user");
    return saved ? JSON.parse(saved) : null;
  });
  const [activeTab, setActiveTab] = useState("metrics");
  const [timeRange, setTimeRange] = useState(24);

  // 权限检查：普通用户如果当前Tab不是发帖广场，强制跳转到发帖广场
  useEffect(() => {
    if (currentUser && currentUser.role === "user" && activeTab !== "feed") {
      const timer = setTimeout(() => {
        setActiveTab("feed");
      }, 0);
      return () => clearTimeout(timer);
    }
  }, [currentUser, activeTab]);

  // Centralised post state via custom hook
  const {
    posts,
    setPosts,
    loading: isLoading,
    loadMore,
    loadingMore,
    hasMore,
  } = usePosts(activeTab === "feed");

  const handleLogin = (user) => {
    setCurrentUser(user);
    localStorage.setItem("loops_current_user", JSON.stringify(user));
    if (user.role === "user") {
      setActiveTab("feed");
    } else {
      setActiveTab("metrics");
    }
  };

  const handleLogout = () => {
    setCurrentUser(null);
    localStorage.removeItem("loops_current_user");
  };

  // Page Transition variants
  const pageVariants = {
    initial: { opacity: 0, y: 8 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: -8 }
  };
 
  const pageTransition = {
    duration: 0.22,
    ease: "easeOut"
  };

  if (!currentUser) {
    return (
      <>
        <AmbientBackground />
        <LoginPage onLogin={handleLogin} />
      </>
    );
  }
 
  return (
    <>
      <AmbientBackground />
      <AppShell 
        activeTab={activeTab} 
        setActiveTab={setActiveTab}
        currentUser={currentUser}
        setCurrentUser={setCurrentUser}
        onLogout={handleLogout}
        timeRange={timeRange}
        setTimeRange={setTimeRange}
      >
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            variants={pageVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            transition={pageTransition}
            className="w-full min-h-full"
          >
            {activeTab === "analytics" && <AnalyticsPage timeRange={timeRange} />}
            {activeTab === "metrics" && (
              <MetricsDashboardPage 
                setActiveTab={setActiveTab} 
                timeRange={timeRange} 
                setTimeRange={setTimeRange} 
              />
            )}
            {activeTab === "moderation" && <HumanModerationPage />}
            {activeTab === "notifications" && <NotificationsPage />}
            
            {activeTab === "feed" && (
              <FeedPage
                posts={posts}
                setPosts={setPosts}
                isLoading={isLoading}
                loadMore={loadMore}
                loadingMore={loadingMore}
                hasMore={hasMore}
              />
            )}
          </motion.div>
        </AnimatePresence>
      </AppShell>
    </>
  );
}

export default App;
