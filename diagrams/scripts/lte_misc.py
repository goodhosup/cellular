"""LTE 구조·절차 그림

1. lte_protocol_stack : 사용자 평면 / 제어 평면 프로토콜 스택 (UE–eNB–S-GW/MME)
2. lte_ca_types       : 캐리어 집성 3가지 유형
3. lte_drx            : C-DRX 동작 (onDuration, inactivity timer, short/long cycle)
4. lte_event_a3       : 측정 이벤트 A3 (offset, hysteresis, time-to-trigger)
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

import style as s


def layer(ax, x, y, w, h, label, fc):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
                                facecolor=fc, edgecolor=s.SURFACE, linewidth=2))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=8.5,
            color=s.text_on(fc), fontweight="bold")


def stack(ax, x, layers, w=1.9, h=0.62):
    for i, (label, fc) in enumerate(reversed(layers)):
        layer(ax, x, i * h, w, h * 0.94, label, fc)


def protocol_stack():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(11, 7.6))
    L2 = s.DL
    PHY = s.CTRL
    RRC = s.SYNC
    NAS = s.UL
    TN = s.MUTED
    for ax in (a1, a2):
        s.bare(ax)
    # 사용자 평면
    up_ue = [("Application / IP", s.EMPTY), ("PDCP", L2), ("RLC", L2), ("MAC", L2), ("PHY", PHY)]
    up_enb_l = [("PDCP", L2), ("RLC", L2), ("MAC", L2), ("PHY", PHY)]
    up_enb_r = [("GTP-U", TN), ("UDP", TN), ("IP", TN), ("L2 / L1", TN)]
    up_sgw = [("GTP-U", TN), ("UDP", TN), ("IP", TN), ("L2 / L1", TN)]
    stack(a1, 0, up_ue)
    stack(a1, 3.4, up_enb_l)
    stack(a1, 5.4, up_enb_r)
    stack(a1, 8.8, up_sgw)
    a1.text(0.95, 3.35, "UE", ha="center", fontsize=10, fontweight="bold")
    a1.text(5.35, 3.35, "eNB", ha="center", fontsize=10, fontweight="bold")
    a1.text(9.75, 3.35, "S-GW / P-GW", ha="center", fontsize=10, fontweight="bold")
    a1.annotate("", xy=(3.35, 0.3), xytext=(1.95, 0.3), arrowprops=dict(arrowstyle="<->", color=s.INK2))
    a1.text(2.65, 0.45, "Uu (LTE-Uu)", ha="center", fontsize=8.5, color=s.INK2)
    a1.annotate("", xy=(8.75, 0.3), xytext=(7.35, 0.3), arrowprops=dict(arrowstyle="<->", color=s.INK2))
    a1.text(8.05, 0.45, "S1-U", ha="center", fontsize=8.5, color=s.INK2)
    a1.text(11.4, 1.6, "User plane\n\nIP packets ride in a\nGTP-U tunnel per\nEPS bearer between\neNB and S-GW", fontsize=9,
            va="center", color=s.INK2)
    a1.set_xlim(-0.3, 14)
    a1.set_ylim(-0.2, 3.8)
    # 제어 평면
    cp_ue = [("NAS", NAS), ("RRC", RRC), ("PDCP", L2), ("RLC", L2), ("MAC", L2), ("PHY", PHY)]
    cp_enb_l = [("RRC", RRC), ("PDCP", L2), ("RLC", L2), ("MAC", L2), ("PHY", PHY)]
    cp_enb_r = [("S1AP", s.SPECIAL), ("SCTP", TN), ("IP", TN), ("L2 / L1", TN)]
    cp_mme = [("NAS", NAS), ("S1AP", s.SPECIAL), ("SCTP", TN), ("IP", TN), ("L2 / L1", TN)]
    stack(a2, 0, cp_ue)
    stack(a2, 3.4, cp_enb_l)
    stack(a2, 5.4, cp_enb_r)
    stack(a2, 8.8, cp_mme)
    a2.text(0.95, 3.95, "UE", ha="center", fontsize=10, fontweight="bold")
    a2.text(5.35, 3.95, "eNB", ha="center", fontsize=10, fontweight="bold")
    a2.text(9.75, 3.95, "MME", ha="center", fontsize=10, fontweight="bold")
    a2.annotate("", xy=(8.75, 3.4), xytext=(1.95, 3.4), arrowprops=dict(arrowstyle="<->", color=NAS, ls="--"))
    a2.text(5.35, 3.55, "NAS (transparent to eNB)", ha="center", fontsize=8.5, color=NAS)
    a2.annotate("", xy=(3.35, 0.3), xytext=(1.95, 0.3), arrowprops=dict(arrowstyle="<->", color=s.INK2))
    a2.text(2.65, 0.45, "Uu", ha="center", fontsize=8.5, color=s.INK2)
    a2.annotate("", xy=(8.75, 0.3), xytext=(7.35, 0.3), arrowprops=dict(arrowstyle="<->", color=s.INK2))
    a2.text(8.05, 0.45, "S1-MME", ha="center", fontsize=8.5, color=s.INK2)
    a2.text(11.4, 1.9, "Control plane\n\nRRC ends in the eNB,\nNAS ends in the MME;\nNAS rides inside RRC\nover the air", fontsize=9,
            va="center", color=s.INK2)
    a2.set_xlim(-0.3, 14)
    a2.set_ylim(-0.2, 4.3)
    s.save(fig, "lte_protocol_stack")


def ca_types():
    fig, axes = plt.subplots(3, 1, figsize=(10, 4.6))
    cases = [
        ("Intra-band contiguous", [(1.0, 2.0, "CC1"), (3.0, 2.0, "CC2")], [(0.5, 5.2, "Band A")]),
        ("Intra-band non-contiguous", [(0.8, 1.6, "CC1"), (4.0, 1.6, "CC2")], [(0.5, 5.2, "Band A")]),
        ("Inter-band", [(0.8, 1.8, "CC1"), (7.4, 1.8, "CC2")], [(0.5, 2.4, "Band A"), (7.1, 2.4, "Band B")]),
    ]
    for ax, (title, ccs, bands) in zip(axes, cases):
        s.bare(ax)
        for x, w, lab in bands:
            ax.add_patch(Rectangle((x, 0), w, 1.1, facecolor=s.EMPTY, edgecolor=s.GRID))
            ax.text(x + w / 2, 1.25, lab, ha="center", fontsize=8.5, color=s.INK2)
        for i, (x, w, lab) in enumerate(ccs):
            fc = s.DL if i == 0 else s.SYNC
            ax.add_patch(Rectangle((x, 0.1), w, 0.9, facecolor=fc, edgecolor=s.SURFACE, lw=1.5))
            ax.text(x + w / 2, 0.55, lab + (" (PCell)" if i == 0 else " (SCell)"), ha="center", va="center",
                    fontsize=8.5, color="#fff", fontweight="bold")
        ax.text(-0.3, 0.55, title, ha="right", va="center", fontsize=9.5, fontweight="bold")
        ax.set_xlim(-4.2, 10)
        ax.set_ylim(-0.2, 1.6)
    axes[-1].annotate("", xy=(10, -0.15), xytext=(0.5, -0.15), arrowprops=dict(arrowstyle="->", color=s.INK2))
    axes[-1].text(10, -0.05, "frequency", ha="right", fontsize=8.5, color=s.INK2)
    s.save(fig, "lte_ca_types")


def drx():
    fig, ax = plt.subplots(figsize=(11.5, 3.6))
    s.bare(ax)
    # 단위: ms. long cycle 40, onDuration 4, inactivity 20, short cycle 10 (shortCycleTimer = 2)
    T = 160
    OND = 4
    ax.plot([0, T], [0, 0], color=s.INK2, lw=1)
    for x in (0, 40, 120):
        ax.add_patch(Rectangle((x, 0), OND, 1.0, facecolor=s.DL, edgecolor="none"))
    ax.text(2, 1.15, "onDuration", ha="center", fontsize=8.5, color=s.DL)
    pd = 42
    ax.add_patch(Rectangle((pd, 0), 1, 1.6, facecolor=s.RS, edgecolor="none"))
    ax.text(pd + 0.5, 1.75, "PDCCH (new data)", ha="center", fontsize=8.5, color=s.RS)
    ax.add_patch(Rectangle((pd + 1, 0), 20, 1.0, facecolor=s.SPECIAL, edgecolor="none"))
    ax.text(pd + 11, 0.5, "drx-InactivityTimer\n(20 ms, restarts on\nevery new PDCCH)", ha="center", va="center", fontsize=8)
    for x in (70, 80):
        ax.add_patch(Rectangle((x, 0), OND, 1.0, facecolor=s.SYNC, edgecolor="none"))
    ax.text(77, 1.15, "short cycle ×2", ha="center", fontsize=8.5, color=s.SYNC)
    ax.annotate("", xy=(40, -0.25), xytext=(0, -0.25), arrowprops=dict(arrowstyle="<->", color=s.INK2))
    ax.text(20, -0.6, "long DRX cycle (40 ms)", ha="center", fontsize=8.5, color=s.INK2)
    ax.annotate("", xy=(80, -0.25), xytext=(70, -0.25), arrowprops=dict(arrowstyle="<->", color=s.SYNC))
    ax.text(75, -0.6, "10 ms", ha="center", fontsize=8.5, color=s.SYNC)
    ax.annotate("", xy=(120, -0.25), xytext=(84, -0.25), arrowprops=dict(arrowstyle="<->", color=s.INK2))
    ax.text(102, -0.6, "drxShortCycleTimer expired\n→ back to long cycle", ha="center", va="top", fontsize=8.5,
            color=s.INK2)
    ax.text(T + 2, 0.5, "Active time = UE monitors PDCCH\nOutside active time = receiver off (sleep)",
            va="center", fontsize=8.5, color=s.INK2)
    for t in range(0, T + 1, 20):
        ax.text(t, -1.25, f"{t}", ha="center", fontsize=7.5, color=s.MUTED)
    ax.text(T / 2, -1.7, "time (ms) — example: long cycle 40 ms, onDuration 4 ms, inactivity 20 ms, short cycle 10 ms",
            ha="center", fontsize=8.5, color=s.INK2)
    ax.set_xlim(-3, T + 45)
    ax.set_ylim(-1.95, 2.1)
    s.save(fig, "lte_drx")


def event_a3():
    fig, ax = plt.subplots(figsize=(10, 4.4))
    t = np.linspace(0, 10, 500)
    serving = -80 - 2.2 * t
    neigh = -102 + 1.6 * t
    off, hys = 3, 1
    ax.plot(t, serving, color=s.DL, lw=2, label="Serving cell RSRP (Mp)")
    ax.plot(t, neigh, color=s.UL, lw=2, label="Neighbour cell RSRP (Mn)")
    ax.plot(t, serving + off + hys, color=s.DL, lw=1.2, ls="--", label="Mp + Off + Hys")
    t_enter = t[np.argmax(neigh > serving + off + hys)]
    ttt = 1.28
    ax.axvspan(t_enter, t_enter + ttt, color=s.SPECIAL, alpha=0.35, lw=0)
    ax.axvline(t_enter, color=s.MUTED, lw=1)
    ax.axvline(t_enter + ttt, color=s.RS, lw=1.5)
    ax.text(t_enter + ttt / 2, -79, "time-\nto-\ntrigger", ha="center", va="top", fontsize=8.5)
    ax.text(t_enter + ttt + 0.15, -85, "Measurement\nReport sent", fontsize=8.5, color=s.RS, va="top")
    ax.text(t_enter - 0.15, -112, "entering\ncondition met", ha="right", fontsize=8.5, color=s.INK2)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("RSRP (dBm)")
    ax.set_ylim(-115, -76)
    ax.set_xlim(0, 10)
    ax.grid(True, color=s.GRID, lw=0.5)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(frameon=False, fontsize=8.5, loc="lower left")
    ax.set_title("Event A3: Mn + Ofn + Ocn − Hys > Mp + Ofp + Ocp + Off   (here Off = 3 dB, Hys = 1 dB, TTT = 1280 ms)",
                 fontsize=9, color=s.INK2)
    s.save(fig, "lte_event_a3")


if __name__ == "__main__":
    s.setup()
    protocol_stack()
    ca_types()
    drx()
    event_a3()
