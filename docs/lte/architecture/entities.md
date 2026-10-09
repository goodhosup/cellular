# 네트워크 엔티티와 식별자

!!! spec "스펙 · 릴리즈"
    EPS 노드 기능: TS 23.401 §4.4 · 식별자: TS 23.003 (IMSI, GUTI, TAI 등) · E-UTRAN 식별자: TS 36.300 §8 · RNTI: TS 36.321 §7.1

!!! basic "한눈에 보기"
    LTE 망에서는 여러 장비가 단말을 구분하기 위해 **다양한 ID**를 씁니다. 사람에게 주민번호, 학번, 사원번호가 따로 있는 것과 비슷합니다.

    - **IMSI**: SIM 카드에 있는 영구 가입자 번호. 보안 때문에 무선으로는 가능한 한 보내지 않습니다.
    - **GUTI**: 핵심망(MME)이 주는 임시 ID. IMSI 대신 씁니다.
    - **C-RNTI**: 기지국이 셀 안에서 주는 16비트 임시 ID. 스케줄링에 씁니다.
    - **PCI**: 셀의 물리 ID (0–503). 동기신호에 숨어 있습니다.
    - **ECGI**: 전 세계에서 유일한 셀 ID

## 노드별 역할 상세 { .l2 }

### eNB (evolved NodeB)

- 무선 자원 관리: 무선 베어러 제어, 승인 제어(admission control), 연결 이동성 제어
- **스케줄링**: 1 ms마다 DL/UL 자원 할당 (MAC)
- 보안: RRC 메시지 무결성·암호화, 사용자 데이터 암호화 (PDCP)
- IP 헤더 압축 (ROHC)
- 단말 Attach 시 MME 선택 (NAS 내용은 보지 않고 GUMMEI로 라우팅)
- 측정 설정과 측정 보고 처리, 핸드오버 결정

### MME (Mobility Management Entity)

- NAS 시그널링 종단, NAS 보안 (24.301)
- 인증 및 키 관리 (HSS와 EPS-AKA)
- Idle 모드 단말의 **Tracking Area 리스트** 관리, 페이징 시작
- 베어러 설정·수정·해제 지시
- S-GW / P-GW 선택, 핸드오버 시 MME/S-GW 재배치 판단
- 로밍 단말의 홈 HSS 연동 (S6a)

### S-GW (Serving Gateway)

- 단말 하나당 하나의 S-GW (한 시점)
- eNB 간 핸드오버의 **로컬 이동성 앵커**: 경로만 바꿔주면 P-GW는 모름
- Idle 단말의 하향 데이터 버퍼링 → MME에 Downlink Data Notification
- 3GPP 간 이동성 앵커 (S4 SGSN과 연동)

### P-GW (PDN Gateway)

- **UE IP 주소 할당** (IPv4, IPv6, IPv4v6)
- 단말별 패킷 필터링, 하향 패킷을 TFT로 베어러에 매핑
- 정책 집행 (PCEF), 과금 데이터 생성
- APN마다 별도 PDN 연결 (예: `internet`, `ims`)

## 주요 식별자 { .l2 }

| 식별자 | 구성 | 길이 | 할당 주체 | 용도 |
|---|---|---|---|---|
| **IMSI** | MCC(3) + MNC(2–3) + MSIN | 최대 15자리 | 사업자 (SIM) | 영구 가입자 ID |
| **IMEI(SV)** | TAC + SNR (+SVN) | 15(16)자리 | 제조사 | 단말 기기 ID |
| **GUTI** | GUMMEI + M-TMSI | 80비트 | MME | 임시 가입자 ID (NAS) |
| GUMMEI | MCC + MNC + MMEGI(16) + MMEC(8) | | 사업자 | MME 식별 |
| **S-TMSI** | MMEC + M-TMSI | 40비트 | MME | 페이징, RRC 연결 요청 |
| **TAI** | MCC + MNC + TAC(16) | | 사업자 | Tracking Area |
| **ECGI** | PLMN + ECI(28비트 = eNB ID 20 + Cell ID 8) | | 사업자 | 전역 셀 ID |
| **PCI** | 3 × N_ID(1) + N_ID(2) | 0–503 | 망 설계 | 물리 셀 ID |
| **C-RNTI** | | 16비트 | eNB | 연결 상태 단말 ID (셀 단위) |
| **EBI** | EPS Bearer ID | 4비트 (5–15) | MME | 베어러 식별 |

## RNTI 종류 { .l2 }

DCI의 CRC는 RNTI로 마스킹됩니다. 단말은 자기가 아는 RNTI로 CRC를 풀어 보고, 맞으면 자기 것이라고 판단합니다.

| RNTI | 값 (16진) | 용도 |
|---|---|---|
| P-RNTI | FFFE | 페이징 |
| SI-RNTI | FFFF | 시스템 정보 (SIB) |
| RA-RNTI | 0001 – 003C | 랜덤 액세스 응답 (RAR) |
| Temporary C-RNTI | | 경쟁 기반 RA 중 Msg3/Msg4 |
| C-RNTI | | 일반 스케줄링 |
| SPS C-RNTI | | 반정적 스케줄링 (VoLTE) |
| TPC-PUCCH/PUSCH-RNTI | | 그룹 전력 제어 (DCI 3/3A) |
| M-RNTI | FFFD | MBMS 변경 통지 |
| SC-RNTI, G-RNTI | | SC-PTM (Rel-13) |

??? expert "전문가 노트 — 식별자 실무 이슈"
    **GUTI 재할당과 프라이버시.** IMSI가 무선에 노출되는 경우는 최초 Attach(유효 GUTI 없음), 망이 Identity Request로 IMSI를 요구할 때뿐입니다. 이른바 IMSI catcher는 이 점을 이용합니다. 5G는 SUCI(공개키 암호화된 SUPI)로 이 문제를 해결했습니다.

    **PCI 계획.** 인접 셀끼리 다음을 피해야 합니다.
    - **PCI 충돌(collision)**: 인접 셀이 같은 PCI
    - **PCI 혼동(confusion)**: 한 셀의 서로 다른 두 이웃이 같은 PCI
    - **mod 3 충돌**: 같은 PSS 시퀀스(N_ID(2))와 같은 CRS 주파수 위치(2포트 CRS 기준) → 채널 추정 성능 저하
    - **mod 6 / mod 30**: 1포트 CRS v_shift 충돌, UL DMRS 시퀀스 그룹(PCI mod 30) 충돌

    SON 기능 중 PCI 자동 할당(Automatic PCI)과 ANR(Automatic Neighbour Relation)이 이를 다룹니다. ANR은 단말에게 미지의 PCI 셀의 **ECGI를 SIB1에서 읽어 보고**하게 해서 이웃 목록을 만듭니다(reportCGI).

    **eNB ID 길이.** Macro eNB ID는 20비트(셀 ID 8비트), Home eNB ID는 28비트입니다. Rel-14 이후 Short/Long Macro eNB ID(18/21비트) 옵션이 추가되었습니다.

    **RA-RNTI (FDD).** \(RA\text{-}RNTI = 1 + t_{id} + 10 \cdot f_{id}\). \(t_{id}\)는 PRACH의 첫 서브프레임 번호(0–9), \(f_{id}\)는 TDD에서의 PRACH 주파수 인덱스(FDD는 0)입니다.

## 관련 페이지

- [E-UTRAN과 EPC](overview.md)
- [NAS (EMM·ESM)](../protocol/nas.md)
- [동기신호 (PSS·SSS)](../phy/pss-sss.md) — PCI 구조
