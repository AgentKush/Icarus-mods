#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BLUEPRINT - drawing-office identity for AgentKush's ICARUS mods.

Every mod is one sheet of a single engineering drawing set: cyanotype paper
with a fine grid, white technical linework, a category "part" drawn with
centre lines, hatching and real dimensions, an inked category stamp, and a
title block that carries the live data (title, description, drawing number,
revision, entries, tables, author).

    render(mod, icon_path, banner_path)

    mod = {folder, name, version, entries, tables, category, tagline, author}

Normally driven by mod_images.py, which reads each mod's live data and writes
icons/<Folder>.png (256x256 Mod Manager icon) and <Folder>/Banner.png (768x256).
Run directly - python mod_image_render.py <mods.json> <out_dir> - it renders a
list of mods into out_dir with 64/128 px icon previews and a contact sheet.

Dependencies: Python 3, Pillow, numpy. Fonts: C:\\Windows\\Fonts only.
All randomness is seeded from the mod folder name, so output is repeatable.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import re
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLES_JSON = os.path.normpath(os.path.join(HERE, "..", "samples.json"))
FONT_DIR = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
BAHNSCHRIFT = os.path.join(FONT_DIR, "bahnschrift.ttf")

# --------------------------------------------------------------------------
# palette
# --------------------------------------------------------------------------
PAPER = np.array([24, 70, 136], np.float32) / 255.0     # cyanotype / Prussian blue
INK = np.array([238, 245, 255], np.float32) / 255.0     # the white of the print
TAB_INK = (13, 34, 70)                                   # dark ink printed on colour tabs

# category -> code, stamp label, stamp ink colour, emblem ("part" drawn on the sheet)
CATEGORIES = {
    "building & construction": ("BLD", "BUILDING & CONSTRUCTION", (255, 158, 58), "house"),
    "combat & defense":        ("CBT", "COMBAT & DEFENSE", (255, 98, 92), "shield"),
    "economy & resources":     ("ECO", "ECONOMY & RESOURCES", (248, 210, 78), "gem"),
    "food & consumables":      ("FOD", "FOOD & CONSUMABLES", (104, 224, 138), "bowl"),
    "mod packs":               ("PAK", "MOD PACKS", (192, 166, 255), "crate"),
    "processing speed":        ("SPD", "PROCESSING SPEED", (76, 226, 230), "gear"),
    "quality of life":         ("QOL", "QUALITY OF LIFE", (255, 144, 198), "sliders"),
    "survival & difficulty":   ("SRV", "SURVIVAL & DIFFICULTY", (204, 238, 76), "hazard"),
    "workshop & items":        ("WSH", "WORKSHOP & ITEMS", (236, 132, 255), "spanner"),
    # added with the live set: an earthy olive - CIEDE2000 21.5 from its nearest
    # neighbour (the palette's own closest pair is 12.4) and 3.3:1 on the paper,
    # level with the Combat red, so the stamp reads like the others
    "taming & breeding":       ("TMB", "TAMING & BREEDING", (152, 160, 92), "paw"),
}
FALLBACK = ("GEN", None, (224, 232, 242), "flange")


def category_info(cat):
    key = re.sub(r"\s+", " ", str(cat or "").lower().replace(" and ", " & ")).strip()
    key = key.replace("defence", "defense")
    if key in CATEGORIES:
        code, label, rgb, emblem = CATEGORIES[key]
    else:
        code, _, rgb, emblem = FALLBACK
        label = (str(cat).strip().upper() if str(cat or "").strip() else "GENERAL")
    return {"code": code, "label": label, "rgb": rgb, "emblem": emblem}


# --------------------------------------------------------------------------
# short form ("drawing number") - a rule, not a lookup table
# --------------------------------------------------------------------------
_STOP = {"and", "or", "of", "the", "a", "an", "on", "in", "to", "for", "with", "by", "at"}


def short_form(name):
    """Initials of the significant words + any qualifier found in the name.

    * function words (and, of, the, on, ...) and symbols (&, -, +) are dropped
    * camelCase words count as several words ("BioLab" -> B, L)
    * a number with an optional x ("10x", "2.5x") becomes a suffix: FP-10X
    * a parenthesised word becomes a 4-letter suffix: "(Instant)" -> FP-INST
    * a single significant word is kept whole (max 7 letters)
    """
    s = str(name or "").replace("\u2019", "'")
    quals = []
    for q in re.findall(r"\(([^)]*)\)", s):
        q = re.sub(r"[^A-Za-z0-9.]", "", q)
        if q:
            quals.append(q)
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"'s\b", "s", s).replace("'", "")
    initials, words = [], []
    for w in re.split(r"[\s\-\u2013\u2014/_&+,.:;!?]+", s):
        if not w or w.lower() in _STOP:
            continue
        if re.fullmatch(r"\d+(\.\d+)?[xX]?", w):
            quals.append(w)
            continue
        parts = re.findall(r"[A-Z]+(?![a-z])|[A-Z]?[a-z]+|\d+", w) or [w]
        words.append(w)
        initials.extend(p[0] for p in parts)
    if len(words) == 1 and len(initials) <= 2:
        code = re.sub(r"[^A-Za-z0-9]", "", words[0]).upper()[:7]
    else:
        code = "".join(initials).upper()[:6]
    if not code:
        code = "MOD"
    for q in quals[:1]:
        q = q.upper()
        if not re.fullmatch(r"\d+(\.\d+)?X?", q):
            q = q[:4]
        code = code + "-" + q
    return code


# --------------------------------------------------------------------------
# fonts & type
# --------------------------------------------------------------------------
_FONTS = {}
_HAVE = {}
THIN = "\u2009"   # rendered by our own layout as a 0.2em gap (Bahnschrift lacks it)


def bahn(size, wght=400, wdth=100):
    key = (round(float(size), 2), int(round(wght)), int(round(wdth)))
    f = _FONTS.get(key)
    if f is None:
        f = ImageFont.truetype(BAHNSCHRIFT, key[0])
        f.set_variation_by_axes([key[1], key[2]])
        _FONTS[key] = f
    return f


def has_glyph(ch):
    if ch in (" ", THIN):
        return True
    r = _HAVE.get(ch)
    if r is None:
        f = bahn(32)
        ref = f.getmask("\ue000")
        m = f.getmask(ch)
        r = not (m.size == ref.size and bytes(m) == bytes(ref))
        _HAVE[ch] = r
    return r


def typeset(text):
    """Typographic clean-up shared by every string we print."""
    t = str(text or "")
    t = t.replace("'", "\u2019").replace("`", "\u2019")
    t = re.sub(r"\s+-\s+", " \u2013 ", t)
    t = re.sub(r"(\d)[xX]\b", "\\1\u00d7", t)          # 10x -> 10×
    t = re.sub(r"\s+", " ", t).strip()
    t = "".join(ch for ch in t if has_glyph(ch))       # drop glyphs the font lacks
    return re.sub(r"\s+", " ", t).strip()


_PROF = {}


class Type:
    """A Bahnschrift instance with tracking and optional optical kerning."""

    def __init__(self, size, wght=400, wdth=100, track=0.0, kern=False):
        self.size, self.wght, self.wdth = float(size), wght, wdth
        self.f = bahn(size, wght, wdth)
        # advances come from a 1000px instance: hinted small sizes round every
        # advance to whole pixels, which makes small type space unevenly
        self.fref = bahn(1000, wght, wdth)
        self.track = track * self.size
        self.kern = kern
        self._cap = None

    @property
    def cap(self):
        if self._cap is None:
            self._cap = -self.f.getbbox("H", anchor="ls")[1]
        return self._cap

    def adv(self, ch):
        if ch == THIN:
            return 0.2 * self.size
        return self.fref.getlength(ch) * self.size / 1000.0

    def layout(self, text):
        xs, x, prev = [], 0.0, None
        for ch in text:
            if prev is not None:
                x += self.adv(prev) + self.track
                if self.kern:
                    x += kern_pair(self, prev, ch)
            xs.append(x)
            prev = ch
        return xs

    def extent(self, text):
        """Ink extent (left, right) relative to the pen origin."""
        xs = self.layout(text)
        lo, hi = [], []
        for x, ch in zip(xs, text):
            if ch in (" ", THIN):
                continue
            bb = self.f.getbbox(ch, anchor="ls")
            lo.append(x + bb[0])
            hi.append(x + bb[2])
        if not lo:
            return 0.0, 0.0
        return min(lo), max(hi)

    def width(self, text):
        a, b = self.extent(text)
        return b - a

    def draw(self, ly, x, baseline, text, op=1.0, align="left", fill=None):
        """Draw onto a Layer (or a raw ImageDraw) with optical edge alignment."""
        xs = self.layout(text)
        a, b = self.extent(text)
        ox = x - a if align == "left" else (x - (a + b) / 2 if align == "center" else x - b)
        d = ly.d if isinstance(ly, Layer) else ly
        if fill is None:
            fill = int(round(255 * op))
        for xi, ch in zip(xs, text):
            if ch in (" ", THIN):
                continue
            d.text((ox + xi, baseline), ch, font=self.f, fill=fill, anchor="ls")
        return ox + a, ox + b


def _glyph_profile(T, ch):
    key = (T.size, T.wght, T.wdth, ch)
    p = _PROF.get(key)
    if p is not None:
        return p
    f = T.f
    asc, desc = f.getmetrics()
    pad = int(T.size) + 4
    adv = T.adv(ch)
    im = Image.new("L", (int(adv) + 2 * pad, asc + desc + 4), 0)
    ImageDraw.Draw(im).text((pad, asc + 2), ch, font=f, fill=255, anchor="ls")
    a = np.asarray(im) > 100
    top = int(round(asc + 2 - T.cap))
    rows = a[top:asc + 2]
    has = rows.any(axis=1)
    left = np.where(has, rows.argmax(axis=1) - pad, np.inf).astype(np.float64)
    right = np.where(has, rows.shape[1] - rows[:, ::-1].argmax(axis=1) - pad, -np.inf).astype(np.float64)
    p = (adv, left, right)
    _PROF[key] = p
    return p


def kern_pair(T, a, b):
    """Optical kerning for capitals: equalise the white area between letters
    against the H|H reference, never letting two letters crowd."""
    if not (a.isalnum() and b.isalnum()):
        return 0.0
    pa, pb, ph = _glyph_profile(T, a), _glyph_profile(T, b), _glyph_profile(T, "H")
    g = (pa[0] - pa[2]) + pb[1] + T.track
    gr = (ph[0] - ph[2]) + ph[1] + T.track
    cap = 0.30 * T.size
    adj = 0.62 * (np.mean(np.minimum(gr, cap)) - np.mean(np.minimum(g, cap)))
    adj = min(max(adj, -0.11 * T.size), 0.03 * T.size)
    gmin = np.min(g)
    if np.isfinite(gmin):
        adj = max(adj, 0.05 * T.size - gmin)
    return float(adj)


_NO_END = {"OF", "THE", "A", "AN", "TO", "IN", "ON", "FOR", "WITH", "BY", "AT"}
_NO_START = {"&", "+", "–", "-"}


def best_lines(words, n, measure):
    """Split words into n lines minimising the widest line, with typographic
    break rules: '&' stays at the end of a line, never ends on 'of'/'the'/..."""
    if n == 1 or len(words) <= 1:
        return [" ".join(words)] if n == 1 else None
    if len(words) < n:
        return None
    best, best_w = None, None
    for cuts in itertools.combinations(range(1, len(words)), n - 1):
        lines, prev, bad = [], 0, 0
        for c in list(cuts) + [len(words)]:
            seg = words[prev:c]
            if prev > 0 and seg[0].upper() in _NO_START:
                bad += 1
            if c < len(words) and seg[-1].upper() in _NO_END:
                bad += 1
            lines.append(" ".join(seg))
            prev = c
        w = max(measure(l) for l in lines) * (1.0 + 0.6 * bad)
        # tiny bias: prefer the longer line on top (reads like a title)
        w += 0.001 * max(0.0, measure(lines[-1]) - measure(lines[0]))
        if best_w is None or w < best_w:
            best, best_w = lines, w
    return best


def fit_block(text, max_w, max_h, smax, smin, wght, max_lines=2, wmin=78,
              track=0.0, kern=False, pitch=1.36, step=0.5, line_cost=0.13, cond_cost=0.006):
    """Auto-fit a text block. For every (line count, width instance) the
    largest fitting size is found; each candidate is scored by its size minus
    a cost per extra line and per unit of condensing, so a name only breaks
    or condenses when that buys a clearly bigger setting.
    Returns (Type, lines, line_pitch_px)."""
    words = text.split()

    def attempt(n, wd, s):
        T = Type(s, wght, wd, track, kern)
        lines = best_lines(words, n, T.width)
        if lines is None:
            return None
        lp = T.cap * pitch
        if max(T.width(l) for l in lines) <= max_w and T.cap + (len(lines) - 1) * lp <= max_h:
            return T, lines, lp
        return None

    best = None
    for n in range(1, min(max_lines, max(1, len(words))) + 1):
        for wd in range(100, wmin - 1, -4):
            hit = attempt(n, wd, smax)
            if hit is None:
                if attempt(n, wd, smin) is None:
                    continue
                lo, hi = smin, smax
                while hi - lo > step:
                    mid = round((lo + hi) / 2 / step) * step
                    if mid <= lo or mid >= hi:
                        break
                    if attempt(n, wd, mid):
                        lo = mid
                    else:
                        hi = mid
                hit = attempt(n, wd, lo)
            score = hit[0].size * (1.0 - line_cost * (n - 1)) * (1.0 - cond_cost * (100 - wd))
            if best is None or score > best[0] + 1e-9:
                best = (score, hit)
    if best:
        return best[1]
    # last resort: smallest, most condensed, hard truncation with ellipsis
    T = Type(smin, wght, wmin, track, kern)
    lines = best_lines(words, max_lines, T.width) or [text]
    out = []
    for l in lines[:max_lines]:
        while T.width(l) > max_w and len(l) > 2:
            l = l[:-2].rstrip() + "\u2026"
        out.append(l)
    return T, out, T.cap * pitch


# --------------------------------------------------------------------------
# analytic ink engine (signed distance fields, ~1px anti-aliasing)
# --------------------------------------------------------------------------
class Layer:
    """Coverage of one ink colour. Geometry is evaluated analytically per pixel;
    text is rasterised by Pillow into a parallel 8-bit plane."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.a = np.zeros((h, w), np.float32)
        self.t = Image.new("L", (w, h), 0)
        self.d = ImageDraw.Draw(self.t)

    def window(self, x0, y0, x1, y1):
        ix0, iy0 = max(0, int(math.floor(x0))), max(0, int(math.floor(y0)))
        ix1, iy1 = min(self.w, int(math.ceil(x1)) + 1), min(self.h, int(math.ceil(y1)) + 1)
        if ix1 <= ix0 or iy1 <= iy0:
            return None
        X, Y = np.meshgrid(np.arange(ix0, ix1, dtype=np.float32) + 0.5,
                           np.arange(iy0, iy1, dtype=np.float32) + 0.5)
        return (slice(iy0, iy1), slice(ix0, ix1)), X, Y

    def put(self, sl, cov, op=1.0):
        cov = np.clip(cov, 0.0, 1.0) * op
        cur = self.a[sl]
        self.a[sl] = cur + cov * (1.0 - cur)

    def paste_text_image(self, im, x, y):
        """Lighten-composite a pre-rendered L image (e.g. rotated text)."""
        x, y = int(round(x)), int(round(y))
        canvas = Image.new("L", (self.w, self.h), 0)
        canvas.paste(im, (x, y))
        self.t = ImageChops.lighter(self.t, canvas)
        self.d = ImageDraw.Draw(self.t)

    def coverage(self):
        t = np.asarray(self.t, np.float32) / 255.0
        return 1.0 - (1.0 - self.a) * (1.0 - t)


class Shape:
    __slots__ = ("f", "bbox")

    def __init__(self, f, bbox):
        self.f, self.bbox = f, bbox

    def __call__(self, X, Y):
        return self.f(X, Y)

    def __or__(self, o):
        a, b = self.bbox, o.bbox
        return Shape(lambda X, Y: np.minimum(self(X, Y), o(X, Y)),
                     (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3])))

    def __sub__(self, o):
        return Shape(lambda X, Y: np.maximum(self(X, Y), -o(X, Y)), self.bbox)

    def __and__(self, o):
        a, b = self.bbox, o.bbox
        bb = (max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3]))
        return Shape(lambda X, Y: np.maximum(self(X, Y), o(X, Y)), bb)

    def grow(self, r):
        a = self.bbox
        return Shape(lambda X, Y: self(X, Y) - r, (a[0] - r, a[1] - r, a[2] + r, a[3] + r))


INF_BOX = (-1e6, -1e6, 1e6, 1e6)


def _seg(X, Y, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    if L2 < 1e-12:
        return np.hypot(X - ax, Y - ay), np.zeros_like(X)
    t = np.clip(((X - ax) * dx + (Y - ay) * dy) / L2, 0.0, 1.0)
    return np.hypot(X - (ax + t * dx), Y - (ay + t * dy)), t


def sd_poly(X, Y, P):
    n = len(P)
    d = (X - P[0][0]) ** 2 + (Y - P[0][1]) ** 2
    s = np.ones_like(X)
    j = n - 1
    for i in range(n):
        vix, viy = P[i]
        vjx, vjy = P[j]
        ex, ey = vjx - vix, vjy - viy
        wx, wy = X - vix, Y - viy
        L2 = ex * ex + ey * ey
        t = np.clip((wx * ex + wy * ey) / L2, 0.0, 1.0) if L2 > 0 else 0.0
        bx, by = wx - ex * t, wy - ey * t
        d = np.minimum(d, bx * bx + by * by)
        c1 = Y >= viy
        c2 = Y < vjy
        c3 = (ex * wy) > (ey * wx)
        flip = (c1 & c2 & c3) | (~c1 & ~c2 & ~c3)
        s = np.where(flip, -s, s)
        j = i
    return s * np.sqrt(d)


def S_poly(P):
    P = [(float(x), float(y)) for x, y in P]
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    return Shape(lambda X, Y: sd_poly(X, Y, P), (min(xs), min(ys), max(xs), max(ys)))


def S_circle(cx, cy, r):
    return Shape(lambda X, Y: np.hypot(X - cx, Y - cy) - r, (cx - r, cy - r, cx + r, cy + r))


def S_ellipse(cx, cy, rx, ry):
    def f(X, Y):
        px, py = X - cx, Y - cy
        k0 = np.hypot(px / rx, py / ry)
        k1 = np.hypot(px / (rx * rx), py / (ry * ry))
        return k0 * (k0 - 1.0) / np.maximum(k1, 1e-6)
    return Shape(f, (cx - rx, cy - ry, cx + rx, cy + ry))


def S_capsule(a, b, r):
    (ax, ay), (bx, by) = a, b
    return Shape(lambda X, Y: _seg(X, Y, ax, ay, bx, by)[0] - r,
                 (min(ax, bx) - r, min(ay, by) - r, max(ax, bx) + r, max(ay, by) + r))


def S_box(cx, cy, hw, hh, ang=0.0, r=0.0):
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))

    def f(X, Y):
        dx, dy = X - cx, Y - cy
        lx, lyy = dx * ca + dy * sa, -dx * sa + dy * ca
        qx, qy = np.abs(lx) - (hw - r), np.abs(lyy) - (hh - r)
        return (np.hypot(np.maximum(qx, 0), np.maximum(qy, 0))
                + np.minimum(np.maximum(qx, qy), 0) - r)
    R = math.hypot(hw, hh)
    return Shape(f, (cx - R, cy - R, cx + R, cy + R))


def S_half(px, py, nx, ny):
    """Half plane; inside where (p - p0) . n < 0."""
    return Shape(lambda X, Y: (X - px) * nx + (Y - py) * ny, INF_BOX)


def inset_convex(P, d):
    n = len(P)
    out = []
    for i in range(n):
        p0, p1, p2 = P[i - 1], P[i], P[(i + 1) % n]
        e1 = np.array(p0, float) - np.array(p1, float)
        e2 = np.array(p2, float) - np.array(p1, float)
        e1 /= np.linalg.norm(e1)
        e2 /= np.linalg.norm(e2)
        bis = e1 + e2
        bis /= np.linalg.norm(bis)
        half = math.acos(max(-1.0, min(1.0, float(np.dot(e1, e2))))) / 2
        q = np.array(p1, float) + bis * d / math.sin(half)
        out.append((float(q[0]), float(q[1])))
    return out


DASH = {"centre": (17.0, 3.2, 3.2, 3.2), "hidden": (6.0, 3.6), "phantom": (16.0, 3.0, 2.5, 3.0, 2.5, 3.0)}


def _fit_pattern(L, pattern, closed=False):
    period = sum(pattern)
    if closed:
        n = max(1, round(L / period))
        k = L / (n * period)
    else:
        first = pattern[0]
        n = max(0, round((L - first) / period))
        k = L / (n * period + first) if n * period + first > 0 else 1.0
    return [p * k for p in pattern]


def _dash_cov(s, pattern):
    period = sum(pattern)
    m = np.mod(s, period)
    cov = np.zeros_like(s)
    pos = 0.0
    for i in range(0, len(pattern), 2):
        a, b = pos, pos + pattern[i]
        for mm in (m, m - period, m + period):
            cov = np.maximum(cov, np.clip(np.minimum(mm - a, b - mm) + 0.5, 0.0, 1.0))
        pos = b + (pattern[i + 1] if i + 1 < len(pattern) else 0.0)
    return cov


def line(ly, p0, p1, w, op=1.0, dash=None, cap="butt", dscale=1.0):
    (x0, y0), (x1, y1) = p0, p1
    pad = w / 2 + 2
    win = ly.window(min(x0, x1) - pad, min(y0, y1) - pad, max(x0, x1) + pad, max(y0, y1) + pad)
    L = math.hypot(x1 - x0, y1 - y0)
    if win is None or L < 1e-6:
        return
    sl, X, Y = win
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    along = (X - x0) * ux + (Y - y0) * uy
    perp = np.abs(-(X - x0) * uy + (Y - y0) * ux)
    if cap == "round":
        ac = np.clip(along, 0, L)
        cov = np.clip(w / 2 - np.hypot(along - ac, perp) + 0.5, 0, 1)
    else:
        cov = np.clip(w / 2 - perp + 0.5, 0, 1) * np.clip(np.minimum(along, L - along) + 0.5, 0, 1)
    if dash:
        cov = cov * _dash_cov(np.clip(along, 0, L), _fit_pattern(L, [p * dscale for p in DASH[dash]]))
    ly.put(sl, cov, op)


def polyline(ly, pts, w, op=1.0, closed=False, dash=None, dscale=1.0):
    P = list(pts) + ([pts[0]] if closed else [])
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    pad = w / 2 + 2
    win = ly.window(min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)
    if win is None:
        return
    sl, X, Y = win
    best = np.full(X.shape, np.inf, np.float32)
    sbest = np.zeros_like(X)
    acc = 0.0
    for (ax, ay), (bx, by) in zip(P[:-1], P[1:]):
        L = math.hypot(bx - ax, by - ay)
        if L < 1e-9:
            continue
        d, t = _seg(X, Y, ax, ay, bx, by)
        m = d < best
        best = np.where(m, d, best)
        sbest = np.where(m, acc + t * L, sbest)
        acc += L
    cov = np.clip(w / 2 - best + 0.5, 0, 1)
    if dash:
        cov = cov * _dash_cov(sbest, _fit_pattern(acc, [p * dscale for p in DASH[dash]], closed))
    ly.put(sl, cov, op)


def arc(ly, c, r, a0, a1, w, op=1.0, dash=None, dscale=1.0):
    """Arc in screen degrees (y down => increasing angle is clockwise)."""
    cx, cy = c
    pad = r + w / 2 + 2
    win = ly.window(cx - pad, cy - pad, cx + pad, cy + pad)
    if win is None:
        return
    sl, X, Y = win
    dx, dy = X - cx, Y - cy
    rho = np.hypot(dx, dy)
    ang = np.degrees(np.arctan2(dy, dx))
    sweep = a1 - a0
    perp = np.abs(rho - r)
    if sweep >= 360 - 1e-6:
        s = np.radians(np.mod(ang - a0, 360.0)) * r
        cov = np.clip(w / 2 - perp + 0.5, 0, 1)
        L, closed = 2 * math.pi * r, True
    else:
        mid = a0 + sweep / 2
        rel = np.mod(ang - mid + 180.0, 360.0) - 180.0 + sweep / 2
        s = np.radians(rel) * r
        L, closed = math.radians(sweep) * r, False
        cov = np.clip(w / 2 - perp + 0.5, 0, 1) * np.clip(np.minimum(s, L - s) + 0.5, 0, 1)
        s = np.clip(s, 0, L)
    if dash:
        cov = cov * _dash_cov(s, _fit_pattern(L, [p * dscale for p in DASH[dash]], closed))
    ly.put(sl, cov, op)


def fill(ly, S, op=1.0):
    x0, y0, x1, y1 = S.bbox
    win = ly.window(x0 - 1, y0 - 1, x1 + 1, y1 + 1)
    if win is None:
        return
    sl, X, Y = win
    ly.put(sl, np.clip(0.5 - S(X, Y), 0, 1), op)


def stroke(ly, S, w, op=1.0, clip=None):
    x0, y0, x1, y1 = S.bbox
    pad = w / 2 + 1.5
    win = ly.window(x0 - pad, y0 - pad, x1 + pad, y1 + pad)
    if win is None:
        return
    sl, X, Y = win
    cov = np.clip(w / 2 - np.abs(S(X, Y)) + 0.5, 0, 1)
    if clip is not None:
        cov = cov * np.clip(0.5 - clip(X, Y), 0, 1)
    ly.put(sl, cov, op)


def hatch(ly, S, spacing, w, angle=45.0, op=1.0, inset=0.0):
    x0, y0, x1, y1 = S.bbox
    win = ly.window(x0 - 1, y0 - 1, x1 + 1, y1 + 1)
    if win is None:
        return
    sl, X, Y = win
    inside = np.clip(0.5 - (S(X, Y) + inset), 0, 1)
    th = math.radians(angle)
    u = X * math.sin(th) + Y * math.cos(th)
    dist = np.abs(np.mod(u, spacing) - spacing / 2)
    ly.put(sl, np.clip(w / 2 - dist + 0.5, 0, 1) * inside, op)


def arrowhead(ly, tip, ux, uy, length, width, op=1.0):
    bx, by = tip[0] - ux * length, tip[1] - uy * length
    nx, ny = -uy, ux
    fill(ly, S_poly([tip, (bx + nx * width / 2, by + ny * width / 2),
                     (bx - nx * width / 2, by - ny * width / 2)]), op)


def rect(ly, x0, y0, x1, y1, w, op=1.0):
    h = w / 2
    line(ly, (x0 - h, y0), (x1 + h, y0), w, op)
    line(ly, (x0 - h, y1), (x1 + h, y1), w, op)
    line(ly, (x0, y0 - h), (x0, y1 + h), w, op)
    line(ly, (x1, y0 - h), (x1, y1 + h), w, op)


def text_image(text, T, op=1.0):
    """Render text tightly into an L image; returns (image, baseline_offset_y, left_ink_x)."""
    a, b = T.extent(text)
    asc, desc = T.f.getmetrics()
    W = int(math.ceil(b - a)) + 6
    H = asc + desc + 6
    im = Image.new("L", (W, H), 0)
    T.draw(ImageDraw.Draw(im), 3, asc + 3, text, op)
    return im, asc + 3


def text_rotated(ly, cx, cy, text, T, angle, op=1.0):
    """Text centred (on its cap-height box) at (cx, cy), rotated by angle degrees CCW."""
    im, base = text_image(text, T, op)
    # centre of the cap box inside im
    mx, my = im.width / 2, base - T.cap / 2
    big = Image.new("L", (im.width * 3, im.height * 3), 0)
    ox, oy = big.width / 2 - mx, big.height / 2 - my
    big.paste(im, (int(round(ox)), int(round(oy))))
    rot = big.rotate(angle, resample=Image.BICUBIC, center=(big.width / 2, big.height / 2))
    bb = rot.getbbox()
    if not bb:
        return
    crop = rot.crop(bb)
    ly.paste_text_image(crop, cx - big.width / 2 + bb[0], cy - big.height / 2 + bb[1])


# --------------------------------------------------------------------------
# paper
# --------------------------------------------------------------------------
def smooth_noise(rng, w, h, cx, cy):
    n = rng.standard_normal((max(2, cy), max(2, cx))).astype(np.float32)
    a = np.asarray(Image.fromarray(n, mode="F").resize((w, h), Image.BICUBIC), np.float32)
    return (a - a.mean()) / (a.std() + 1e-6)


def make_paper(w, h, rng):
    m = 0.7 * smooth_noise(rng, w, h, w // 150 + 3, h // 150 + 3) \
        + 0.3 * smooth_noise(rng, w, h, w // 46 + 4, h // 46 + 4)
    m /= m.std() + 1e-6
    g = rng.standard_normal((h, w)).astype(np.float32)
    g = (g + np.roll(g, 1, 0) + np.roll(g, 1, 1) + np.roll(np.roll(g, 1, 0), 1, 1)) / 2.0
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    vx, vy = (xx + 0.5) / w * 2 - 1, (yy + 0.5) / h * 2 - 1
    vig = 1.0 - 0.06 * vx ** 2 - 0.09 * vy ** 2
    lum = (1.0 + 0.045 * m + 0.02 * g) * vig
    rgb = PAPER[None, None, :] * lum[..., None]
    rgb[..., 1] += 0.010 * m
    rgb[..., 2] += 0.006 * m
    return np.clip(rgb, 0, 1)


def grid_cov(w, h, box, minor, major, a_minor, a_major):
    x0, y0, x1, y1 = box
    G = np.zeros((h, w), np.float32)
    for x in range(x0, x1 + 1, minor):
        a = a_major if (x - x0) % major == 0 else a_minor
        G[y0:y1 + 1, x] = np.maximum(G[y0:y1 + 1, x], a)
    for y in range(y0, y1 + 1, minor):
        a = a_major if (y - y0) % major == 0 else a_minor
        G[y, x0:x1 + 1] = np.maximum(G[y, x0:x1 + 1], a)
    return G


def ink_texture(cov, rng):
    """Cyanotype exposure: the white is never perfectly even."""
    h, w = cov.shape
    n = smooth_noise(rng, w, h, w // 60 + 3, h // 60 + 3)
    return cov * np.clip(0.95 + 0.05 * n, 0.85, 1.0)


def composite(paper, layers):
    out = paper.copy()
    for cov, col in layers:
        c = np.asarray(col, np.float32)
        if c.max() > 1.0:
            c = c / 255.0
        out = out * (1.0 - cov[..., None]) + c[None, None, :] * cov[..., None]
    return Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8), "RGB")


# --------------------------------------------------------------------------
# rubber stamp (category)
# --------------------------------------------------------------------------
def stamp_cov(label, code, rng, max_w=136, smax=17.0, smin=10.0):
    """Two-rule rubber stamp: small 'CATEGORY . CODE' line over the label
    (one line when it fits at full size, otherwise stacked on two)."""
    sub = Type(7.6, 500, 85, track=0.18)
    pad_x, pad_y, gap = 11.0, 8.5, 5.0
    T, lines, lp = fit_block(label, max_w - 2 * pad_x, smax * 2.0, smax, smin, 700,
                             max_lines=2, wmin=74, track=0.03, pitch=1.34, cond_cost=0.003)
    text_w = max(T.width(l) for l in lines)
    sub_txt = "CATEGORY \u00b7 " + code
    W = int(math.ceil(max(text_w, sub.width(sub_txt)) + 2 * pad_x))
    block_h = sub.cap + gap + T.cap + (len(lines) - 1) * lp
    H = int(math.ceil(block_h + 2 * pad_y))
    ly = Layer(W + 8, H + 8)
    o = 4.0
    rect(ly, o + 1.2, o + 1.2, o + W - 1.2, o + H - 1.2, 2.4)
    rect(ly, o + 4.6, o + 4.6, o + W - 4.6, o + H - 4.6, 1.0)
    y = o + (H - block_h) / 2 + sub.cap
    sub.draw(ly, o + W / 2, y, sub_txt, 1.0, "center")
    y += gap + T.cap
    for l in lines:
        T.draw(ly, o + W / 2, y, l, 1.0, "center")
        y += lp
    cov = ly.coverage()
    # rubber: uneven pressure + small voids
    hh, ww = cov.shape
    press = smooth_noise(rng, ww, hh, 4, 3)
    voids = smooth_noise(rng, ww, hh, ww // 3 + 2, hh // 3 + 2)
    cov = cov * np.clip(0.84 + 0.12 * press, 0.6, 1.0)
    cov = cov * np.where(voids > 1.55, 0.35, 1.0)
    return cov


def rotate_cov(cov, angle):
    im = Image.fromarray((np.clip(cov, 0, 1) * 255).astype(np.uint8), "L")
    im = im.rotate(angle, resample=Image.BICUBIC, expand=True)
    return np.asarray(im, np.float32) / 255.0


def paste_cov(dst, src, x, y):
    h, w = src.shape
    x, y = int(round(x)), int(round(y))
    X0, Y0 = max(0, x), max(0, y)
    X1, Y1 = min(dst.shape[1], x + w), min(dst.shape[0], y + h)
    if X1 <= X0 or Y1 <= Y0:
        return
    s = src[Y0 - y:Y1 - y, X0 - x:X1 - x]
    d = dst[Y0:Y1, X0:X1]
    dst[Y0:Y1, X0:X1] = 1.0 - (1.0 - d) * (1.0 - s)


# --------------------------------------------------------------------------
# emblems: one technical "part" per category
# --------------------------------------------------------------------------
class Pen:
    """Maps emblem units ([-1, 1] box, y down) to pixels and carries the
    line-weight set for icon or banner rendering."""

    def __init__(self, ly, cx, cy, k, mode, rng, field=None, seed=0):
        self.ly, self.cx, self.cy, self.k, self.mode, self.rng = ly, cx, cy, k, mode, rng
        self.seed = seed              # per-mod seed: part variations match on icon and banner
        icon = mode == "icon"
        self.icon = icon
        self.H = 5.4 if icon else 3.0          # visible outline
        self.M = 3.4 if icon else 2.0          # secondary visible edges
        self.T = 1.7 if icon else 1.05         # thin: centre lines, hatch, dimensions
        self.hs = 6.6 if icon else 4.7         # hatch pitch
        self.ds = 0.95 if icon else 0.72       # dash scale
        self.field = field or (0, 0, ly.w, ly.h)
        self.note = Type(10.5, 400, 78, track=0.05)

    def p(self, u, v):
        return (self.cx + u * self.k, self.cy + v * self.k)

    def ps(self, seq):
        return [self.p(u, v) for u, v in seq]

    # drawing wrappers -----------------------------------------------------
    def line(self, a, b, w=None, op=1.0, dash=None, cap="round"):
        line(self.ly, self.p(*a), self.p(*b), self.H if w is None else w, op, dash, cap, self.ds)

    def poly(self, seq, w=None, closed=True, op=1.0, dash=None):
        polyline(self.ly, self.ps(seq), self.H if w is None else w, op, closed, dash, self.ds)

    def circle(self, c, r, w=None, op=1.0, dash=None):
        arc(self.ly, self.p(*c), r * self.k, 0, 360, self.H if w is None else w, op, dash, self.ds)

    def arc(self, c, r, a0, a1, w=None, op=1.0, dash=None):
        arc(self.ly, self.p(*c), r * self.k, a0, a1, self.H if w is None else w, op, dash, self.ds)

    def SP(self, seq):
        return S_poly(self.ps(seq))

    def SC(self, c, r):
        return S_circle(*self.p(*c), r * self.k)

    def stroke(self, S, w=None, op=1.0, clip=None):
        stroke(self.ly, S, self.H if w is None else w, op, clip)

    def fill(self, S, op=1.0):
        fill(self.ly, S, op)

    def hatch(self, S, angle=45.0, op=0.92, pitch=None):
        hatch(self.ly, S, pitch or self.hs, self.T, angle, op, inset=self.H * 0.35)

    def centre(self, a, b, op=0.9):
        line(self.ly, self.p(*a), self.p(*b), self.T, op, "centre", "butt", self.ds)

    # annotation (banner only) ---------------------------------------------
    def _clampx(self, x0, x1):
        fx0, _, fx1, _ = self.field
        shift = 0.0
        if x0 < fx0 + 8:
            shift = fx0 + 8 - x0
        if x1 + shift > fx1 - 9:
            shift = fx1 - 9 - x1
        return shift

    def dim(self, a, b, off, text, op=0.9):
        """Aligned linear dimension between feature points a, b (units), offset
        perpendicular by `off` units (sign picks the side)."""
        A, B = np.array(self.p(*a)), np.array(self.p(*b))
        d = B - A
        L = float(np.linalg.norm(d))
        u = d / L
        n = np.array([-u[1], u[0]])
        o = off * self.k
        A2, B2 = A + n * o, B + n * o
        sgn = 1.0 if o >= 0 else -1.0
        gap, over = 3.0, 4.0
        for P, Q in ((A, A2), (B, B2)):
            line(self.ly, tuple(P + n * sgn * gap), tuple(Q + n * sgn * over), self.T, op * 0.85)
        line(self.ly, tuple(A2), tuple(B2), self.T, op)
        arrowhead(self.ly, tuple(A2), -u[0], -u[1], 7.5, 2.6, op)
        arrowhead(self.ly, tuple(B2), u[0], u[1], 7.5, 2.6, op)
        mid = (A2 + B2) / 2
        ang = -math.degrees(math.atan2(u[1], u[0]))
        if ang > 90:
            ang -= 180
        if ang <= -90:
            ang += 180
        tpos = mid + n * sgn * (self.note.cap / 2 + 3.5)
        if abs(ang) < 1e-3:
            T = self.note
            w = T.width(text)
            x0 = tpos[0] - w / 2
            s = self._clampx(x0, x0 + w)
            T.draw(self.ly, tpos[0] + s, tpos[1] + T.cap / 2, text, op, "center")
        else:
            text_rotated(self.ly, tpos[0], tpos[1], text, self.note, ang, op)

    def angle(self, vertex, a0, a1, r, text, op=0.9, ext=(0.0, 0.0), tr=None):
        """Angular dimension at `vertex` between screen angles a0 < a1."""
        V = self.p(*vertex)
        R = r * self.k
        for a, e in ((a0, ext[0]), (a1, ext[1])):
            if e > 0:
                ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
                line(self.ly, (V[0] + ca * 2, V[1] + sa * 2),
                     (V[0] + ca * (R + e * self.k), V[1] + sa * (R + e * self.k)), self.T, op * 0.85)
        arc(self.ly, V, R, a0, a1, self.T, op)
        alen = 7.0
        inside = math.radians(a1 - a0) * R > 2.2 * alen
        if not inside:
            # tight angle: arrows sit outside the extension lines, pointing in
            tail = math.degrees(1.9 * alen / R)
            arc(self.ly, V, R, a0 - tail, a0, self.T, op)
            arc(self.ly, V, R, a1, a1 + tail, self.T, op)
        for a, sgn in ((a0, -1), (a1, 1)):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            tip = (V[0] + ca * R, V[1] + sa * R)
            tx, ty = -sa * sgn, ca * sgn
            if not inside:
                tx, ty = -tx, -ty
            arrowhead(self.ly, tip, tx, ty, alen, 2.5, op)
        m = math.radians((a0 + a1) / 2)
        rr = (tr if tr is not None else r + 0.22) * self.k
        T = self.note
        cx, cy = V[0] + math.cos(m) * rr, V[1] + math.sin(m) * rr
        w = T.width(text)
        s = self._clampx(cx - w / 2, cx + w / 2)
        T.draw(self.ly, cx + s, cy + T.cap / 2, text, op, "center")

    def leader(self, target, elbow, text, op=0.9, dot=False):
        """Leader line with arrowhead (or dot) at target, shoulder and note."""
        Tp, E = np.array(self.p(*target)), np.array(self.p(*elbow))
        T = self.note
        w = T.width(text)
        right = E[0] >= Tp[0]
        sh = 9.0
        S = E + np.array([sh if right else -sh, 0.0])
        if right:
            tx0 = S[0] + 3
            s = self._clampx(tx0, tx0 + w)
        else:
            tx0 = S[0] - 3 - w
            s = self._clampx(tx0, tx0 + w)
        E = E + np.array([s, 0.0])
        S = S + np.array([s, 0.0])
        d = Tp - E
        L = float(np.linalg.norm(d))
        u = d / L
        if dot:
            fill(self.ly, S_circle(Tp[0], Tp[1], 2.2), op)
            line(self.ly, tuple(E), tuple(Tp), self.T, op)
        else:
            line(self.ly, tuple(E), tuple(Tp - u * 5), self.T, op)
            arrowhead(self.ly, tuple(Tp), u[0], u[1], 7.5, 2.6, op)
        line(self.ly, tuple(E), tuple(S), self.T, op)
        x = S[0] + 3 if right else S[0] - 3
        T.draw(self.ly, x, S[1] + T.cap / 2, text, op, "left" if right else "right")

    def balloon(self, target, at, label, op=0.9):
        Tp, B = np.array(self.p(*target)), np.array(self.p(*at))
        r = 8.0
        d = Tp - B
        L = float(np.linalg.norm(d))
        u = d / L
        fill(self.ly, S_circle(Tp[0], Tp[1], 2.1), op)
        line(self.ly, tuple(B + u * r), tuple(Tp), self.T, op)
        arc(self.ly, tuple(B), r, 0, 360, self.T * 1.1, op)
        T = Type(10, 500, 90)
        T.draw(self.ly, B[0], B[1] + T.cap / 2, label, op, "center")


def _bez(p0, p1, p2, n):
    out = []
    for t in np.linspace(0, 1, n):
        out.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
    return out


def em_house(pen):
    gy = 0.80
    roof = [(-0.94, 0.02), (0.0, -0.70), (0.94, 0.02)]
    walls = [(-0.68, 0.02), (0.68, 0.02), (0.68, gy), (-0.68, gy)]
    door = [(-0.17, 0.36), (0.17, 0.36), (0.17, gy), (-0.17, gy)]
    pen.hatch(pen.SP(door))
    pen.centre((0, -0.92), (0, 0.32))
    pen.stroke(pen.SP(roof))
    pen.stroke(pen.SP(walls))
    pen.stroke(pen.SP(door), pen.M)
    pen.line((0, -0.70), (0, 0.02), pen.M)
    pen.line((0, 0.02), (-0.47, -0.34), pen.M)
    pen.line((0, 0.02), (0.47, -0.34), pen.M)
    for x0 in (-0.53, 0.31):
        win = [(x0, 0.22), (x0 + 0.22, 0.22), (x0 + 0.22, 0.46), (x0, 0.46)]
        pen.stroke(pen.SP(win), pen.M * 0.8)
        pen.line((x0 + 0.11, 0.22), (x0 + 0.11, 0.46), pen.T)
        pen.line((x0, 0.34), (x0 + 0.22, 0.34), pen.T)
    pen.line((-1.06, gy), (1.06, gy), pen.H)
    for x in np.arange(-0.98, 1.02, 0.15 if pen.icon else 0.12):
        pen.line((x, gy + 0.03), (x - 0.10, gy + 0.15), pen.T, 0.9)
    if not pen.icon:
        pen.dim((-0.68, gy), (0.68, gy), 0.40, "13" + THIN + "600")
        rise = math.degrees(math.atan2(0.72, 0.94))
        pen.angle((0.94, 0.02), 0.0, rise, 0.52, "%d\u00b0" % round(rise), ext=(0.18, 0.12), tr=0.72)
        pen.balloon((0.24, -0.16), (1.30, -0.80), "1")


def _shield_pts():
    top = -0.84
    right = _bez((0.76, -0.10), (0.76, 0.54), (0.0, 0.94), 22)
    left = [(-x, y) for (x, y) in reversed(right[:-1])]
    return [(-0.76, top), (0.76, top)] + right + left


def em_shield(pen):
    pts = _shield_pts()
    S = pen.SP(pts)
    inner = S.grow(-0.14 * pen.k)
    pen.hatch(inner & S_half(pen.cx, 0, 1, 0))
    pen.centre((0, -1.04), (0, 1.12))
    pen.stroke(S)
    pen.stroke(inner, pen.M * 0.75)
    if not pen.icon:
        A, B = pen.p(0.76, -0.84), pen.p(0.0, 0.94)
        x = pen.p(1.18, 0)[0]
        line(pen.ly, (A[0] + 3, A[1]), (x + 4, A[1]), pen.T, 0.75)
        line(pen.ly, (B[0] + 3, B[1]), (x + 4, B[1]), pen.T, 0.75)
        line(pen.ly, (x, A[1]), (x, B[1]), pen.T, 0.9)
        arrowhead(pen.ly, (x, A[1]), 0, -1, 7.5, 2.6, 0.9)
        arrowhead(pen.ly, (x, B[1]), 0, 1, 7.5, 2.6, 0.9)
        text_rotated(pen.ly, x + pen.note.cap / 2 + 4, (A[1] + B[1]) / 2, "720", pen.note, 90, 0.9)
        pen.leader((-0.40, 0.18), (-1.28, 0.78), "SECT. A\u2013A")


def em_gem(pen):
    R = 0.95
    t = 0.53 * R
    crown = (R - t) * math.tan(math.radians(34.5))
    pav = R * math.tan(math.radians(40.75))
    gt = 0.05
    top = -(crown + gt + pav) / 2 - 0.06
    g0, g1 = top + crown, top + crown + gt
    cul = g1 + pav
    outline = [(-t, top), (t, top), (R, g0), (R, g1), (0, cul), (-R, g1), (-R, g0)]
    G = [-R, -R / 2, 0.0, R / 2, R]
    TT = [-t, -t / 3, t / 3, t]
    for a, b in ((0, 1), (2, 3)):
        tri = [(G[a], g1), (G[b], g1), (0.0, cul)]
        pen.hatch(pen.SP(tri), angle=45 if a == 0 else -45)
    pen.centre((0, top - 0.16), (0, cul + 0.18))
    pen.stroke(pen.SP(outline))
    pen.line((-R, g0), (R, g0), pen.M)
    pen.line((-R, g1), (R, g1), pen.M)
    zig = [(G[0], g0), (TT[0], top), (G[1], g0), (TT[1], top), (G[2], g0),
           (TT[2], top), (G[3], g0), (TT[3], top), (G[4], g0)]
    pen.poly(zig, pen.M * 0.8, closed=False)
    for gx in G[1:4]:
        pen.line((gx, g1), (0.0, cul), pen.M * 0.8)
    if not pen.icon:
        pen.dim((-R, g1), (R, g1), (cul - g1) + 0.30, "\u00d8" + "6.50")
        pen.angle((R, g0), -34.5, 0.0, 0.50, "34.5\u00b0", ext=(0.12, 0.16), tr=0.74)
        pen.angle((-R, g1), 180.0, 180.0 + 40.75, 0.46, "40.75\u00b0", ext=(0.16, 0.10), tr=0.70)


def em_bowl(pen):
    rim = -0.10
    ro, ri = (0.93, 0.70), (0.82, 0.59)
    cx, cy = pen.p(0, rim)
    outer = S_ellipse(cx, cy, ro[0] * pen.k, ro[1] * pen.k)
    inner = S_ellipse(cx, cy, ri[0] * pen.k, ri[1] * pen.k)
    below = S_half(0, cy, 0, -1)                    # inside where y > rim
    foot = pen.SP([(-0.37, 0.50), (0.37, 0.50), (0.31, 0.76), (-0.31, 0.76)])
    body = (outer & below) | foot
    wall = body - inner
    left = S_half(pen.cx, 0, 1, 0)
    pen.hatch(wall & left)
    pen.centre((0, rim - 0.10), (0, 0.92))
    pen.stroke(body)
    pen.stroke(inner, pen.H, clip=(below & left))
    pen.line((-0.93, rim), (0.93, rim), pen.H)
    for i, x0 in enumerate((-0.38, 0.0, 0.38)):
        top = -0.94 if i == 1 else -0.82
        pts = []
        for tt in np.linspace(0, 1, 40):
            v = rim - 0.13 + (top - rim + 0.13) * tt
            pts.append((x0 + 0.075 * math.sin(2 * math.pi * (1.15 * tt) + (0.0 if i != 1 else math.pi)), v))
        polyline(pen.ly, pen.ps(pts), pen.M, 1.0, False)
    if not pen.icon:
        pen.dim((-0.93, rim), (0.93, rim), 1.12, "\u00d8" + "180")
        pen.balloon((-0.55, 0.32), (-1.45, 0.62), "1")


def em_crate(pen):
    a, c = 0.90, 0.04
    h = 0.866 * a
    T, UL, UR = (0, c - a), (-h, c - a / 2), (h, c - a / 2)
    C, LL, LR, B = (0, c), (-h, c + a / 2), (h, c + a / 2), (0, c + a)
    pen.hatch(pen.SP([UL, C, B, LL]), angle=90, pitch=pen.hs * 1.05)
    if not pen.icon:
        for q in (LL, LR, T):
            pen.line(C, q, pen.T * 1.2, 0.85, dash="hidden", cap="butt")
    lerp = lambda p, q, s: (p[0] + (q[0] - p[0]) * s, p[1] + (q[1] - p[1]) * s)
    for s in (0.40, 0.60):
        e1, e2 = lerp(UL, T, s), lerp(C, UR, s)
        pen.line(e1, e2, pen.M * 0.8)
        pen.line(e2, lerp(B, LR, s), pen.M * 0.8)
    pen.poly([T, UR, LR, B, LL, UL])
    pen.line(C, UL)
    pen.line(C, UR)
    pen.line(C, B)
    if not pen.icon:
        pen.angle(LR, -30.0, 0.0, 0.56, "30\u00b0", ext=(0.12, 0.14), tr=0.76)
        pen.dim(LL, LR, (B[1] - LL[1]) + 0.28, "1" + THIN + "560")
        pen.balloon(lerp(C, UR, 0.5), (1.28, -0.95), "1")


def _gear_pts(Z, Ra, Rf, Rp, phase=-90.0):
    p = 360.0 / Z
    hr, hp, ht = 0.27 * p, 0.21 * p, 0.15 * p
    pts = []
    pol = lambda r, a: (r * math.cos(math.radians(a)), r * math.sin(math.radians(a)))
    for i in range(Z):
        c = phase + i * p
        for a in np.linspace(c - p / 2, c - hr, 3)[:-1]:
            pts.append(pol(Rf, a))
        pts.append(pol(Rf, c - hr))
        pts.append(pol(Rp, c - hp))
        for a in np.linspace(c - ht, c + ht, 3):
            pts.append(pol(Ra, a))
        pts.append(pol(Rp, c + hp))
        pts.append(pol(Rf, c + hr))
    return pts


def em_gear(pen):
    Z, Ra, Rf, Rp = 12, 0.80, 0.63, 0.72
    gear = pen.SP(_gear_pts(Z, Ra, Rf, Rp))
    web = pen.SC((0, 0), 0.52) - pen.SC((0, 0), 0.31)
    pen.hatch(web)
    for a, b in (((-1.0, 0), (1.0, 0)), ((0, -1.0), (0, 1.0))):
        pen.centre(a, b)
    pen.circle((0, 0), Rp, pen.T, 0.9, dash="centre")
    pen.stroke(gear)
    pen.circle((0, 0), 0.52, pen.M * 0.8)
    pen.circle((0, 0), 0.31, pen.M)
    bore = pen.SC((0, 0), 0.14) | S_box(*pen.p(0, -0.14), 0.045 * pen.k, 0.06 * pen.k)
    pen.stroke(bore, pen.M)
    r = 0.97 if pen.icon else 0.98
    a0, a1 = -168.0, -52.0
    pen.arc((0, 0), r, a0, a1 - 4, pen.M)
    ca, sa = math.cos(math.radians(a1)), math.sin(math.radians(a1))
    tip = pen.p(r * ca, r * sa)
    tl = pen.H * 3.0 if pen.icon else 11.0
    arrowhead(pen.ly, tip, -sa, ca, tl, tl * 0.85, 1.0)
    if not pen.icon:
        pen.leader((Ra * math.cos(math.radians(-15)), Ra * math.sin(math.radians(-15))), (1.20, -0.34), "Z = 12")
        pen.dim((-Ra, 0), (Ra, 0), 1.20, "\u00d8" + "160")


def em_sliders(pen):
    rng = np.random.default_rng(pen.seed ^ 0xA11CE)
    xs = [-0.86, 0.86]
    rows = (-0.56, 0.0, 0.56)
    pos = []
    while len(pos) < 3:
        u = float(rng.uniform(-0.55, 0.55))
        if not pos or abs(u - pos[-1]) > 0.34:
            pos.append(u)
    sw = 0.065
    for x in np.linspace(xs[0], xs[1], 9):
        big = abs(x) < 1e-6 or abs(abs(x) - 0.86) < 1e-6
        pen.line((x, -0.86), (x, -0.86 + (0.13 if big else 0.08)), pen.T, 0.95, cap="butt")
    for v, u in zip(rows, pos):
        track = S_capsule(pen.p(xs[0], v), pen.p(xs[1], v), sw * pen.k)
        pen.stroke(track, pen.M * 0.85)
        knob = S_box(*pen.p(u, v), 0.115 * pen.k, 0.19 * pen.k, 0, 0.045 * pen.k)
        grip = S_box(*pen.p(u, v), 0.016 * pen.k, 0.10 * pen.k)
        pen.fill(knob - grip)
    if not pen.icon:
        pct = int(round((pos[1] - xs[0]) / (xs[1] - xs[0]) * 100))
        pen.leader((pos[1] + 0.12, 0.0), (1.10, 0.34), "SET %d%%" % pct)
        pen.dim((xs[0], 0.56), (xs[1], 0.56), 0.52, "0\u2013100%")


def em_hazard(pen):
    tri = [(0.0, -0.86), (0.98, 0.84), (-0.98, 0.84)]
    rr = 0.10
    outer = pen.SP(inset_convex(tri, rr)).grow(rr * pen.k)
    inner = outer.grow(-0.17 * pen.k)
    pen.hatch(outer - inner, pitch=pen.hs * 0.9)
    pen.stroke(outer)
    pen.stroke(inner, pen.M * 0.8)
    pen.fill(pen.SP([(-0.095, -0.36), (0.095, -0.36), (0.062, 0.30), (-0.062, 0.30)]).grow(0.01 * pen.k))
    pen.fill(pen.SC((0, 0.50), 0.088))
    if not pen.icon:
        pen.angle((-0.98, 0.84), 120.0, 180.0, 0.42, "60\u00b0", ext=(0.10, 0.12), tr=0.62)
        pen.dim((-0.98, 0.84), (0.98, 0.84), 0.30, "1" + THIN + "960")
        pen.leader((0.49, -0.01), (1.02, -0.62), "ISO 7010")


def _rot(v, deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return (v[0] * c - v[1] * s, v[0] * s + v[1] * c)


def em_spanner(pen):
    A, B = (-0.56, 0.56), (0.50, -0.50)
    d = np.array(B) - np.array(A)
    d = d / np.linalg.norm(d)
    s = _rot(d, -15.0)
    k = pen.k
    pa, pb = pen.p(*A), pen.p(*B)
    handle = S_capsule(pa, pb, 0.115 * k)
    jaw = pen.SC(B, 0.34)
    ring = pen.SC(A, 0.27)
    ang_s = math.degrees(math.atan2(s[1], s[0]))
    slot = S_box(pb[0] + s[0] * 0.36 * k, pb[1] + s[1] * 0.36 * k, 0.40 * k, 0.15 * k, ang_s) \
        | S_circle(pb[0], pb[1], 0.15 * k)
    ang_d = math.degrees(math.atan2(d[1], d[0]))
    hexh = [(A[0] + 0.155 * math.cos(math.radians(ang_d + 30 + 60 * i)),
             A[1] + 0.155 * math.sin(math.radians(ang_d + 30 + 60 * i))) for i in range(6)]
    body = (handle | jaw | ring) - slot - pen.SP(hexh)
    pen.hatch(body, angle=-15)
    if not pen.icon:
        pen.centre((A[0] - d[0] * 0.42, A[1] - d[1] * 0.42), (B[0] + d[0] * 0.80, B[1] + d[1] * 0.80))
        pen.centre(B, (B[0] + s[0] * 0.82, B[1] + s[1] * 0.82))
    pen.stroke(body)
    nut_c = (B[0] + s[0] * 0.05, B[1] + s[1] * 0.05)
    Rh = 0.15 / math.cos(math.radians(30))
    nut = [(nut_c[0] + Rh * math.cos(math.radians(ang_s + 90 + 60 * i)),
            nut_c[1] + Rh * math.sin(math.radians(ang_s + 90 + 60 * i))) for i in range(6)]
    pen.stroke(pen.SP(nut).grow(-0.012 * k), pen.M * 0.7)
    pen.circle(nut_c, 0.075, pen.T * 1.2)
    if not pen.icon:
        a0 = math.degrees(math.atan2(s[1], s[0]))
        a1 = math.degrees(math.atan2(d[1], d[0]))
        pen.angle(B, min(a0, a1), max(a0, a1), 0.66, "15\u00b0", tr=0.86)
        pen.leader((-0.56 + 0.10, 0.56 + 0.20), (-1.30, 1.02), "S 24")


def em_flange(pen):
    R, bore, face, pcd, hole = 0.90, 0.30, 0.50, 0.70, 0.085
    pen.hatch(pen.SC((0, 0), face) - pen.SC((0, 0), bore))
    for a, b in (((-1.08, 0), (1.08, 0)), ((0, -1.08), (0, 1.08))):
        pen.centre(a, b)
    pen.circle((0, 0), pcd, pen.T, 0.9, dash="centre")
    pen.circle((0, 0), R)
    pen.circle((0, 0), face, pen.M * 0.8)
    pen.circle((0, 0), bore, pen.M)
    for i in range(6):
        a = math.radians(30 + 60 * i)
        pen.circle((pcd * math.cos(a), pcd * math.sin(a)), hole, pen.M)
    if not pen.icon:
        a = math.radians(-30)
        pen.leader((pcd * math.cos(a) + 0.06, pcd * math.sin(a) - 0.06), (1.08, -0.82), "6\u00d7 \u00d8" + "18")
        pen.dim((-R, 0), (R, 0), 1.18, "\u00d8" + "180")


def _ell_pts(c, rx, ry, ang, n=44):
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts = []
    for i in range(n):
        t = 2.0 * math.pi * i / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        pts.append((c[0] + x * ca - y * sa, c[1] + x * sa + y * ca))
    return pts


def em_paw(pen):
    """Taming & Breeding: a paw print - hatched three-lobed main pad with four
    toe pads on an arc, drafted like the other parts."""
    hub = (0.0, 0.24)
    pad = (pen.SP(_ell_pts((0.0, 0.20), 0.40, 0.26, 0.0)) | pen.SC((0.0, 0.30), 0.30)
           | pen.SC((-0.25, 0.40), 0.21) | pen.SC((0.25, 0.40), 0.21))
    toes = []
    for a in (-152.0, -112.0, -68.0, -28.0):
        r = 0.66 if a in (-112.0, -68.0) else 0.60
        c = (hub[0] + r * math.cos(math.radians(a)), hub[1] + r * math.sin(math.radians(a)))
        toes.append((c, pen.SP(_ell_pts(c, 0.135, 0.185, a + 90.0))))
    pen.hatch(pad)
    if not pen.icon:
        pen.centre((0.0, -0.80), (0.0, 0.86))
    pen.stroke(pad)
    for c, t in toes:
        pen.stroke(t, pen.M)
    if not pen.icon:
        pen.dim((-0.46, 0.61), (0.46, 0.61), 0.30, "92")
        pen.angle(hub, -152.0, -28.0, 0.98, "124°", tr=1.18)
        pen.leader(toes[3][0], (1.04, 0.05), "4× TOE PAD")


EMBLEMS = {"house": em_house, "shield": em_shield, "gem": em_gem, "bowl": em_bowl,
           "crate": em_crate, "gear": em_gear, "sliders": em_sliders, "hazard": em_hazard,
           "spanner": em_spanner, "flange": em_flange, "paw": em_paw}


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def seed_for(mod):
    key = str(mod.get("folder") or mod.get("name") or "mod")
    return int.from_bytes(hashlib.sha256(key.encode("utf-8")).digest()[:8], "big")


def fmt_int(n):
    """Data values use comma thousands (1,364) so players read one number;
    the drawn dimensions keep the drafting thin space."""
    return "{:,}".format(int(n))


def clean_version(v):
    v = str(v or "").strip()
    v = re.sub(r"^[vV]\s*", "", v)
    return v or "1.0"


def to_int(v):
    try:
        return max(0, int(float(v)))
    except (TypeError, ValueError):
        return 0


def zones(ly, w, h, trim, frame, nx, ny, label=None, op=0.6):
    """ISO 5457 style zone ticks + centring marks between trim and frame."""
    x0, y0, x1, y1 = frame, frame, w - frame, h - frame
    for i in range(1, nx):
        x = x0 + (x1 - x0) * i / nx
        centre = abs(x - w / 2) < 1
        for ya, yb in ((trim, frame), (h - frame, h - trim)):
            line(ly, (x, ya), (x, yb), 2.0 if centre else 1.0, 0.95 if centre else op)
    for j in range(1, ny):
        y = y0 + (y1 - y0) * j / ny
        centre = abs(y - h / 2) < 1
        for xa, xb in ((trim, frame), (w - frame, w - trim)):
            line(ly, (xa, y), (xb, y), 2.0 if centre else 1.0, 0.95 if centre else op)
    if label is not None:
        T = label
        cy_top, cy_bot = (trim + frame) / 2, h - (trim + frame) / 2
        for i in range(nx):
            x = x0 + (x1 - x0) * (i + 0.5) / nx
            for cy in (cy_top, cy_bot):
                T.draw(ly, x, cy + T.cap / 2, str(i + 1), op, "center")
        for j in range(ny):
            y = y0 + (y1 - y0) * (j + 0.5) / ny
            for cx in ((trim + frame) / 2, w - (trim + frame) / 2):
                T.draw(ly, cx, y + T.cap / 2, "ABCDEFGH"[j], op, "center")


# --------------------------------------------------------------------------
# ICON 256 x 256
# --------------------------------------------------------------------------
def render_icon(mod, path):
    W = H = 256
    info = category_info(mod.get("category"))
    rng = np.random.default_rng(seed_for(mod))
    paper = make_paper(W, H, rng)
    ly = Layer(W, H)

    TRIM, FR, FW = 4.5, 11.5, 3.0
    inner = (13, 13, 243, 243)
    G = grid_cov(W, H, inner, 8, 32, 0.065, 0.13)
    rect(ly, TRIM, TRIM, W - TRIM, H - TRIM, 1.0, 0.5)
    rect(ly, FR, FR, W - FR, H - FR, FW, 1.0)
    zones(ly, W, H, TRIM, FR, 4, 4, None, 0.55)

    # title strip
    ys = 173.5
    line(ly, (13, ys), (243, ys), 3.0, 1.0)
    tab_x1 = 47.0
    line(ly, (tab_x1, ys + 1.5), (tab_x1, 243), 2.0, 1.0)

    # emblem (the category "part")
    pen = Pen(ly, 128, 93, 63, "icon", rng, seed=seed_for(mod))
    EMBLEMS[info["emblem"]](pen)

    # drawing number (short form of the name)
    code = short_form(mod.get("name")).replace("-", "\u2013")
    x0, x1 = tab_x1 + 1, 243
    T, lines, lp = fit_block(code, x1 - x0 - 22, 243 - (ys + 1.5) - 20, 64, 26, 700,
                             max_lines=1, wmin=70, track=0.02, kern=True, cond_cost=0.004)
    cy = (ys + 1.5 + 243) / 2 + 3.5
    T.draw(ly, (x0 + x1) / 2, cy + T.cap / 2, lines[0], 1.0, "center")
    lab = Type(7.5, 400, 82, track=0.12)
    lab.draw(ly, x0 + 6, ys + 6 + lab.cap, "DWG NO.", 0.7)
    lab.draw(ly, x1 - 6, ys + 6 + lab.cap, "REV " + clean_version(mod.get("version")), 0.7, "right")

    # colour tag (category) - solid ink tab at the head of the title strip
    tab = np.zeros((H, W), np.float32)
    tab[int(ys + 2):243, 13:int(tab_x1 - 1)] = 1.0
    tex = smooth_noise(rng, W, H, 6, 6)
    tab = tab * np.clip(0.94 + 0.05 * tex, 0.86, 1.0)
    tl = Layer(W, H)                      # category code, lettered up the tab
    text_rotated(tl, (13 + tab_x1 - 1) / 2, (ys + 243) / 2 + 1, info["code"], Type(17, 700, 80, track=0.08), 90)

    ink = ink_texture(ly.coverage(), rng)
    img = composite(paper, [(G, INK), (ink, INK), (tab, info["rgb"]), (tl.coverage() * 0.85, TAB_INK)])
    img.save(path)
    return img


# --------------------------------------------------------------------------
# BANNER 768 x 256
# --------------------------------------------------------------------------
def render_banner(mod, path):
    W, H = 768, 256
    info = category_info(mod.get("category"))
    rng = np.random.default_rng(seed_for(mod) ^ 0x5EED)
    paper = make_paper(W, H, rng)
    ly = Layer(W, H)

    TRIM, FR = 4.5, 15.0
    G = grid_cov(W, H, (16, 16, 752, 240), 8, 40, 0.06, 0.12)
    G[:, 301:] *= 0.55          # the title block is the clean, lettered zone
    rect(ly, TRIM, TRIM, W - TRIM, H - TRIM, 1.0, 0.5)
    rect(ly, FR, FR, W - FR, H - FR, 2.0, 1.0)
    zones(ly, W, H, TRIM, FR, 8, 4, Type(7.5, 400, 80), 0.6)

    # ---- title block -----------------------------------------------------
    TB = 300.0
    r1, r2 = 140.5, 192.5
    line(ly, (TB, 16), (TB, 240), 2.0, 1.0)
    line(ly, (TB + 1, r1), (752, r1), 1.0, 0.95)
    line(ly, (TB + 1, r2), (752, r2), 1.0, 0.95)
    lab = Type(8.5, 400, 82, track=0.10)

    def label(x, y, s):
        lab.draw(ly, x + 6, y + 5 + lab.cap, s, 0.72)

    name = typeset(mod.get("name") or "Untitled").upper()
    label(TB, 16, "TITLE")
    proj = "ICARUS \u00b7 MOD SERIES"
    lab.draw(ly, 752 - 6, 16 + 5 + lab.cap, proj, 0.72, "right")
    T, lines, lp = fit_block(name, 752 - TB - 30, r1 - 16 - 30, 46, 20, 600, max_lines=3,
                             wmin=76, track=0.01, kern=True)
    block_h = T.cap + (len(lines) - 1) * lp
    top = 16 + 22 + (r1 - 16 - 22 - 8 - block_h) / 2
    y = top + T.cap
    for l in lines:
        T.draw(ly, TB + 15, y, l, 1.0)
        y += lp

    label(TB, r1, "DESCRIPTION")
    tag = typeset(mod.get("tagline") or "")
    if tag:
        Tt, tl, tlp = fit_block(tag, 752 - TB - 30, r2 - r1 - 24, 18, 11, 390, max_lines=2,
                                wmin=80, pitch=1.75, line_cost=0.22)
        bh = Tt.cap + (len(tl) - 1) * tlp
        y = r1 + 16 + (r2 - r1 - 16 - bh) / 2 + Tt.cap
        for l in tl:
            Tt.draw(ly, TB + 15, y, l, 0.95)
            y += tlp

    entries, tables = to_int(mod.get("entries")), to_int(mod.get("tables"))
    cells = [("DWG NO.", short_form(mod.get("name")).replace("-", "\u2013"), 104),
             ("REV", clean_version(mod.get("version")), 70)]
    if entries > 0:
        cells += [("ENTRIES", fmt_int(entries), 92), ("TABLES", str(tables) if tables else "\u2013", 66)]
    else:
        cells += [("TYPE", "PAK ONLY", 158)]
    author = typeset(mod.get("author") or "AgentKush")
    cells += [("DRAWN", author, None)]

    def value_type(val, cw, smin):
        Tv = Type(19, 600, 100, kern=True)
        wd = 100
        while Tv.width(val) > cw - 16 and wd > 72:
            wd -= 4
            Tv = Type(19, 600, wd, kern=True)
        s = 19
        while Tv.width(val) > cw - 16 and s > smin:
            s -= 1
            Tv = Type(s, 600, wd, kern=True)
        return Tv, Tv.width(val) <= cw - 16

    # A long author (e.g. "CritFail (Updated by AgentKush)") first takes width back
    # from the other cells - each keeps room for its label and value - and then
    # wraps onto two lines; it never drops below 12 px or runs over a rule.
    a_lines, T_auth = [author], None
    rest = 752 - TB - sum(c[2] for c in cells if c[2])
    T_auth, ok = value_type(author, rest, 15)
    if not ok:
        T19 = Type(19, 600, 100, kern=True)
        cells = [(lb, val, max(52.0, lab.width(lb) + 14, T19.width(val) + 16) if cw else None)
                 for lb, val, cw in cells]
        rest = 752 - TB - sum(c[2] for c in cells if c[2])
        T_auth, ok = value_type(author, rest, 15)
        if not ok:
            words, best = author.split(), None
            for i in range(1, len(words)):
                l1, l2 = " ".join(words[:i]), " ".join(words[i:])
                for s in range(17, 11, -1):
                    T2 = Type(s, 600, 92, kern=True)
                    if max(T2.width(l1), T2.width(l2)) <= rest - 16:
                        cand = (s, -abs(T2.width(l1) - T2.width(l2)), [l1, l2], T2)
                        if best is None or cand[:2] > best[:2]:
                            best = cand
                        break
            if best:
                T_auth, a_lines = best[3], best[2]

    x = TB
    used = sum(c[2] for c in cells if c[2])
    for i, (lb, val, cw) in enumerate(cells):
        cw = cw if cw else (752 - TB - used)
        if i:
            line(ly, (x + 0.5, r2 + 0.5), (x + 0.5, 240), 1.0, 0.95)
        label(x, r2, lb)
        if lb == "DRAWN":
            if len(a_lines) == 1:
                T_auth.draw(ly, x + 7, 240 - 10, author, 1.0)
            else:                                  # two lines, the second on the row's baseline
                b2 = 240 - 8
                b1 = b2 - T_auth.cap - max(3.5, 0.32 * T_auth.cap)
                T_auth.draw(ly, x + 7, b1, a_lines[0], 1.0)
                T_auth.draw(ly, x + 7, b2, a_lines[1], 1.0)
        else:
            Tv, _ = value_type(val, cw, 11)
            Tv.draw(ly, x + 7, 240 - 10, val, 1.0)
        x += cw

    # ---- drawing field -----------------------------------------------------
    field = (16, 16, TB - 1, 240)
    pen = Pen(ly, 174, 140, 62, "banner", rng, field, seed=seed_for(mod))
    EMBLEMS[info["emblem"]](pen)
    note = Type(7.5, 400, 82, track=0.12)
    note.draw(ly, 24, 233, "DIMENSIONS IN MM · DO NOT SCALE", 0.6)

    # ---- stamp (category) ------------------------------------------------------
    # placed top-left of the drawing field; if it would touch the drawn part
    # (4px margin), it flattens and/or shifts before it may overlap.
    base = stamp_cov(info["label"], info["code"], rng)
    tilt = float(rng.uniform(2.5, 5.0))
    drawn = ly.coverage()[:, :int(TB) - 2] > 0.12
    keep = np.asarray(Image.fromarray((drawn * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9))) > 0
    stamp = None
    for ang, (sx, sy) in ((tilt, (22, 20)), (tilt * 0.5, (22, 20)), (0.0, (20, 19)), (0.0, (19, 17))):
        st = rotate_cov(base, ang)
        cand = np.zeros((H, W), np.float32)
        paste_cov(cand, st, sx, sy)
        if stamp is None:
            stamp = cand
        if not np.any((cand[:, :keep.shape[1]] > 0.15) & keep):
            stamp = cand
            break

    ink = ink_texture(ly.coverage(), rng)
    img = composite(paper, [(G, INK), (ink, INK), (stamp * 0.95, info["rgb"])])
    img.save(path)
    return img


def render(mod, icon_path, banner_path):
    """Render the 256x256 icon and the 768x256 banner for one mod."""
    for pth in (icon_path, banner_path):
        d = os.path.dirname(os.path.abspath(pth))
        os.makedirs(d, exist_ok=True)
    render_icon(mod, icon_path)
    render_banner(mod, banner_path)


# --------------------------------------------------------------------------
# script entry: samples + previews + contact sheet
# --------------------------------------------------------------------------
def contact_sheet(mods, out_dir, path):
    gap, margin = 22, 34
    lab = Type(13, 500, 90, track=0.04)
    W = max(768, 5 * 256 + 4 * gap) + 2 * margin
    rows_h = 30 + 5 * (20 + 256 + gap) + (20 + 256 + gap) + (20 + 64) + margin
    sheet = Image.new("RGB", (W, rows_h + margin), (128, 128, 128))
    d = ImageDraw.Draw(sheet)
    head = Type(16, 600, 100, track=0.06)
    ink = (24, 24, 24)
    y = margin
    head.draw(d, margin, y + head.cap, "BLUEPRINT \u2014 DRAWING-OFFICE IDENTITY \u00b7 5 SAMPLE SHEETS",
              fill=ink)
    y += 30
    for m in mods:
        f = m["folder"]
        lab.draw(d, margin, y + 13, "BANNER 768\u00d7256 \u00b7 " + f, fill=ink)
        sheet.paste(Image.open(os.path.join(out_dir, "banner_%s.png" % f)), (margin, y + 20))
        y += 20 + 256 + gap
    x = margin
    for m in mods:
        f = m["folder"]
        lab.draw(d, x, y + 13, "ICON 256 \u00b7 " + f[:26], fill=ink)
        sheet.paste(Image.open(os.path.join(out_dir, "icon_%s.png" % f)), (x, y + 20))
        x += 256 + gap
    y += 20 + 256 + gap
    x = margin
    for m in mods:
        f = m["folder"]
        lab.draw(d, x, y + 13, "64 px \u00b7 " + f[:24], fill=ink)
        sheet.paste(Image.open(os.path.join(out_dir, "icon64_%s.png" % f)), (x, y + 20))
        x += 256 + gap
    sheet.save(path)


def main(argv):
    src = argv[1] if len(argv) > 1 else SAMPLES_JSON
    out = argv[2] if len(argv) > 2 else HERE
    with open(src, encoding="utf-8") as fh:
        mods = json.load(fh)
    os.makedirs(out, exist_ok=True)
    for m in mods:
        f = m["folder"]
        ip, bp = os.path.join(out, "icon_%s.png" % f), os.path.join(out, "banner_%s.png" % f)
        render(m, ip, bp)
        ic = Image.open(ip)
        ic.resize((64, 64), Image.LANCZOS).save(os.path.join(out, "icon64_%s.png" % f))
        ic.resize((128, 128), Image.LANCZOS).save(os.path.join(out, "icon128_%s.png" % f))
        print("rendered", f, "->", short_form(m.get("name")))
    contact_sheet(mods, out, os.path.join(out, "sheet.png"))
    print("sheet.png written")


if __name__ == "__main__":
    main(sys.argv)
