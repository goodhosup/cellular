# LTE (4G)

!!! spec "핵심 규격"
    전체 개요 TS 36.300 · 물리계층 36.211/212/213/214 · L2 36.321/322/323 · RRC 36.331 · NAS 24.301 · EPC 23.401

    Rel-8(2008) LTE → Rel-10 LTE-Advanced → Rel-13 LTE-Advanced Pro → Rel-15 이후 NR과 공존 (EN-DC 앵커)

!!! basic "LTE란"
    **LTE(Long Term Evolution)**는 3GPP가 만든 4세대 이동통신 기술입니다. 3G(WCDMA/HSPA)와 비교한 가장 큰 변화는 다음과 같습니다.

    - **OFDMA** 무선 접속 (하향), **SC-FDMA** (상향)
    - **All-IP**: 회선 교환망이 없고, 음성도 IP 패킷(VoLTE)으로 전달
    - **평평한 구조**: 3G의 RNC(기지국 제어기)를 없애고 기지국(eNB)이 직접 무선 자원을 관리
    - 1.4 – 20 MHz 유연한 대역폭, 최대 4×4 MIMO (Rel-8)

    LTE는 지금도 전 세계에서 가장 넓게 쓰이는 이동통신 기술이며, 5G NSA(EN-DC)에서는 NR의 **앵커**로 동작합니다.

## 이 섹션의 구성

| 영역 | 페이지 | 내용 |
|---|---|---|
| **아키텍처** | [E-UTRAN과 EPC](architecture/overview.md) · [네트워크 엔티티](architecture/entities.md) · [인터페이스](architecture/interfaces.md) · [베어러와 QoS](architecture/bearer-qos.md) | 망 구조, 각 노드의 역할, EPS 베어러 |
| **프로토콜 스택** | [개요](protocol/overview.md) · [MAC](protocol/mac.md) · [RLC](protocol/rlc.md) · [PDCP](protocol/pdcp.md) · [RRC](protocol/rrc.md) · [NAS](protocol/nas.md) | 계층별 기능과 채널 매핑 |
| **물리계층** | [프레임 구조](phy/frame-structure.md) → [리소스 그리드](phy/resource-grid.md) → 채널·신호별 페이지 | 시간–주파수 자원, 물리 채널, 참조신호, TBS |
| **절차** | [셀 탐색](procedures/cell-search.md) → [랜덤 액세스](procedures/random-access.md) → [Attach](procedures/attach.md) → [핸드오버](procedures/handover.md) … | 단말이 켜져서 데이터를 주고받기까지 |
| **고급 기능** | [전송 모드](advanced/transmission-modes.md) · [CA](advanced/carrier-aggregation.md) · [CoMP/eICIC](advanced/comp-eicic.md) · [VoLTE](advanced/volte-ims.md) · [LAA](advanced/laa.md) · [IoT](advanced/lte-m-nbiot.md) · [V2X](advanced/v2x.md) · [eMBMS](advanced/mbms.md) | LTE-Advanced / Pro 기능 |
| **측정과 성능** | [RSRP/RSRQ](measurement/rsrp-rsrq.md) · [CSI](measurement/csi.md) · [측정 이벤트](measurement/events.md) · [처리량](measurement/throughput.md) | 측정량 정의, 보고, 처리량 계산 |

## 핵심 수치 { .l2 }

| 항목 | 값 |
|---|---|
| 채널 대역폭 | 1.4, 3, 5, 10, 15, 20 MHz (CA로 최대 100 MHz, Rel-13 이후 최대 32 CC) |
| 부반송파 간격 | 15 kHz (MBSFN 7.5 kHz, NB-IoT UL 3.75 kHz 옵션) |
| 프레임 / 서브프레임 / 슬롯 | 10 ms / 1 ms / 0.5 ms |
| 스케줄링 단위 (TTI) | 1 ms (Rel-15 sTTI: 2/3 심볼, 1 슬롯) |
| 자원 블록 (RB) | 12 부반송파 × 1 슬롯 (180 kHz × 0.5 ms) |
| 변조 | QPSK, 16QAM, 64QAM, 256QAM (DL Rel-12, UL Rel-14), 1024QAM (DL Rel-15) |
| 채널 코딩 | Turbo (데이터), TBCC (제어) |
| MIMO | DL 최대 8 레이어 (Rel-10), UL 최대 4 레이어 (Rel-10) |
| 최대 처리량 (Rel-8, 20 MHz, 4×4) | DL 약 300 Mbps, UL 약 75 Mbps |
| 사용자 평면 지연 목표 | 5 ms 미만 (단방향, 무부하) |
| 제어 평면 지연 목표 | Idle → Active 100 ms 미만 |

## LTE 학습 순서 추천

```mermaid
flowchart LR
    A[아키텍처] --> B[프로토콜 스택]
    B --> C[프레임 구조]
    C --> D[리소스 그리드]
    D --> E[PSS/SSS · PBCH]
    E --> F[셀 탐색 절차]
    F --> G[PRACH · 랜덤 액세스]
    G --> H[Attach]
    H --> I[PDCCH/DCI · PDSCH]
    I --> J[PUCCH · PUSCH]
    J --> K[측정 · 핸드오버]
    K --> L[고급 기능]
```
