"""LTE 프레임 구조 그림 3종 (TS 36.211 §4, §6.10.1)

1. lte_frame_hierarchy : 무선 프레임 → 서브프레임 → 슬롯 → OFDM 심볼 계층
2. lte_tdd_configs     : TDD UL/DL Configuration 0–6
3. lte_rb_crs          : 1 RB pair 리소스 그리드 위의 PDCCH 영역과 CRS(포트 0/1)
"""
from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

import style as s


def box(ax, x, y, w, h, fc, label="", fs=9, ec="#ffffff", lw=1.5, tc=None, bold=False):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs,
                color=tc or s.text_on(fc), fontweight="bold" if bold else "normal")


def zoom(ax, x0, x1, y_top, X0, X1, y_bot):
    """위 행의 [x0,x1] 구간이 아래 행의 [X0,X1]로 확대됨을 나타내는 사다리꼴."""
    ax.add_patch(Polygon([(x0, y_top), (x1, y_top), (X1, y_bot), (X0, y_bot)],
                         closed=True, facecolor=s.EMPTY, edgecolor="none", zorder=0))


def frame_hierarchy():
    fig, ax = plt.subplots(figsize=(11, 5.6))
    s.bare(ax)
    W = 100
    h = 0.75
    rows = [4.6, 3.1, 1.6, 0.1]

    # 1) 무선 프레임 10 ms
    ax.text(-1.5, rows[0] + h / 2, "Radio frame\n10 ms", ha="right", va="center", fontsize=9, color=s.INK2)
    box(ax, 0, rows[0], W, h, s.DL, "One radio frame = 10 subframes = 20 slots  (Tf = 307200·Ts = 10 ms)", fs=10, bold=True)

    # 2) 서브프레임 10개
    ax.text(-1.5, rows[1] + h / 2, "Subframe\n1 ms", ha="right", va="center", fontsize=9, color=s.INK2)
    for i in range(10):
        fc = s.DL if i != 3 else s.CTRL
        box(ax, i * 10, rows[1], 10, h, fc, f"#{i}", fs=9)
    zoom(ax, 0, W, rows[0], 0, W, rows[1] + h)

    # 3) 서브프레임 #3 → 슬롯 2개
    ax.text(-1.5, rows[2] + h / 2, "Slot\n0.5 ms", ha="right", va="center", fontsize=9, color=s.INK2)
    box(ax, 0, rows[2], 50, h, s.CTRL, "Slot 2i  (Tslot = 15360·Ts)", fs=9)
    box(ax, 50, rows[2], 50, h, s.CTRL, "Slot 2i+1", fs=9)
    zoom(ax, 30, 40, rows[1], 0, W, rows[2] + h)

    # 4) 슬롯 → 7 심볼 (Normal CP)
    ax.text(-1.5, rows[3] + h / 2, "OFDM symbol\n(normal CP)", ha="right", va="center", fontsize=9, color=s.INK2)
    # 첫 심볼 CP 160 Ts, 나머지 144 Ts, 유효 심볼 2048 Ts → 슬롯 15360 Ts
    total = 15360
    x = 0.0
    for l in range(7):
        cp = 160 if l == 0 else 144
        cw = cp / total * W
        sw = 2048 / total * W
        box(ax, x, rows[3], cw, h, s.SPECIAL, "", lw=0.8)
        box(ax, x + cw, rows[3], sw, h, s.DL, f"l={l}", fs=8, lw=0.8)
        x += cw + sw
    zoom(ax, 0, 50, rows[2], 0, W, rows[3] + h)

    # 범례
    ax.add_patch(Rectangle((0, -0.75), 2, 0.35, facecolor=s.SPECIAL))
    ax.text(2.8, -0.575, "Cyclic prefix: 160·Ts (l=0), 144·Ts (l=1..6)", va="center", fontsize=8.5, color=s.INK2)
    ax.add_patch(Rectangle((46, -0.75), 2, 0.35, facecolor=s.DL))
    ax.text(48.8, -0.575, "Useful symbol: 2048·Ts = 66.7 µs  (Ts = 1/(15000×2048) s ≈ 32.55 ns)",
            va="center", fontsize=8.5, color=s.INK2)

    ax.set_xlim(-14, W + 1)
    ax.set_ylim(-1.0, rows[0] + h + 0.2)
    s.save(fig, "lte_frame_hierarchy")


# TS 36.211 Table 4.2-2
TDD_CONFIGS = [
    ("0", "5 ms", "DSUUUDSUUU"),
    ("1", "5 ms", "DSUUDDSUUD"),
    ("2", "5 ms", "DSUDDDSUDD"),
    ("3", "10 ms", "DSUUUDDDDD"),
    ("4", "10 ms", "DSUUDDDDDD"),
    ("5", "10 ms", "DSUDDDDDDD"),
    ("6", "5 ms", "DSUUUDSUUD"),
]


def tdd_configs():
    fig, ax = plt.subplots(figsize=(10, 4.4))
    s.bare(ax)
    color = {"D": s.DL, "U": s.UL, "S": s.SPECIAL}
    n = len(TDD_CONFIGS)
    for r, (cfg, period, pattern) in enumerate(TDD_CONFIGS):
        y = n - 1 - r
        ax.text(-0.25, y + 0.4, f"Config {cfg}", ha="right", va="center", fontsize=9.5, fontweight="bold")
        ax.text(-2.25, y + 0.4, period, ha="right", va="center", fontsize=8.5, color=s.INK2)
        for i, sf in enumerate(pattern):
            box(ax, i, y, 1, 0.8, color[sf], sf, fs=10, bold=True)
        ax.text(10.3, y + 0.4, f"DL:UL = {pattern.count('D')}+{pattern.count('S')}S : {pattern.count('U')}",
                va="center", fontsize=8.5, color=s.INK2)
    for i in range(10):
        ax.text(i + 0.5, n + 0.15, f"{i}", ha="center", va="bottom", fontsize=8.5, color=s.INK2)
    ax.text(5, n + 0.65, "Subframe number", ha="center", fontsize=9, color=s.INK2)
    ax.text(-2.25, n + 0.15, "Switch\nperiod", ha="right", va="bottom", fontsize=8, color=s.INK2)
    ax.set_xlim(-4.2, 13.6)
    ax.set_ylim(-0.3, n + 1.2)
    s.save(fig, "lte_tdd_configs")


def rb_crs(v_shift: int = 0, cfi: int = 3):
    """1 RB pair (12 subcarriers × 14 symbols, normal CP) — CRS 포트 0/1과 PDCCH 영역.

    TS 36.211 §6.10.1.2:  k = 6m + (v + v_shift) mod 6
      port 0: l=0 → v=0,  l=4 → v=3
      port 1: l=0 → v=3,  l=4 → v=0
    """
    fig, ax = plt.subplots(figsize=(9, 5.6))
    s.bare(ax)
    grid = {}
    for slot in range(2):
        for l, v0, v1 in ((0, 0, 3), (4, 3, 0)):
            sym = slot * 7 + l
            for m in range(2):
                grid[(sym, 6 * m + (v0 + v_shift) % 6)] = ("R0", s.RS)
                grid[(sym, 6 * m + (v1 + v_shift) % 6)] = ("R1", s.ALT)

    for sym in range(14):
        for k in range(12):
            if (sym, k) in grid:
                label, fc = grid[(sym, k)]
            elif sym < cfi:
                label, fc = "", s.CTRL
            else:
                label, fc = "", s.DL
            box(ax, sym, k, 1, 1, fc, label, fs=8, lw=1.2, bold=True)

    # 슬롯 경계
    ax.plot([7, 7], [-0.2, 12.2], color=s.INK, linewidth=2)
    for sym in range(14):
        ax.text(sym + 0.5, -0.45, f"{sym % 7}", ha="center", va="top", fontsize=8, color=s.INK2)
    ax.text(3.5, -1.45, "Slot 0  (l = 0…6)", ha="center", fontsize=9, color=s.INK2)
    ax.text(10.5, -1.45, "Slot 1  (l = 0…6)", ha="center", fontsize=9, color=s.INK2)
    for k in range(12):
        ax.text(-0.3, k + 0.5, f"{k}", ha="right", va="center", fontsize=8, color=s.INK2)
    ax.text(-1.4, 6, "Subcarrier k (12 = 1 RB, 180 kHz)", rotation=90, ha="center", va="center", fontsize=9, color=s.INK2)
    ax.annotate("", xy=(cfi, 12.55), xytext=(0, 12.55),
                arrowprops=dict(arrowstyle="<->", color=s.CTRL, lw=1.4))
    ax.text(cfi / 2, 12.75, f"PDCCH region (CFI={cfi})", ha="center", va="bottom", fontsize=8.5, color=s.CTRL)

    # 범례
    items = [(s.RS, "R0", "CRS antenna port 0"), (s.ALT, "R1", "CRS antenna port 1"),
             (s.CTRL, "", "Control region (PCFICH/PHICH/PDCCH)"), (s.DL, "", "PDSCH")]
    for i, (fc, lab, txt) in enumerate(items):
        x = 15.0
        y = 10.5 - i * 1.4
        box(ax, x, y, 1, 1, fc, lab, fs=8, bold=True)
        ax.text(x + 1.4, y + 0.5, txt, va="center", fontsize=8.5)
    ax.text(15.0, 3.6, f"v_shift = PCI mod 6 = {v_shift}\nOther PCIs shift CRS\nalong frequency",
            fontsize=8.5, color=s.INK2, va="top")

    ax.set_xlim(-2, 24)
    ax.set_ylim(-1.9, 13.4)
    ax.set_aspect("equal")
    s.save(fig, "lte_rb_crs")


if __name__ == "__main__":
    s.setup()
    frame_hierarchy()
    tdd_configs()
    rb_crs()
