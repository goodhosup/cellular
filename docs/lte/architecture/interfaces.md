# 인터페이스 (Uu · S1 · X2)

!!! spec "스펙 · 릴리즈"
    S1: TS 36.410 (일반), 36.413 (S1AP), 29.281 (GTP-U) · X2: TS 36.420, 36.423 (X2AP) · EPC: 29.274 (GTPv2-C), 29.272 (S6a Diameter), 29.212 (Gx)

    Rel-8~ (Rel-12 DC용 X2 확장, Rel-15 EN-DC용 X2 확장)

!!! basic "한눈에 보기"
    LTE 장비들은 정해진 **인터페이스(참조점)**로 연결됩니다. 각 인터페이스는 "누가 누구와, 어떤 프로토콜로" 대화하는지를 정합니다.

    - **Uu**: 단말 ↔ 기지국 (무선)
    - **S1**: 기지국 ↔ 핵심망. 제어용(S1-MME)과 데이터용(S1-U)으로 나뉩니다.
    - **X2**: 기지국 ↔ 기지국. 핸드오버 때 데이터를 넘기고, 간섭 정보를 교환합니다.

## 인터페이스 요약 { .l2 }

| 인터페이스 | 연결 | 제어 프로토콜 | 사용자 평면 | 전송 |
|---|---|---|---|---|
| LTE-Uu | UE – eNB | RRC (+NAS) | PDCP/RLC/MAC/PHY | 무선 |
| **S1-MME** | eNB – MME | **S1AP** | — | SCTP (포트 36412) |
| **S1-U** | eNB – S-GW | — | **GTP-U** | UDP (포트 2152) |
| **X2-C** | eNB – eNB | **X2AP** | — | SCTP (포트 36422) |
| **X2-U** | eNB – eNB | — | GTP-U (핸드오버 데이터 포워딩) | UDP 2152 |
| S11 | MME – S-GW | GTPv2-C | — | UDP 2123 |
| S5 / S8 | S-GW – P-GW | GTPv2-C (또는 PMIPv6) | GTP-U | UDP |
| S6a | MME – HSS | Diameter | — | SCTP/TCP |
| S10 | MME – MME | GTPv2-C | — | UDP |
| Gx | P-GW – PCRF | Diameter | — | |
| SGi | P-GW – 외부망 | — | IP | |
| SGs | MME – MSC/VLR | SGsAP | — | SCTP (CSFB, SMS) |

## S1AP 주요 절차 { .l2 }

| 분류 | 절차 | 쓰임 |
|---|---|---|
| 인터페이스 관리 | S1 Setup, eNB/MME Configuration Update, Reset | eNB 기동 시 MME와 연결 수립 |
| NAS 전달 | Initial UE Message, Downlink/Uplink NAS Transport | NAS 메시지를 S1AP로 감싸 전달 |
| 컨텍스트 관리 | **Initial Context Setup**, UE Context Release, UE Context Modification | 보안 키, 베어러, UE 능력 전달 |
| 베어러 관리 | E-RAB Setup / Modify / Release | 전용 베어러 (예: VoLTE QCI 1) |
| 이동성 | Handover Required / Request / Command / Notify, **Path Switch Request** | S1 핸드오버, X2 핸드오버 후 경로 변경 |
| 페이징 | Paging | MME → TA 내 모든 eNB |

## X2AP 주요 절차 { .l2 }

| 절차 | 쓰임 |
|---|---|
| X2 Setup, eNB Configuration Update | 이웃 셀 정보 교환 (PCI, EARFCN, ECGI) |
| **Handover Request / Ack**, SN Status Transfer, UE Context Release | X2 핸드오버 |
| Load Information | ICIC: RNTP, HII, OI, ABS 패턴 |
| Resource Status Reporting | 부하 정보 → 부하 분산(MLB) |
| Mobility Settings Change | 핸드오버 파라미터 협상 (MRO) |
| SeNB Addition / Modification / Release (Rel-12) | LTE 이중 연결 |
| **SgNB Addition** / Modification / Release (Rel-15) | EN-DC — NR 보조 셀 추가 |

## GTP-U 터널 { .l2 }

사용자 IP 패킷은 eNB와 S-GW 사이, S-GW와 P-GW 사이에서 **GTP-U 터널**로 감싸서 전달됩니다.
각 터널은 양 끝의 **TEID(Tunnel Endpoint ID, 32비트)**로 구분되며, EPS 베어러마다 하나씩 만들어집니다.

```
| 외부 IP | UDP (2152) | GTP-U 헤더 (TEID) | 사용자 IP 패킷 |
```

단말이 이동해 eNB가 바뀌어도 S-GW는 하향 터널의 목적지(eNB 주소·TEID)만 바꾸면 됩니다. 단말의 IP 주소는 그대로입니다.

??? expert "전문가 노트 — 구현과 운용 포인트"
    **SCTP 멀티호밍과 스트림.** S1AP는 SCTP 위에서 동작합니다. 스트림 0은 공통(non-UE-associated) 절차용이고, UE 관련 메시지는 다른 스트림에 분산합니다. 멀티호밍으로 전송망 장애에 대비합니다.

    **UE S1AP ID 쌍.** S1AP의 UE 관련 메시지는 `eNB UE S1AP ID`(24비트)와 `MME UE S1AP ID`(32비트) 쌍으로 단말을 구분합니다. 로그 분석 시 이 쌍으로 메시지를 묶어 봅니다.

    **X2 핸드오버 vs S1 핸드오버.** X2가 있고 MME가 바뀌지 않으면 X2 핸드오버를 씁니다(빠름, 핵심망 관여는 Path Switch 한 번). X2가 없거나 MME/S-GW 재배치가 필요하면 S1 핸드오버입니다. → [핸드오버](../procedures/handover.md)

    **GTP-U End Marker.** 핸드오버 후 S-GW가 경로를 바꿀 때 이전 경로에 End Marker를 보내, 타깃 eNB가 포워딩된 패킷과 새 경로 패킷의 순서를 맞출 수 있게 합니다.

    **EN-DC에서의 X2.** Rel-15부터 X2AP에 EN-DC 절차(EN-DC X2 Setup, SgNB Addition 등)가 추가되었습니다. NR 기지국은 X2-C로 eNB와 제어 신호를 주고받고, 사용자 데이터는 S1-U로 S-GW와 직접 연결하거나(SCG bearer / split at SgNB), X2-U로 eNB를 거칩니다.

## 관련 페이지

- [E-UTRAN과 EPC](overview.md)
- [베어러와 QoS](bearer-qos.md)
- [Attach 절차](../procedures/attach.md)
- [핸드오버](../procedures/handover.md)
