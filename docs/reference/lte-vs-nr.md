# LTE vs NR 비교

!!! basic "이 표의 용도"
    LTE와 NR의 차이를 한 곳에 모은 요약표입니다. 각 행의 자세한 내용은 해당 LTE·NR 페이지에서 확인하세요. LTE는 Rel-8 기준에 주요 확장(LTE-A/Pro)을 괄호로, NR은 Rel-15 기준에 이후 확장을 괄호로 적었습니다.

## 시스템과 주파수 { .l2 }

| 항목 | LTE | NR |
|---|---|---|
| 첫 릴리즈 | Rel-8 (2008) | Rel-15 (2018) |
| 주파수 범위 | 6 GHz 이하 | FR1 410 MHz – 7.125 GHz, FR2 24.25 – 71 GHz |
| 캐리어 대역폭 | 1.4 – 20 MHz | FR1 최대 100 MHz, FR2 최대 400 MHz (FR2-2 2 GHz) |
| 최대 RB | 100 (규격 110) | 275 |
| 대역 점유율 | 90% | 최대 약 98% |
| CA | 5 CC (Rel-13 32 CC) | 16 CC |
| 듀플렉스 | FDD, TDD(7 구성), LAA | FDD, TDD(심볼 단위 유연), SUL, NR-U, (Rel-19 SBFD) |
| 주파수 번호 | EARFCN (100 kHz) | NR-ARFCN (5/15/60 kHz 전역 래스터) + GSCN (동기 래스터) |

## 물리계층 { .l2 }

| 항목 | LTE | NR |
|---|---|---|
| 파형 DL / UL | CP-OFDM / SC-FDMA | CP-OFDM / CP-OFDM 또는 DFT-s-OFDM |
| 부반송파 간격 | 15 kHz | 15 · 30 · 60 · 120 · (240 SSB) · 480 · 960 kHz |
| 슬롯 | 0.5 ms, 7 심볼 | 1 ms / 2^μ, 14 심볼 |
| 스케줄링 단위 | 1 ms 서브프레임 | 슬롯, 미니슬롯 (2·4·7 심볼) |
| 기본 시간 단위 | \(T_s\) = 1/30.72 MHz | \(T_c\) = \(T_s\)/64 |
| 기준점 | 캐리어 중심 (DC) | Point A |
| 부분 대역 | 없음 | BWP (최대 4개) |
| 동기신호 | PSS/SSS (5 ms), 중앙 6 RB | SSB (4 심볼 × 20 RB), 5–160 ms, 빔 스윕 |
| PCI | 504 | 1008 |
| 방송 | PBCH (TBCC, 40 ms) | PBCH (Polar, 80 ms, SSB 인덱스 포함) |
| 상시 참조신호 | CRS | 없음 |
| 복조 기준 | CRS 또는 DMRS (TM 의존) | 항상 DMRS (front-loaded) |
| 위상 추적 | 없음 | PTRS |
| 제어 영역 | 서브프레임 앞 1–3 심볼, 대역 전체 (PCFICH) | CORESET (설정형) + Search Space |
| PHICH | 있음 | 없음 |
| DCI | 0, 1, 1A, 2 … (TBCC, CRC 16) | 0_x, 1_x, 2_x (Polar, CRC 24) |
| 데이터 코딩 | Turbo | LDPC (BG1/BG2) |
| 최고 변조 DL / UL | 256QAM (Rel-12), 1024QAM (Rel-15) / 64QAM (Rel-14 256QAM) | 256QAM (Rel-17 1024QAM FR1) / 256QAM, π/2-BPSK |
| MIMO DL / UL | 8 / 4 레이어 (Rel-10) | 8 / 4 레이어 (Rel-18 8Tx UL) |
| 전송 모드 | TM1–10 | TM 개념 없음 (DMRS 포트·TCI로 일원화) |
| CSI | CQI/PMI/RI, CRS·CSI-RS | CSI-RS 프레임워크, Type I/II 코드북, 빔 보고 |
| 빔 관리 | 제한적 (FD-MIMO) | P-1/2/3, TCI/QCL, BFR |
| TBS | 표 조회 | 계산식 |
| PUCCH | 포맷 1–5, 서브프레임 전체 | 포맷 0–4, 1–14 심볼 |
| PRACH | 839 (포맷 0–3), 139 (포맷 4) | 839 (0–3), 139 (A·B·C), SSB 연동 RO |

## L2 / L3 { .l2 }

| 항목 | LTE | NR |
|---|---|---|
| 신규 계층 | — | SDAP |
| MAC 서브헤더 | 앞에 모음 | 각 SDU 앞 |
| LCG / SR 설정 | 4 / 1 | 8 / 여러 개 |
| HARQ DL / UL | 비동기 / **동기 + PHICH** | 비동기 / 비동기 |
| HARQ 프로세스 | FDD 8 | 최대 16 (Rel-17 32) |
| HARQ 타이밍 | 고정 (n+4) | K1, K2 동적 |
| 무승인 상향 | SPS | Configured Grant Type 1/2 |
| RLC | 연결·순서 정렬 있음 | 연결·정렬 없음 |
| PDCP | DRB 무결성 없음 | DRB 무결성, 복제, 정렬 |
| RRC 상태 | IDLE, CONNECTED | IDLE, **INACTIVE**, CONNECTED |
| 시스템 정보 | 모두 방송 | Minimum SI + on-demand |
| 접근 제어 | ACB, SSAC, ACDC | UAC (통합) |

## 절차와 이동성 { .l2 }

| 항목 | LTE | NR |
|---|---|---|
| 랜덤 액세스 | 4-step | 4-step + 2-step (Rel-16) |
| 핸드오버 | X2/S1 HO (Rel-16 CHO, DAPS) | Xn/NG HO, CHO, DAPS, LTM (Rel-18) |
| 측정 기준 | CRS (RSRP/RSRQ) | SSB (SS-RSRP), CSI-RS, 빔 기반 셀 품질 |
| 페이징 | CN 페이징 | CN + RAN 페이징, 빔 스윕 PO, PEI |
| 소량 데이터 | EDT (Rel-15) | SDT (Rel-17) |

## 핵심망 { .l2 }

| 항목 | EPC | 5GC |
|---|---|---|
| 구조 | 노드 기반 (MME, S-GW, P-GW, HSS, PCRF) | 서비스 기반 SBA (AMF, SMF, UPF, AUSF, UDM, PCF, NRF, NSSF …) |
| 제어/사용자 분리 | Rel-14 CUPS | 기본 (SMF / UPF) |
| 등록 + 세션 | Attach에 기본 베어러 포함 | Registration과 PDU 세션 분리 |
| QoS 단위 | EPS 베어러, QCI | QoS 플로우, 5QI |
| 가입자 ID 보호 | IMSI 노출 가능 | SUCI |
| 인증 | EPS-AKA | 5G-AKA, EAP-AKA' |
| 슬라이싱 | (DECOR 수준) | S-NSSAI 기반 |
| 비3GPP 접속 | ePDG (S2b) | N3IWF, TNGF (같은 N1 NAS) |
| 음성 | VoLTE, CSFB | VoNR, EPS Fallback |

## 관련 페이지

- [LTE 개요](../lte/index.md) · [NR 개요](../nr/index.md)
- [3GPP 스펙 인덱스](spec-index.md)
