import { useState } from "react";
import { motion } from "framer-motion";
import { Lock, User, LogIn, ShieldAlert, Fingerprint } from "lucide-react";
import { Aurora, SpotlightCard } from "./reactbits/ReactBits";

const DEMO_USERS = [
  { username: "admin", role: "admin", name: "系统管理员", avatar: "A" },
  { username: "user", role: "user", name: "发帖运营专员", avatar: "U" }
];

export default function LoginPage({ onLogin, error: externalError }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    if (!username || !password) {
      setError("请输入用户名 and 密码");
      return;
    }

    // 本地匹配演示账号 (密码默认为 123)
    const foundUser = DEMO_USERS.find(
      (u) => u.username.toLowerCase() === username.trim().toLowerCase()
    );

    if (foundUser && password === "123") {
      // 成功登录，从缓存或内存读取/初始化其密码信息
      const userWithCreds = {
        ...foundUser,
        password: password
      };
      
      // 保存至本地存储以方便改密等模拟操作
      const savedUsers = JSON.parse(localStorage.getItem("loops_users") || "[]");
      const localUser = savedUsers.find(u => u.username === foundUser.username);
      
      if (localUser) {
        onLogin(localUser);
      } else {
        // 首次登录，保存其默认初始状态
        savedUsers.push(userWithCreds);
        localStorage.setItem("loops_users", JSON.stringify(savedUsers));
        onLogin(userWithCreds);
      }
    } else {
      // 检查是否修改过密码并保存在本地
      const savedUsers = JSON.parse(localStorage.getItem("loops_users") || "[]");
      const localUser = savedUsers.find(
        (u) => u.username.toLowerCase() === username.trim().toLowerCase() && u.password === password
      );

      if (localUser) {
        onLogin(localUser);
      } else {
        setError("用户名错误，或密码（默认123）输入不正确");
      }
    }
  };

  const handleQuickLogin = (role) => {
    const defaultUser = DEMO_USERS.find((u) => u.role === role);
    const savedUsers = JSON.parse(localStorage.getItem("loops_users") || "[]");
    const localUser = savedUsers.find((u) => u.role === role);

    if (localUser) {
      onLogin(localUser);
    } else {
      const userWithCreds = { ...defaultUser, password: "123" };
      savedUsers.push(userWithCreds);
      localStorage.setItem("loops_users", JSON.stringify(savedUsers));
      onLogin(userWithCreds);
    }
  };

  return (
    <div className="login-container relative overflow-hidden">
      {/* 炫酷流体极光背景 */}
      <div className="absolute inset-0 z-0 opacity-20 pointer-events-none">
        <Aurora colorStops={["#4F46E5", "#06B6D4", "#7C3AED"]} speed={0.45} />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="z-10 w-full max-w-[420px] px-4"
      >
        <SpotlightCard className="login-card w-full" spotlightColor="rgba(99, 102, 241, 0.15)">
          <div className="login-header">
            <div className="login-logo">
              <Fingerprint className="w-8 h-8 text-indigo-500 animate-pulse" />
            </div>
            <h1>LOOPS AI SAFETY</h1>
            <p>内容安全与即时审核系统后台</p>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            <div className="input-group">
              <label>
                <User className="w-4 h-4 text-slate-400" />
                <input
                  type="text"
                  placeholder="用户名 (admin / user)"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </label>
            </div>

            <div className="input-group">
              <label>
                <Lock className="w-4 h-4 text-slate-400" />
                <input
                  type="password"
                  placeholder="密码 (默认 123)"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </label>
            </div>

            {(error || externalError) && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="login-error-msg"
              >
                <ShieldAlert className="w-4 h-4 shrink-0" />
                <span>{error || externalError}</span>
              </motion.div>
            )}

            <button type="submit" className="login-submit-btn cursor-pointer">
              <span>登 录</span>
              <LogIn className="w-4 h-4" />
            </button>
          </form>

          <div className="login-divider">
            <span>快捷登录通道</span>
          </div>

          <div className="quick-login-actions flex flex-col gap-3">
            <SpotlightCard
              as="button"
              onClick={() => handleQuickLogin("admin")}
              className="quick-btn admin-quick-btn text-left p-3 rounded-xl border border-white/5 hover:border-indigo-500/30 transition-all duration-300 w-full"
              spotlightColor="rgba(99, 102, 241, 0.12)"
            >
              <div className="flex flex-col pointer-events-none">
                <span className="font-semibold text-xs text-white">以管理员登录</span>
                <span className="text-[10px] text-slate-400 mt-1">拥有所有监控、配置与复核权限</span>
              </div>
            </SpotlightCard>

            <SpotlightCard
              as="button"
              onClick={() => handleQuickLogin("user")}
              className="quick-btn user-quick-btn text-left p-3 rounded-xl border border-white/5 hover:border-indigo-500/30 transition-all duration-300 w-full"
              spotlightColor="rgba(16, 185, 129, 0.12)"
            >
              <div className="flex flex-col pointer-events-none">
                <span className="font-semibold text-xs text-white">以普通用户登录</span>
                <span className="text-[10px] text-slate-400 mt-1">仅有发帖广场，不具备管理面板</span>
              </div>
            </SpotlightCard>
          </div>

          <div className="login-footer mt-4">
            <p>默认登录密码均为 <strong>123</strong>。登录后可在右上角修改密码。</p>
          </div>
        </SpotlightCard>
      </motion.div>
    </div>
  );
}
