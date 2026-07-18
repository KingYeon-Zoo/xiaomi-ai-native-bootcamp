import { useEffect, useRef, useState } from "react";
import { Camera, Color, Geometry, Mesh, Program, Renderer, Triangle } from "ogl";
import "./react-bits.css";

// Project-local adaptations of the React Bits JS/CSS registry components.
// Source: https://reactbits.dev
const DEFAULT_AURORA_COLORS = ["#7C3AED", "#2563EB", "#22D3EE"];
const DEFAULT_PARTICLE_COLORS = ["#7C3AED", "#22D3EE", "#F8FAFC"];

const AURORA_VERTEX = `#version 300 es
in vec2 position;
void main() { gl_Position = vec4(position, 0.0, 1.0); }`;

const AURORA_FRAGMENT = `#version 300 es
precision highp float;
uniform float uTime;
uniform float uAmplitude;
uniform vec3 uColorStops[3];
uniform vec2 uResolution;
uniform float uBlend;
out vec4 fragColor;

vec3 permute(vec3 x) { return mod(((x * 34.0) + 1.0) * x, 289.0); }
float snoise(vec2 v) {
  const vec4 C = vec4(.2113248654, .3660254038, -.5773502692, .0243902439);
  vec2 i = floor(v + dot(v, C.yy));
  vec2 x0 = v - i + dot(i, C.xx);
  vec2 i1 = x0.x > x0.y ? vec2(1., 0.) : vec2(0., 1.);
  vec4 x12 = x0.xyxy + C.xxzz;
  x12.xy -= i1;
  i = mod(i, 289.);
  vec3 p = permute(permute(i.y + vec3(0., i1.y, 1.)) + i.x + vec3(0., i1.x, 1.));
  vec3 m = max(.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy), dot(x12.zw,x12.zw)), 0.);
  m = m*m; m = m*m;
  vec3 x = 2. * fract(p * C.www) - 1.;
  vec3 h = abs(x) - .5;
  vec3 ox = floor(x + .5);
  vec3 a0 = x - ox;
  m *= 1.792842914 - .853734721 * (a0*a0 + h*h);
  vec3 g;
  g.x = a0.x*x0.x + h.x*x0.y;
  g.yz = a0.yz*x12.xz + h.yz*x12.yw;
  return 130. * dot(m, g);
}

void main() {
  vec2 uv = gl_FragCoord.xy / uResolution;
  vec3 ramp = uv.x < .5
    ? mix(uColorStops[0], uColorStops[1], uv.x * 2.)
    : mix(uColorStops[1], uColorStops[2], (uv.x - .5) * 2.);
  float wave = snoise(vec2(uv.x * 2. + uTime * .1, uTime * .25)) * .5 * uAmplitude;
  float height = uv.y * 2. - exp(wave) + .2;
  float intensity = .6 * height;
  float alpha = smoothstep(.2 - uBlend * .5, .2 + uBlend * .5, intensity);
  fragColor = vec4(intensity * ramp * alpha, alpha);
}`;

export function Aurora({
  colorStops = DEFAULT_AURORA_COLORS,
  amplitude = 0.8,
  blend = 0.65,
  speed = 0.35,
  className = "",
}) {
  const containerRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return undefined;

    const renderer = new Renderer({ alpha: true, premultipliedAlpha: true });
    const gl = renderer.gl;
    gl.clearColor(0, 0, 0, 0);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);

    const geometry = new Triangle(gl);
    if (geometry.attributes.uv) delete geometry.attributes.uv;
    const colors = colorStops.map((hex) => {
      const color = new Color(hex);
      return [color.r, color.g, color.b];
    });
    const program = new Program(gl, {
      vertex: AURORA_VERTEX,
      fragment: AURORA_FRAGMENT,
      uniforms: {
        uTime: { value: 0 },
        uAmplitude: { value: amplitude },
        uColorStops: { value: colors },
        uResolution: { value: [1, 1] },
        uBlend: { value: blend },
      },
    });
    const mesh = new Mesh(gl, { geometry, program });
    container.appendChild(gl.canvas);

    const resize = () => {
      const width = container.clientWidth;
      const height = container.clientHeight;
      renderer.setSize(width, height);
      program.uniforms.uResolution.value = [width, height];
    };
    let frame;
    const render = (time) => {
      program.uniforms.uTime.value = time * 0.0001 * speed;
      renderer.render({ scene: mesh });
      frame = requestAnimationFrame(render);
    };
    resize();
    window.addEventListener("resize", resize);
    frame = requestAnimationFrame(render);

    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener("resize", resize);
      if (gl.canvas.parentNode === container) container.removeChild(gl.canvas);
      gl.getExtension("WEBGL_lose_context")?.loseContext();
    };
  }, [amplitude, blend, colorStops, speed]);

  return <div ref={containerRef} className={`rb-aurora ${className}`} aria-hidden="true" />;
}

const PARTICLE_VERTEX = `
attribute vec3 position;
attribute vec4 random;
attribute vec3 color;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float uTime;
uniform float uSpread;
uniform float uBaseSize;
varying vec4 vRandom;
varying vec3 vColor;
void main() {
  vRandom = random; vColor = color;
  vec3 pos = position * uSpread;
  pos.z *= 8.0;
  vec4 mPos = modelMatrix * vec4(pos, 1.0);
  mPos.x += sin(uTime * random.z + 6.28 * random.w) * mix(.1, 1.2, random.x);
  mPos.y += sin(uTime * random.y + 6.28 * random.x) * mix(.1, 1.0, random.w);
  vec4 mvPos = viewMatrix * mPos;
  gl_PointSize = uBaseSize * mix(.7, 1.25, random.x) / length(mvPos.xyz);
  gl_Position = projectionMatrix * mvPos;
}`;

const PARTICLE_FRAGMENT = `
precision highp float;
varying vec3 vColor;
void main() {
  float d = length(gl_PointCoord.xy - vec2(.5));
  float alpha = smoothstep(.5, .18, d) * .82;
  gl_FragColor = vec4(vColor, alpha);
}`;

const hexToRgb = (hex) => {
  const value = parseInt(hex.replace("#", ""), 16);
  return [((value >> 16) & 255) / 255, ((value >> 8) & 255) / 255, (value & 255) / 255];
};

export function Particles({
  particleCount = 72,
  particleSpread = 12,
  speed = 0.08,
  particleColors = DEFAULT_PARTICLE_COLORS,
  moveParticlesOnHover = true,
  particleHoverFactor = 0.12,
  particleBaseSize = 68,
  className = "",
}) {
  const containerRef = useRef(null);
  const mouseRef = useRef({ x: 0, y: 0 });

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return undefined;
    const renderer = new Renderer({ dpr: Math.min(window.devicePixelRatio, 1.5), depth: false, alpha: true });
    const gl = renderer.gl;
    gl.clearColor(0, 0, 0, 0);
    container.appendChild(gl.canvas);
    const camera = new Camera(gl, { fov: 15 });
    camera.position.set(0, 0, 20);

    const positions = new Float32Array(particleCount * 3);
    const randoms = new Float32Array(particleCount * 4);
    const colors = new Float32Array(particleCount * 3);
    for (let index = 0; index < particleCount; index += 1) {
      const radius = Math.cbrt(Math.random());
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      positions.set([
        radius * Math.sin(phi) * Math.cos(theta),
        radius * Math.sin(phi) * Math.sin(theta),
        radius * Math.cos(phi),
      ], index * 3);
      randoms.set([Math.random(), Math.random(), Math.random(), Math.random()], index * 4);
      colors.set(hexToRgb(particleColors[index % particleColors.length]), index * 3);
    }
    const geometry = new Geometry(gl, {
      position: { size: 3, data: positions },
      random: { size: 4, data: randoms },
      color: { size: 3, data: colors },
    });
    const program = new Program(gl, {
      vertex: PARTICLE_VERTEX,
      fragment: PARTICLE_FRAGMENT,
      uniforms: {
        uTime: { value: 0 },
        uSpread: { value: particleSpread },
        uBaseSize: { value: particleBaseSize },
      },
      transparent: true,
      depthTest: false,
    });
    const particles = new Mesh(gl, { mode: gl.POINTS, geometry, program });
    const resize = () => {
      renderer.setSize(container.clientWidth, container.clientHeight);
      camera.perspective({ aspect: gl.canvas.width / gl.canvas.height });
    };
    const pointer = (event) => {
      mouseRef.current = {
        x: (event.clientX / window.innerWidth) * 2 - 1,
        y: -((event.clientY / window.innerHeight) * 2 - 1),
      };
    };
    let frame;
    const render = (time) => {
      program.uniforms.uTime.value = time * 0.001 * speed;
      if (moveParticlesOnHover) {
        particles.position.x += (-mouseRef.current.x * particleHoverFactor - particles.position.x) * 0.035;
        particles.position.y += (-mouseRef.current.y * particleHoverFactor - particles.position.y) * 0.035;
      }
      particles.rotation.z += 0.0002 * speed;
      renderer.render({ scene: particles, camera });
      frame = requestAnimationFrame(render);
    };
    resize();
    window.addEventListener("resize", resize);
    window.addEventListener("pointermove", pointer, { passive: true });
    frame = requestAnimationFrame(render);
    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener("resize", resize);
      window.removeEventListener("pointermove", pointer);
      if (gl.canvas.parentNode === container) container.removeChild(gl.canvas);
      gl.getExtension("WEBGL_lose_context")?.loseContext();
    };
  }, [moveParticlesOnHover, particleBaseSize, particleColors, particleCount, particleHoverFactor, particleSpread, speed]);

  return <div ref={containerRef} className={`rb-particles ${className}`} aria-hidden="true" />;
}

export function SpotlightCard({
  children,
  className = "",
  spotlightColor = "rgba(124, 58, 237, 0.14)",
  as: Element = "div",
  ...props
}) {
  const ref = useRef(null);
  const handlePointerMove = (event) => {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    ref.current.style.setProperty("--mouse-x", `${event.clientX - rect.left}px`);
    ref.current.style.setProperty("--mouse-y", `${event.clientY - rect.top}px`);
    ref.current.style.setProperty("--spotlight-color", spotlightColor);
  };
  return (
    <Element ref={ref} onPointerMove={handlePointerMove} className={`rb-spotlight ${className}`} {...props}>
      {children}
    </Element>
  );
}

export function BorderGlow({ children, className = "", color = "#7C3AED", danger = false }) {
  return (
    <div
      className={`rb-border-glow ${danger ? "rb-border-glow-danger" : ""} ${className}`}
      style={{ "--glow-accent": color }}
    >
      <div className="rb-border-glow-inner">{children}</div>
    </div>
  );
}

export function Counter({ value = 0, duration = 750, formatter }) {
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    const numeric = Number(value) || 0;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      const reducedFrame = requestAnimationFrame(() => setDisplay(numeric));
      return () => cancelAnimationFrame(reducedFrame);
    }
    const startAt = performance.now();
    let frame;
    const tick = (now) => {
      const progress = Math.min((now - startAt) / duration, 1);
      const eased = 1 - (1 - progress) ** 3;
      setDisplay(Math.round(numeric * eased));
      if (progress < 1) frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [duration, value]);

  return formatter ? formatter(display) : display.toLocaleString();
}
