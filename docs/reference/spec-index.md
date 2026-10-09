# 3GPP 스펙 인덱스

!!! basic "이 페이지의 용도"
    이 핸드북에서 인용한 3GPP 규격을 번호순으로 모았습니다. 원문은 3GPP 사이트의 Specifications 메뉴에서 번호로 찾을 수 있습니다. 문서를 고르는 요령은 [스펙 문서 읽는 법](../getting-started/reading-specs.md)을 참고하세요.

## 무선 접속 — LTE (36 시리즈) { .l2 }

| 번호 | 제목 (요약) | 관련 페이지 |
|---|---|---|
| TS 36.101 | UE 무선 송수신 (밴드, EARFCN, MPR) | [리소스 그리드](../lte/phy/resource-grid.md), [전력 제어](../lte/phy/power-control.md) |
| TS 36.104 | 기지국 무선 송수신 | [변조](../basics/modulation.md) |
| TS 36.133 | RRM 요구사항 | [핸드오버](../lte/procedures/handover.md) |
| TS 36.211 | 물리 채널과 변조 | [프레임 구조](../lte/phy/frame-structure.md) 외 물리계층 |
| TS 36.212 | 다중화와 채널 코딩 | [PDCCH와 DCI](../lte/phy/pdcch-dci.md) |
| TS 36.213 | 물리계층 절차 | [TBS와 MCS](../lte/phy/tbs-mcs.md), [PUCCH](../lte/phy/pucch.md) |
| TS 36.214 | 물리계층 측정 | [RSRP·RSRQ](../lte/measurement/rsrp-rsrq.md) |
| TS 36.300 | E-UTRAN 전체 설명 (Stage 2) | [E-UTRAN과 EPC](../lte/architecture/overview.md) |
| TS 36.304 | Idle 모드 절차 | [셀 탐색](../lte/procedures/cell-search.md), [Paging](../lte/procedures/paging-tau.md) |
| TS 36.306 | UE 무선 접속 능력 (카테고리) | [PDSCH](../lte/phy/pdsch.md) |
| TS 36.321 | MAC | [MAC](../lte/protocol/mac.md) |
| TS 36.322 | RLC | [RLC](../lte/protocol/rlc.md) |
| TS 36.323 | PDCP | [PDCP](../lte/protocol/pdcp.md) |
| TS 36.331 | RRC | [RRC](../lte/protocol/rrc.md) |
| TS 36.413 / 36.423 | S1AP / X2AP | [인터페이스](../lte/architecture/interfaces.md) |

## 무선 접속 — NR (38 시리즈) { .l2 }

| 번호 | 제목 (요약) | 관련 페이지 |
|---|---|---|
| TS 38.101-1 / -2 / -3 / -5 | UE 무선 (FR1 / FR2 / 연동 / NTN) | [밴드](../nr/spectrum/bands.md), [ARFCN](../nr/spectrum/arfcn-gscn.md) |
| TS 38.104 | 기지국 무선 | |
| TS 38.133 | RRM 요구사항 | [측정 이벤트와 갭](../nr/measurement/events-gaps.md) |
| TS 38.211 | 물리 채널과 변조 | [Numerology](../nr/phy/numerology.md) 외 물리계층 |
| TS 38.212 | 다중화와 채널 코딩 (LDPC, Polar, DCI) | [PDCCH와 DCI](../nr/phy/pdcch-dci.md) |
| TS 38.213 | 제어 물리계층 절차 (동기, RA, PDCCH, PUCCH, 전력) | [SSB](../nr/phy/ssb.md), [CORESET](../nr/phy/coreset-searchspace.md) |
| TS 38.214 | 데이터 물리계층 절차 (PDSCH, PUSCH, CSI) | [TBS와 MCS](../nr/phy/tbs-mcs.md), [CSI-RS](../nr/phy/csi-rs.md) |
| TS 38.215 | 물리계층 측정 | [SS-RSRP](../nr/measurement/ss-rsrp.md) |
| TS 38.300 | NR·NG-RAN 전체 설명 (Stage 2) | [NG-RAN](../nr/architecture/ng-ran.md) |
| TS 38.304 | Idle/Inactive 절차 | [Paging](../nr/procedures/paging.md) |
| TS 38.305 | NG-RAN 측위 | [포지셔닝](../nr/advanced/positioning.md) |
| TS 38.306 | UE 능력 (최대 데이터율 공식) | [처리량 계산](../nr/measurement/throughput.md) |
| TS 38.321 | MAC | [MAC](../nr/protocol/mac.md) |
| TS 38.322 | RLC | [RLC](../nr/protocol/rlc.md) |
| TS 38.323 | PDCP | [PDCP](../nr/protocol/pdcp.md) |
| TS 38.331 | RRC | [RRC](../nr/protocol/rrc.md) |
| TS 38.340 | BAP (IAB) | [IAB](../nr/advanced/iab.md) |
| TS 38.401 | NG-RAN 구조 (CU/DU) | [CU/DU와 O-RAN](../nr/architecture/cu-du-oran.md) |
| TS 38.413 / 38.423 / 38.473 / 38.463 | NGAP / XnAP / F1AP / E1AP | [NG-RAN](../nr/architecture/ng-ran.md) |
| TR 38.901 | 0.5–100 GHz 채널 모델 | [무선 채널](../basics/radio-channel.md) |

## 공통·연동 (37 시리즈) { .l2 }

| 번호 | 제목 | 관련 페이지 |
|---|---|---|
| TS 37.213 | 공유 스펙트럼 채널 접속 (NR-U LBT) | [NR-U](../nr/advanced/nr-u.md) |
| TS 37.324 | SDAP | [NR 프로토콜 개요](../nr/protocol/overview.md) |
| TS 37.340 | Multi-RAT 이중 연결 (EN-DC 등) | [NSA와 SA](../nr/architecture/nsa-sa.md) |
| TS 37.355 | LPP (측위 프로토콜) | [포지셔닝](../nr/advanced/positioning.md) |

## 시스템·핵심망·NAS·보안 { .l2 }

| 번호 | 제목 | 관련 페이지 |
|---|---|---|
| TS 22.261 | 5G 서비스 요구사항 | [URLLC](../nr/advanced/urllc.md) |
| TR 22.870 | 6G 사용 사례·요구사항 (Rel-20) | [6G 일정](../sixg/3gpp-6g-timeline.md) |
| TS 23.003 | 번호·식별자 체계 | [LTE 식별자](../lte/architecture/entities.md) |
| TS 23.203 | 정책·과금 (QCI 표) | [베어러와 QoS](../lte/architecture/bearer-qos.md) |
| TS 23.228 | IMS | [VoLTE와 IMS](../lte/advanced/volte-ims.md) |
| TS 23.401 | EPS (GPRS 향상) 구조·절차 | [Attach](../lte/procedures/attach.md) |
| TS 23.501 | 5G 시스템 구조 | [5GC와 SBA](../nr/architecture/5gc-sba.md), [QoS 플로우](../nr/architecture/qos-flow.md) |
| TS 23.502 | 5G 시스템 절차 | [등록](../nr/procedures/registration.md), [PDU 세션](../nr/procedures/pdu-session.md) |
| TS 23.503 | 5G 정책·과금 구조 | |
| TS 24.301 | EPS NAS | [LTE NAS](../lte/protocol/nas.md) |
| TS 24.501 | 5GS NAS | [NR NAS](../nr/protocol/nas.md) |
| TS 29.244 | PFCP (N4, Sx) | [PDU 세션](../nr/procedures/pdu-session.md) |
| TS 29.274 / 29.281 | GTPv2-C / GTP-U | [LTE 인터페이스](../lte/architecture/interfaces.md) |
| TS 29.500 / 29.501 | SBA 프레임워크 / API 설계 | [5GC와 SBA](../nr/architecture/5gc-sba.md) |
| TS 33.401 / 33.501 | EPS / 5GS 보안 | [PDCP](../nr/protocol/pdcp.md), [등록](../nr/procedures/registration.md) |

## 주요 연구 보고서 (TR) { .l2 }

| 번호 | 주제 | 릴리즈 |
|---|---|---|
| TR 38.801 | NR 무선 구조 (기능 분할) | Rel-14 |
| TR 38.802 / 38.912 | NR 물리계층 / 전체 연구 | Rel-14 |
| TR 38.913 | 5G 요구사항·시나리오 | Rel-14 |
| TR 38.821 | NTN 해결책 | Rel-16 |
| TR 38.824 | URLLC 물리계층 향상 | Rel-16 |
| TR 38.840 | UE 전력 절약 | Rel-16 |
| TR 38.875 | RedCap | Rel-17 |
| TR 38.843 | AI/ML 무선 인터페이스 | Rel-18 |
| TR 38.864 | 망 에너지 절감 | Rel-18 |
| TR 38.858 | SBFD | Rel-18 |
| TR 38.869 | LP-WUS | Rel-18 |
| TR 38.848 | Ambient IoT | Rel-18 |

## ITU-R { .l2 }

| 문서 | 내용 |
|---|---|
| M.2012 | IMT-Advanced (4G) |
| M.2083 | IMT-2020 (5G) 비전 |
| M.2410 | IMT-2020 최소 기술 요구사항 |
| M.2160 | IMT-2030 (6G) 프레임워크 |
| M.2516 | IMT 2030 이후 기술 동향 |
