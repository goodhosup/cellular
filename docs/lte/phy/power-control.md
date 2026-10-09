# 전력 제어

!!! spec "스펙 · 릴리즈"
    상향 전력 제어: TS 36.213 §5.1 (PUSCH §5.1.1, PUCCH §5.1.2, SRS §5.1.3), §6.1 (PRACH) · 하향 전력 할당: §5.2 · 단말 최대 전력·MPR: TS 36.101 §6.2

    Rel-8~ (Rel-10 CA 전력 우선순위, Rel-12 DC 전력 공유)

!!! basic "한눈에 보기"
    **상향 전력 제어**는 단말 송신 전력을 "딱 필요한 만큼"으로 맞추는 기술입니다.

    - 너무 약하면 기지국이 못 받습니다.
    - 너무 세면 배터리를 낭비하고, **이웃 셀에 간섭**을 줍니다.

    두 가지를 섞어서 씁니다.

    1. **개루프(open loop)**: 단말이 하향 신호 세기로 거리(경로 손실)를 추정해서 스스로 정합니다.
    2. **폐루프(closed loop)**: 기지국이 받은 세기를 보고 "올려(+1 dB)", "내려(−1 dB)" 명령(**TPC**)을 보냅니다.

    LTE 단말의 최대 송신 전력은 보통 **23 dBm (200 mW, Power Class 3)**입니다.

## PUSCH 전력 { .l2 }

\[
P_{PUSCH}(i) = \min\Big\{ P_{CMAX},\ 10\log_{10} M_{PUSCH}(i) + P_{O\_PUSCH}(j) + \alpha(j)\cdot PL + \Delta_{TF}(i) + f(i) \Big\} \ \text{[dBm]}
\]

| 항 | 의미 | 설정 |
|---|---|---|
| \(M_{PUSCH}\) | 할당 RB 수 → RB가 많으면 전력도 비례해서 증가 | DCI |
| \(P_{O\_PUSCH}\) | RB당 목표 수신 전력 (셀 공통 + 단말별) | SIB2 / RRC (예: −80 ~ −100 dBm) |
| \(\alpha\) | 경로 손실 보상 비율 | 0, 0.4, 0.5, …, 1 |
| \(PL\) | 경로 손실 = `referenceSignalPower` − 필터링된 RSRP | 단말 측정 |
| \(\Delta_{TF}\) | MCS(비트/RE)가 높을수록 추가 전력 | `deltaMCS-Enabled` |
| \(f(i)\) | 폐루프 TPC 누적값 | DCI 0/3/3A |

### 부분 경로 손실 보상 (Fractional PC)

\(\alpha = 1\)이면 모든 단말이 같은 전력으로 수신되도록 완전히 보상합니다. \(\alpha < 1\)(예: 0.8)이면 셀 가장자리 단말은 덜 보상받아 **이웃 셀 간섭이 줄고**, 셀 중심 단말은 높은 SINR로 높은 MCS를 씁니다. 전체 셀 처리량이 좋아지는 경우가 많아 실무에서 흔히 씁니다.

## PUCCH 전력 { .l2 }

\[
P_{PUCCH}(i) = \min\Big\{ P_{CMAX},\ P_{O\_PUCCH} + PL + h(n_{CQI}, n_{HARQ}, n_{SR}) + \Delta_{F\_PUCCH}(F) + \Delta_{TxD}(F') + g(i) \Big\}
\]

PUCCH는 항상 **경로 손실을 완전히 보상**합니다(\(\alpha = 1\)). 제어 정보는 꼭 받아야 하기 때문입니다.
\(\Delta_{F\_PUCCH}\)는 포맷별 보정(format 1a 기준), \(h(\cdot)\)는 실린 비트 수에 따른 보정입니다.

## TPC 명령 { .l2 }

| 모드 | 2비트 TPC 값 → δ | 쓰임 |
|---|---|---|
| **누적 (accumulated)** | −1, 0, +1, +3 dB | 기본. \(f(i) = f(i-1) + \delta\) |
| **절대 (absolute)** | −4, −1, +1, +4 dB | `accumulationEnabled` = false |
| DCI 3A (1비트) | −1, +1 dB | 그룹 TPC |

누적 모드에서는 단말이 \(P_{CMAX}\)에 도달하면 양의 TPC를, 최소 전력에 도달하면 음의 TPC를 더 쌓지 않습니다.

## 기타 채널 { .l2 }

| 채널 | 전력 식 |
|---|---|
| SRS | \(\min\{P_{CMAX},\ P_{SRS\_OFFSET} + 10\log_{10}M_{SRS} + P_{O\_PUSCH} + \alpha \cdot PL + f(i)\}\) — PUSCH 폐루프 공유 |
| PRACH | \(\min\{P_{CMAX},\ \text{목표 수신 전력} + PL\}\), 재시도마다 ramping |
| 하향 | CRS EPRE (`referenceSignalPower`) 기준 \(\rho_A\), \(\rho_B\) → [PDSCH](pdsch.md#하향-전력-할당) |

??? expert "전문가 노트 — P_CMAX, PHR, CA 전력"
    **\(P_{CMAX}\) 범위 (TS 36.101 §6.2.5).**

    \[
    P_{CMAX\_L} \le P_{CMAX} \le P_{CMAX\_H}, \quad
    P_{CMAX\_L} = \min\{P_{EMAX} - \Delta T_C,\ P_{PowerClass} - \max(MPR + A\text{-}MPR + \Delta T_{IB}, P\text{-}MPR) - \Delta T_C\}
    \]

    - **MPR**: 변조·RB 할당에 따른 허용 감소 (예: QPSK 대역 넓게 할당 시 ≤ 1 dB, 16QAM ≤ 1–2 dB)
    - **A-MPR**: 망이 `additionalSpectrumEmission`(NS 값)으로 요구하는 추가 감소 (인접 대역 보호)
    - **P-MPR**: 인체 SAR 규제 등으로 단말이 스스로 줄이는 값
    - \(P_{EMAX}\): 셀이 허용하는 최대 (SIB1 `p-Max`)

    **PHR와의 관계.** 단말은 \(PH = P_{CMAX} - P_{PUSCH,\text{계산값}}\)을 보고합니다. 음수면 이미 최대 전력에서 부족하다는 뜻이므로 스케줄러는 RB 수나 MCS를 줄여야 합니다.

    **CA 전력 제한 (Rel-10).** 총 전력이 \(P_{CMAX}\)를 넘으면 우선순위대로 줄입니다:
    PRACH(PCell) > PUCCH > UCI가 실린 PUSCH > 나머지 PUSCH(셀 간 동일 비율 스케일링). Rel-12 DC에서는 MCG/SCG 간 보장 전력(`p-MeNB`, `p-SeNB`)과 동기/비동기 전력 공유 모드(PCM1/PCM2)가 추가되었습니다.

    **TPC 누적 리셋.** \(P_{O\_UE\_PUSCH}\) 변경, 랜덤 액세스 응답 수신 시 \(f(0) = \Delta P_{rampup} + \delta_{msg2}\)로 초기화됩니다(Msg3 전력은 RACH 마지막 전력 기준).

    **경로 손실 필터링.** RSRP는 `filterCoefficient`(L3 필터)로 평균한 값을 씁니다. CA SCell의 경로 손실 기준은 `pathlossReferenceLinking`으로 PCell 또는 해당 SCell DL을 고릅니다.

## 관련 페이지

- [PUSCH](pusch.md)
- [PUCCH와 UCI](pucch.md)
- [MAC](../protocol/mac.md) — PHR
- [RSRP·RSRQ·SINR](../measurement/rsrp-rsrq.md)
