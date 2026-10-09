# 참조신호 (CRS · DMRS · CSI-RS · SRS)

!!! spec "스펙 · 릴리즈"
    DL: TS 36.211 §6.10 (CRS §6.10.1, MBSFN-RS §6.10.2, UE-RS/DMRS §6.10.3, PRS §6.10.4, CSI-RS §6.10.5) · UL: §5.5 (DMRS §5.5.2, SRS §5.5.3) · SRS 절차: TS 36.213 §8.2

    Rel-8 CRS·UE-RS(포트 5)·SRS → Rel-9 PRS·포트 7/8 → Rel-10 CSI-RS·포트 7–14·비주기 SRS → Rel-13/14 FD-MIMO CSI-RS 최대 32포트

!!! basic "한눈에 보기"
    수신기가 데이터를 제대로 읽으려면 **채널이 신호를 어떻게 바꿨는지** 알아야 합니다. 그래서 송신기는 수신기가 **미리 알고 있는 값**을 정해진 위치에 섞어 보냅니다. 이것이 **참조신호(RS, Reference Signal)**, 또는 파일럿입니다.

    | 참조신호 | 방향 | 하는 일 |
    |---|---|---|
    | **CRS** | 하향 | 셀의 모든 단말이 쓰는 공통 기준. 채널 추정, 측정(RSRP), 복조 |
    | **DMRS (UE-RS)** | 하향 | 특정 단말의 데이터와 같은 빔으로 보냄 → 빔포밍 데이터 복조 |
    | **CSI-RS** | 하향 | 채널 상태 측정 전용 (드문드문, 많은 안테나 포트) |
    | **PRS** | 하향 | 단말 위치 측정 |
    | **DMRS** | 상향 | PUSCH, PUCCH 복조 |
    | **SRS** | 상향 | 기지국이 단말의 상향 채널을 측정 (주파수 스케줄링, TDD 빔포밍) |

## 하향 안테나 포트 { .l2 }

| 포트 | 참조신호 | 용도 |
|---|---|---|
| 0–3 | CRS | 셀 공통, TM1–6 복조, 측정 |
| 4 | MBSFN-RS | PMCH |
| 5 | UE-specific RS | TM7 |
| 6 | PRS | 측위 (OTDOA) |
| 7–14 | DMRS | TM8 (7, 8), TM9/10 (7–14) |
| 15–22 (최대 15–46) | CSI-RS | TM9/10 CSI 측정 (Rel-13/14에서 최대 32포트) |
| 107–110 | ePDCCH DMRS | Rel-11 |

## CRS { .l2 }

<figure markdown>
![RB 안의 CRS 배치](../../assets/figures/lte_rb_crs.svg)
<figcaption>2포트 CRS 배치 (v_shift = 0). 포트 0·1은 각 슬롯의 심볼 0과 4에, 주파수 방향 6 부반송파 간격으로 서로 엇갈려 놓입니다. 포트 2·3은 각 슬롯의 심볼 1에 놓입니다.</figcaption>
</figure>

| 포트 수 | RB 쌍당 CRS RE | 오버헤드 |
|---|---|---|
| 1 | 8 | 4.8 % |
| 2 | 16 | 9.5 % |
| 4 | 24 | 14.3 % |

포트 0/1은 RB 쌍당 8 RE씩, 포트 2/3은 4 RE씩입니다(포트 2/3은 채널 추정 정확도가 낮아 고속 이동에 약함).
주파수 위치는 \(v_{shift} = N_{ID}^{cell} \bmod 6\)만큼 이동합니다. CRS는 **모든 서브프레임, 전체 대역**에 항상 전송되므로(MBSFN 서브프레임 제외) 빈 셀도 간섭을 냅니다.

## CSI-RS (Rel-10) { .l2 }

CRS로는 안테나 4개까지만 측정할 수 있어서, 8포트 MIMO를 위해 **드문드문 보내는** 측정 전용 신호를 추가했습니다.

| 항목 | 값 |
|---|---|
| 밀도 | 포트당 RB 쌍당 1 RE |
| 주기 | 5, 10, 20, 40, 80 ms (`subframeConfig`) |
| 포트 | 1, 2, 4, 8 (Rel-13: 12, 16 / Rel-14: 20, 24, 28, 32) |
| ZP CSI-RS | 데이터를 비워 두는 자리 (이웃 셀 CSI-RS 보호, 간섭 측정) |
| CSI-IM (Rel-11) | ZP 위치에서 간섭만 측정 (TM10 CoMP) |

## 상향 참조신호 { .l2 }

| 신호 | 위치 | 대역 | 시퀀스 |
|---|---|---|---|
| PUSCH DMRS | 각 슬롯 심볼 3 (Normal CP) | PUSCH와 같은 RB | ZC 기반, 30 그룹, 순환 이동 |
| PUCCH DMRS | format 1: 심볼 2–4 / format 2: 심볼 1, 5 | PUCCH RB | 길이 12 시퀀스 + 순환 이동 |
| **SRS** | **서브프레임 마지막 심볼** (TDD는 UpPTS도) | 설정 대역 (최대 전체) | ZC 기반, comb 2 (Rel-13: comb 4) |

### SRS 설정

| 파라미터 | 의미 |
|---|---|
| `srs-SubframeConfig` (SIB2) | 셀의 SRS 서브프레임 (모든 단말이 이 심볼을 비움) |
| `srs-BandwidthConfig` \(C_{SRS}\), `srs-Bandwidth` \(B_{SRS}\) | SRS 대역 크기 (트리 구조) |
| `srs-HoppingBandwidth` \(b_{hop}\) | 주파수 호핑 범위 |
| `srs-ConfigIndex` | 단말별 주기 (2–320 ms)와 오프셋 |
| `transmissionComb` | 짝수/홀수 부반송파 (단말 다중화) |
| `cyclicShift` (0–7) | 같은 comb 단말 구분 |
| 비주기 SRS (Rel-10) | DCI 0/4/1A/2B/2C/2D의 SRS request 필드로 트리거 |

??? expert "전문가 노트 — 시퀀스 초기화와 설계 이슈"
    **CRS 시퀀스.** QPSK Gold 시퀀스로, 심볼마다 초기값

    \[
    c_{init} = 2^{10}\,(7(n_s+1) + l + 1)(2N_{ID}^{cell}+1) + 2N_{ID}^{cell} + N_{CP}
    \]

    (\(N_{CP}\) = 1 Normal, 0 Extended). 길이 \(2N_{RB}^{max}\) = 220 시퀀스를 만들고, 실제 대역의 중앙 부분을 잘라 씁니다. 그래서 단말은 셀 대역폭과 관계없이 중앙 6 RB의 CRS로 측정할 수 있습니다.

    **CRS 간섭과 대책.** 부하가 없어도 CRS는 간섭을 냅니다. 이웃 셀의 CRS가 같은 위치(같은 v_shift)면 CRS끼리, 다르면 이웃 CRS가 PDSCH를 때립니다.
    - Rel-11 FeICIC: 단말 **CRS-IC**(간섭 셀 CRS를 재생성해 제거)
    - Rel-12 NAICS: 간섭 셀 파라미터 시그널링
    - NR이 CRS를 없앤 가장 큰 이유입니다. LTE–NR **DSS**에서는 NR이 LTE CRS 자리를 레이트 매칭으로 피합니다(`lte-CRS-ToMatchAround`).

    **DMRS (포트 7–14).** RB 쌍당 12 RE(포트 7–10, CDM) 또는 24 RE(포트 7–14). 길이 2/4의 OCC로 코드 분할합니다. `n_SCID`로 두 가지 스크램블 ID를 써서 MU-MIMO 단말 간 비직교 다중화를 지원합니다.

    **SRS 용량.** comb 2 × 순환 이동 8 = SRS 심볼당 같은 대역에 최대 16개 단말. Massive MIMO TDD에서는 SRS 용량이 병목이 되어 Rel-13에서 **comb 4**, UpPTS 추가 심볼(최대 6 심볼, Rel-13), Rel-14 **SRS 캐리어 전환**(PUSCH 없는 TDD SCell에 SRS 송신)이 추가되었습니다.

    **PRS (Rel-9 OTDOA).** PRS 서브프레임에서는 PDSCH를 비우고(저간섭 서브프레임) 대역 전체에 대각선 패턴으로 PRS를 보냅니다. 단말은 여러 셀 PRS의 도착 시간 차(RSTD)를 측정해 E-SMLC에 보고합니다(LPP, TS 36.355).

## LTE ↔ NR 비교

| 항목 | LTE | NR |
|---|---|---|
| 항상 켜진 공통 RS | **CRS** (모든 서브프레임) | **없음** (SSB만 주기적) |
| 데이터 복조 | CRS (TM1–6) 또는 DMRS (TM7–10) | **항상 DMRS** |
| 위상 추적 | 없음 | **PTRS** (FR2 위상 잡음) |
| 측정 | CRS (RSRP), CSI-RS | SSB (SS-RSRP), CSI-RS |
| SRS | 마지막 심볼 1개 (Rel-13 UpPTS 확장) | 슬롯 마지막 6 심볼 중 1/2/4 심볼, 용도별 집합 (CB/NCB/빔 관리/안테나 전환) |

## 관련 페이지

- [리소스 그리드](resource-grid.md)
- [RSRP·RSRQ·SINR](../measurement/rsrp-rsrq.md)
- [CQI·PMI·RI](../measurement/csi.md)
- [NR DMRS·PTRS](../../nr/phy/dmrs-ptrs.md)
