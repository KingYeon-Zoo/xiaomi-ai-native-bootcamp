#!/usr/bin/env python3
"""Geometric preview renderer for QA without LibreOffice.
Draws each shape's bounding box + text at scale so we can catch overflow,
off-slide elements, and overlaps. Not pixel-accurate, but reliable for layout QA."""
import sys, math
from pptx import Presentation
from pptx.util import Emu
from PIL import Image, ImageDraw, ImageFont

EMU = 914400
SCALE = 96  # px per inch
try:
    FONT_PATHS = ["/System/Library/Fonts/STHeiti Medium.ttc",
                  "/System/Library/Fonts/PingFang.ttc",
                  "/Library/Fonts/Arial Unicode.ttf"]
    FP = next(p for p in FONT_PATHS if __import__("os").path.exists(p))
except StopIteration:
    FP = None

def font(sz):
    try: return ImageFont.truetype(FP, max(8, int(sz))) if FP else ImageFont.load_default()
    except Exception: return ImageFont.load_default()

def hexc(rgb):
    try: return "#%02x%02x%02x" % (rgb[0], rgb[1], rgb[2])
    except Exception: return None

def render(pptx_path, out_prefix):
    prs = Presentation(pptx_path)
    w_in = prs.slide_width / EMU
    h_in = prs.slide_height / EMU
    W, Hh = int(w_in * SCALE), int(h_in * SCALE)
    files = []
    for idx, slide in enumerate(prs.slides, 1):
        img = Image.new("RGB", (W, Hh), (10, 14, 34))
        d = ImageDraw.Draw(img)
        for sh in slide.shapes:
            try:
                x = int(sh.left / EMU * SCALE); y = int(sh.top / EMU * SCALE)
                sw = int(sh.width / EMU * SCALE); sh_h = int(sh.height / EMU * SCALE)
            except Exception:
                continue
            off = (x < -2 or y < -2 or x + sw > W + 2 or y + sh_h > Hh + 2)
            if sh.shape_type == 13:  # picture
                d.rectangle([x, y, x+sw, y+sh_h], outline=(80, 100, 160), width=1)
                d.line([x, y, x+sw, y+sh_h], fill=(60, 76, 130), width=1)
                d.line([x+sw, y, x, y+sh_h], fill=(60, 76, 130), width=1)
            else:
                oc = (255, 60, 60) if off else (70, 86, 140)
                try: d.rectangle([x, y, x+sw, y+sh_h], outline=oc, width=1)
                except Exception: pass
            if sh.has_text_frame and sh.text_frame.text.strip():
                ty = y + 3
                for para in sh.text_frame.paragraphs:
                    txt = "".join(r.text for r in para.runs) or para.text
                    if not txt.strip():
                        ty += 10; continue
                    sz = 14
                    for r in para.runs:
                        if r.font.size: sz = r.font.size / EMU * SCALE * 1.34; break
                    col = (226, 232, 240)
                    for r in para.runs:
                        try:
                            if r.font.color and r.font.color.rgb:
                                c = r.font.color.rgb; col = (c[0], c[1], c[2])
                        except Exception: pass
                        break
                    f = font(sz)
                    lh = max(sz * 1.35, 12)
                    # naive CJK-aware wrapping to box width
                    avail = max(sw - 8, 20)
                    line, lines = "", []
                    for ch2 in txt:
                        if d.textlength(line + ch2, font=f) > avail and line:
                            lines.append(line); line = ch2
                        else:
                            line += ch2
                    if line: lines.append(line)
                    bullet = (para.text != txt) or False
                    for ln in lines:
                        d.text((x + 4, ty), ln, fill=col, font=f)
                        ty += lh
                    if ty > y + sh_h + 2 and sh_h > 20:
                        d.line([x, y+sh_h, x+sw, y+sh_h], fill=(255, 140, 0), width=2)
        outp = f"{out_prefix}-{idx}.png"
        img.save(outp); files.append(outp)
    print("\n".join(files))

if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "qa")
