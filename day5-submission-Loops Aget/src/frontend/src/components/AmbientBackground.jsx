import { Aurora, Particles } from "./reactbits/ReactBits";
import { useMotionPreference } from "../context/MotionPreferenceContext";
import { useTheme } from "../context/ThemeContext";

export default function AmbientBackground() {
  const { reducedMotion, compactEffects } = useMotionPreference();
  const { theme } = useTheme();
  const isDark = theme === "dark";

  return (
    <div className="ambient-background" aria-hidden="true">
      {!compactEffects && !reducedMotion && (
        <div className={`ambient-aurora ${isDark ? "" : "ambient-aurora-light"}`}>
          <Aurora
            colorStops={["#7C3AED", "#2563EB", "#22D3EE"]}
            amplitude={0.72}
            blend={0.68}
            speed={0.3}
          />
        </div>
      )}
      <div className={`ambient-particles ${isDark ? "" : "ambient-particles-light"}`}>
        {!reducedMotion ? (
          <Particles
            particleCount={compactEffects ? 34 : 72}
            particleSpread={compactEffects ? 8 : 13}
            speed={0.075}
            particleColors={["#7C3AED", "#22D3EE", "#E2E8F0"]}
            moveParticlesOnHover={!compactEffects}
            particleHoverFactor={0.13}
            particleBaseSize={compactEffects ? 48 : 64}
          />
        ) : (
          <div className="ambient-static-dots" />
        )}
      </div>
      <div className="ambient-readability-mask" />
    </div>
  );
}
