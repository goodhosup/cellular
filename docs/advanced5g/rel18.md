# Rel-18 — 5G-Advanced 첫 릴리즈

!!! spec "스펙 · 릴리즈"
    Release Description: TR 21.918 · 주요 연구 보고서: TR 38.843 (AI/ML 무선), TR 38.864 (망 에너지 절감), TR 38.858 (SBFD), TR 38.869 (LP-WUS), TR 38.848 (Ambient IoT), TR 38.865 (eRedCap) · 동결: Stage 3 2024-03, ASN.1 2024-06 (대략)

!!! basic "한눈에 보기"
    Rel-18은 "5G-Advanced"라는 이름이 처음 붙은 릴리즈입니다. 성격이 다른 세 종류의 일이 섞여 있습니다.

    1. **기존 기능 고도화**: MIMO, 이동성, 커버리지, 사이드링크, 측위, 위성
    2. **새 서비스 지원**: XR, 드론, 철도·전력망용 5 MHz 미만 NR, 저가 단말(eRedCap)
    3. **미래 기술 연구**: AI/ML 무선 인터페이스, 전이중(SBFD), 초저전력 웨이크업, Ambient IoT

    3번은 연구(Study)만 했고, 실제 규격화는 Rel-19로 넘어갔습니다.

## 무선(RAN) 주요 항목 { .l2 }

### 성능 고도화

| 항목 | 내용 | 관련 페이지 |
|---|---|---|
| **MIMO 진화** | multi-TRP용 통합 TCI, **UL 8Tx**(CPE/FWA), **CJT**(여러 TRP 동기 결합) CSI, 고속 이동용 **Doppler CSI**(시간 영역 압축), DMRS 직교 포트 확장(최대 24), 2 TA multi-TRP | [CSI-RS](../nr/phy/csi-rs.md), [TCI](../nr/beam/tci-qcl.md) |
| **이동성 향상** | **LTM**(L1/L2 셀 전환, MAC CE 명령), CHO + 후보 SCG, NR-DC 이동성 | [핸드오버](../nr/procedures/handover.md) |
| **커버리지 향상** | PRACH 반복, UL 파형 동적 전환(CP-OFDM ↔ DFT-s-OFDM), UL 전력 향상 | [PUSCH](../nr/phy/pusch.md) |
| 다중 캐리어 | **DCI 하나로 여러 셀 스케줄링**(DCI 0_3/1_3), 다중 셀 SRS | [CA와 DC](../nr/advanced/ca-dc.md) |
| DSS 향상 | NR PDCCH가 LTE CRS와 겹치는 심볼 사용 | [DSS](../nr/advanced/dss.md) |

### 새 서비스·시장

| 항목 | 내용 |
|---|---|
| **XR** | PDU Set 인지 스케줄링·폐기, 비정수 주기 DRX, 다중 PUSCH CG, 지연 상태 보고 → [XR](xr.md) |
| **망 에너지 절감** | 셀 DTX/DRX, SSB 없는 SCell, 공간·전력 도메인 적응 → [에너지 절감](network-energy-saving.md) |
| **eRedCap** | 5 MHz 기저대역, 피크 약 10 Mbps → [RedCap](../nr/advanced/redcap.md) |
| **NCR** | 망 제어 중계기 (빔·ON/OFF 제어) |
| **Mobile IAB** | 차량 탑재 IAB 노드 → [IAB](../nr/advanced/iab.md) |
| NTN 향상 | 커버리지, **Ka 대역**(10 GHz 이상), 망 검증 단말 위치, NTN–지상망 이동성 → [NTN](../nr/advanced/ntn.md) |
| 사이드링크 진화 | **SL-U**(비면허), SL CA, LTE/NR V2X 동일 채널 공존 → [Sidelink](../nr/advanced/sidelink.md) |
| 측위 확장 | 사이드링크 측위, **반송파 위상 측위**, 대역 집성, LPHAP, RedCap 측위 → [포지셔닝](../nr/advanced/positioning.md) |
| 드론(UAV) | 공중 단말 식별·측정 보고·고도 기반 설정 |
| 5 MHz 미만 NR | 철도(FRMCS)·전력·공공 안전 전용 좁은 대역(3–5 MHz) |
| MBS 향상 | **INACTIVE 상태 멀티캐스트 수신** |
| SDT 향상 | 망 시작 소량 데이터 (MT-SDT) |

### 연구 (Rel-19로 이어짐)

| 연구 | TR | 결과 |
|---|---|---|
| AI/ML 무선 인터페이스 | 38.843 | CSI 압축·예측, 빔 관리, 측위 유스케이스 평가 → Rel-19 규격화 |
| SBFD | 38.858 | 기지국 부대역 전이중 타당성 → Rel-19 WI |
| LP-WUS | 38.869 | 초저전력 웨이크업 수신기 → Rel-19 WI |
| Ambient IoT | 38.848 | 무전원 단말 유형·배치 → Rel-19 WI |

## 시스템·핵심망(SA) 주요 항목 { .l2 }

| 항목 | 내용 |
|---|---|
| AI/ML 지원 | NWDAF 확장, 연합 학습, 단말·응용 간 AI 데이터 지원 |
| XR·미디어 | PDU Set QoS, 혼잡 정보 노출(L4S 등) |
| 위성 | 위성 백홀, 비연속 커버리지 대응 |
| 에너지 | 에너지 효율 정보 수집·정책 |
| 기타 | UE-to-UE 릴레이, 개인 IoT 네트워크(PIN), 레인징, 엣지 컴퓨팅 2단계, 네트워크 슬라이싱 2단계 |

??? expert "전문가 노트 — Rel-18의 의미"
    **RAN3 망 AI (규격화).** 무선 인터페이스 AI가 연구에 머문 것과 달리, Rel-18 RAN3는 **NG-RAN용 AI/ML 지원**(에너지 절감, 부하 분산, 이동성 최적화를 위한 Xn·NG 입력/출력 데이터 교환)을 규격으로 만들었습니다. 모델 자체는 구현이고, 노드 간 예측 정보 교환을 표준화한 것입니다.

    **연구 결과의 성격.** AI/ML 연구는 성능 이득과 함께 **모델 수명 주기 관리(LCM)**, 단말–망 협력 수준, 데이터 수집, 모델 일반화 문제를 정리한 것이 큰 성과입니다. 이것이 Rel-19의 "어떤 것을 먼저 표준화할지" 결정의 근거가 되었습니다.

    **상용화 관점.** Rel-18 기능은 2025–2026년 칩셋·장비에 들어오기 시작합니다. 사업자 입장에서는 에너지 절감, 상향 커버리지, XR·FWA용 MIMO, LTM이 우선 관심사인 경우가 많습니다.

## 관련 페이지

- [5G-Advanced 개요](index.md)
- [Rel-19](rel19.md)
- [3GPP와 릴리즈 타임라인](../getting-started/3gpp-releases.md)
