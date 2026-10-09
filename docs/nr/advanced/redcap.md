# RedCap (Reduced Capability)

!!! spec "스펙 · 릴리즈"
    개요: TS 38.300 §16.13 · 단말 능력: TS 38.306 §4.2.21 · 초기 접속·BWP: TS 38.331 (`redCap-ConfigCommon`, `cellBarredRedCap`), TS 38.213 · eDRX: TS 38.304 · 연구: TR 38.875 (Rel-17), TR 38.865 (Rel-18)
    Rel-17 **RedCap** → Rel-18 **eRedCap** (5 MHz 기저대역, 약 10 Mbps) → Rel-19 RedCap 확장 (NTN·측위 등)

!!! basic "한눈에 보기"
    5G 스마트폰 칩은 비싸고 전력을 많이 씁니다. 그런데 **스마트워치, 산업용 센서, CCTV** 같은 기기는 그렇게 빠를 필요가 없습니다.

    **RedCap**은 NR의 기능을 일부러 줄인 **중간급 5G 단말**입니다.

    | | 스마트폰 (eMBB) | **RedCap** | **eRedCap** | LTE-M / NB-IoT |
    |---|---|---|---|---|
    | 대역폭 | 100 MHz (FR1) | **20 MHz** | 5 MHz (기저대역) | 1.4 MHz / 180 kHz |
    | 수신 안테나 | 4 | **1 – 2** | 1 – 2 | 1 |
    | 최대 속도 | Gbps | 약 **150 Mbps** DL | 약 10 Mbps | ~1 Mbps / 수십 kbps |
    | 용도 | 폰, FWA | 웨어러블, 영상 감시, 산업 센서 | LTE Cat-1 대체 | 계량기, 추적 |

    5G SA 망 안에서 동작하므로 슬라이싱, 측위, 5GC 기능을 그대로 씁니다.

## 줄인 기능 (Rel-17) { .l2 }

| 항목 | 일반 NR 단말 | RedCap |
|---|---|---|
| 최대 대역폭 | FR1 100 MHz / FR2 400 MHz | **FR1 20 MHz / FR2 100 MHz** |
| 수신 안테나 | 2–4 (FR1) | **1 또는 2** |
| DL MIMO 레이어 | 최대 4 | 최대 2 (2Rx일 때) |
| 송신 / UL 레이어 | 1–2 / 최대 4 | **1 / 1** |
| 듀플렉스 | FD-FDD | FD-FDD 또는 **HD-FDD** (선택) |
| 최고 변조 | DL 256QAM | DL 64QAM (256QAM 선택), UL 64QAM |
| 처리 시간 | Capability 1/2 | 완화 (Capability 1 수준) |
| CA / DC | 지원 | **미지원** |

## 망이 RedCap을 다루는 방법 { .l2 }

| 기능 | 내용 |
|---|---|
| **조기 식별** | 전용 프리앰블/RO(Msg1) 또는 Msg3의 LCID로 "나는 RedCap" 표시 → 기지국이 맞춤 스케줄링 |
| 전용 초기 BWP | SIB1의 RedCap용 초기 DL/UL BWP (20 MHz 이내), 넓은 캐리어에서도 접속 가능 |
| 접속 제어 | `cellBarredRedCap1Rx/2Rx`, `intraFreqReselectionRedCap` — 셀이 RedCap을 받을지 결정 |
| **확장 DRX** | IDLE eDRX 최대 **10485.76 s**, INACTIVE eDRX 최대 10.24 s |
| RRM 완화 | 정지·셀 중심 단말 측정 주기 완화 |
| NCD-SSB | 셀 정의 SSB가 없는 BWP에서도 동기·측정 (Rel-17/18) |

??? expert "전문가 노트 — 최대 속도, eRedCap, 공존"
    **최대 속도 계산 (TS 38.306 공식).** 20 MHz, 30 kHz(51 PRB), 2 레이어, 64QAM, \(f\) = 1 → 약 **164 Mbps** DL (15 kHz 106 PRB면 약 170 Mbps). 1Rx이면 절반 수준, UL 1 레이어 64QAM은 약 90 Mbps 안팎입니다.

    **eRedCap (Rel-18).** RF 대역폭은 20 MHz를 유지하되 **PDSCH/PUSCH 대역(기저대역 처리)을 5 MHz**로 제한하거나(공통 채널은 20 MHz), 피크 속도를 낮춰 칩 비용을 LTE Cat-1 수준에 맞춥니다. FR1 전용, 목표 피크 약 10 Mbps.

    **셀 용량 영향.** 1Rx·HD-FDD 단말은 커버리지가 2–3 dB 이상 줄어 같은 데이터에 더 많은 자원을 씁니다. 그래서 RedCap 전용 커버리지 보상(PDCCH AL 증가, 반복)과 접속 제한 정책이 필요합니다.

    **LTE-M/NB-IoT와의 관계.** RedCap은 LPWA를 대체하지 않습니다. 배터리 수년·극한 커버리지(MCL 164 dB)는 여전히 NB-IoT/LTE-M 몫이고, NR 쪽 초저전력·무전원은 **Ambient IoT**(Rel-19)가 맡습니다. → [Ambient IoT](../../advanced5g/ambient-iot.md)

## 관련 페이지

- [BWP](../phy/bwp.md)
- [UE 전력 절약](power-saving.md)
- [LTE-M과 NB-IoT](../../lte/advanced/lte-m-nbiot.md)
- [처리량 계산](../measurement/throughput.md)
