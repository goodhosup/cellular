"""공통 기초 그림

1. ofdm_subcarriers : 직교 부반송파 스펙트럼 (sinc) — 각 피크에서 다른 부반송파는 0
2. ofdm_cp          : 다중경로 지연과 CP — FFT 창 안에서 심볼 간 간섭이 사라지는 원리
3. qam_constellations : QPSK / 16QAM / 64QAM / 256QAM 성상도
4. channel_pdp      : 3GPP 페이딩 채널 모델 EPA / EVA / ETU 전력 지연 프로파일 (TS 36.101 Annex B.2)
5. duplexing        : FDD와 TDD의 시간–주파수 자원 사용
6. harq_processes   : LTE FDD 하향 HARQ 8 프로세스 (n+4 ACK/NACK, 재전송 n+8 이후)
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import style as s

SERIES = [s.DL, s.UL, s.SYNC, s.SPECIAL, s.ALT]


def ofdm_subcarriers():
    fig, ax = plt.subplots(figsize=(10, 4.2))
    f = np.linspace(-4.5, 4.5, 2000)
    for i, k in enumerate(range(-2, 3)):
        y = np.sinc(f - k)
        ax.plot(f, y, color=SERIES[i], lw=2)
        ax.plot([k], [1], "o", color=SERIES[i], ms=8, mec=s.SURFACE, mew=2, zorder=5)
        ax.text(k, 1.08, f"k{k:+d}" if k else "k", ha="center", fontsize=9, color=s.INK2)
    for k in range(-2, 3):
        ax.axvline(k, color=s.GRID, lw=0.8, ls="--", zorder=0)
    ax.axhline(0, color=s.MUTED, lw=0.8)
    ax.set_xticks(range(-4, 5))
    ax.set_xticklabels([f"{k:+d}Δf" if k else "0" for k in range(-4, 5)])
    ax.set_yticks([0, 0.5, 1])
    ax.set_ylim(-0.3, 1.2)
    ax.set_xlim(-4.5, 4.5)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_ylabel("amplitude")
    ax.set_xlabel("frequency  (Δf = 1/T_u, e.g. 15 kHz ↔ 66.7 µs)")
    ax.set_title("at each peak (dot), every other subcarrier crosses zero → no inter-carrier interference",
                 fontsize=9.5, color=s.INK2, pad=14)
    s.save(fig, "ofdm_subcarriers")


def ofdm_cp():
    fig, ax = plt.subplots(figsize=(11, 4.0))
    s.bare(ax)
    cp, tu = 1.2, 8.0
    h = 0.62
    paths = [(0.0, "path 1 (direct)"), (0.45, "path 2 (delay τ₂)"), (0.95, "path 3 (delay τ₃ < CP)")]
    for r, (d, name) in enumerate(paths):
        y = 2.2 - r * 0.95
        ax.text(-1.7, y + h / 2, name, ha="right", va="center", fontsize=9)
        x0 = d
        # 앞 심볼 꼬리
        ax.add_patch(Rectangle((x0 - 1.4, y), 1.4, h, facecolor=s.MUTED, edgecolor=s.SURFACE, lw=1.5))
        ax.text(x0 - 0.7, y + h / 2, "prev", ha="center", va="center", fontsize=8, color="#fff")
        ax.add_patch(Rectangle((x0, y), cp, h, facecolor=s.SPECIAL, edgecolor=s.SURFACE, lw=1.5))
        ax.text(x0 + cp / 2, y + h / 2, "CP", ha="center", va="center", fontsize=8.5, fontweight="bold")
        ax.add_patch(Rectangle((x0 + cp, y), tu, h, facecolor=s.DL, edgecolor=s.SURFACE, lw=1.5, alpha=1 - 0.18 * r))
        ax.text(x0 + cp + tu / 2, y + h / 2, "useful symbol  T_u", ha="center", va="center", fontsize=9, color="#fff")
    # FFT 창
    top, bot = 2.2 + h + 0.25, 2.2 - 2 * 0.95 - 0.25
    ax.add_patch(Rectangle((cp, bot), tu, top - bot, facecolor="none", edgecolor=s.RS, lw=2, ls="--"))
    ax.text(cp + tu / 2, top + 0.12, "receiver FFT window (length T_u)", ha="center", fontsize=9, color=s.RS)
    ax.annotate("", xy=(0.95, bot - 0.15), xytext=(0, bot - 0.15),
                arrowprops=dict(arrowstyle="<->", color=s.INK2, lw=1))
    ax.text(0.47, bot - 0.45, "max delay\nspread", ha="center", va="top", fontsize=8, color=s.INK2)
    ax.text(cp + tu + 1.2, 1.25,
            "Every path's previous symbol\nends before the FFT window\n→ no inter-symbol interference\n\n"
            "Delay inside CP only\nrotates each subcarrier's phase\n→ fixed by 1-tap equalizer",
            fontsize=9, va="center", color=s.INK2)
    ax.set_xlim(-6.2, cp + tu + 6)
    ax.set_ylim(bot - 1.1, top + 0.5)
    s.save(fig, "ofdm_cp")


def qam_constellations():
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.4))
    for ax, (name, m) in zip(axes, [("QPSK", 4), ("16QAM", 16), ("64QAM", 64), ("256QAM", 256)]):
        n = int(np.sqrt(m))
        lv = np.arange(-(n - 1), n, 2)
        xx, yy = np.meshgrid(lv, lv)
        norm = np.sqrt(np.mean(xx ** 2 + yy ** 2))
        ax.scatter(xx / norm, yy / norm, s=max(70 / np.sqrt(m) * 4, 6), color=s.DL, edgecolor="none")
        ax.axhline(0, color=s.GRID, lw=0.8, zorder=0)
        ax.axvline(0, color=s.GRID, lw=0.8, zorder=0)
        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-1.6, 1.6)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_color(s.GRID)
        bits = int(np.log2(m))
        ax.set_title(f"{name}\n{bits} bit / symbol", fontsize=10)
        ax.set_xlabel("I", fontsize=9)
    axes[0].set_ylabel("Q", fontsize=9)
    fig.text(0.5, -0.04, "same average power — more points means points sit closer together, so higher SNR is required",
             ha="center", fontsize=9, color=s.INK2)
    s.save(fig, "qam_constellations")


# TS 36.101 Table B.2.1-2/3/4 (excess tap delay ns, relative power dB)
PDP = {
    "EPA (pedestrian)": ([0, 30, 70, 90, 110, 190, 410], [0, -1, -2, -3, -8, -17.2, -20.8]),
    "EVA (vehicular)": ([0, 30, 150, 310, 370, 710, 1090, 1730, 2510],
                        [0, -1.5, -1.4, -3.6, -0.6, -9.1, -7.0, -12.0, -16.9]),
    "ETU (typical urban)": ([0, 50, 120, 200, 230, 500, 1600, 2300, 5000],
                            [-1, -1, -1, 0, 0, 0, -3, -5, -7]),
}


def channel_pdp():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.4), sharey=True)
    for ax, (name, (d, p)) in zip(axes, PDP.items()):
        ax.vlines(d, -25, p, color=s.DL, lw=2)
        ax.plot(d, p, "o", color=s.DL, ms=6, mec=s.SURFACE, mew=1.5)
        ax.set_title(name, fontsize=10)
        ax.set_xlabel("excess delay (ns)", fontsize=9)
        ax.set_ylim(-25, 3)
        ax.axvline(4690, color=s.RS, lw=1.2, ls="--")
        ax.set_xlim(-150, 5600)
        ax.text(4650, -23.5, "normal CP\n≈ 4.7 µs", ha="right", fontsize=8, color=s.RS)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.grid(axis="y", color=s.GRID, lw=0.6)
        ax.set_axisbelow(True)
    axes[0].set_ylabel("relative power (dB)", fontsize=9)
    s.save(fig, "channel_pdp")


def duplexing():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.8))
    for ax in (a1, a2):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.set_xlabel("time →", fontsize=9)
        ax.set_ylabel("frequency →", fontsize=9)
    # FDD
    a1.add_patch(Rectangle((0.2, 6.2), 9.6, 2.8, facecolor=s.DL))
    a1.text(5, 7.6, "Downlink carrier (f_DL)", ha="center", va="center", color="#fff", fontweight="bold")
    a1.add_patch(Rectangle((0.2, 1.0), 9.6, 2.8, facecolor=s.UL))
    a1.text(5, 2.4, "Uplink carrier (f_UL)", ha="center", va="center", color="#fff", fontweight="bold")
    a1.annotate("", xy=(0.6, 6.1), xytext=(0.6, 3.9), arrowprops=dict(arrowstyle="<->", color=s.INK2))
    a1.text(0.9, 5.0, "duplex gap", va="center", fontsize=8.5, color=s.INK2)
    a1.set_title("FDD — paired spectrum, DL and UL at the same time", fontsize=10)
    # TDD
    pat = "DDDSUDDDSU"
    color = {"D": s.DL, "U": s.UL, "S": s.SPECIAL}
    for i, c in enumerate(pat):
        a2.add_patch(Rectangle((0.2 + i * 0.96, 2.0), 0.9, 6.0, facecolor=color[c]))
        a2.text(0.2 + i * 0.96 + 0.45, 5.0, c, ha="center", va="center", color=s.text_on(color[c]),
                fontweight="bold")
    a2.text(5, 1.2, "D = downlink, U = uplink, S = switching (guard period)", ha="center", fontsize=8.5,
            color=s.INK2)
    a2.set_title("TDD — one carrier, DL and UL take turns in time", fontsize=10)
    s.save(fig, "duplexing")


def harq_processes():
    """LTE FDD DL: 서브프레임 n에 PDSCH → n+4에 ACK/NACK → 가장 빠른 재전송 n+8"""
    fig, ax = plt.subplots(figsize=(11.5, 3.6))
    s.bare(ax)
    N = 20
    nack = {2}  # 프로세스 2의 첫 전송이 NACK
    h = 0.7
    for sf in range(N):
        pid = sf % 8
        retx = pid in nack and sf >= 8 and sf < 16
        fc = s.ALT if retx else s.DL
        ax.add_patch(Rectangle((sf, 2), 0.94, h, facecolor=fc, edgecolor="none"))
        ax.text(sf + 0.47, 2 + h / 2, f"P{pid}" + ("'" if retx else ""), ha="center", va="center", fontsize=8.5,
                color=s.text_on(fc), fontweight="bold")
        ax.text(sf + 0.47, 3.0, f"{sf}", ha="center", fontsize=8, color=s.INK2)
        if sf + 4 < N:
            ok = not (pid in nack and sf < 8)
            fc2 = s.SYNC if ok else s.RS
            ax.add_patch(Rectangle((sf + 4, 0.6), 0.94, h, facecolor=fc2, edgecolor="none"))
            ax.text(sf + 4 + 0.47, 0.6 + h / 2, ("A" if ok else "N") + f"{pid}", ha="center", va="center",
                    fontsize=8.5, color="#fff", fontweight="bold")
    ax.annotate("", xy=(6.47, 1.35), xytext=(2.47, 1.95), arrowprops=dict(arrowstyle="->", color=s.RS, lw=1.4))
    ax.annotate("", xy=(10.47, 1.95), xytext=(6.47, 1.35), arrowprops=dict(arrowstyle="->", color=s.RS, lw=1.4))
    ax.text(-0.3, 2 + h / 2, "DL PDSCH", ha="right", va="center", fontsize=9, fontweight="bold")
    ax.text(-0.3, 0.6 + h / 2, "UL ACK/NACK", ha="right", va="center", fontsize=9, fontweight="bold")
    ax.text(-0.3, 3.0, "subframe", ha="right", fontsize=8, color=s.INK2)
    ax.text(N / 2, -0.3, "P2 first transmission → NACK at n+4 → retransmission P2' at n+8 "
            "(RTT = 8 ms → 8 HARQ processes keep the pipe full)", ha="center", fontsize=9, color=s.INK2)
    ax.set_xlim(-3.2, N + 0.2)
    ax.set_ylim(-0.6, 3.5)
    s.save(fig, "harq_processes")


def papr_ccdf(seed: int = 7):
    """CP-OFDM vs DFT-s-OFDM(SC-FDMA) PAPR CCDF — QPSK, 300 subcarriers in a 2048 FFT, 4× oversampling."""
    rng = np.random.default_rng(seed)
    nfft, m, os_, trials = 2048, 300, 4, 3000
    qpsk = (rng.choice([-1, 1], (trials, m)) + 1j * rng.choice([-1, 1], (trials, m))) / np.sqrt(2)

    def papr(freq):
        grid = np.zeros((trials, nfft * os_), complex)
        grid[:, :m] = freq
        x = np.fft.ifft(grid, axis=1)
        p = np.abs(x) ** 2
        return 10 * np.log10(p.max(axis=1) / p.mean(axis=1))

    ofdm = papr(qpsk)
    dfts = papr(np.fft.fft(qpsk, axis=1) / np.sqrt(m))
    fig, ax = plt.subplots(figsize=(8.5, 4.4))
    th = np.linspace(2, 12, 200)
    for data, name, c in ((ofdm, "CP-OFDM (LTE DL, NR DL/UL)", s.DL), (dfts, "DFT-s-OFDM / SC-FDMA (LTE UL, NR UL option)", s.UL)):
        ccdf = [(data > x).mean() for x in th]
        ax.semilogy(th, np.maximum(ccdf, 1e-4), color=c, lw=2, label=name)
    ax.set_ylim(1e-3, 1.2)
    ax.set_xlim(2, 12)
    ax.set_xlabel("PAPR threshold (dB)")
    ax.set_ylabel("P(PAPR > threshold)")
    ax.grid(True, which="both", color=s.GRID, lw=0.5)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(frameon=False, fontsize=9, loc="lower left")
    ax.set_title("QPSK, 300 subcarriers (25 RB), 4× oversampled", fontsize=9.5, color=s.INK2)
    s.save(fig, "papr_ccdf")


def array_pattern():
    """λ/2 간격 균일 선형 배열(ULA)의 배열 이득 — 소자 수가 늘수록 빔이 좁아지고 이득이 커진다."""
    th = np.radians(np.linspace(-90, 90, 2001))
    fig, ax = plt.subplots(figsize=(9, 4.2))
    steer = np.radians(20)
    for n, c in ((4, s.SYNC), (8, s.UL), (16, s.DL)):
        k = np.arange(n)
        af = np.abs(np.exp(1j * np.pi * np.outer(np.sin(th) - np.sin(steer), k)).sum(axis=1)) ** 2
        g = 10 * np.log10(np.maximum(af, 1e-6))
        ax.plot(np.degrees(th), g, color=c, lw=2, label=f"N = {n}  (array gain 10·log10 N = {10*np.log10(n):.0f} dB)")
    ax.axvline(20, color=s.MUTED, lw=1, ls="--")
    ax.text(21.5, -17, "steering angle 20°", fontsize=8.5, color=s.INK2)
    ax.set_ylim(-20, 26)
    ax.set_xlim(-90, 90)
    ax.set_xlabel("angle (degrees)")
    ax.set_ylabel("|AF|² (dB, unnormalized)")
    ax.grid(True, color=s.GRID, lw=0.5)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    s.save(fig, "array_pattern")


def hex_reuse():
    """주파수 재사용: 재사용 계수 7 (왼쪽) vs 재사용 계수 1 (오른쪽, LTE/NR)."""
    from matplotlib.patches import RegularPolygon
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 5))
    palette = [s.DL, s.UL, s.SYNC, s.SPECIAL, s.ALT, s.CTRL, s.RS]
    r = 1.0
    w = np.sqrt(3) * r

    def center(q, rr):
        return (w * (q + rr / 2), 1.5 * r * rr)

    cells = [(q, rr) for rr in range(-3, 4) for q in range(-3, 4) if abs(q + rr) <= 3]
    for ax, reuse7 in ((a1, True), (a2, False)):
        for q, rr in cells:
            x, y = center(q, rr)
            idx = (q + 3 * rr) % 7 if reuse7 else 0
            fc = palette[idx]
            ax.add_patch(RegularPolygon((x, y), 6, radius=r * 0.98, facecolor=fc, edgecolor=s.SURFACE, lw=2))
            ax.text(x, y, f"f{idx + 1}", ha="center", va="center", fontsize=8.5,
                    color=s.text_on(fc), fontweight="bold")
        ax.set_xlim(-6.5, 6.5)
        ax.set_ylim(-5.5, 5.5)
        ax.set_aspect("equal")
        s.bare(ax)
    a1.set_title("Reuse 7 (2G era): neighbours never share a frequency\n→ low interference, each cell gets 1/7 of the band",
                 fontsize=9.5)
    a2.set_title("Reuse 1 (LTE/NR): every cell uses the whole band\n→ 7× spectrum per cell, interference handled by scheduling",
                 fontsize=9.5)
    s.save(fig, "hex_reuse")


if __name__ == "__main__":
    s.setup()
    ofdm_subcarriers()
    ofdm_cp()
    qam_constellations()
    channel_pdp()
    duplexing()
    harq_processes()
    papr_ccdf()
    array_pattern()
    hex_reuse()
