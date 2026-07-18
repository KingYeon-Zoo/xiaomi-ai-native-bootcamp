// Render react-icons to PNG at high res, tinted to a given color, for embedding in the deck.
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fs = require("fs");
const path = require("path");

const Fi = require("react-icons/fi");
const Tb = require("react-icons/tb");

const OUT = path.join(__dirname, "icons");
fs.mkdirSync(OUT, { recursive: true });

// name -> [pack, iconName, hexColor]
const ICONS = {
  // routing / architecture
  "route":        [Fi, "FiGitBranch",    "22d3ee"],
  "shield":       [Fi, "FiShield",       "8b5cf6"],
  "shieldcheck":  [Tb, "TbShieldCheck",  "22d3ee"],
  "gavel":        [Tb, "TbGavel",        "f6b73c"],
  "cpu":          [Fi, "FiCpu",          "22d3ee"],
  "layers":       [Fi, "FiLayers",       "8b5cf6"],
  "eye":          [Fi, "FiEye",          "22d3ee"],
  "text":         [Fi, "FiFileText",     "8b5cf6"],
  "users":        [Fi, "FiUsers",        "f6b73c"],
  "alert":        [Fi, "FiAlertTriangle","fb5f6f"],
  "lock":         [Fi, "FiLock",         "22d3ee"],
  "search":       [Fi, "FiSearch",       "8b5cf6"],
  "zap":          [Fi, "FiZap",          "f6b73c"],
  "database":     [Fi, "FiDatabase",     "22d3ee"],
  "check":        [Fi, "FiCheckCircle",  "34d399"],
  "x":            [Fi, "FiXCircle",      "fb5f6f"],
  "edit":         [Fi, "FiEdit3",        "f6b73c"],
  "code":         [Fi, "FiCode",         "22d3ee"],
  "git":          [Fi, "FiGitCommit",    "8b5cf6"],
  "refresh":      [Fi, "FiRefreshCw",    "22d3ee"],
  "flow":         [Tb, "TbTopologyStar3","8b5cf6"],
  "robot":        [Tb, "TbRobot",        "22d3ee"],
  "brain":        [Tb, "TbBrain",        "8b5cf6"],
  "test":         [Tb, "TbTestPipe",     "34d399"],
  "target":       [Fi, "FiTarget",       "fb5f6f"],
  "tool":         [Fi, "FiTool",         "22d3ee"],
  "compass":      [Fi, "FiCompass",      "8b5cf6"],
  "grid":         [Fi, "FiGrid",         "22d3ee"],
  "trend":        [Fi, "FiTrendingUp",   "34d399"],
  "server":       [Fi, "FiServer",       "8b5cf6"],
  "image":        [Fi, "FiImage",        "22d3ee"],
  "scale":        [Tb, "TbScale",        "f6b73c"],
  "person":       [Fi, "FiUser",         "22d3ee"],
  "book":         [Fi, "FiBookOpen",     "8b5cf6"],
  "arrow":        [Fi, "FiArrowRight",   "cbd5e1"],
  "clock":        [Fi, "FiClock",        "94a3b8"],
  "package":      [Fi, "FiPackage",      "22d3ee"],
  "filter":       [Fi, "FiFilter",       "8b5cf6"],
  "globe":        [Fi, "FiGlobe",        "22d3ee"],
};

async function render(name, [pack, iconName, color]) {
  const IconComp = pack[iconName];
  if (!IconComp) { console.error("MISSING", iconName); return; }
  const el = React.createElement(IconComp, { color: "#" + color, size: 256 });
  let svg = ReactDOMServer.renderToStaticMarkup(el);
  if (!svg.includes("xmlns")) svg = svg.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"');
  const png = await sharp(Buffer.from(svg)).resize(256, 256, { fit: "contain", background: { r:0,g:0,b:0,alpha:0 } }).png().toBuffer();
  fs.writeFileSync(path.join(OUT, name + ".png"), png);
}

(async () => {
  for (const [name, spec] of Object.entries(ICONS)) await render(name, spec);
  console.log("rendered", Object.keys(ICONS).length, "icons");
})();
