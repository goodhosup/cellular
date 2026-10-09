# NR-ARFCN과 GSCN

!!! spec "스펙 · 릴리즈"
    NR-ARFCN·채널 래스터: TS 38.101-1 §5.4.2 (FR1), 38.101-2 §5.4.2 (FR2), TS 38.104 §5.4.2 · 동기 래스터(GSCN): TS 38.101-1 §5.4.3, Table 5.4.3.1-1, 밴드별 GSCN 표 Table 5.4.3.3-1
    Rel-15~ (Rel-16 n77/n78 등 래스터 정정, Rel-17 FR2-2 래스터)

!!! basic "한눈에 보기"
    NR은 주파수를 번호로 부르는 방법이 두 가지입니다.

    - **NR-ARFCN**: 캐리어 중심·Point A 같은 **기준 주파수** 번호 (LTE의 EARFCN에 해당)
    - **GSCN** (Global Synchronization Channel Number): **SSB가 놓일 수 있는 위치** 번호

    LTE는 100 kHz마다 셀을 찾아야 했지만, NR은 SSB를 **듬성듬성한 GSCN 위치에만** 두기로 정했습니다. 단말은 GSCN 위치만 훑으면 되므로 셀 탐색이 훨씬 빠릅니다.

## NR-ARFCN { .l2 }

\[
F_{REF} = F_{REF\text{-}Offs} + \Delta F_{Global} \cdot (N_{REF} - N_{REF\text{-}Offs})
\]

| 주파수 범위 | \(\Delta F_{Global}\) | \(F_{REF\text{-}Offs}\) | \(N_{REF\text{-}Offs}\) | NR-ARFCN 범위 |
|---|---|---|---|---|
| 0 – 3000 MHz | 5 kHz | 0 MHz | 0 | 0 – 599999 |
| 3000 – 24250 MHz | 15 kHz | 3000 MHz | 600000 | 600000 – 2016666 |
| 24250 – 100000 MHz | 60 kHz | 24250.08 MHz | 2016667 | 2016667 – 3279165 |

**계산 예**

| 주파수 | NR-ARFCN |
|---|---|
| 1842.5 MHz (n3) | 1842.5 / 0.005 = **368500** |
| 2140 MHz (n1) | **428000** |
| 3600 MHz (n78) | 600000 + 600 / 0.015 = **640000** |
| 28000.08 MHz (n257) | 2016667 + 3750 / 0.06 = **2079167** |

밴드마다 실제로 쓸 수 있는 **채널 래스터**(\(\Delta F_{Raster}\))가 따로 있습니다. 예: n78은 15 kHz(또는 30 kHz) 래스터, LTE 재배치 밴드(n1, n3 등)는 100 kHz 래스터(LTE와 같은 중심 주파수 가능).

## GSCN (동기 래스터) { .l2 }

| 주파수 범위 | SSB 기준 주파수 \(SS_{REF}\) | GSCN | 간격 |
|---|---|---|---|
| 0 – 3000 MHz | \(N \times 1200\,\text{kHz} + M \times 50\,\text{kHz}\), \(N\) = 1–2499, \(M \in \{1, 3, 5\}\) | \(3N + (M-3)/2\) | 1.2 MHz |
| 3000 – 24250 MHz | \(3000\,\text{MHz} + N \times 1.44\,\text{MHz}\), \(N\) = 0–14756 | \(7499 + N\) | **1.44 MHz** |
| 24250 – 100000 MHz | \(24250.08\,\text{MHz} + N \times 17.28\,\text{MHz}\), \(N\) = 0–4383 | \(22256 + N\) | **17.28 MHz** |

**계산 예**

| SSB 중심 | GSCN |
|---|---|
| 2139.75 MHz (N = 1783, M = 3) | 3 × 1783 + 0 = **5349** |
| 3499.68 MHz (N = 347) | 7499 + 347 = **7846** |
| 3600.48 MHz (N = 417) | **7916** |
| 27999.84 MHz (N = 217) | 22256 + 217 = **22473** |

\(SS_{REF}\)는 SSB의 **부반송파 120번**(20 RB 중 RB 10의 부반송파 0)의 중심 주파수입니다.

## 탐색 후보 수 비교 { .l2 }

100 MHz 폭의 n78 일부를 훑는다고 할 때:

| 방식 | 간격 | 후보 수 |
|---|---|---|
| LTE식 채널 래스터 | 100 kHz | 약 1000 |
| NR GSCN | 1.44 MHz | 약 **70** |

밴드별로 허용 GSCN 범위와 간격(예: n77은 GSCN 7711–8329, n78은 7711–8051, 간격 1)이 TS 38.101-1 Table 5.4.3.3-1에 정의됩니다.

??? expert "전문가 노트 — SSB와 캐리어 정렬"
    **SSB가 CRB 격자와 어긋나는 이유.** GSCN은 1.44 MHz 간격이고, 캐리어의 CRB 격자는 RB(30 kHz × 12 = 360 kHz) 단위입니다. 그래서 SSB의 첫 부반송파가 CRB 경계와 맞지 않을 수 있고, 그 차이를 **\(k_{SSB}\)**(부반송파 단위)로 알려 줍니다. → [리소스 그리드와 Point A](../phy/resource-grid.md)

    **NSA 앵커 정보.** EN-DC에서는 LTE RRC의 `MeasObjectNR.ssbFrequency`(NR-ARFCN 표기)로 SSB 위치를 알려 줍니다. 이때 SSB는 GSCN 위에 있지 않아도 됩니다(셀 정의 SSB가 아닌 경우).

    **채널 래스터와 Point A.** `absoluteFrequencyPointA`와 `absoluteFrequencySSB`는 NR-ARFCN으로 표현됩니다. SSB의 NR-ARFCN은 \(SS_{REF}\)와 같은 주파수의 NR-ARFCN 값입니다.

    **FR2-2 (Rel-17).** 480/960 kHz SSB를 위해 FR2-2 전용 GSCN 간격과 밴드 n263의 동기 래스터가 정의되었습니다. 2 GHz 채널에서도 탐색 후보 수를 관리하기 위해 간격이 넓습니다.

    **LTE 재배치 밴드의 7.5 kHz.** LTE와 같은 대역의 NR UL에서 부반송파를 LTE UL 격자와 맞추려면 \(\Delta_{shift}\) = 7.5 kHz가 필요할 수 있습니다(`frequencyShift7p5khz`). NR-ARFCN 정의식 자체는 바뀌지 않고 RF 래스터 오프셋으로 처리합니다.

## 관련 페이지

- [FR1·FR2와 밴드](bands.md)
- [SSB 구조](../phy/ssb.md)
- [초기 접속](../procedures/initial-access.md)
- [LTE 리소스 그리드](../../lte/phy/resource-grid.md) — EARFCN
