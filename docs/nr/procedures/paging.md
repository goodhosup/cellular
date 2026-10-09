# Paging

!!! spec "스펙 · 릴리즈"
    페이징 기회: TS 38.304 §7.1 (PF/PO) · 페이징 PDCCH: TS 38.213 §10.1 (Type2-PDCCH CSS) · Paging 메시지: TS 38.331 §5.3.2 · 짧은 메시지: TS 38.331 §6.5 · PEI·하위그룹: TS 38.304 §7.2–7.3 (Rel-17)
    Rel-15~ (Rel-17 **PEI**(DCI 2_7)·페이징 하위그룹·TRS 활용, Rel-18 RedCap eDRX 확장)

!!! basic "한눈에 보기"
    잠든(IDLE/INACTIVE) 단말을 깨우는 방법은 LTE와 같습니다: 단말은 정해진 **페이징 기회(PO)**에만 잠깐 깨어 자기 이름이 불리는지 확인합니다.

    NR에서 달라진 점:

    - **두 종류의 페이징**: 핵심망(AMF)이 시작하는 **CN 페이징**(IDLE 단말), 기지국이 시작하는 **RAN 페이징**(INACTIVE 단말)
    - **빔 스윕 페이징**: 기지국이 단말이 어느 방향에 있는지 모르므로, 페이징 PDCCH를 **SSB 빔마다 한 번씩** 보냅니다.
    - **조기 지시(PEI, Rel-17)**: 진짜 페이징 전에 "이 그룹은 깨어나라"를 짧게 알려, 해당 없는 단말은 계속 잘 수 있습니다.

## 페이징 기회 계산 { .l2 }

\[
\text{PF: } (SFN + PF_{offset}) \bmod T = (T \div N)\cdot(UE\_ID \bmod N), \qquad i_s = \lfloor UE\_ID / N \rfloor \bmod N_s
\]

| 기호 | 의미 |
|---|---|
| \(T\) | DRX 주기 (32, 64, 128, 256 프레임) — min(셀 기본, 단말 요청 / RAN 페이징 주기) |
| \(N\) | 주기 안 PF 수 |
| \(N_s\) | PF당 PO 수 (1, 2, 4) |
| \(PF_{offset}\) | PF 오프셋 (`nAndPagingFrameOffset`) |
| \(UE\_ID\) | **5G-S-TMSI mod 1024** |

## 빔 스윕 PO { .l2 }

하나의 PO는 **S × X개의 연속 PDCCH 감시 시점**으로 구성됩니다.

- \(S\): 실제 전송하는 SSB 수 (`ssb-PositionsInBurst`의 1 개수)
- \(X\): SSB당 감시 시점 수 (`nrofPDCCH-MonitoringOccasionPerSSB-InPO`, 기본 1)
- \(K\)번째 감시 시점은 \(K\)번째 SSB와 같은 빔(QCL)

단말은 자기에게 가장 좋은 SSB에 대응하는 감시 시점만 봐도 됩니다.

## 페이징 DCI와 메시지 { .l2 }

DCI 1_0 (P-RNTI)에는 두 가지가 담길 수 있습니다.

| 지시 | 내용 |
|---|---|
| **Short Message** (8비트) | 비트 1: **systemInfoModification**, 비트 2: **etwsAndCmasIndication**, 비트 3: stopPagingMonitoring (NR-U) |
| 스케줄링 정보 | Paging 메시지가 실린 PDSCH |

| Paging 메시지 필드 | 내용 |
|---|---|
| `pagingRecordList` | 최대 32개 레코드 |
| `ue-Identity` | **ng-5G-S-TMSI** (CN 페이징) 또는 **fullI-RNTI** (RAN 페이징) |
| `accessType` | non3GPP (Wi-Fi 쪽 데이터 도착) |

INACTIVE 단말이 CN 페이징(5G-S-TMSI)을 받으면 IDLE로 가서 RRCSetup으로 연결합니다(앵커 컨텍스트 문제 등 예외 상황).

??? expert "전문가 노트 — PEI, 하위그룹, 페이징 부하"
    **PEI (Paging Early Indication, Rel-17).** PO보다 앞선 PEI-O에서 **DCI 2_7**(PEI-RNTI)을 감시합니다. DCI 2_7은 PO별 **하위그룹 비트맵**을 담아, 자기 하위그룹 비트가 0이면 단말은 PO를 건너뜁니다. 오경보 페이징(같은 PO의 다른 단말 때문에 깨는 것)이 줄어 대기 전력이 감소합니다. PEI 전에 **TRS**(SIB17)로 동기를 맞춰, SSB 여러 개를 기다리지 않고 빠르게 깨어날 수 있습니다.

    **하위그룹 할당.** UE_ID 기반(망 설정 수의 하위그룹) 또는 AMF가 지정(CN 할당 하위그룹, 단말 페이징 확률 기반)합니다.

    **페이징 부하와 SSB 수.** FR2에서 SSB가 많으면 PO당 감시 시점과 페이징 PDCCH 송신 횟수가 늘어 자원을 많이 씁니다. 페이징 대상의 마지막 빔 정보를 활용하는 구현 최적화가 흔합니다.

    **RAN 페이징 주기.** `suspendConfig.ran-PagingCycle`(32–256 프레임)로 INACTIVE 단말은 CN 주기와 RAN 주기 중 짧은 쪽을 따릅니다.

    **eDRX.** IDLE eDRX(최대 10485.76 s 수준, RedCap 확장)와 Rel-17/18 INACTIVE eDRX(최대 10.24 s, RedCap은 더 김)에서는 H-SFN 기반 PH와 PTW를 씁니다(LTE와 유사).

## 관련 페이지

- [RRC 상태와 INACTIVE](rrc-states.md)
- [UE 전력 절약](../advanced/power-saving.md)
- [SSB 구조](../phy/ssb.md)
- [LTE Paging과 TAU](../../lte/procedures/paging-tau.md)
