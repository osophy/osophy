"""Generate the pixel-art water profile images.

Usage: python3 scripts/gen_profile.py
Edit CONFIG below, then re-run. Writes assets/*.svg and preview.html.
Font covers A-Z 0-9 and  , ' ! . - : > _ / + ? ( ) · *  (* draws a heart).
"""
import base64
import math
import os

CONFIG = {
    "title": "HI, I'M JACE",
    "tagline": "DATA · CODE · DANCE",
    "handle": "OSOPHY",
    "footer": "THANKS FOR DIVING IN *",
    "footer_hint": "PRESS START",
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
P = 5  # wave grid: one pixel-art pixel = 5 svg units
W = 1000

# palette
DEEP, BLUE, MID, LIGHT, PALE, FOAM = "#0B4FB3", "#1565D8", "#2E86DE", "#6EC1FF", "#D6ECFF", "#FFFFFF"
HEART, LAMP = "#FF6B9A", "#22C7A0"

FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".####", "#....", "#....", "#..##", "#...#", "#...#", ".###."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    ",": ["...", "...", "...", "...", "...", ".#.", "#.."],
    "'": [".#.", ".#.", "#..", "...", "...", "...", "..."],
    "!": ["#", "#", "#", "#", "#", ".", "#"],
    ".": [".", ".", ".", ".", ".", ".", "#"],
    ":": [".", "#", ".", ".", ".", "#", "."],
    "·": [".", ".", ".", "#", ".", ".", "."],
    "-": ["...", "...", "...", "###", "...", "...", "..."],
    "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
    ">": ["#...", ".#..", "..#.", "...#", "..#.", ".#..", "#..."],
    "_": [".....", ".....", ".....", ".....", ".....", ".....", "#####"],
    "/": ["....#", "...#.", "...#.", "..#..", ".#...", ".#...", "#...."],
    "?": [".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."],
    "(": [".#", "#.", "#.", "#.", "#.", "#.", ".#"],
    ")": ["#.", ".#", ".#", ".#", ".#", ".#", "#."],
    "*": [".....", ".#.#.", "#####", "#####", ".###.", "..#..", "....."],
    " ": ["...", "...", "...", "...", "...", "...", "..."],
}

# Ocean sprites. Two-frame ones are lists of frames.
HEAD = ["....oooooo.....", "...obbbbbbo....", "..obwwbbbbbo..."]
OCTOPUS = [
    HEAD + [
        "..obwbbbbmbo..o",
        "..obbbbbbbbo.ob",
        "..obkwbbkwbo.ob",
        "..obkkbbkkboob.",
        "..obbbbbbbbob..",
        "..obmbbbbmbo...",
        ".obbobbobbobo..",
        ".ob.ob..ob.ob..",
        "ob..ob..ob..bo.",
        "o...ob...ob..o.",
        "....oo...oo....",
    ],
    HEAD + [
        "..obwbbbbmbo...",
        "..obbbbbbbbo...",
        "..obkwbbkwbo...",
        "..obkkbbkkbo...",
        "..obbbbbbbbooo.",
        "..obmbbbbmbbbbo",
        ".obbobbobbooo..",
        "..ob.ob.ob.ob..",
        "..ob..bo.bo..bo",
        ".o...bo...bo..o",
        "....oo...oo....",
    ],
]
OCTOPUS_COLORS = {"o": ("#B83B6B", 1), "b": ("#FF8FB1", .95), "m": ("#E56B95", 1),
                  "w": (FOAM, 1), "k": ("#3A1530", 1)}

FISH = ["..oooo.o", ".obbbboo", "okbbbbbo", ".obbbboo", "..oooo.o"]
FISH_COLORS = {"o": ("#D9822B", 1), "b": ("#FFB547", 1), "k": ("#3A1530", 1)}

JELLY = [
    ["..ooo..", ".obbbo.", "obwbbbo", "obbbbbo", "ooooooo", ".o.o.o.", "o.o.o.o", ".o.o.o."],
    ["..ooo..", ".obbbo.", "obwbbbo", "obbbbbo", "ooooooo", "o.o.o.o", ".o.o.o.", "o.o.o.o"],
]
JELLY_COLORS = {"o": ("#7F77DD", .9), "b": ("#C9B6FF", .7), "w": (FOAM, .95)}

CRAB = [
    ["oo.......oo", "oro.....oro", ".oo.k.k.oo.", "..ooooooo..", ".orrrrrrro.", "o.orrrrro.o", ".o.o.o.o.o."],
    ["oo.......oo", "oro.....oro", ".oo.k.k.oo.", "..ooooooo..", ".orrrrrrro.", ".oorrrrroo.", "o.o.o.o.o.o"],
]
CRAB_COLORS = {"o": ("#A3271F", 1), "r": ("#FF6B5A", 1), "k": ("#3A1530", 1)}

STARFISH = ["....o....", "...oyo...", "...oyo...", "ooooyoooo", "oyyywyyyo", ".oyyyyyo.",
            "..oyoyo..", ".oyo.oyo.", ".oo...oo."]
SHELL = ["...ooo...", ".oopwpoo.", "opwpwpwpo", "opwpwpwpo", ".opwpwpo.", "..ooooo.."]
SHELL_COLORS = {"o": ("#C77D93", 1), "p": ("#FFD1DC", 1), "w": (FOAM, 1)}
SEA_COLORS = {"o": ("#D9822B", 1), "y": ("#FFB547", 1), "w": ("#FFE2A8", 1)}

SKY = [("#E4F3FF", 1), ("#EAF6FF", 1), ("#F0F9FF", 1), ("#E6F5FF", 1), ("#DCF0FF", 1)]
CLOUD = ["...####...", ".########.", "##########", ".########."]

STYLE = """
@keyframes flow{from{transform:translateX(0)}to{transform:translateX(-1000px)}}
@keyframes flowR{from{transform:translateX(-1000px)}to{transform:translateX(0)}}
@keyframes rise{0%{transform:translateY(0);opacity:0}10%{opacity:1}80%{opacity:1}100%{transform:translateY(-120px);opacity:0}}
@keyframes blink{0%,100%{opacity:0}50%{opacity:1}}
@keyframes cur{0%,49.9%{opacity:1}50%,100%{opacity:0}}
@keyframes fa{0%,49.9%{opacity:1}50%,100%{opacity:0}}
@keyframes fb{0%,49.9%{opacity:0}50%,100%{opacity:1}}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
.cl{animation:flow 80s steps(200) infinite}
.w1{animation:flow 20s steps(200) infinite}
.w2{animation:flowR 14s steps(200) infinite}
.w3{animation:flow 9s steps(200) infinite}
.bub{animation:rise steps(24) infinite}
.spk{animation:blink steps(2) infinite}
.cur{animation:cur 1s infinite}
.fa{animation:fa .8s infinite}
.fb{animation:fb .8s infinite}
.bob{animation:bob .8s steps(2) infinite}
@keyframes swimL{from{transform:translateX(1100px)}to{transform:translateX(-100px)}}
@keyframes drift{0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}
@keyframes walk{0%,100%{transform:translateX(0)}50%{transform:translateX(260px)}}
.swim{animation:swimL steps(240) infinite}
.drift{animation:drift 3s steps(3) infinite}
.walk{animation:walk 10s steps(52) infinite}
.sw{animation:fa 1.2s infinite}.sw2{animation:fb 1.2s infinite}
"""


# ---------- primitives (absolute svg coords) ----------

def rect(x, y, w, h):
    return f"M{x} {y}h{w}v{h}h{-w}z"


def path(d, fill, op=None):
    o = f' fill-opacity="{op}"' if op is not None else ""
    return f'<path d="{d}" fill="{fill}"{o}/>' if d else ""


def glyph(ch):
    return FONT.get(ch, FONT["?"])


def text_width(text, s):
    if not text:
        return 0
    return (sum(len(glyph(c)[0]) + 1 for c in text.upper()) - 1) * s


def text_d(text, x, y, s, rows=range(7)):
    d = []
    for ch in text.upper():
        g = glyph(ch)
        for r in rows:
            for c, v in enumerate(g[r]):
                if v == "#":
                    d.append(rect(x + c * s, y + r * s, s, s))
        x += (len(g[0]) + 1) * s
    return "".join(d)


def text(t, x, y, s, fill, op=None):
    return path(text_d(t, x, y, s), fill, op)


def text_hearts(t, x, y, s, fill):
    """Text with '*' drawn as a pink heart."""
    out, cx = [], x
    for ch in t.upper():
        out.append(text(ch, cx, y, s, HEART if ch == "*" else fill))
        cx += (len(glyph(ch)[0]) + 1) * s
    return "".join(out)


def sprite(frame, x, y, s, colors):
    by = {k: [] for k in colors}
    for r, row in enumerate(frame):
        for c, v in enumerate(row):
            if v in by:
                by[v].append(rect(x + c * s, y + r * s, s, s))
    return "".join(path("".join(p), colors[k][0], colors[k][1]) for k, p in by.items())


def two_frames(frames, x, y, s, colors):
    return (f'<g class="fa">{sprite(frames[0], x, y, s, colors)}</g>'
            f'<g class="fb">{sprite(frames[1], x, y, s, colors)}</g>')


def octopus(x, y, s):
    return two_frames(OCTOPUS, x, y, s, OCTOPUS_COLORS)


def seaweed(x, bottom, rows, s, phase):
    """Swaying kelp: two frames with opposite sine offsets."""
    out = []
    for cls, ph in (("sw", phase), ("sw2", phase + math.pi)):
        d = hi = ""
        for r in range(rows):
            dx = round(math.sin(r / 2.2 + ph) * (r / rows) * 1.6)
            y = bottom - (r + 1) * s
            d += rect(x + dx * s, y, 2 * s, s)
            if r % 3 == 1:
                hi += rect(x + dx * s, y, s, s)
        out.append(f'<g class="{cls}">{path(d, "#1F9E6E", .9)}{path(hi, "#7EE0A8")}</g>')
    return "".join(out)


def pixel_box(x, y, w, h, s, fill, border=None):
    """Rectangle with notched (pixel-rounded) corners."""
    out = ""
    if border:
        out += path(rect(x + s, y, w - 2 * s, h) + rect(x, y + s, w, h - 2 * s), border)
        x, y, w, h = x + s, y + s, w - 2 * s, h - 2 * s
    out += path(rect(x + s, y, w - 2 * s, h) + rect(x, y + s, w, h - 2 * s), fill)
    return out


def bubble(x, y, s):
    ring = [".##.", "#w.#", "#..#", ".##."]
    d = "".join(rect(x + c * s, y + r * s, s, s) for r, row in enumerate(ring) for c, v in enumerate(row) if v == "#")
    w = "".join(rect(x + c * s, y + r * s, s, s) for r, row in enumerate(ring) for c, v in enumerate(row) if v == "w")
    return path(d, "#8FD3FF", .85) + path(w, FOAM)


def sparkle(x, y, s):
    return path(rect(x, y - s, s, 3 * s) + rect(x - s, y, 3 * s, s), FOAM)


def banded(gid, top, bottom, stops):
    """Hard-stop gradient -> pixel colour bands."""
    out = [f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="0" y1="{top}" x2="0" y2="{bottom}">']
    n = len(stops)
    for i, (col, op) in enumerate(stops):
        for off in (i / n, (i + 1) / n):
            out.append(f'<stop offset="{off:.3f}" stop-color="{col}" stop-opacity="{op}"/>')
    out.append("</linearGradient>")
    return "".join(out)


# ---------- water ----------

def heights(base, amp, period_cols, cols, phase=0.0):
    return [round(base - amp * math.sin(2 * math.pi * c / period_cols + phase)) for c in range(cols)]


def stepped(hs, bottom, s=P, x0=0):
    d = f"M{x0} {bottom}"
    for c, h in enumerate(hs):
        d += f"V{h*s}H{x0+(c+1)*s}"
    return d + f"V{bottom}Z"


def crest(hs, s=P, dy=0, x0=0):
    return "".join(rect(x0 + c * s, (h + dy) * s, s, s) for c, h in enumerate(hs))


def cloud(cx, cy):
    d = "".join(rect((cx + c) * P, (cy + r) * P, P, P) for r, row in enumerate(CLOUD) for c, v in enumerate(row) if v == "#")
    sh = "".join(rect((cx + c) * P, (cy + len(CLOUD)) * P, P, P) for c, v in enumerate(CLOUD[-1]) if v == "#")
    return path(sh, "#BFE0FF") + path(d, FOAM)


def sky(H, clouds=()):
    out = f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    if clouds:
        out += '<g class="cl">' + "".join(cloud(x + off, y) for off in (0, W // P) for x, y in clouds) + "</g>"
    return out


WATER_BACK = [("#6EC1FF", .5), ("#4AA8F5", .42), ("#2E8BE6", .34), ("#1E6FD9", .26), ("#1259C3", .18)]
WATER_MID = [("#8FD3FF", .55), ("#5CB8FF", .45), ("#3A9BF0", .38), ("#1E6FD9", .28), ("#0B4FB3", .18)]
WATER_FRONT = [("#9AD8FF", .7), ("#5CB8FF", .58), ("#3A9BF0", .48), ("#1E6FD9", .4), ("#1259C3", .3), ("#0B4FB3", .2)]


def svg(w, h, defs, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'shape-rendering="crispEdges">\n<defs>{defs}</defs>\n<style>{STYLE}</style>\n{body}\n</svg>\n')


# ---------- images ----------

def banner(cfg):
    H = 300
    cols, rows = 2 * W // P, H // P
    back = heights(33, 3, 100, cols)
    mid = heights(37, 2, 40, cols, 1.2)
    front = heights(42, 2, 25, cols, 2.4)
    defs = (banded("sky", 0, H, SKY) + banded("gBack", 150, H, WATER_BACK)
            + banded("gMid", 175, H, WATER_MID) + banded("gFront", 200, H, WATER_FRONT))

    bubbles = "".join(
        f'<g class="bub" style="animation-duration:{d}s;animation-delay:-{dl}s">{bubble(x * P, y * P, P)}</g>'
        for x, y, d, dl in [(20, 55, 5.5, 0), (46, 56, 4.4, 1.6), (70, 54, 6.0, 2.5), (98, 56, 5.0, .7),
                            (118, 55, 4.6, 3.2), (140, 56, 5.8, 1.9), (172, 55, 4.8, .3), (190, 56, 6.4, 2.8)])
    sparkles = "".join(
        f'<g class="spk" style="animation-duration:2.4s;animation-delay:-{dl}s">{sparkle(x * P, y * P, P)}</g>'
        for x, y, dl in [(30, 44, 0), (75, 46, .9), (122, 43, 1.7), (150, 47, .4), (185, 44, 1.2)])

    tx, ty = 60, 35
    title = (text(cfg["title"], tx + P, ty + P, P, BLUE, .28) + text(cfg["title"], tx, ty, P, "#2E9BF0")
             + path(text_d(cfg["title"], tx, ty, P, rows=[0]), "#9AD8FF"))
    tag = text(cfg["tagline"], tx, 86, 3, MID)
    handle = "> " + cfg["handle"]
    hl = text(handle, tx, 116, 3, BLUE) + f'<g class="cur">{text("_", tx + text_width(handle + " ", 3), 116, 3, BLUE)}</g>'

    fish = "".join(
        f'<g class="swim" style="animation-duration:{d}s;animation-delay:-{dl}s">{sprite(FISH, 0, y, s, FISH_COLORS)}</g>'
        for y, s, d, dl in [(232, 4, 16, 0), (250, 3, 21, 6), (262, 4, 18, 11), (276, 3, 24, 3)])
    jellies = "".join(
        f'<g class="drift" style="animation-delay:-{dl}s">{two_frames(JELLY, x, y, 4, JELLY_COLORS)}</g>'
        for x, y, dl in [(250, 236, 0), (560, 250, 1.5)])
    kelp = "".join(seaweed(x, H, rows, P, ph) for x, rows, ph in
                   [(30, 12, 0), (45, 8, 1), (440, 10, 2), (690, 13, .5), (705, 9, 1.7), (960, 11, 2.4)])

    body = f'''{sky(H, [(40, 4), (110, 9), (175, 3)])}
<g class="w1">{path(stepped(back, H), "url(#gBack)")}</g>
<g class="w2">{path(stepped(mid, H), "url(#gMid)")}{path(crest(mid), FOAM, .35)}</g>
<g class="bob">{octopus(800, 140, P)}</g>
<g class="w3">{path(stepped(front, H), "url(#gFront)")}{path(crest(front), FOAM, .85)}{path(crest(front, dy=1), "#D6F0FF", .6)}</g>
{kelp}{jellies}{fish}{bubbles}{sparkles}{title}{tag}{hl}'''
    return svg(W, 300, defs, body)



# Section / project icons. o=outline b=water w=shine m=deep p=pale y=gold r=red g=green
ICON_COLORS = {"o": (BLUE, 1), "b": (LIGHT, 1), "w": (FOAM, 1), "m": (MID, 1), "p": (PALE, 1),
               "y": ("#FFB547", 1), "r": (HEART, 1), "g": (LAMP, 1)}

ICONS = {
    "shell": (SHELL, SHELL_COLORS),
    "starfish": (STARFISH, SEA_COLORS),
    "bottle": ([
        "...yy...", "...oo...", "..obbo..", "..obbo..", ".obwwbo.", "obwbbbbo",
        "obpppbbo", "obpppbbo", "obwbbbbo", "obbbbbbo", ".oooooo.",
    ], None),
    "note": [
        "....oooooooo", "....obbbbbbo", "....oooooooo", "....ob....ob", "....ob....ob", "....ob....ob",
        "....ob....ob", "..ooob..ooob", ".obbbb.obbbb", "obwbbbobwbbb", "obbbbo.obbbo", ".oooo...ooo.",
    ],
    "window": [
        "oooooooooooo", "ommmmmmmmmmo", "omrmymgmmmmo", "oooooooooooo", "owwwwwwwwwwo", "owbbbbwwwwwo",
        "owwwwwwwwwwo", "owppppppppwo", "owppppppwwwo", "owppppwwwwwo", "owwwwwwwwwwo", "oooooooooooo",
    ],
    "chart": [
        "o...........", "o........oo.", "o.......obbo", "o.......obbo", "o....oo.obbo", "o...obbooobo",
        "o...obbobbbo", "o.oo.obbobbo", "oobbooobbobo", "oobbobobbobo", "oobbobobbobo", "oooooooooooo",
    ],
    "globe": [
        "...oooooo...", "..obbgbbbbo.", ".obgggbbbbbo", "obbggbbbggbo", "obbbgbbbggbo", "obwbbbbbgbbo",
        "obwbbbbbbbbo", "obbggbbbbbbo", ".obgggbbbbo.", "..obggbbbo..", "...oooooo...",
    ],
    "tomato": [
        "....g..g....", ".....gg.....", "...oogggoo..", "..orrrrrrro.", ".orwrrrrrrro", ".orwrrrrrrro",
        ".orrrrrrrrro", ".orrrrrrrrro", "..orrrrrrro.", "...ooooooo..",
    ],
}


def icon(spec, s=2):
    rows, colors = spec if isinstance(spec, tuple) else (spec, None)
    w, h = max(len(r) for r in rows) * s, len(rows) * s
    return svg(w, h, "", sprite(rows, 0, 0, s, colors or ICON_COLORS))


def octopus_icon(s=2):
    return svg(15 * s, 14 * s, "", octopus(0, 0, s))


def footer(cfg):
    H = 220
    cols = 2 * W // P
    back = heights(30, 2, 100, cols)
    front = heights(35, 2, 40, cols, 1.5)
    defs = (banded("sky", 0, H, SKY) + banded("fb", 140, H, WATER_BACK) + banded("ff", 165, H, WATER_FRONT))
    msg = cfg["footer"]
    mw = text_width(msg, P)
    hint = cfg["footer_hint"]
    hw = text_width(hint, 3)
    sand = "".join(rect(c * P, (41 - (1 if math.sin(c / 6) > .6 else 0)) * P, P, H) for c in range(W // P))
    dots = "".join(rect(c * P, 42 * P + (c % 3) * P, P, P) for c in range(3, W // P, 7))
    seabed = (path(sand, "#F3D9A4") + path(dots, "#D9B77A")
              + "".join(seaweed(x, 41 * P, rows, P, ph) for x, rows, ph in [(60, 9, 0), (75, 6, 1.4), (900, 10, .8), (915, 7, 2)])
              + sprite(STARFISH, 180, 41 * P - 25, 3, SEA_COLORS)
              + sprite(SHELL, 760, 41 * P - 15, 3, SHELL_COLORS)
              + sprite(SHELL, 520, 41 * P - 12, 2, SHELL_COLORS)
              + f'<g class="walk">{two_frames(CRAB, 300, 41 * P - 28, 4, CRAB_COLORS)}</g>')
    body = f'''{sky(H, [(8, 3), (182, 2)])}
{text(msg, (W - mw) // 2 + P, 46, P, BLUE, .28)}{text_hearts(msg, (W - mw) // 2, 41, P, "#2E9BF0")}
<g class="cur">{text(hint, (W - hw) // 2, 100, 3, MID)}</g>
<g class="w2">{path(stepped(back, H), "url(#fb)")}</g>
<g class="w3">{path(stepped(front, H), "url(#ff)")}{path(crest(front), FOAM, .85)}</g>
{seabed}'''
    return svg(W, H, defs, body)


def preview(files):
    enc = lambda c: "data:image/svg+xml;base64," + base64.b64encode(c.encode()).decode()
    big = "".join(f'<img class="big" src="{enc(files[n])}"/>' for n in ["banner", "footer"])
    small = "".join(f'<figure><img src="{enc(c)}"/><figcaption>{n}</figcaption></figure>'
                    for n, c in files.items() if n.startswith("icons/"))
    return f'''<!doctype html>
<meta charset="utf-8" />
<title>Profile preview</title>
<style>
  body {{ margin: 0; font-family: -apple-system, sans-serif; }}
  section {{ padding: 24px; }}
  .light {{ background: #ffffff; }}
  .dark {{ background: #0d1117; color: #e6edf3; }}
  img {{ image-rendering: pixelated; }}
  .big {{ width: 100%; max-width: 1000px; display: block; margin: 0 auto 12px; }}
  .icons {{ display: flex; gap: 20px; flex-wrap: wrap; max-width: 1000px; margin: 0 auto; }}
  figure {{ margin: 0; text-align: center; font-size: 11px; }}
  figure img {{ height: 48px; display: block; margin: 0 auto 4px; }}
  p {{ max-width: 1000px; margin: 0 auto 8px; font-size: 13px; opacity: .6; }}
</style>
<section class="light"><p>GitHub light</p>{big}<div class="icons">{small}</div></section>
<section class="dark"><p>GitHub dark</p>{big}<div class="icons">{small}</div></section>
'''


if __name__ == "__main__":
    os.makedirs(ASSETS, exist_ok=True)
    files = {"banner": banner(CONFIG), "footer": footer(CONFIG), "icons/octopus": octopus_icon()}
    files.update({f"icons/{n}": icon(rows) for n, rows in ICONS.items()})
    os.makedirs(os.path.join(ASSETS, "icons"), exist_ok=True)
    for name, content in files.items():
        with open(os.path.join(ASSETS, f"{name}.svg"), "w") as f:
            f.write(content)
    with open(os.path.join(ROOT, "preview.html"), "w") as f:
        f.write(preview(files))
    print("wrote", ", ".join(f"{n}.svg" for n in files), "and preview.html")
