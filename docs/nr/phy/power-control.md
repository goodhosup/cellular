# 전력 제어

!!! spec "스펙 · 릴리즈"
    TS 38.213 §7 (UL 전력 제어: §7.1 PUSCH, §7.2 PUCCH, §7.3 SRS, §7.4 PRACH, §7.5 우선순위, §7.6 EN-DC 이중 연결 전력), §4.1 (DL SSB 전력) · 단말 최대 전력·MPR: TS 38.101-1 §6.2, 38.101-2 §6.2, 38.101-3 (EN-DC)
    Rel-15~ (Rel-16 동적 전력 공유 향상, Rel-17 FR2 MPE 보고·통합 TCI 연동 전력)

!!! basic "한눈에 보기"
    NR 상향 전력 제어의 기본 원리는 LTE와 같습니다. **개루프**(경로 손실 추정) + **폐루프**(기지국 TPC 명령).

    NR에서 달라진 점:

    - **빔마다 경로 손실이 다릅니다.** 그래서 어떤 하향 신호(SSB 또는 CSI-RS)로 경로 손실을 잴지 여러 개 중 고릅니다.
    - **numerology**가 바뀌면 RB 폭이 바뀌므로 식에 \(2^\mu\) 항이 들어갑니다.
    - 폐루프를 **2개** 따로 운영할 수 있습니다(서로 다른 서비스·빔).
    - NSA(EN-DC)에서는 LTE와 NR 상향이 **전력을 나눠 써야** 합니다.

## PUSCH 전력 { .l2 }

\[
P_{PUSCH} = \min\Big\{P_{CMAX},\ P_{O\_PUSCH}(j) + 10\log_{10}\big(2^{\mu} M_{RB}^{PUSCH}\big) + \alpha(j)\,PL(q_d) + \Delta_{TF} + f(l)\Big\}
\]

| 항 | 의미 | NR에서 새로운 점 |
|---|---|---|
| \(j\) | 파라미터 집합 (0: Msg3, 1: grant-free, 2+: 일반) | 여러 \(P_O\), \(\alpha\) 집합 |
| \(2^{\mu} M_{RB}\) | 대역폭 (SCS 반영) | \(2^{\mu}\) |
| \(PL(q_d)\) | 경로 손실 기준 RS \(q_d\) (SSB 또는 CSI-RS) | **빔별** 경로 손실 (최대 4개, Rel-16 최대 64개 설정) |
| \(f(l)\) | 폐루프 상태, \(l\) = 0 또는 1 | **2개 루프** |
| SRI | DCI의 SRI가 \(j\), \(q_d\), \(l\)을 한 번에 고름 | 빔 → 전력 파라미터 연동 |

TPC: 누적 {−1, 0, +1, +3} dB / 절대 {−4, −1, +1, +4} dB (LTE와 같음).

## 기타 채널 { .l2 }

| 채널 | 전력 식 요지 |
|---|---|
| PUCCH | \(P_{O\_PUCCH} + 10\log_{10}(2^\mu M_{RB}) + PL + \Delta_{F\_PUCCH}(F) + \Delta_{TF} + g(l)\) — \(\alpha\) = 1 고정 |
| SRS | \(P_{O\_SRS} + 10\log_{10}(2^\mu M_{SRS}) + \alpha_{SRS} PL + h(l)\) — PUSCH 루프 공유 또는 별도 |
| PRACH | \(\min\{P_{CMAX}, P_{PRACH,target} + PL\}\) — PL 기준은 선택한 SSB |
| DL | SIB1 `ss-PBCH-BlockPower`(SSB EPRE), CSI-RS는 `powerControlOffsetSS`로 SSB 대비 오프셋 |

## EN-DC 전력 공유 { .l2 }

| 방식 | 설명 |
|---|---|
| 반정적 분할 | `p-MaxEUTRA`, `p-NR-FR1`로 각 RAT 최대값 설정 (합이 \(P_{CMAX}\) 이하) |
| **동적 전력 공유 (DPS)** | 합이 넘으면 NR 전력을 줄임 (LTE 우선) — 단말 능력 |
| **단일 UL 전송 (TDM 패턴)** | 혼변조(IMD) 문제 밴드 조합에서 LTE와 NR이 같은 시간에 송신하지 않음 (`tdm-PatternConfig`) |

예: B3 + n78 조합은 2차 혼변조가 수신 대역에 떨어지는 문제가 있어 단일 UL이나 전력 제한을 씁니다.

??? expert "전문가 노트 — 우선순위, MPE, PHR"
    **전력 부족 시 우선순위 (TS 38.213 §7.5).** 합이 \(P_{CMAX}\)를 넘으면 다음 순서로 보호하고 낮은 것부터 줄이거나 버립니다:
    PCell PRACH > HARQ-ACK·SR(또는 LRR)이 실린 PUCCH/PUSCH > CSI 실린 PUCCH/PUSCH > UCI 없는 PUSCH > SRS(비주기 > 반지속/주기) > PCell 외 PRACH. Rel-16 이후 고우선/저우선 트래픽 구분이 추가되었습니다.

    **MPE (Maximum Permissible Exposure, FR2).** 손이나 몸이 안테나 앞에 있으면 인체 노출 규제 때문에 출력을 줄여야 합니다(P-MPR). Rel-16/17에서 단말이 P-MPR 값과 영향받지 않는 빔을 **PHR MAC CE에 보고**해 기지국이 다른 패널·빔으로 전환하게 했습니다.

    **경로 손실 RS 수 제한.** 단말이 동시에 추적해야 하는 PL RS가 많으면 측정 부담이 커서, Rel-15는 최대 4개, Rel-16은 최대 64개 설정 중 MAC CE로 활성화된 것만 추적하게 했습니다.

    **Msg3 전력.** \(P_{O\_PUSCH}(0) = P_{O\_PRE} + \Delta_{PREAMBLE\_Msg3}\), \(\alpha\) = `msg3-Alpha`, 폐루프 초기값은 RA 램핑 누적분 + RAR의 TPC.

    **TDD에서 상향 듀티와 전력 등급.** PC2(26 dBm) 단말은 SAR 규제상 상향 듀티 50% 이하 등에서만 최대 출력을 유지합니다(`maxUplinkDutyCycle-PC2-FR1`). 듀티가 높으면 PC3 수준으로 되돌아갑니다.

## 관련 페이지

- [PUSCH](pusch.md)
- [MAC](../protocol/mac.md) — PHR
- [NSA와 SA](../architecture/nsa-sa.md)
- [LTE 전력 제어](../../lte/phy/power-control.md)
