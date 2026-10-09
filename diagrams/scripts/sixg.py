"""6G 그림

1. imt2030_scenarios : ITU-R M.2160 IMT-2030 사용 시나리오 6개와 공통 원칙 4개
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge

import style as s

SCENARIOS = [
    ("Immersive\nCommunication", "(extends eMBB)", s.DL),
    ("Hyper Reliable &\nLow-Latency", "(extends URLLC)", s.UL),
    ("Massive\nCommunication", "(extends mMTC)", s.SYNC),
    ("Ubiquitous\nConnectivity", "NEW", s.SPECIAL),
    ("AI and\nCommunication", "NEW", s.CTRL),
    ("Integrated Sensing\nand Communication", "NEW", s.ALT),
]
ASPECTS = ["Sustainability", "Connecting the unconnected", "Ubiquitous intelligence",
           "Security · privacy · resilience"]


def imt2030_scenarios():
    fig, ax = plt.subplots(figsize=(8.5, 8.5))
    s.bare(ax)
    n = len(SCENARIOS)
    for i, (name, tag, color) in enumerate(SCENARIOS):
        th0 = 90 - (i + 1) * 360 / n
        th1 = th0 + 360 / n
        ax.add_patch(Wedge((0, 0), 4.8, th0 + 0.8, th1 - 0.8, width=2.7, facecolor=color,
                           edgecolor=s.SURFACE))
        mid = np.radians((th0 + th1) / 2)
        r = 3.45
        ax.text(r * np.cos(mid), r * np.sin(mid) + 0.18, name, ha="center", va="center", fontsize=8.5,
                fontweight="bold", color=s.text_on(color))
        ax.text(r * np.cos(mid), r * np.sin(mid) - 0.5, tag, ha="center", va="center", fontsize=8,
                color=s.text_on(color))
    ax.add_patch(Circle((0, 0), 2.1, facecolor=s.EMPTY, edgecolor=s.GRID))
    ax.text(0, 0.35, "IMT-2030", ha="center", va="center", fontsize=15, fontweight="bold")
    ax.text(0, -0.35, "(6G)", ha="center", va="center", fontsize=11, color=s.INK2)
    for i, a in enumerate(ASPECTS):
        th = np.radians(45 + i * 90)
        ax.text(5.9 * np.cos(th), 5.9 * np.sin(th), a, ha="center", va="center", fontsize=8.5, color=s.INK2,
                rotation=0, bbox=dict(boxstyle="round,pad=0.3", facecolor=s.SURFACE, edgecolor=s.GRID))
    ax.add_patch(Circle((0, 0), 5.05, facecolor="none", edgecolor=s.MUTED, lw=1, ls="--"))
    ax.text(0, -6.9, "Inner ring: 6 usage scenarios (3 extended from IMT-2020, 3 new)\n"
            "Outer labels: 4 overarching aspects that apply to all scenarios",
            ha="center", fontsize=8.5, color=s.INK2)
    ax.set_xlim(-7.6, 7.6)
    ax.set_ylim(-7.5, 6.8)
    ax.set_aspect("equal")
    s.save(fig, "imt2030_scenarios")


if __name__ == "__main__":
    s.setup()
    imt2030_scenarios()
