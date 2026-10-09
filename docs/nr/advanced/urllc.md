# URLLC

!!! spec "스펙 · 릴리즈"
    요구사항: TR 38.913 §7.5, TS 22.261 (서비스), TS 22.104 (산업 자동화) · 물리계층 향상: TR 38.824 (Rel-16 연구), TS 38.213/38.214 Rel-16 · TSN 통합: TS 23.501 §5.27–5.28 · 이중화: TS 23.501 §5.33
    Rel-15 기본 URLLC → Rel-16 **URLLC/IIoT 강화** (서브슬롯 PUCCH, 우선순위, DCI 0_2/1_2, TSN) → Rel-17 IIoT 확장 (전파 지연 보정, 생존 시간) → Rel-18 XR·산업 연동

!!! basic "한눈에 보기"
    **URLLC (Ultra-Reliable Low-Latency Communication)**는 공장 로봇 제어, 원격 수술, 자율 주행 협력처럼 **"늦거나 틀리면 안 되는"** 통신입니다.

    대표 목표(IMT-2020): **32바이트 패킷을 1 ms 안에, 99.999% 확률로** 전달

    NR은 이를 위해 두 방향으로 손을 썼습니다.

    - **빠르게**: 짧은 전송 단위(미니슬롯), 넓은 SCS, 빠른 단말 처리, 기다리지 않는 상향 전송(Configured Grant)
    - **확실하게**: 낮은 코딩률 MCS 표, 반복 전송, 여러 경로로 복제(PDCP duplication), 다중 TRP

## 지연을 줄이는 기법 { .l2 }

| 기법 | 효과 | 릴리즈 |
|---|---|---|
| 미니슬롯 (Type B, 2–7 심볼) | 슬롯 경계를 기다리지 않음 | 15 |
| 넓은 SCS (30/60 kHz) | 심볼·슬롯 짧아짐 | 15 |
| **Configured Grant** | SR → grant 왕복 생략 | 15 (Rel-16 다중 CG) |
| 처리 능력 Capability 2 | \(N_1\), \(N_2\) 단축 | 15 |
| **서브슬롯 PUCCH** | 슬롯당 여러 번 HARQ-ACK | 16 |
| 다중 SPS (최대 8) | 짧은 주기 DL | 16 |
| **선점 DCI 2_1 / UL 취소 DCI 2_4** | eMBB 자원 즉시 회수 | 15 / 16 |

## 신뢰성을 높이는 기법 { .l2 }

| 기법 | 효과 | 릴리즈 |
|---|---|---|
| 저효율 MCS·CQI 표 (BLER 10⁻⁵ 목표) | 매우 낮은 코딩률 | 15 |
| PDCCH AL 16, DCI 0_2/1_2 (작은 DCI) | 제어 채널 신뢰성 | 15 / 16 |
| PDSCH/PUSCH 반복 (Type A/B) | 시간 다이버시티 | 15 / 16 |
| **PDCP 복제** (CA·DC, 최대 4 경로) | 경로 다이버시티 | 15 / 16 |
| Multi-TRP PDSCH/PDCCH 반복 | 공간 다이버시티 | 16 / 17 |
| 우선순위 (고/저 HARQ-ACK 코드북) | 단말 내 충돌 시 URLLC 보호 | 16 |
| 이중화 PDU 세션 (N3/N9 이중 경로) | 핵심망 경로 다이버시티 | 16 |

## 지연 예산 예 { .l2 }

상향 URLLC, 30 kHz, Configured Grant 2 심볼 주기 가정:

| 구간 | 시간 |
|---|---|
| 패킷 도착 → 다음 CG 기회 (최대) | 약 0.07 ms |
| PUSCH 전송 (2–4 심볼) | 약 0.07–0.14 ms |
| gNB 디코딩 | 약 0.1–0.2 ms |
| 재전송 1회 여유 (HARQ 또는 반복) | 약 0.3 ms |
| **무선 구간 합계** | **약 0.5–0.7 ms** |

??? expert "전문가 노트 — TSN 통합과 산업용 요구"
    **5GS를 TSN 브리지로.** 5G 시스템 전체가 IEEE 802.1Q 브리지 하나로 보이도록, 단말 측 **DS-TT**와 UPF 측 **NW-TT** 변환기가 TSN 관리(CNC)와 연동합니다. TSC(Time Sensitive Communication) 보조 정보(TSCAI: 주기, 버스트 도착 시간, 생존 시간)를 gNB에 넘겨 CG/SPS를 트래픽 주기에 정렬합니다.

    **시간 동기.** 산업망은 단말까지 ±1 µs 수준의 시각 정확도가 필요합니다. gNB가 RRC `ReferenceTimeInfo`(10 ns 단위)나 SIB9로 기준 시각을 주고, Rel-17에서 **전파 지연 보정**(TA 또는 RTT 기반)으로 정확도를 높였습니다.

    **생존 시간 (survival time, Rel-17).** 응용이 연속 패킷 손실을 견딜 수 있는 시간입니다. 첫 손실이 생기면 PDCP 복제를 자동 활성화하는 등 생존 시간 안에 복구하도록 동작합니다.

    **용량 대가.** URLLC는 낮은 코딩률·반복·복제·예약 자원 때문에 스펙트럼 효율이 매우 낮습니다. 같은 셀에서 eMBB와 섞어 운용할 때 선점·우선순위 기법이 셀 전체 용량을 좌우합니다.

    **사설망 (NPN).** 공장 URLLC는 주로 SNPN(독립 사설망) 또는 PNI-NPN(공중망 통합 사설망, 슬라이스·CAG)으로 구축합니다(Rel-16).

## 관련 페이지

- [스케줄링과 HARQ](../procedures/scheduling-harq.md)
- [PDCP](../protocol/pdcp.md) — 복제
- [QoS 플로우](../architecture/qos-flow.md) — Delay-critical GBR
- [PDCCH와 DCI](../phy/pdcch-dci.md)
