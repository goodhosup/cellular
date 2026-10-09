"""LTE 물리계층 그림 (TS 36.211)

1. lte_dl_subframe0 : FDD 서브프레임 0, 중앙 6 RB — PSS/SSS/PBCH/제어 영역/CRS 배치
2. lte_sync_location : FDD와 TDD에서 PSS·SSS·PBCH의 시간 위치
3. lte_ul_subframe  : 상향 서브프레임 — PUCCH(대역 가장자리, 슬롯 호핑), PUSCH, DMRS, SRS
4. lte_prach_formats : PRACH 프리앰블 포맷 0–3 (CP / 시퀀스 / 보호 시간)
"""
from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import style as s


def cell(ax, x, y, w, h, fc, ec="#ffffff", lw=0.6):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw))


def legend(ax, items, x, y, step=3.2, size=2.2):
    for i, (fc, txt) in enumerate(items):
        yy = y - i * step
        ax.add_patch(Rectangle((x, yy), size, size, facecolor=fc, edgecolor=s.GRID, linewidth=0.6))
        ax.text(x + size + 0.8, yy + size / 2, txt, va="center", fontsize=8.5)


def dl_subframe0(cfi: int = 2):
    """10 MHz FDD 셀(2 CRS 포트, PCI mod 6 = 0)의 서브프레임 0 중앙 72 subcarrier."""
    K = 72
    fig, ax = plt.subplots(figsize=(10, 8.4))
    s.bare(ax)
    W = 2.0  # 심볼 폭 (그림 단위). 높이 1 = 1 subcarrier

    def crs(sym, k):
        slot, l = divmod(sym, 7)
        if l == 0:
            return k % 6 in (0, 3)          # 포트 0: v=0, 포트 1: v=3
        if l == 4:
            return k % 6 in (3, 0)          # 포트 0: v=3, 포트 1: v=0
        return False

    def reserved_crs_ports23(sym, k):
        slot, l = divmod(sym, 7)
        return l == 1 and k % 3 == 0        # 포트 2/3 위치 (PBCH 레이트 매칭은 4포트 가정)

    for sym in range(14):
        for k in range(K):
            slot, l = divmod(sym, 7)
            fc = s.DL
            if sym < cfi:
                fc = s.CTRL
            if slot == 0 and l in (5, 6):    # SSS(l=5), PSS(l=6)
                fc = s.SYNC if 5 <= k <= 66 else s.EMPTY
            if slot == 1 and l <= 3:         # PBCH
                fc = s.SPECIAL
                if reserved_crs_ports23(sym, k):
                    fc = s.EMPTY
            if crs(sym, k):
                fc = s.RS
            cell(ax, sym * W, k, W, 1, fc, lw=0.35)
    # 라벨
    ax.text(5 * W + W / 2, 36, "SSS", rotation=90, ha="center", va="center", fontsize=9, color="#fff", fontweight="bold")
    ax.text(6 * W + W / 2, 36, "PSS", rotation=90, ha="center", va="center", fontsize=9, color="#fff", fontweight="bold")
    ax.text(9 * W, 36, "PBCH", ha="center", va="center", fontsize=10, fontweight="bold",
            bbox=dict(facecolor=s.SPECIAL, edgecolor="none", pad=2))
    ax.text(cfi * W / 2, 36, "PDCCH\nregion", ha="center", va="center", fontsize=8, color="#fff", fontweight="bold",
            bbox=dict(facecolor=s.CTRL, edgecolor="none", pad=1.5))
    ax.text(12.5 * W, 36, "PDSCH", ha="center", va="center", fontsize=10, color="#fff", fontweight="bold",
            bbox=dict(facecolor=s.DL, edgecolor="none", pad=2))
    ax.plot([7 * W, 7 * W], [-1, K + 1], color=s.INK, lw=2)
    for sym in range(14):
        ax.text(sym * W + W / 2, -1.6, f"{sym % 7}", ha="center", va="top", fontsize=8, color=s.INK2)
    ax.text(3.5 * W, -4.2, "slot 0", ha="center", fontsize=9, color=s.INK2)
    ax.text(10.5 * W, -4.2, "slot 1", ha="center", fontsize=9, color=s.INK2)
    for k in (0, 5, 36, 66, 72):
        ax.text(-0.5, k, f"{k}", ha="right", va="center", fontsize=8, color=s.INK2)
    ax.text(-3.4, K / 2, "subcarrier within centre 6 RB (DC lies between 35 and 36)", rotation=90,
            ha="center", va="center", fontsize=9, color=s.INK2)
    legend(ax, [(s.RS, "CRS (ports 0/1)"), (s.CTRL, f"Control region, CFI={cfi}\n(PCFICH/PHICH/PDCCH)"),
                (s.SYNC, "PSS / SSS (62 sc)"), (s.SPECIAL, "PBCH (72 sc, 4 symbols)"),
                (s.EMPTY, "Reserved / unused\n(sync guard, CRS ports 2/3)"), (s.DL, "PDSCH")],
           x=14 * W + 2, y=66, step=7)
    ax.set_xlim(-5, 14 * W + 22)
    ax.set_ylim(-5.5, K + 1.5)
    s.save(fig, "lte_dl_subframe0")


def sync_location():
    fig, ax = plt.subplots(figsize=(11, 3.6))
    s.bare(ax)
    rows = {"FDD (frame type 1)": 1.6, "TDD (frame type 2)": 0}
    pat = "DSUDDDSUDD"  # config 1 계열 예시 (위치 설명용)
    for name, y in rows.items():
        ax.text(-0.2, y + 0.45, name, ha="right", va="center", fontsize=9.5, fontweight="bold")
        for sf in range(10):
            kind = "D" if name.startswith("FDD") else pat[sf]
            fc = {"D": s.EMPTY, "S": "#fbe3a6", "U": "#f9d3c4"}[kind]
            ax.add_patch(Rectangle((sf, y), 0.96, 0.9, facecolor=fc, edgecolor=s.GRID, lw=0.8))
            ax.text(sf + 0.48, y + 1.02, f"{sf}" + ("" if name.startswith("FDD") else f" {kind}"),
                    ha="center", fontsize=7.5, color=s.INK2)

    def mark(sf, l, y, fc, lab, n_sym=14):
        x = sf + l / n_sym * 0.96
        ax.add_patch(Rectangle((x, y + 0.05), 0.96 / n_sym, 0.8, facecolor=fc, edgecolor="none"))
        return x

    for sf in (0, 5):
        mark(sf, 5, 1.6, s.SYNC, "SSS")
        mark(sf, 6, 1.6, s.SYNC, "PSS")
        mark(sf, 13, 0, s.SYNC, "SSS")      # TDD SSS: 서브프레임 0/5의 마지막 심볼
    for sf in (1, 6):
        mark(sf, 2, 0, s.RS, "PSS")         # TDD PSS: 서브프레임 1/6의 3번째 심볼 (DwPTS)
    for l in range(7, 11):
        mark(0, l, 1.6, s.SPECIAL, "PBCH")
        mark(0, l, 0, s.SPECIAL, "PBCH")
    # 범례
    for i, (fc, txt) in enumerate([(s.SYNC, "SSS (and PSS in FDD)"), (s.RS, "PSS in TDD (DwPTS, symbol 2)"),
                                   (s.SPECIAL, "PBCH: subframe 0, slot 1, symbols 0–3")]):
        ax.add_patch(Rectangle((10.5, 2.0 - i * 0.7), 0.3, 0.4, facecolor=fc))
        ax.text(10.95, 2.2 - i * 0.7, txt, va="center", fontsize=8.5)
    ax.text(5, -0.55, "FDD: SSS → PSS in adjacent symbols (5, 6) of slots 0 and 10.  "
            "TDD: SSS in the last symbol of subframes 0/5, PSS three symbols later.",
            ha="center", fontsize=8.5, color=s.INK2)
    ax.set_xlim(-3.4, 16.5)
    ax.set_ylim(-0.9, 2.9)
    s.save(fig, "lte_sync_location")


def ul_subframe():
    nrb = 12
    fig, ax = plt.subplots(figsize=(10, 5.4))
    s.bare(ax)
    W = 1.0
    for sym in range(14):
        slot, l = divmod(sym, 7)
        for rb in range(nrb):
            fc = s.UL
            # PUCCH: 양 끝 RB, 슬롯 경계에서 반대편으로 호핑
            if rb in (0, nrb - 1):
                fc = s.CTRL
            elif rb in (1, nrb - 2):
                fc = s.ALT
            if l == 3 and 3 <= rb <= 8:
                fc = s.RS                    # PUSCH DMRS (normal CP: 각 슬롯 4번째 심볼)
            if sym == 13 and 2 <= rb <= nrb - 3:
                fc = s.SYNC                  # SRS: 서브프레임 마지막 심볼
            if not (rb in (0, 1, nrb - 2, nrb - 1)) and not (3 <= rb <= 8) and sym != 13:
                fc = s.EMPTY
            cell(ax, sym * W, rb, W, 1, fc, lw=1.0)
    # PUCCH 호핑 화살표 (m=0: slot0 아래 → slot1 위)
    ax.text(3.5, 0.5, "PUCCH m=0", ha="center", va="center", fontsize=8, color="#fff", fontweight="bold")
    ax.text(10.5, nrb - 0.5, "PUCCH m=0", ha="center", va="center", fontsize=8, color="#fff", fontweight="bold")
    ax.text(3.5, nrb - 0.5, "PUCCH m=1", ha="center", va="center", fontsize=8, color="#fff", fontweight="bold")
    ax.text(10.5, 0.5, "PUCCH m=1", ha="center", va="center", fontsize=8, color="#fff", fontweight="bold")
    ax.text(3.5, 1.5, "m=2", ha="center", va="center", fontsize=8)
    ax.text(10.5, nrb - 1.5, "m=2", ha="center", va="center", fontsize=8)
    ax.text(1.5, 6, "PUSCH\n(UE A)", ha="center", va="center", fontsize=9, color="#fff", fontweight="bold")
    ax.text(12.0, 6, "PUSCH\n(UE A)", ha="center", va="center", fontsize=9, color="#fff", fontweight="bold")
    ax.plot([7, 7], [-0.3, nrb + 0.3], color=s.INK, lw=2)
    for sym in range(14):
        ax.text(sym + 0.5, -0.45, f"{sym % 7}", ha="center", va="top", fontsize=8, color=s.INK2)
    ax.text(3.5, -1.3, "slot 0", ha="center", fontsize=9, color=s.INK2)
    ax.text(10.5, -1.3, "slot 1", ha="center", fontsize=9, color=s.INK2)
    ax.text(-0.5, nrb / 2, "PRB (frequency)", rotation=90, ha="center", va="center", fontsize=9, color=s.INK2)
    legend(ax, [(s.CTRL, "PUCCH format 2/2a/2b (outermost, m=0,1)"), (s.ALT, "PUCCH format 1/1a/1b (m=2,3)"),
                (s.UL, "PUSCH data (SC-FDMA)"), (s.RS, "PUSCH DMRS (symbol 3 of each slot)"),
                (s.SYNC, "SRS (last symbol, if configured)"), (s.EMPTY, "Other UEs / unallocated")],
           x=15.2, y=nrb - 1.2, step=1.9, size=0.9)
    ax.set_xlim(-1.2, 27)
    ax.set_ylim(-1.8, nrb + 0.6)
    ax.set_aspect("equal")
    s.save(fig, "lte_ul_subframe")


# TS 36.211 Table 5.7.1-1 (Ts 단위)
PRACH = [
    ("Format 0", 1, 3168, 24576),
    ("Format 1", 2, 21024, 24576),
    ("Format 2", 2, 6240, 2 * 24576),
    ("Format 3", 3, 21024, 2 * 24576),
]


def prach_formats():
    ts_us = 1 / 30.72
    fig, ax = plt.subplots(figsize=(11, 3.8))
    s.bare(ax)
    scale = 1 / 30720 * 30  # 1 ms → 30 단위
    for r, (name, nsf, cp, seq) in enumerate(PRACH):
        y = 3 - r
        total = nsf * 30720
        gt = total - cp - seq
        x = 0
        for w, fc, lab in ((cp, s.SPECIAL, "CP"), (seq, s.UL, ""),
                           (gt, s.EMPTY, "GT")):
            ax.add_patch(Rectangle((x * scale, y), w * scale, 0.7, facecolor=fc, edgecolor=s.SURFACE, lw=1.5))
            if fc == s.UL:
                lab = "sequence (800 µs)" if seq == 24576 else "sequence × 2 (repeated, 1600 µs)"
            if w * scale > 2.5:
                ax.text((x + w / 2) * scale, y + 0.35, lab, ha="center", va="center", fontsize=8.5,
                        color=s.text_on(fc), fontweight="bold" if fc != s.UL else "normal")
            x += w
        r_km = gt * ts_us * 1e-6 * 3e8 / 2 / 1000
        ax.text(-0.6, y + 0.35, f"{name}\n{nsf} subframe" + ("s" if nsf > 1 else ""), ha="right", va="center",
                fontsize=9, fontweight="bold")
        ax.text(nsf * 30 + 1.0, y + 0.35,
                f"CP {cp * ts_us:.0f} µs · GT {gt * ts_us:.0f} µs → cell radius ≤ {r_km:.0f} km",
                va="center", fontsize=8.5, color=s.INK2)
    for t in range(4):
        ax.plot([t * 30, t * 30], [-0.2, -0.05], color=s.INK2, lw=0.8)
        ax.text(t * 30, -0.3, f"{t} ms", ha="center", va="top", fontsize=8, color=s.INK2)
    ax.text(45, -0.95, "sequence = Zadoff-Chu length 839 on 1.25 kHz subcarriers;  radius = GT × c / 2 (round trip)",
            ha="center", fontsize=8.5, color=s.INK2)
    ax.set_xlim(-14, 150)
    ax.set_ylim(-1.3, 3.9)
    s.save(fig, "lte_prach_formats")


if __name__ == "__main__":
    s.setup()
    dl_subframe0()
    sync_location()
    ul_subframe()
    prach_formats()
