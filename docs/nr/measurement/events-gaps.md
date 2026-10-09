# 측정 이벤트와 갭

!!! spec "스펙 · 릴리즈"
    측정 설정·이벤트: TS 38.331 §5.5 (§5.5.4 이벤트 A1–A6, B1–B2, I1, C1–C2, D1, T1, X1–X2, Y1–Y2) · 측정 갭: TS 38.133 §9.1.2 (Table 9.1.2-1 갭 패턴), TS 38.331 `MeasGapConfig` · 갭 없는 측정: TS 38.133 §9.2
    Rel-15 A1–A6·B1·B2 → Rel-16 CHO 조건 이벤트·CLI 이벤트 I1 → Rel-17 NTN D1·T1, **사전 설정 갭·동시 갭·NCSG** → Rel-18 LTM L1 측정 보고

!!! basic "한눈에 보기"
    NR 측정 이벤트는 LTE와 거의 같습니다. "옆 셀이 더 좋아지면(A3) 알려라", "지금 셀이 나빠지면(A2) 다른 주파수를 재라" 같은 규칙입니다. NR에서 달라진 점은 다음과 같습니다.

    - 측정값이 **빔 단위로 모은 셀 품질**입니다.
    - 위성(NTN)용 **거리(D1)·시간(T1)** 이벤트가 생겼습니다.
    - **측정 갭**이 FR1·FR2별로 나뉘고, 갭이 꼭 필요한지 여부가 단말 능력과 BWP 설정에 따라 달라집니다.

## 이벤트 목록 { .l2 }

| 이벤트 | 조건 | 주 용도 |
|---|---|---|
| A1 / A2 | 서빙 > / < 임계값 | 갭 해제 / 다른 주파수 측정 시작 |
| **A3** | 이웃 > SpCell + 오프셋 | 핸드오버, **CHO 실행 조건** |
| A4 | 이웃 > 임계값 | 부하 분산, SCell·SN 추가 |
| **A5** | SpCell < 임계값1 그리고 이웃 > 임계값2 | 다른 주파수 HO, CHO 조건 |
| A6 | 이웃 > SCell + 오프셋 | SCell 교체 |
| **B1** | 다른 RAT 이웃 > 임계값 | **EPS Fallback**, LTE 연동 |
| B2 | SpCell < 임계값1 그리고 다른 RAT > 임계값2 | LTE로 HO |
| I1 (Rel-16) | CLI 간섭 > 임계값 | 동적 TDD |
| C1 / C2 (Rel-16) | 채널 점유율 기반 | NR-U |
| **D1** (Rel-17) | 서빙 셀 기준점과의 거리 > 임계값1 그리고 후보 기준점 거리 < 임계값2 | **NTN** 이동성 |
| **T1** (Rel-17) | 시간이 특정 구간에 들어감 | NTN (위성 통과 시점) |

이벤트 수식, 히스테리시스, TTT의 의미는 LTE와 같습니다 → [LTE 측정 이벤트](../../lte/measurement/events.md)

## MeasObjectNR 주요 필드 { .l2 }

| 필드 | 의미 |
|---|---|
| `ssbFrequency`, `ssbSubcarrierSpacing` | 측정할 SSB 위치·SCS |
| `smtc1`, `smtc2` | 측정 창 |
| `refFreqCSI-RS` | CSI-RS 기반 측정 시 기준 |
| `referenceSignalConfig` | 측정할 SSB 인덱스 집합 (`ssb-ToMeasure`), CSI-RS 자원 |
| `absThreshSS-BlocksConsolidation`, `nrofSS-BlocksToAverage` | 셀 품질 도출 규칙 |
| `quantityConfigIndex`, `offsetMO` | 필터·오프셋 |
| `cellsToAddModList` | 셀별 오프셋(CIO) |
| `excludedCellsToAddModList` / `allowedCellsToAddModList` | 블랙/화이트리스트 |

## 측정 갭 { .l2 }

| 항목 | 값 |
|---|---|
| 갭 반복 주기 (MGRP) | 20, 40, 80, 160 ms |
| 갭 길이 (MGL) | 1.5, 3, 3.5, 4, 5.5, 6 ms (Rel-16 이후 10, 20 ms 추가) |
| 갭 패턴 ID | 0 – 23 (MGL × MGRP 조합) |
| 갭 유형 | **per-UE** (모든 서빙 셀 중단) / **per-FR** (FR1용·FR2용 따로, `gapFR1`, `gapFR2`) |
| 타이밍 보정 | `mgta` (갭 시작 0.5 ms / 0.25 ms 앞당김) |

**갭이 필요 없는 경우**: 측정할 SSB가 단말의 **활성 BWP 안에 있고 SCS가 같으면** 갭 없이 측정(intra-frequency)합니다. SSB가 BWP 밖이거나 SCS가 다르면 갭이 필요할 수 있습니다(단말 능력에 따라).

??? expert "전문가 노트 — Rel-17 갭 향상과 실무"
    **사전 설정 갭 (Pre-configured gap, Rel-17).** 갭을 설정만 해 두고, BWP 전환으로 측정 대상 SSB가 활성 BWP 밖이 될 때만 자동으로 활성화합니다. 불필요한 갭 낭비를 줄입니다.

    **동시 갭 (Concurrent gaps, Rel-17).** 서로 다른 주파수·RAT·PRS 측정을 위해 여러 갭 패턴을 동시에 둡니다(최대 수는 단말 능력).

    **NCSG (Network Controlled Small Gap, Rel-17).** 서빙 셀 송수신을 완전히 멈추지 않고 RF 재조정에 필요한 짧은 **중단 구간(VIL)**만 두는 방식입니다. 추가 수신 체인이 있는 단말에 유리합니다.

    **측정 스케일링(CSSF).** 측정할 주파수가 많으면 단말 측정 능력을 나눠 쓰므로 측정 지연 요구사항이 CSSF(Carrier-Specific Scaling Factor)만큼 늘어납니다. 측정 대상 주파수를 너무 많이 설정하면 핸드오버가 늦어질 수 있습니다.

    **EPS Fallback.** SA에서 VoNR을 지원하지 않는 경우, IMS 음성 QoS 플로우(5QI 1) 생성 요청이 오면 gNB가 B1 측정(또는 블라인드)으로 LTE로 핸드오버/리디렉션하고 VoLTE로 통화합니다. B1 임계값과 측정 속도가 통화 연결 시간을 좌우합니다.

## 관련 페이지

- [SS-RSRP·RSRQ·SINR](ss-rsrp.md)
- [핸드오버 (CHO·DAPS·LTM)](../procedures/handover.md)
- [NTN](../advanced/ntn.md)
- [LTE 측정 이벤트](../../lte/measurement/events.md)
