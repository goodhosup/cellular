"""NR 프레임/SSB 그림 (TS 38.211 §4.3, §7.4.3 / TS 38.213 §4.1)

1. nr_numerology_slots : μ=0…4 에서 1 ms(서브프레임) 안의 슬롯 수와 심볼 길이
2. nr_ssb_structure    : SS/PBCH 블록의 RE 배치 (240 subcarriers × 4 symbols)
3. nr_ssb_burst        : 하프 프레임(5 ms) 안의 SSB 후보 위치 — Case A–E
"""
from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import style as s


def box(ax, x, y, w, h, fc, label="", fs=9, ec="#ffffff", lw=1.2, tc=None, bold=False):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs,
                color=tc or s.text_on(fc), fontweight="bold" if bold else "normal")


def numerology_slots():
    fig, ax = plt.subplots(figsize=(11, 4.8))
    s.bare(ax)
    W = 100.0  # 1 ms
    h = 0.62
    for mu in range(5):
        y = 4 - mu
        scs = 15 * 2 ** mu
        n = 2 ** mu
        sw = W / n
        ax.text(-1.5, y + h / 2, f"μ={mu}  ·  {scs} kHz", ha="right", va="center", fontsize=9.5, fontweight="bold")
        for i in range(n):
            label = f"slot {i}" if n <= 4 else (f"{i}" if n <= 8 else "")
            box(ax, i * sw, y, sw, h, s.DL, label, fs=8.5 if n <= 8 else 7, lw=1.0)
        dur = 1000 / n
        sym = 1000 / 14 / n
        ax.text(W + 1.5, y + h / 2,
                f"{n:>2} slot/ms   slot {dur:g} µs   symbol ≈ {sym:.2f} µs",
                va="center", fontsize=8.5, color=s.INK2, family="DejaVu Sans Mono")
    # 축
    for t in range(0, 11):
        x = t * 10
        ax.plot([x, x], [-0.15, -0.05], color=s.INK2, lw=0.8)
        ax.text(x, -0.3, f"{t / 10:g}", ha="center", va="top", fontsize=8, color=s.INK2)
    ax.text(W / 2, -0.85, "time (ms) — one subframe, always 14 symbols per slot (normal CP)", ha="center",
            fontsize=9, color=s.INK2)
    ax.set_xlim(-18, 150)
    ax.set_ylim(-1.1, 4.9)
    s.save(fig, "nr_numerology_slots")


def ssb_structure():
    """TS 38.211 Table 7.4.3.1-1"""
    fig, ax = plt.subplots(figsize=(9.5, 6.2))
    s.bare(ax)
    # 세로축 = subcarrier (0..239) → 그림에서는 1 RB(12 sc)를 1 단위로 축소해 20 단위로 표현
    K = 240
    sc = 1 / 12  # 1 subcarrier 높이
    w = 2.2      # 심볼 폭

    def seg(sym, k0, k1, fc, label="", fs=9):
        box(ax, sym * w, k0 * sc, w, (k1 - k0 + 1) * sc, fc, label, fs=fs, lw=1.4, bold=True)

    # symbol 0: PSS 56..182, 나머지 0
    seg(0, 0, 55, s.EMPTY)
    seg(0, 56, 182, s.SYNC, "PSS\n127 sc")
    seg(0, 183, 239, s.EMPTY)
    # symbol 1: PBCH 0..239
    seg(1, 0, 239, s.CTRL, "PBCH\n+ DMRS\n240 sc")
    # symbol 2: PBCH 0..47, 0 48..55, SSS 56..182, 0 183..191, PBCH 192..239
    seg(2, 0, 47, s.CTRL, "PBCH\n48 sc", fs=8)
    seg(2, 48, 55, s.EMPTY)
    seg(2, 56, 182, s.SYNC, "SSS\n127 sc")
    seg(2, 183, 191, s.EMPTY)
    seg(2, 192, 239, s.CTRL, "PBCH\n48 sc", fs=8)
    # symbol 3: PBCH 0..239
    seg(3, 0, 239, s.CTRL, "PBCH\n+ DMRS\n240 sc")

    for sym in range(4):
        ax.text(sym * w + w / 2, -0.45, f"symbol {sym}", ha="center", va="top", fontsize=9, color=s.INK2)
    for k in (0, 48, 56, 183, 192, 240):
        ax.plot([-0.12, 0], [k * sc, k * sc], color=s.INK2, lw=0.8)
        ax.text(-0.2, k * sc, f"{k}" if k < 240 else "240", ha="right", va="center", fontsize=8, color=s.INK2)
    ax.text(-1.4, K * sc / 2, "subcarrier index within SSB  (240 sc = 20 RB)", rotation=90,
            ha="center", va="center", fontsize=9, color=s.INK2)

    # 범례
    lx = 4 * w + 0.8
    items = [(s.SYNC, "PSS / SSS — m-sequence & Gold sequence, length 127"),
             (s.CTRL, "PBCH — Polar coded, QPSK, 432 data RE"),
             (s.EMPTY, "Set to zero (guard)")]
    for i, (fc, txt) in enumerate(items):
        y = 17.5 - i * 1.5
        ax.add_patch(Rectangle((lx, y), 0.8, 0.8, facecolor=fc, edgecolor=s.GRID))
        ax.text(lx + 1.1, y + 0.4, txt, va="center", fontsize=8.5)
    ax.text(lx, 12.3,
            "PBCH RE = 240 + 96 + 240 = 576\n"
            "  · DMRS every 4th sc, offset v = PCI mod 4\n"
            "    → 144 DMRS RE\n"
            "  · data → 432 RE × 2 bit (QPSK) = 864 bit\n\n"
            "Payload: MIB 23 + 1 choice bit\n"
            "  + 8 timing bits (SFN LSB 4, half-frame 1,\n"
            "    SSB index MSB / k_SSB MSB 3)\n"
            "  = 32 bit + CRC 24 → Polar(N=512) → 864",
            fontsize=8.3, va="top", color=s.INK2, family="DejaVu Sans Mono")
    ax.set_xlim(-2, 4 * w + 10.5)
    ax.set_ylim(-1.1, K * sc + 0.3)
    s.save(fig, "nr_ssb_structure")


# TS 38.213 §4.1 — 하프 프레임 안의 SSB 후보 첫 심볼 인덱스
CASES = [
    # (이름, SCS kHz, 기준 심볼 패턴, 주기(심볼), n 목록, 설명)
    ("Case A", 15, (2, 8), 14, [0, 1, 2, 3], "FR1, Lmax=8 (≤3 GHz: n=0,1 → Lmax=4)"),
    ("Case B", 30, (4, 8, 16, 20), 28, [0, 1], "FR1 (e.g. n5/n66), Lmax=8"),
    ("Case C", 30, (2, 8), 14, [0, 1, 2, 3], "FR1 (e.g. n78), Lmax=8"),
    ("Case D", 120, (4, 8, 16, 20), 28, [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15, 16, 17, 18], "FR2, Lmax=64"),
    ("Case E", 240, (8, 12, 16, 20, 32, 36, 40, 44), 56, [0, 1, 2, 3, 5, 6, 7, 8], "FR2, Lmax=64"),
]


SYNC_DARK = "#0f7a53"  # 연속된 SSB를 구분하기 위한 교대 음영


def _ssb_marks(ax, y, h, case, t0, t1, W):
    """[t0, t1] ms 구간을 폭 W로 그린다. 연속 SSB는 두 음영을 번갈아 칠한다."""
    name, scs, base, period, ns, note = case
    sym_ms = 1.0 / (14 * scs / 15)   # 심볼 길이 (ms), CP 길이 차이는 무시
    scale = W / (t1 - t0)
    idx = 0
    for n in ns:
        for b in base:
            start = (b + period * n) * sym_ms
            if t0 <= start < t1:
                ax.add_patch(Rectangle(((start - t0) * scale, y), 4 * sym_ms * scale, h,
                                       facecolor=SYNC_DARK if idx % 2 else s.SYNC, edgecolor="none"))
            idx += 1
    return idx, sym_ms


def ssb_burst():
    fig, (ax, az) = plt.subplots(2, 1, figsize=(11, 6.6), gridspec_kw={"height_ratios": [5, 2.3]})
    s.bare(ax)
    s.bare(az)
    W = 100.0
    h = 0.55

    # (위) 하프 프레임 5 ms 전체
    for r, case in enumerate(CASES):
        y = len(CASES) - 1 - r
        ax.add_patch(Rectangle((0, y), W, h, facecolor=s.EMPTY, edgecolor="none"))
        count, _ = _ssb_marks(ax, y, h, case, 0, 5, W)
        name, scs, *_, note = case
        ax.text(-1.2, y + h / 2, f"{name}\n{scs} kHz", ha="right", va="center", fontsize=9, fontweight="bold")
        ax.text(W + 1.2, y + h / 2, f"L={count}  ·  {note}", va="center", fontsize=8.3, color=s.INK2)
    for t in range(6):
        x = t / 5 * W
        ax.plot([x, x], [-0.12, -0.02], color=s.INK2, lw=0.8)
        ax.text(x, -0.22, f"{t}", ha="center", va="top", fontsize=8, color=s.INK2)
    ax.text(W / 2, -0.72, "time within half frame (ms) — one mark = one candidate SSB (4 symbols), shades alternate",
            ha="center", fontsize=9, color=s.INK2)
    ax.add_patch(Rectangle((0, -0.05), 0.25 / 5 * W, len(CASES) - 0.4, facecolor="none",
                           edgecolor=s.INK2, linewidth=0.9, linestyle="--"))
    ax.set_xlim(-12, 152)
    ax.set_ylim(-1.0, len(CASES))

    # (아래) 처음 0.25 ms 확대 — FR2 Case D / E
    for r, case in enumerate(CASES[3:]):
        y = 1 - r
        az.add_patch(Rectangle((0, y), W, h, facecolor=s.EMPTY, edgecolor="none"))
        _, sym_ms = _ssb_marks(az, y, h, case, 0, 0.25, W)
        name, scs, *_ = case
        az.text(-1.2, y + h / 2, f"{name}\n{scs} kHz", ha="right", va="center", fontsize=9, fontweight="bold")
        slot = 14 * sym_ms
        k = 0
        while k * slot < 0.25 - 1e-9:
            x = k * slot / 0.25 * W
            az.plot([x, x], [y - 0.06, y + h + 0.06], color=s.INK2, lw=0.6)
            k += 1
        az.text(W + 1.2, y + h / 2, f"{k} slots shown · SSB at symbols\n" +
                ("{4,8,16,20}+28n" if scs == 120 else "{8,12,16,20,32,36,40,44}+56n"),
                va="center", fontsize=8.3, color=s.INK2)
    for t in (0, 0.0625, 0.125, 0.1875, 0.25):
        x = t / 0.25 * W
        az.text(x, -0.15, f"{t * 1000:g}", ha="center", va="top", fontsize=8, color=s.INK2)
    az.text(W / 2, -0.62, "zoom: first 0.25 ms (µs) — thin ticks mark slot boundaries", ha="center",
            fontsize=9, color=s.INK2)
    az.set_xlim(-12, 152)
    az.set_ylim(-0.9, 2)
    s.save(fig, "nr_ssb_burst")


if __name__ == "__main__":
    s.setup()
    numerology_slots()
    ssb_structure()
    ssb_burst()
