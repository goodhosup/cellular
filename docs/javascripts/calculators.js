// 레퍼런스 > 계산기 페이지 전용 스크립트
// 모든 계산식은 해당 페이지에 출처(TS 번호)를 함께 적어 둠.
(function () {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const num = (id) => parseFloat($(id).value);
  const fmt = (x, d = 1) => Number.isFinite(x) ? x.toLocaleString("ko-KR", { maximumFractionDigits: d }) : "—";

  // ---------- 1. NR 최대 데이터율 (TS 38.306 §4.1.2) ----------
  // 전송 대역 구성 RB 수 (TS 38.101-1 / -2 Table 5.3.2-1)
  const NRB = {
    FR1: {
      15: { 5: 25, 10: 52, 15: 79, 20: 106, 25: 133, 30: 160, 40: 216, 50: 270 },
      30: { 5: 11, 10: 24, 15: 38, 20: 51, 25: 65, 30: 78, 40: 106, 50: 133, 60: 162, 70: 189, 80: 217, 90: 245, 100: 273 },
      60: { 10: 11, 15: 18, 20: 24, 25: 31, 30: 38, 40: 51, 50: 65, 60: 79, 70: 93, 80: 107, 90: 121, 100: 135 },
    },
    FR2: {
      60: { 50: 66, 100: 132, 200: 264 },
      120: { 50: 32, 100: 66, 200: 132, 400: 264 },
    },
  };
  const OH = { FR1: { DL: 0.14, UL: 0.08 }, FR2: { DL: 0.18, UL: 0.10 } };

  const DEFAULT_SCS = { FR1: "30", FR2: "120" };

  // FR이나 SCS가 바뀌면 그 조합의 최대 대역폭을 기본으로 선택
  function fillScs() {
    const fr = $("pr-fr").value;
    const scsSel = $("pr-scs");
    scsSel.innerHTML = Object.keys(NRB[fr]).map((s) => `<option value="${s}">${s} kHz</option>`).join("");
    scsSel.value = DEFAULT_SCS[fr];
    fillBw();
  }

  function fillBw() {
    const fr = $("pr-fr").value;
    const scs = $("pr-scs").value;
    const bwSel = $("pr-bw");
    const bws = Object.keys(NRB[fr][scs]);
    bwSel.innerHTML = bws.map((b) => `<option value="${b}">${b} MHz</option>`).join("");
    bwSel.value = bws[bws.length - 1];
    peakRate();
  }

  function peakRate() {
    const fr = $("pr-fr").value;
    const dir = $("pr-dir").value;
    const scs = parseInt($("pr-scs").value, 10);
    const bw = $("pr-bw").value;
    const nprb = NRB[fr][scs][bw];
    const mu = Math.log2(scs / 15);
    const layers = num("pr-layers");
    const qm = num("pr-qm");
    const f = num("pr-f");
    const cc = num("pr-cc");
    const ratio = num("pr-ratio") / 100;
    const Ts = 1e-3 / (14 * Math.pow(2, mu));
    const oh = OH[fr][dir];
    const per = 1e-6 * layers * qm * f * (948 / 1024) * (nprb * 12 / Ts) * (1 - oh);
    $("pr-nprb").textContent = nprb;
    $("pr-oh").textContent = oh;
    $("pr-out").textContent = fmt(per * cc);
    $("pr-out-tdd").textContent = fmt(per * cc * ratio);
  }

  // ---------- 2. NR-ARFCN ↔ 주파수 (TS 38.101-1 §5.4.2.1) ----------
  function arfcnToFreq(n) {
    if (n >= 0 && n < 600000) return 0.005 * n;
    if (n >= 600000 && n < 2016667) return 3000 + 0.015 * (n - 600000);
    if (n >= 2016667 && n <= 3279165) return 24250.08 + 0.06 * (n - 2016667);
    return NaN;
  }
  function freqToArfcn(f) {
    if (f >= 0 && f < 3000) return Math.round(f / 0.005);
    if (f >= 3000 && f < 24250) return Math.round(600000 + (f - 3000) / 0.015);
    if (f >= 24250 && f <= 100000) return Math.round(2016667 + (f - 24250.08) / 0.06);
    return NaN;
  }
  function arfcnCalc(from) {
    if (from === "n") {
      const f = arfcnToFreq(num("ar-n"));
      $("ar-f").value = Number.isFinite(f) ? +f.toFixed(3) : "";
      $("ar-note").textContent = Number.isFinite(f) ? "" : "범위 밖 NR-ARFCN (0 – 3279165)";
    } else {
      const n = freqToArfcn(num("ar-f"));
      $("ar-n").value = Number.isFinite(n) ? n : "";
      const back = arfcnToFreq(n);
      const diff = Math.abs(back - num("ar-f")) * 1000;
      $("ar-note").textContent = !Number.isFinite(n) ? "범위 밖 주파수" :
        diff > 0.0005 ? `가장 가까운 NR-ARFCN의 주파수는 ${back.toFixed(3)} MHz (차이 ${diff.toFixed(1)} kHz)` : "";
    }
  }

  // ---------- 3. GSCN ↔ SS_REF (TS 38.101-1 Table 5.4.3.1-1) ----------
  function gscnToFreq(g) {
    if (g >= 2 && g <= 7498) {
      // GSCN = 3N + (M-3)/2, M ∈ {1,3,5}
      for (const M of [1, 3, 5]) {
        const N = (g - (M - 3) / 2) / 3;
        if (Number.isInteger(N) && N >= 1 && N <= 2499) return N * 1.2 + M * 0.05;
      }
      return NaN;
    }
    if (g >= 7499 && g <= 22255) return 3000 + (g - 7499) * 1.44;
    if (g >= 22256 && g <= 26639) return 24250.08 + (g - 22256) * 17.28;
    return NaN;
  }
  function freqToGscn(f) {
    if (f > 0 && f < 3000) {
      let best = null;
      for (const M of [1, 3, 5]) {
        const N = Math.round((f - M * 0.05) / 1.2);
        if (N < 1 || N > 2499) continue;
        const ss = N * 1.2 + M * 0.05;
        const g = 3 * N + (M - 3) / 2;
        if (!best || Math.abs(ss - f) < Math.abs(best.ss - f)) best = { g, ss };
      }
      return best;
    }
    if (f >= 3000 && f < 24250) {
      const N = Math.round((f - 3000) / 1.44);
      return { g: 7499 + N, ss: 3000 + N * 1.44 };
    }
    if (f >= 24250 && f <= 100000) {
      const N = Math.round((f - 24250.08) / 17.28);
      return { g: 22256 + N, ss: 24250.08 + N * 17.28 };
    }
    return null;
  }
  function gscnCalc(from) {
    if (from === "g") {
      const f = gscnToFreq(num("gs-g"));
      $("gs-f").value = Number.isFinite(f) ? +f.toFixed(3) : "";
      $("gs-note").textContent = Number.isFinite(f) ? "" : "유효하지 않은 GSCN";
    } else {
      const r = freqToGscn(num("gs-f"));
      $("gs-g").value = r ? r.g : "";
      $("gs-note").textContent = !r ? "범위 밖 주파수" :
        Math.abs(r.ss - num("gs-f")) > 0.0005 ? `가장 가까운 동기 래스터: ${r.ss.toFixed(3)} MHz` : "";
    }
  }

  // ---------- 4. LTE EARFCN → 주파수 (TS 36.101 Table 5.7.3-1) ----------
  const LTE = [
    // band, F_DL_low, N_offs_DL, N_DL 범위, F_UL_low, N_offs_UL (TDD는 UL = DL)
    [1, 2110, 0, 0, 599, 1920, 18000],
    [2, 1930, 600, 600, 1199, 1850, 18600],
    [3, 1805, 1200, 1200, 1949, 1710, 19200],
    [4, 2110, 1950, 1950, 2399, 1710, 19950],
    [5, 869, 2400, 2400, 2649, 824, 20400],
    [7, 2620, 2750, 2750, 3449, 2500, 20750],
    [8, 925, 3450, 3450, 3799, 880, 21450],
    [12, 729, 5010, 5010, 5179, 699, 23010],
    [13, 746, 5180, 5180, 5279, 777, 23180],
    [20, 791, 6150, 6150, 6449, 832, 24150],
    [28, 758, 9210, 9210, 9659, 703, 27210],
    [38, 2570, 37750, 37750, 38249, null, null],
    [40, 2300, 38650, 38650, 39649, null, null],
    [41, 2496, 39650, 39650, 41589, null, null],
    [42, 3400, 41590, 41590, 43589, null, null],
  ];
  function earfcnCalc() {
    const n = num("lte-n");
    const row = LTE.find((r) => n >= r[3] && n <= r[4]);
    if (!row) {
      $("lte-out").textContent = "목록에 없는 DL EARFCN (지원 밴드: " + LTE.map((r) => r[0]).join(", ") + ")";
      return;
    }
    const [band, fdl, offs, , , ful, offsUl] = row;
    const dl = fdl + 0.1 * (n - offs);
    let txt = `Band ${band} · DL ${dl.toFixed(1)} MHz`;
    if (ful !== null) {
      const nul = n - offs + offsUl;
      txt += ` · 짝 UL EARFCN ${nul} → ${(ful + 0.1 * (nul - offsUl)).toFixed(1)} MHz`;
    } else {
      txt += " (TDD: UL 같은 주파수)";
    }
    $("lte-out").textContent = txt;
  }

  // ---------- 5. NR TBS (TS 38.214 §5.1.3.2) ----------
  const TBS_SMALL = [24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 208, 224, 240, 256, 272, 288, 304, 320, 336, 352, 368, 384, 408, 432, 456, 480, 504, 528, 552, 576, 608, 640, 672, 704, 736, 768, 808, 848, 888, 928, 984, 1032, 1064, 1128, 1160, 1192, 1224, 1256, 1288, 1320, 1352, 1416, 1480, 1544, 1608, 1672, 1736, 1800, 1864, 1928, 2024, 2088, 2152, 2216, 2280, 2408, 2472, 2536, 2600, 2664, 2728, 2792, 2856, 2976, 3104, 3240, 3368, 3496, 3624, 3752, 3824];
  // [Qm, R×1024]
  const MCS = {
    t1: [[2,120],[2,157],[2,193],[2,251],[2,308],[2,379],[2,449],[2,526],[2,602],[2,679],[4,340],[4,378],[4,434],[4,490],[4,553],[4,616],[4,658],[6,438],[6,466],[6,517],[6,567],[6,616],[6,666],[6,719],[6,772],[6,822],[6,873],[6,910],[6,948]],
    t2: [[2,120],[2,193],[2,308],[2,449],[2,602],[4,378],[4,434],[4,490],[4,553],[4,616],[4,658],[6,466],[6,517],[6,567],[6,616],[6,666],[6,719],[6,772],[6,822],[6,873],[8,682.5],[8,711],[8,754],[8,797],[8,841],[8,885],[8,916.5],[8,948]],
  };

  function fillMcs() {
    const t = $("tb-table").value;
    const sel = $("tb-mcs");
    // 처음에는 표의 가장 높은 MCS를, 표를 바꾸면 같은 번호(없으면 최대)를 선택
    const prev = sel.value === "" ? MCS[t].length - 1 : parseInt(sel.value, 10);
    sel.innerHTML = MCS[t].map((m, i) => `<option value="${i}">MCS ${i} — Qm ${m[0]}, R ${m[1]}/1024</option>`).join("");
    sel.value = Math.min(prev, MCS[t].length - 1);
    tbsCalc();
  }

  function tbsCalc() {
    const [qm, r1024] = MCS[$("tb-table").value][parseInt($("tb-mcs").value, 10)];
    const R = r1024 / 1024;
    const nprb = num("tb-prb");
    const nsym = num("tb-sym");
    const ndmrs = num("tb-dmrs");
    const noh = num("tb-oh");
    const v = num("tb-layers");
    const nre1 = 12 * nsym - ndmrs - noh;
    const nre = Math.min(156, nre1) * nprb;
    const ninfo = nre * R * qm * v;
    let tbs, C = 1, detail;
    if (ninfo <= 3824) {
      const n = Math.max(3, Math.floor(Math.log2(ninfo)) - 6);
      const np = Math.max(24, Math.pow(2, n) * Math.floor(ninfo / Math.pow(2, n)));
      tbs = TBS_SMALL.find((x) => x >= np);
      detail = `N_info ≤ 3824 → n = ${n}, N'_info = ${np} → 표 5.1.3.2-1`;
    } else {
      const n = Math.floor(Math.log2(ninfo - 24)) - 5;
      const np = Math.max(3840, Math.pow(2, n) * Math.round((ninfo - 24) / Math.pow(2, n)));
      if (R <= 0.25) {
        C = Math.ceil((np + 24) / 3816);
        tbs = 8 * C * Math.ceil((np + 24) / (8 * C)) - 24;
      } else if (np > 8424) {
        C = Math.ceil((np + 24) / 8424);
        tbs = 8 * C * Math.ceil((np + 24) / (8 * C)) - 24;
      } else {
        tbs = 8 * Math.ceil((np + 24) / 8) - 24;
      }
      detail = `n = ${n}, N'_info = ${np.toLocaleString("ko-KR")}, C = ${C}`;
    }
    $("tb-nre").textContent = nre.toLocaleString("ko-KR");
    $("tb-ninfo").textContent = fmt(ninfo, 1);
    $("tb-detail").textContent = detail;
    $("tb-out").textContent = Number.isFinite(tbs) ? tbs.toLocaleString("ko-KR") : "—";
  }

  function bind(ids, fn) {
    ids.forEach((id) => {
      const el = $(id);
      if (el) el.addEventListener("input", fn);
    });
  }

  function init() {
    if (!$("pr-fr")) return;
    $("pr-fr").addEventListener("change", fillScs);
    $("pr-scs").addEventListener("change", fillBw);
    bind(["pr-dir", "pr-bw", "pr-layers", "pr-qm", "pr-f", "pr-cc", "pr-ratio"], peakRate);
    fillScs();

    $("ar-n").addEventListener("input", () => arfcnCalc("n"));
    $("ar-f").addEventListener("input", () => arfcnCalc("f"));
    arfcnCalc("f");

    $("gs-g").addEventListener("input", () => gscnCalc("g"));
    $("gs-f").addEventListener("input", () => gscnCalc("f"));
    gscnCalc("f");

    $("lte-n").addEventListener("input", earfcnCalc);
    earfcnCalc();

    $("tb-table").addEventListener("change", fillMcs);
    bind(["tb-mcs", "tb-prb", "tb-sym", "tb-dmrs", "tb-oh", "tb-layers"], tbsCalc);
    fillMcs();
  }

  if (typeof document$ !== "undefined") document$.subscribe(init);
  else document.addEventListener("DOMContentLoaded", init);
})();
