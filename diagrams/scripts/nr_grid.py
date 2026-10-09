"""NR 물리계층·빔·스펙트럼 그림 (TS 38.211 / 38.213 / 38.214 / 38.101)

1. nr_point_a          : Point A, 공통 RB 격자(15/30 kHz), 캐리어, BWP, SSB 위치
2. nr_bwp              : BWP 전환 (시간–주파수)
3. nr_slot_formats     : TDD 패턴 예 (DDDSU, DDDDDDDSUU, FR2 DDDSU) + 특수 슬롯 심볼 구성
4. nr_coreset          : CORESET의 CCE→REG 매핑 (비인터리브 vs 인터리브)
5. nr_pdsch_dmrs       : PDSCH 매핑 Type A/B와 DMRS 위치, DMRS 설정 Type 1/2 CDM 그룹
6. nr_beam_sweep       : SSB 빔 스윕 (공간 + 시간)
7. nr_ssb_ro           : SSB ↔ RACH occasion 연동
8. nr_k0k1k2           : K0 / K1 / K2 슬롯 타이밍
9. nr_bands            : 주요 NR 밴드와 FR1/FR2/FR3 범위
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Wedge, Polygon

import style as s


def box(ax, x, y, w, h, fc, label="", fs=8.5, ec="#ffffff", lw=1.0, tc=None, bold=False):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs,
                color=tc or s.text_on(fc), fontweight="bold" if bold else "normal")


def arrow(ax, x0, x1, y, text, color=s.INK2, fs=8.5, above=True):
    ax.annotate("", xy=(x1, y), xytext=(x0, y), arrowprops=dict(arrowstyle="<->", color=color, lw=1.1))
    ax.text((x0 + x1) / 2, y + (0.12 if above else -0.12), text, ha="center", va="bottom" if above else "top",
            fontsize=fs, color=color)


def point_a():
    fig, ax = plt.subplots(figsize=(11.5, 5.0))
    s.bare(ax)
    # 단위: 15 kHz RB 하나 = 1
    N = 48
    # 15 kHz CRB 격자
    for k in range(N):
        box(ax, k, 3.0, 1, 0.5, s.EMPTY, ec=s.GRID, lw=0.6)
        if k % 8 == 0:
            ax.text(k + 0.5, 3.6, f"{k}", ha="center", fontsize=7.5, color=s.INK2)
    ax.text(-0.6, 3.25, "CRB (15 kHz)", ha="right", va="center", fontsize=9)
    # 30 kHz CRB 격자 (RB 폭 2배)
    for k in range(N // 2):
        box(ax, 2 * k, 2.2, 2, 0.5, s.EMPTY, ec=s.GRID, lw=0.6)
        if k % 4 == 0:
            ax.text(2 * k + 1, 2.8, f"{k}", ha="center", fontsize=7.5, color=s.INK2)
    ax.text(-0.6, 2.45, "CRB (30 kHz)", ha="right", va="center", fontsize=9)
    # 캐리어 (30 kHz, offsetToCarrier = 3 RB → 6 단위)
    car0, car_len = 6, 36
    box(ax, car0, 1.2, car_len, 0.6, s.DL, "carrier (SCS 30 kHz, 18 RB shown)", fs=9, bold=True)
    # BWP
    bwp0, bwp_len = 14, 16
    box(ax, bwp0, 0.3, bwp_len, 0.6, s.SYNC, "active BWP", fs=8.5, bold=True)
    # SSB (20 RB @30 kHz = 40 단위는 너무 크므로 15 kHz SSB 20 RB = 20 단위로 예시)
    ssb0 = 20.5
    box(ax, ssb0, 4.3, 20, 0.6, s.CTRL, "SSB (20 RB, SCS 15 kHz example)", fs=8.5, bold=True)
    # Point A
    ax.plot([0, 0], [-0.4, 5.3], color=s.RS, lw=2)
    ax.text(0, 5.4, "Point A\n(absoluteFrequencyPointA)", ha="center", va="bottom", fontsize=9, color=s.RS,
            fontweight="bold")
    ax.annotate("", xy=(car0, 1.5), xytext=(0, 1.5), arrowprops=dict(arrowstyle="<->", color=s.INK2, lw=1.1))
    ax.text(-0.4, 1.5, "offsetToCarrier = 3\n(30 kHz RBs)", ha="right", va="center", fontsize=8.5, color=s.INK2)
    arrow(ax, car0, bwp0, -0.05, "RB_start = 4", above=False)
    arrow(ax, 0, 20, 5.0, "offsetToPointA = 20 RB (15 kHz units)")
    ax.annotate("", xy=(20.5, 4.25), xytext=(20, 4.25), arrowprops=dict(arrowstyle="-", color=s.INK2))
    ax.text(21.0, 3.95, "k_SSB (subcarrier offset)", fontsize=8, color=s.INK2)
    ax.annotate("", xy=(N + 1.2, -0.3), xytext=(-0.4, -0.3), arrowprops=dict(arrowstyle="->", color=s.INK2))
    ax.text(N + 1.2, -0.55, "frequency", ha="right", fontsize=8.5, color=s.INK2)
    ax.text(N + 2, 3.0,
            "• Point A = centre of subcarrier 0\n  of CRB 0 for every numerology\n"
            "• All CRB grids start at Point A,\n  so different SCS grids nest\n"
            "• Carrier and BWP are offsets\n  on the CRB grid of their SCS",
            fontsize=8.5, va="center", color=s.INK2)
    ax.set_xlim(-8, N + 17)
    ax.set_ylim(-1.3, 6.4)
    s.save(fig, "nr_point_a")


def bwp():
    fig, ax = plt.subplots(figsize=(11, 4.0))
    s.bare(ax)
    # 시간 0–20 (슬롯), 주파수 0–10
    ax.add_patch(Rectangle((0, 0), 20, 10, facecolor=s.EMPTY, edgecolor=s.GRID))
    ax.text(-0.3, 5, "carrier\n100 MHz", ha="right", va="center", fontsize=9)
    segs = [(0, 6, 3, 2, s.SYNC, "BWP#1  20 MHz\n(power saving)"),
            (6, 8, 0, 10, s.DL, "BWP#2  100 MHz\n(high throughput)"),
            (14, 6, 3, 2, s.SYNC, "BWP#1")]
    for x, w, y, h, fc, lab in segs:
        ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=s.SURFACE, lw=2))
        ax.text(x + w / 2, y + h / 2, lab, ha="center", va="center", fontsize=9, color="#fff", fontweight="bold")
    ax.annotate("DCI with BWP indicator\n(data burst arrives)", xy=(6, 8), xytext=(2.5, 8.6), fontsize=8.5,
                color=s.INK2, arrowprops=dict(arrowstyle="->", color=s.INK2))
    ax.annotate("bwp-InactivityTimer expires\n→ back to default BWP", xy=(14, 4), xytext=(15.2, 7.5), fontsize=8.5,
                color=s.INK2, arrowprops=dict(arrowstyle="->", color=s.INK2))
    ax.annotate("", xy=(20.5, -0.4), xytext=(0, -0.4), arrowprops=dict(arrowstyle="->", color=s.INK2))
    ax.text(20.5, -0.8, "time", ha="right", fontsize=8.5, color=s.INK2)
    ax.text(10, -1.4, "Only one DL BWP and one UL BWP are active at a time per serving cell (up to 4 configured each)",
            ha="center", fontsize=8.5, color=s.INK2)
    ax.set_xlim(-3, 21)
    ax.set_ylim(-1.8, 10.5)
    s.save(fig, "nr_bwp")


def slot_formats():
    fig, ax = plt.subplots(figsize=(11.5, 4.6))
    s.bare(ax)
    color = {"D": s.DL, "U": s.UL, "F": s.SPECIAL}
    rows = [
        ("30 kHz · DDDSU (2.5 ms)", 0.5, "DDDSU" * 2, "D" * 10 + "FF" + "UU"),
        ("30 kHz · DDDDDDDSUU (5 ms)", 0.5, "DDDDDDDSUU", "D" * 6 + "F" * 4 + "UUUU"),
        ("30 kHz · DSUUU (UL heavy, 2.5 ms)", 0.5, "DSUUU" * 2, "D" * 10 + "FF" + "UU"),
        ("120 kHz · DDDSU (0.625 ms)", 0.125, "DDDSU" * 8, "D" * 10 + "FF" + "UU"),
    ]
    W = 50.0  # 5 ms → 50 단위
    for r, (name, slot_ms, pattern, special) in enumerate(rows):
        y = 3 - r
        sw = slot_ms / 5 * W
        ax.text(-0.5, y + 0.3, name, ha="right", va="center", fontsize=9, fontweight="bold")
        for i, c in enumerate(pattern):
            x = i * sw
            if x >= W - 1e-9:
                break
            if c == "S":
                for l, sc in enumerate(special):
                    box(ax, x + l * sw / 14, y, sw / 14, 0.6, color[sc], ec=color[sc], lw=0.2)
                box(ax, x, y, sw, 0.6, "none", ec="#ffffff", lw=0.8)
            else:
                box(ax, x, y, sw, 0.6, color[c], c if sw > 2 else "", fs=8, bold=True, lw=0.8)
    for t in range(6):
        ax.text(t * 10, -0.4, f"{t} ms", ha="center", fontsize=8, color=s.INK2)
    # 특수 슬롯 확대 설명
    for i, (fc, lab) in enumerate([(s.DL, "D = downlink symbol/slot"), (s.SPECIAL, "F = flexible (guard / switching)"),
                                   (s.UL, "U = uplink symbol/slot")]):
        ax.add_patch(Rectangle((W + 2, 3.2 - i * 0.6), 0.9, 0.4, facecolor=fc))
        ax.text(W + 3.2, 3.4 - i * 0.6, lab, va="center", fontsize=8.5)
    ax.text(W + 2, 1.0, "Special slot S shown symbol by symbol\n(e.g. 10D : 2F : 2U, 6D : 4F : 4U)",
            fontsize=8.5, color=s.INK2, va="center")
    ax.set_xlim(-22, W + 20)
    ax.set_ylim(-0.8, 3.9)
    s.save(fig, "nr_slot_formats")


def coreset():
    """CORESET 24 RB × 2 심볼 = 48 REG = 8 CCE. REG 번호는 시간 우선(time-first)."""
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(11.5, 4.8))
    nrb, nsym = 24, 2
    palette = [s.DL, s.UL, s.SYNC, s.SPECIAL, s.ALT, s.CTRL, s.RS, s.MUTED]
    R, L = 2, 6
    nbundle = nrb * nsym // L
    C = nbundle // R

    def f(x):
        c, r = divmod(x, R)
        return (r * C + c) % nbundle

    for ax, inter in ((a1, False), (a2, True)):
        s.bare(ax)
        for cce in range(8):
            bundle = f(cce) if inter else cce
            rb0 = bundle * (L // nsym)
            for rb in range(rb0, rb0 + L // nsym):
                for l in range(nsym):
                    box(ax, rb, l, 1, 1, palette[cce], "", lw=1.0)
                    # PDCCH DMRS: 각 REG의 부반송파 1, 5, 9 → 점으로 표시
                    for k in (1, 5, 9):
                        ax.plot(rb + (k + 0.5) / 12, l + 0.5, "o", ms=1.6, color="#ffffff")
            ax.text(rb0 + (L // nsym) / 2, 2.15, f"CCE{cce}", ha="center", fontsize=8, color=s.INK2)
        ax.text(-0.4, 1, "symbol\n0–1", ha="right", va="center", fontsize=8.5, color=s.INK2)
        ax.set_xlim(-3.5, nrb + 0.5)
        ax.set_ylim(-0.3, 2.7)
        ax.set_title("non-interleaved (CCE j → REG bundle j)" if not inter else
                     f"interleaved, bundle size L=6, R={R}: f(x) = (rC + c) mod {nbundle}", fontsize=9.5,
                     loc="left", color=s.INK2)
    a2.text(nrb / 2, -0.75, "frequency → (1 column = 1 RB = 12 subcarriers; white dots = PDCCH DMRS on subcarriers 1, 5, 9 of each REG)",
            ha="center", fontsize=8.5, color=s.INK2)
    s.save(fig, "nr_coreset")


def pdsch_dmrs():
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.2))
    W = 1.0

    def grid(ax, title, dmrs_syms, dmrs_sc, pdsch_syms, ctrl_syms=(0, 1), cdm2=None):
        for l in range(14):
            for k in range(12):
                fc = s.EMPTY
                if l in ctrl_syms:
                    fc = s.CTRL
                if l in pdsch_syms:
                    fc = s.DL
                if l in dmrs_syms:
                    if k in dmrs_sc:
                        fc = s.RS
                    elif cdm2 and k in cdm2:
                        fc = s.ALT
                    else:
                        fc = s.DL if l in pdsch_syms else fc
                box(ax, l * W, k, W, 1, fc, lw=0.8)
        ax.set_xlim(-0.5, 14.3)
        ax.set_ylim(-1.6, 12.8)
        ax.set_aspect("equal")
        s.bare(ax)
        for l in range(14):
            ax.text(l + 0.5, -0.5, f"{l}", ha="center", fontsize=7, color=s.INK2)
        ax.set_title(title, fontsize=9, color=s.INK)

    grid(axes[0], "Type A, DMRS type 1\npos2 (l0=2) + additional pos1 (l=11)",
         dmrs_syms=(2, 11), dmrs_sc=range(0, 12, 2), pdsch_syms=range(2, 14), cdm2=range(1, 12, 2))
    grid(axes[1], "Type A, DMRS type 2\n(3 CDM groups, 2 shown)",
         dmrs_syms=(2, 11), dmrs_sc=(0, 1, 6, 7), pdsch_syms=range(2, 14), cdm2=(2, 3, 8, 9))
    grid(axes[2], "Type B (mini-slot, 4 symbols)\nDMRS on first PDSCH symbol",
         dmrs_syms=(6,), dmrs_sc=range(0, 12, 2), pdsch_syms=range(6, 10), ctrl_syms=(4, 5),
         cdm2=range(1, 12, 2))
    fig.text(0.5, 0.07,
             "■ blue = PDSCH data   ■ red = DMRS CDM group 0   ■ pink = CDM group 1 (other ports or no data)   "
             "■ purple = CORESET (PDCCH)   — symbol index l along the bottom, subcarrier k (0–11) vertically",
             ha="center", fontsize=8.5, color=s.INK2)
    s.save(fig, "nr_pdsch_dmrs")


def beam_sweep():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 4.6), gridspec_kw={"width_ratios": [1.1, 1]})
    s.bare(a1)
    n = 8
    span = 120
    colors = [s.DL, s.UL, s.SYNC, s.SPECIAL, s.ALT, s.CTRL, s.RS, s.MUTED]
    for i in range(n):
        th0 = 90 - span / 2 + i * span / n
        a1.add_patch(Wedge((0, 0), 9.5, th0 + 0.8, th0 + span / n - 0.8, facecolor=colors[i], alpha=0.85,
                           edgecolor=s.SURFACE))
        mid = np.radians(th0 + span / n / 2)
        a1.text(7.6 * np.cos(mid), 7.6 * np.sin(mid), f"SSB\n#{i}", ha="center", va="center", fontsize=8,
                color=s.text_on(colors[i]), fontweight="bold")
    a1.add_patch(Polygon([(-0.6, -0.8), (0.6, -0.8), (0, 0.4)], facecolor=s.INK))
    a1.text(0, -1.5, "gNB", ha="center", fontsize=9, fontweight="bold")
    ue_th = np.radians(90 - span / 2 + 5.5 * span / n)
    ux, uy = 5.0 * np.cos(ue_th), 5.0 * np.sin(ue_th)
    a1.plot(ux, uy, "s", ms=9, color=s.INK, mec=s.SURFACE)
    a1.text(ux - 0.4, uy + 0.6, "UE", ha="right", fontsize=9, fontweight="bold")
    a1.set_xlim(-10, 10)
    a1.set_ylim(-2, 10)
    a1.set_aspect("equal")
    a1.set_title("space: each SSB index is sent on a different beam", fontsize=9.5, color=s.INK2)
    # 시간 축
    s.bare(a2)
    for i in range(n):
        a2.add_patch(Rectangle((i * 1.1, 2.5), 1.0, 1.0, facecolor=colors[i], edgecolor="none"))
        a2.text(i * 1.1 + 0.5, 3.0, f"#{i}", ha="center", va="center", fontsize=8.5, color=s.text_on(colors[i]),
                fontweight="bold")
    a2.text(4.4, 3.8, "SS burst set within one 5 ms half frame", ha="center", fontsize=9)
    a2.annotate("", xy=(8.8, 2.2), xytext=(0, 2.2), arrowprops=dict(arrowstyle="->", color=s.INK2))
    a2.text(8.8, 1.85, "time", ha="right", fontsize=8.5, color=s.INK2)
    a2.text(0, 1.0, "UE measures all SSBs, picks the strongest (#5),\nthen uses the RACH occasion linked to SSB #5\n"
            "→ gNB learns which beam reaches the UE", fontsize=9, color=s.INK2, va="top")
    a2.set_xlim(-0.5, 9.5)
    a2.set_ylim(-1.0, 4.4)
    s.save(fig, "nr_beam_sweep")


def ssb_ro():
    fig, ax = plt.subplots(figsize=(11.5, 3.4))
    s.bare(ax)
    colors = [s.DL, s.UL, s.SYNC, s.SPECIAL, s.ALT, s.CTRL, s.RS, s.MUTED]
    # 8 SSB, ssb-perRACH-Occasion = 1/2 → SSB 2개 per RO? 여기선 2 SSB per RO, msg1-FDM = 2
    per_ro, fdm = 2, 2
    ro = 0
    for t in range(2):
        for fidx in range(fdm):
            x, y = t * 6, fidx * 1.2
            ax.add_patch(Rectangle((x, y), 5.4, 1.0, facecolor=s.EMPTY, edgecolor=s.GRID))
            ssbs = [ro * per_ro + j for j in range(per_ro)]
            for j, sidx in enumerate(ssbs):
                ax.add_patch(Rectangle((x + 0.2 + j * 2.6, y + 0.15), 2.4, 0.7, facecolor=colors[sidx], edgecolor="none"))
                ax.text(x + 1.4 + j * 2.6, y + 0.5, f"SSB#{sidx}\npreamble {j * 32}–{j * 32 + 31}", ha="center",
                        va="center", fontsize=6.8, color=s.text_on(colors[sidx]), fontweight="bold")
            ax.text(x + 2.7, y + 1.05, f"RO {ro}", ha="center", va="bottom", fontsize=8, color=s.INK2)
            ro += 1
    ax.text(-0.3, 0.5, "f = 0", ha="right", va="center", fontsize=8.5, color=s.INK2)
    ax.text(-0.3, 1.7, "f = 1", ha="right", va="center", fontsize=8.5, color=s.INK2)
    ax.text(2.7, -0.4, "PRACH slot t", ha="center", fontsize=8.5, color=s.INK2)
    ax.text(8.7, -0.4, "PRACH slot t+1", ha="center", fontsize=8.5, color=s.INK2)
    ax.text(12.6, 1.1, "Example: 8 SSBs, ssb-perRACH-Occasion = 2,\nmsg1-FDM = 2, 64 preambles per RO\n\n"
            "SSBs map to ROs in order: preamble index\n→ frequency → time. After one full cycle\n"
            "(association period) the pattern repeats.", fontsize=8.5, va="center", color=s.INK2)
    ax.set_xlim(-1.5, 21.5)
    ax.set_ylim(-0.8, 2.6)
    s.save(fig, "nr_ssb_ro")


def k0k1k2():
    fig, ax = plt.subplots(figsize=(11.5, 3.6))
    s.bare(ax)
    pattern = "DDDSUDDDSU"
    color = {"D": s.DL, "S": s.SPECIAL, "U": s.UL}
    for i, c in enumerate(pattern):
        ax.add_patch(Rectangle((i, 1.0), 0.94, 0.8, facecolor=color[c], alpha=0.25, edgecolor=s.GRID))
        ax.text(i + 0.47, 0.75, f"slot {i}\n{c}", ha="center", va="top", fontsize=8, color=s.INK2)
    # DL: slot 0 PDCCH → PDSCH slot 0 (K0=0) → HARQ-ACK slot 4 (K1=4)
    ax.add_patch(Rectangle((0.02, 1.05), 0.18, 0.7, facecolor=s.CTRL))
    ax.add_patch(Rectangle((0.22, 1.05), 0.7, 0.7, facecolor=s.DL))
    ax.text(0.57, 1.4, "PDSCH", ha="center", va="center", fontsize=7.5, color="#fff", fontweight="bold")
    ax.add_patch(Rectangle((4.1, 1.05), 0.74, 0.7, facecolor=s.SYNC))
    ax.text(4.47, 1.4, "ACK\n(PUCCH)", ha="center", va="center", fontsize=7, color="#fff", fontweight="bold")
    ax.annotate("", xy=(4.3, 1.9), xytext=(0.5, 1.9), arrowprops=dict(arrowstyle="->", color=s.SYNC, lw=1.5,
                                                                       connectionstyle="arc3,rad=-0.25"))
    ax.text(2.4, 2.65, "K1 = 4 slots (PDSCH → HARQ-ACK)", ha="center", fontsize=8.5, color=s.SYNC)
    ax.text(0.1, 2.0, "K0 = 0", fontsize=8, color=s.CTRL)
    # UL: slot 2 PDCCH (UL grant) → PUSCH slot 4? K2=2 → slot 4
    ax.add_patch(Rectangle((2.02, 1.05), 0.18, 0.7, facecolor=s.CTRL))
    ax.annotate("", xy=(9.3, 0.95), xytext=(2.1, 0.95), arrowprops=dict(arrowstyle="->", color=s.UL, lw=1.5,
                                                                        connectionstyle="arc3,rad=0.12"))
    ax.add_patch(Rectangle((9.1, 1.05), 0.74, 0.7, facecolor=s.UL))
    ax.text(9.47, 1.4, "PUSCH", ha="center", va="center", fontsize=7.5, color="#fff", fontweight="bold")
    ax.text(6.0, -0.65, "UL grant in slot 2 with K2 = 7 → PUSCH in slot 9", ha="center", fontsize=8.5, color=s.UL)
    ax.text(10.4, 1.4, "■ PDCCH (DCI)\nK0: DCI → PDSCH\nK1: PDSCH → ACK\nK2: DCI → PUSCH\n(all signalled in DCI\nfrom RRC tables)",
            fontsize=8.5, va="center", color=s.INK2)
    ax.set_xlim(-0.3, 13.2)
    ax.set_ylim(-1.0, 3.0)
    s.save(fig, "nr_k0k1k2")


BANDS = [
    # (name, low MHz, high MHz, duplex)
    ("n71", 617, 652, "FDD"), ("n28", 758, 803, "FDD"), ("n20", 791, 821, "FDD"), ("n5", 869, 894, "FDD"),
    ("n8", 925, 960, "FDD"), ("n3", 1805, 1880, "FDD"), ("n1", 2110, 2170, "FDD"), ("n40", 2300, 2400, "TDD"),
    ("n41", 2496, 2690, "TDD"), ("n7", 2620, 2690, "FDD"), ("n77", 3300, 4200, "TDD"), ("n78", 3300, 3800, "TDD"),
    ("n79", 4400, 5000, "TDD"), ("n46", 5150, 5925, "TDD-U"), ("n96", 5925, 7125, "TDD-U"),
    ("n258", 24250, 27500, "TDD"), ("n257", 26500, 29500, "TDD"), ("n261", 27500, 28350, "TDD"),
    ("n260", 37000, 40000, "TDD"), ("n259", 39500, 43500, "TDD"), ("n262", 47200, 48200, "TDD"),
    ("n263", 57000, 71000, "TDD"),
]


def bands():
    fig, ax = plt.subplots(figsize=(12, 5.4))
    ax.set_xscale("log")
    ax.axvspan(410, 7125, color=s.DL, alpha=0.08, lw=0)
    ax.axvspan(7125, 24250, color=s.SPECIAL, alpha=0.12, lw=0)
    ax.axvspan(24250, 52600, color=s.UL, alpha=0.08, lw=0)
    ax.axvspan(52600, 71000, color=s.ALT, alpha=0.12, lw=0)
    for x, lab in ((1700, "FR1  410 MHz – 7.125 GHz"), (13000, "FR3 (6G candidate)\n7.125 – 24.25 GHz"),
                   (35000, "FR2-1\n24.25 – 52.6 GHz"), (61000, "FR2-2\n52.6–71 GHz")):
        ax.text(x, len(BANDS) + 0.4, lab, ha="center", va="bottom", fontsize=8.5, color=s.INK2)
    col = {"FDD": s.DL, "TDD": s.UL, "TDD-U": s.SPECIAL}
    for i, (name, lo, hi, dup) in enumerate(BANDS):
        y = i
        ax.barh(y, hi - lo, left=lo, height=0.62, color=col[dup], edgecolor="none")
        ax.text(hi * 1.04, y, name, va="center", fontsize=7.5, color=s.INK)
    ax.set_yticks([])
    ax.set_ylim(-1, len(BANDS) + 2.2)
    ax.set_xlim(400, 90000)
    ax.set_xticks([500, 1000, 2000, 3500, 7125, 24250, 52600, 71000])
    ax.set_xticklabels(["0.5", "1", "2", "3.5", "7.1", "24.25", "52.6", "71"])
    ax.set_xlabel("frequency (GHz, log scale) — DL range shown for FDD bands")
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    for dup, lab in (("FDD", "FDD (paired)"), ("TDD", "TDD (unpaired)"), ("TDD-U", "unlicensed / shared (NR-U)")):
        ax.barh(-5, 1, left=1, color=col[dup], label=lab)
    ax.legend(frameon=False, fontsize=8.5, loc="lower right")
    s.save(fig, "nr_bands")


if __name__ == "__main__":
    s.setup()
    point_a()
    bwp()
    slot_formats()
    coreset()
    pdsch_dmrs()
    beam_sweep()
    ssb_ro()
    k0k1k2()
    bands()
