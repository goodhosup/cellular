# PUSCH

!!! spec "스펙 · 릴리즈"
    TS 38.211 §6.3.1 (PUSCH 처리, transform precoding §6.3.1.4), §6.4.1.1 (PUSCH DMRS) · TS 38.212 §6.2 (UL-SCH), §6.3.2 (UCI on PUSCH) · TS 38.214 §6.1 (PUSCH 절차: 코드북/비코드북 §6.1.1, 반복 §6.1.2.1, 처리 시간 §6.4)
    Rel-15~ (Rel-16 반복 Type B·full power, Rel-17 TBoMS·DMRS 번들링·커버리지 향상, Rel-18 8Tx UL·UL 다중 패널)

!!! basic "한눈에 보기"
    **PUSCH**는 NR 상향 **데이터 채널**입니다. LTE PUSCH와 비교하면 다음이 다릅니다.

    - 파형을 두 가지 중 고릅니다: **CP-OFDM**(셀 중심, 다중 레이어) / **DFT-s-OFDM**(셀 가장자리, 낮은 PAPR)
    - **최대 4 레이어** 상향 MIMO가 기본 기능
    - HARQ가 **비동기**: 재전송도 항상 DCI로 지시 (PHICH 없음)
    - grant 없이 미리 정한 자원으로 보내는 **Configured Grant** 지원
    - 커버리지를 위한 **반복 전송**이 다양함

## 파형 선택 { .l2 }

| 항목 | CP-OFDM | DFT-s-OFDM (`transformPrecoder` enabled) |
|---|---|---|
| 레이어 | 1–4 | **1** |
| 변조 | QPSK ~ 256QAM | **π/2-BPSK**, QPSK ~ 256QAM |
| RB 할당 | Type 0/1, 자유 | Type 1 연속, \(2^a3^b5^c\) |
| PAPR / MPR | 높음 | 낮음 → 실효 출력 ↑ |
| Msg3 | SIB1 `msg3-transformPrecoder`로 지정 | |

## 전송 방식 { .l2 }

| 방식 | 프리코딩 결정 | DCI 필드 | 적합한 경우 |
|---|---|---|---|
| **코드북 기반** | 기지국이 SRS로 측정 → **TPMI**(프리코딩 행렬) + **TRI**(랭크) + SRI 지시 | Precoding information and number of layers | FDD, 상호성 약할 때 |
| **비코드북 기반** | 단말이 DL CSI-RS로 프리코딩 후보 만들어 SRS 송신 → 기지국이 **SRI**로 선택 | SRI | TDD 상호성 |

## 시간 자원과 반복 { .l2 }

| 항목 | 내용 |
|---|---|
| \(K_2\) | UL grant 슬롯 → PUSCH 슬롯 (0–32) |
| 매핑 Type A / B | A: 슬롯 시작(S=0) 4–14 심볼 / B: 아무 시작 1–14 심볼 |
| **반복 Type A** (Rel-15) | 연속 슬롯에 같은 심볼 위치로 K번 (`pusch-AggregationFactor` 또는 TDRA의 `numberOfRepetitions`) |
| **반복 Type B** (Rel-16) | 미니슬롯 단위로 **연속 이어 붙임**, 슬롯 경계·DL 심볼에서 분할 (nominal → actual repetition) |
| **TBoMS** (Rel-17) | 하나의 TB를 **여러 슬롯에 걸쳐** 전송 → 작은 패킷의 커버리지 향상 |
| 주파수 호핑 | 슬롯 내(intra-slot) / 슬롯 간(inter-slot) |

## UCI on PUSCH { .l2 }

PUCCH와 PUSCH가 같은 슬롯에서 겹치면 UCI를 PUSCH에 싣습니다.

| UCI | 배치 | 자원 양 |
|---|---|---|
| HARQ-ACK | 첫 DMRS 바로 뒤 심볼부터 (≤ 2비트면 데이터 펑처링, 초과면 레이트 매칭) | \(\beta_{offset}^{HARQ\text{-}ACK}\) |
| CSI Part 1 | ACK 다음 | \(\beta_{offset}^{CSI\text{-}1}\) |
| CSI Part 2 | 그다음 | \(\beta_{offset}^{CSI\text{-}2}\) |
| 데이터 | 나머지 | — |

\(\alpha\) (`scaling`)로 UCI가 차지할 수 있는 최대 비율을 제한합니다. UL 데이터 없이 UCI만 PUSCH로 보내는 것(비주기 CSI)도 가능합니다.

??? expert "전문가 노트 — 전력 등급, 처리 시간, 최신 기능"
    **단말 전력 등급 (FR1).** PC3 23 dBm(기본), **PC2 26 dBm**(n41, n77, n78, n79 등 TDD 밴드), PC1.5 29 dBm(Rel-17, 일부 TDD 밴드), PC1 31 dBm(FWA·고출력). TDD 상향 듀티가 작으면 평균 SAR 기준을 맞추기 쉬워 높은 등급을 허용합니다.

    **UL full power (Rel-16).** 송신 체인별 PA가 23 dBm보다 작은 단말(예: 2 × 20 dBm)도 랭크 1에서 총 23 dBm을 낼 수 있도록 모드 0/1/2(가상 포트, TPMI 그룹)를 정의했습니다.

    **처리 시간 \(N_2\).** UL grant 마지막 심볼과 PUSCH 첫 심볼 사이 최소 간격(심볼). Capability 1: μ0 10, μ1 12, μ2 23, μ3 36. Capability 2(FR1, μ 0–2): 5, 5.5, 11. URLLC 단말은 Capability 2로 지연을 줄입니다.

    **Configured Grant와 반복.** CG에도 반복(`repK` 1/2/4/8)과 RV 패턴(0000, 0303, 0231)을 쓸 수 있고, 반복 중 첫 기회 아무 곳에서 시작해 지연을 줄이는 방식이 있습니다.

    **DMRS 번들링 (Rel-17).** 여러 슬롯에 걸쳐 단말이 위상 연속성을 유지하면 기지국이 DMRS를 결합(joint channel estimation)할 수 있어 커버리지가 늘어납니다.

    **8Tx UL (Rel-18).** CPE/FWA처럼 안테나가 많은 단말을 위해 8 포트 상향 코드북·SRS를 정의했습니다. 다중 패널 동시 송신(STxMP)도 Rel-18에 포함됩니다.

## LTE ↔ NR 비교

| 항목 | LTE | NR |
|---|---|---|
| 파형 | SC-FDMA만 | CP-OFDM / DFT-s-OFDM |
| HARQ | 동기, PHICH | 비동기, DCI |
| grant → 전송 | n+4 고정 | K2 (가변) |
| 무승인 전송 | SPS (활성화 필요) | CG Type 1/2 |
| 반복 | TTI bundling (4 서브프레임) | Type A/B 반복, TBoMS |
| MIMO | 최대 4 (거의 미구현) | 최대 4 (Rel-18 8Tx 포트) |

## 관련 페이지

- [SRS](srs.md)
- [OFDMA와 DFT-s-OFDM](../../basics/ofdma-scfdma.md)
- [전력 제어](power-control.md)
- [PUCCH와 UCI](pucch.md)
- [LTE PUSCH](../../lte/phy/pusch.md)
