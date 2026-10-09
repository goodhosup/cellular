# 계산기

!!! spec "계산식 출처"
    NR 최대 데이터율: TS 38.306 §4.1.2 · NR-ARFCN: TS 38.101-1 §5.4.2.1 · GSCN: TS 38.101-1 Table 5.4.3.1-1 · LTE EARFCN: TS 36.101 Table 5.7.3-1 · NR TBS: TS 38.214 §5.1.3.2, MCS 표 5.1.3.1-1/-2

!!! basic "사용법"
    값을 바꾸면 결과가 바로 갱신됩니다. 모든 계산은 브라우저에서만 이루어집니다. 결과는 규격 공식을 그대로 옮긴 값이지만, 실무 판단 전에는 원문 규격으로 다시 확인하세요.

## NR 최대 데이터율 { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>주파수 범위
      <select id="pr-fr"><option value="FR1">FR1</option><option value="FR2">FR2</option></select>
    </label>
    <label>방향
      <select id="pr-dir"><option value="DL">하향 (DL)</option><option value="UL">상향 (UL)</option></select>
    </label>
    <label>부반송파 간격
      <select id="pr-scs"></select>
    </label>
    <label>채널 대역폭
      <select id="pr-bw"></select>
    </label>
    <label>레이어 수
      <input id="pr-layers" type="number" min="1" max="8" value="4">
    </label>
    <label>변조
      <select id="pr-qm"><option value="2">QPSK</option><option value="4">16QAM</option><option value="6">64QAM</option><option value="8" selected>256QAM</option><option value="10">1024QAM</option></select>
    </label>
    <label>스케일링 계수 f
      <select id="pr-f"><option value="1" selected>1</option><option value="0.8">0.8</option><option value="0.75">0.75</option><option value="0.4">0.4</option></select>
    </label>
    <label>캐리어 수 (같은 구성)
      <input id="pr-cc" type="number" min="1" max="16" value="1">
    </label>
    <label>TDD 해당 방향 비율 (%)
      <input id="pr-ratio" type="number" min="1" max="100" value="74">
    </label>
  </div>
  <div class="calc-result">
    <div>RB 수 <b id="pr-nprb">—</b> · 오버헤드 <b id="pr-oh">—</b></div>
    <div class="calc-big"><span id="pr-out">—</span> Mbps <small>(모든 슬롯이 해당 방향일 때)</small></div>
    <div>TDD 비율 적용 시 <b id="pr-out-tdd">—</b> Mbps</div>
  </div>
</div>

## NR-ARFCN ↔ 주파수 { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>NR-ARFCN
      <input id="ar-n" type="number" min="0" max="3279165" value="640000">
    </label>
    <label>주파수 (MHz)
      <input id="ar-f" type="number" step="0.001" value="3600">
    </label>
  </div>
  <div class="calc-result"><span id="ar-note"></span></div>
</div>

## GSCN ↔ SSB 기준 주파수 { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>GSCN
      <input id="gs-g" type="number" min="2" max="26639" value="7846">
    </label>
    <label>SS_REF (MHz)
      <input id="gs-f" type="number" step="0.001" value="3499.68">
    </label>
  </div>
  <div class="calc-result"><span id="gs-note"></span></div>
</div>

## LTE EARFCN → 주파수 { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>DL EARFCN
      <input id="lte-n" type="number" min="0" max="43589" value="1350">
    </label>
  </div>
  <div class="calc-result"><b id="lte-out">—</b></div>
</div>

## NR TBS { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>MCS 표
      <select id="tb-table"><option value="t1">표 1 (64QAM)</option><option value="t2" selected>표 2 (256QAM)</option></select>
    </label>
    <label>MCS
      <select id="tb-mcs"></select>
    </label>
    <label>PRB 수
      <input id="tb-prb" type="number" min="1" max="275" value="273">
    </label>
    <label>PDSCH 심볼 수
      <input id="tb-sym" type="number" min="1" max="14" value="12">
    </label>
    <label>PRB당 DMRS RE
      <input id="tb-dmrs" type="number" min="0" max="72" value="12">
    </label>
    <label>xOverhead
      <select id="tb-oh"><option value="0">0</option><option value="6">6</option><option value="12">12</option><option value="18">18</option></select>
    </label>
    <label>레이어 수
      <input id="tb-layers" type="number" min="1" max="4" value="4">
    </label>
  </div>
  <div class="calc-result">
    <div>N_RE <b id="tb-nre">—</b> · N_info <b id="tb-ninfo">—</b></div>
    <div><small id="tb-detail"></small></div>
    <div class="calc-big">TBS <span id="tb-out">—</span> 비트</div>
  </div>
</div>

??? expert "계산기 사용 시 주의"
    - **최대 데이터율**은 단말 능력 비교용 근사식입니다. 실제 TBS 상한 검사·셀 처리량과는 다릅니다. TDD 비율은 공식에 없는 항목이라 별도로 곱했습니다.
    - **TBS**는 코드워드 하나(레이어 1–4) 기준입니다. 5–8 레이어는 코드워드 2개로 나눠 각각 계산합니다. 레이어 수 입력은 4까지만 받습니다.
    - **NR-ARFCN**은 전역 래스터 기준입니다. 실제 사용 가능한 값은 밴드별 채널 래스터(100 kHz / 15 kHz / 30 kHz)를 따라야 합니다.
    - **GSCN**은 밴드별 허용 범위를 검사하지 않습니다(TS 38.101-1 Table 5.4.3.3-1 확인).
    - **LTE EARFCN**은 목록에 있는 주요 밴드만 지원합니다.

<script src="../../javascripts/calculators.js"></script>
