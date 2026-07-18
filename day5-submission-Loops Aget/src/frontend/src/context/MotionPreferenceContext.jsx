import { createContext, useContext, useEffect, useMemo, useState } from "react";

const MotionPreferenceContext = createContext({
  reducedMotion: false,
  compactEffects: false,
});

export function MotionPreferenceProvider({ children }) {
  const [reducedMotion, setReducedMotion] = useState(false);
  const [compactEffects, setCompactEffects] = useState(false);

  useEffect(() => {
    const motionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    const compactQuery = window.matchMedia("(max-width: 767px)");
    const sync = () => {
      setReducedMotion(motionQuery.matches);
      setCompactEffects(compactQuery.matches);
    };
    sync();
    motionQuery.addEventListener("change", sync);
    compactQuery.addEventListener("change", sync);
    return () => {
      motionQuery.removeEventListener("change", sync);
      compactQuery.removeEventListener("change", sync);
    };
  }, []);

  const value = useMemo(() => ({ reducedMotion, compactEffects }), [reducedMotion, compactEffects]);
  return <MotionPreferenceContext.Provider value={value}>{children}</MotionPreferenceContext.Provider>;
}

export const useMotionPreference = () => useContext(MotionPreferenceContext);
