import { useState, useRef, useEffect } from "react";
import CreatePost from "../components/CreatePost";
import PostCard from "../components/PostCard";
import Toast from "../components/Toast";
import postService from "../services/postService";
import { useTranslation } from "react-i18next";

export default function Feed({ posts, setPosts, isLoading, loadMore, loadingMore, hasMore }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [toast, setToast] = useState({ message: null, type: null });
  const sentinelRef = useRef(null);
  const { t } = useTranslation();

  // ── Infinite scroll with IntersectionObserver ────────────────────────
  useEffect(() => {
    if (!sentinelRef.current || !loadMore) return;

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore && !loadingMore) {
          loadMore();
        }
      },
      { rootMargin: "200px" }
    );

    observer.observe(sentinelRef.current);
    return () => observer.disconnect();
  }, [loadMore, hasMore, loadingMore]);

  const pollModerationRun = async (postId, runId) => {
    for (let attempt = 0; attempt < 60; attempt += 1) {
      await new Promise((resolve) => setTimeout(resolve, 1500));
      const run = await postService.getModerationRun(runId);

      if (run.status === "completed") {
        const refreshed = await postService.getPost(postId);
        setPosts((prev) =>
          prev.map((post) =>
            (post.id || post._id) === postId ? refreshed : post
          )
        );
        setToast({
          message:
            run.verdict === "allow"
              ? t("feed.postAllowed")
              : `${t("feed.postBlocked")}: ${run.decision?.reasons?.join(", ") || t("feed.communityViolation")}`,
          type: run.verdict === "allow" ? "success" : "error",
        });
        return;
      }

      if (run.status === "waiting_human" || run.status === "failed") {
        setPosts((prev) =>
          prev.map((post) =>
            (post.id || post._id) === postId
              ? { ...post, moderation_status: run.status }
              : post
          )
        );
        setToast({
          message:
            run.status === "waiting_human"
              ? "自动裁决不确定，已进入人工审核队列"
              : "Agent 审核失败，请稍后重试",
          type: run.status === "waiting_human" ? "loading" : "error",
        });
        return;
      }
    }
  };

  // ── Inline post creation (feed page also has a CreatePost) ──────────
  const handleSubmit = async ({ text, image }) => {
    setIsSubmitting(true);
    setToast({ message: t("feed.analyzing"), type: "loading" });
    
    try {
      const result = await postService.createPost({ text, image });
      if (!result.id) result.id = Date.now().toString();
      
      if (result.moderation_run_id) {
        setToast({ message: "Agent 已接收任务，正在分层审核…", type: "loading" });
        void pollModerationRun(result.id, result.moderation_run_id).catch(() => {
          setToast({ message: "无法获取 Agent 审核状态", type: "error" });
        });
      } else if (result.allowed === false) {
        setToast({ 
          message: `${t("feed.postBlocked")}: ${result.reasons?.map(r => t(`category.${r}`, r)).join(", ") || t("feed.communityViolation")}`, 
          type: "error" 
        });
      } else {
        setToast({ 
          message: t("feed.postAllowed"), 
          type: "success" 
        });
      }
      
      // Always add the post to the feed dynamically
      setPosts((prev) => [result, ...prev]);
    } catch (error) {
      console.error("Error submitting post:", error);
      setToast({ message: t("feed.failedProcess"), type: "error" });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="feed-workspace max-w-3xl mx-auto w-full pb-20">
      <CreatePost onSubmit={handleSubmit} isSubmitting={isSubmitting} />

      <div className="h-px bg-gray-200 dark:bg-gray-800 my-4 w-full" />

      <div className="space-y-1">
        {isLoading ? (
          <div className="flex justify-center p-8">
            <div className="w-8 h-8 rounded-full border-4 border-indigo-200 border-t-indigo-600 animate-spin" />
          </div>
        ) : posts.length === 0 ? (
          <div className="text-center py-12 text-gray-400 dark:text-gray-500">
            <p className="text-lg font-medium">{t("feed.noPosts")}</p>
            <p className="text-sm">{t("feed.beFirst")}</p>
          </div>
        ) : (
          posts.map((post, idx) => (
            <PostCard key={post.id || post._id || idx} post={post} />
          ))
        )}

        {/* Infinite scroll sentinel */}
        {!isLoading && hasMore && (
          <div ref={sentinelRef} className="flex justify-center p-4">
            {loadingMore && (
              <div className="w-6 h-6 rounded-full border-3 border-indigo-200 border-t-indigo-600 animate-spin" />
            )}
          </div>
        )}

        {/* End of feed */}
        {!isLoading && !hasMore && posts.length > 0 && (
          <div className="text-center py-6 text-gray-400 dark:text-gray-500 text-sm">
            {t("feed.end")}
          </div>
        )}
      </div>

      {toast.message && (
        <Toast 
          message={toast.message} 
          type={toast.type} 
          onClose={() => setToast({ message: null, type: null })} 
        />
      )}
    </div>
  );
}
/**This file is the main feed page of the frontend application. It displays a list of posts and includes a form for creating new posts. The page also implements infinite scrolling to load more posts as the user scrolls down. Additionally, it provides real-time feedback on post submissions using a toast notification system.**/
