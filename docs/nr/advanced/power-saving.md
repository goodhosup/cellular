# UE 전력 절약

!!! spec "스펙 · 릴리즈"
    연구: TR 38.840 (Rel-16, 전력 모델), TR 38.875 (RedCap) · WUS (DCI 2_6): TS 38.213 §10.3 · 최소 스케줄링 오프셋: TS 38.214 §5.3.1 · PDCCH 감시 적응: TS 38.213 §10.4 (Rel-17) · PEI: TS 38.304 §7.2 · LP-WUS: Rel-18 연구 TR 38.869 → Rel-19 규격
    Rel-15 BWP·C-DRX → Rel-16 **WUS·교차 슬롯 스케줄링·SCell 휴면·단말 보조 정보** → Rel-17 **PDCCH 감시 생략·PEI·Idle TRS** → Rel-19 **LP-WUS/LP-SS**

!!! basic "한눈에 보기"
    5G 단말은 넓은 대역, 많은 안테나, 잦은 PDCCH 감시 때문에 LTE보다 전력을 많이 쓸 수 있습니다. NR은 "**필요 없을 때는 확실히 쉬게**" 하는 기능을 릴리즈마다 추가했습니다.

    | 상황 | 기능 |
    |---|---|
    | 데이터가 적을 때 | 좁은 **BWP**로 전환, 적은 안테나·레이어 사용 |
    | 데이터가 없을 때 | **C-DRX**, **WUS**(깨울 필요 없으면 계속 잠), PDCCH 감시 생략 |
    | 잠든 상태 | **INACTIVE**, eDRX, **PEI**(진짜 내 페이징일 때만 깸) |
    | 단말이 원할 때 | **UE Assistance Information**으로 선호 설정 요청 |

## Rel-16 이후 주요 기능 { .l2 }

| 기능 | 원리 | 효과 |
|---|---|---|
| **WUS (DCI 2_6)** | C-DRX onDuration 직전에 짧은 PDCCH로 "이번에 깨어날지" 지시 | 데이터 없는 onDuration 전체를 건너뜀 |
| **교차 슬롯 스케줄링** | `minimumSchedulingOffset`(K0 최소값)을 보장 → PDCCH 디코딩 전까지 PDSCH 버퍼링 불필요 | PDCCH만 볼 때 RF·버퍼 전력 감소 |
| SCell 휴면 | 휴면 BWP로 PDCCH 감시 중지, CSI만 유지 | CA 전력 절감, 빠른 복귀 |
| **UE Assistance Information** | 선호 DRX, 최대 대역폭, 최대 CC 수, 최대 MIMO 레이어, 최소 스케줄링 오프셋, 과열 상태, RRC 상태 선호 | 단말 상황에 맞춘 재설정 |
| RRM 완화 (Rel-16/17) | 정지·저이동 단말의 이웃 측정 주기 완화 | 측정 전력 감소 |
| **PDCCH 감시 생략 (Rel-17)** | DCI로 "앞으로 N 슬롯 PDCCH 감시 생략" 또는 **탐색 공간 집합 그룹(SSSG) 전환** | 데이터 사이 공백 구간 절약 |
| **PEI + 페이징 하위그룹 (Rel-17)** | 페이징 전 조기 지시로 해당 그룹만 깸 | 대기 전력 감소 |
| Idle/Inactive TRS (Rel-17) | SIB17 TRS로 빠른 동기 → SSB 여러 개 기다릴 필요 없음 | 깨어나는 시간 단축 |

## 전력 소모 모델 (TR 38.840) { .l2 }

| 상태 | 상대 전력 (대략) |
|---|---|
| 깊은 수면 (deep sleep) | 1 |
| 얕은 수면 (light sleep) | 20 |
| 마이크로 수면 | 45 |
| PDCCH만 감시 | 100 |
| PDCCH + PDSCH 수신 | 300 |
| 상향 송신 (23 dBm) | 250–700 |

수면 상태로 들어가고 나오는 전환에도 에너지와 시간이 들기 때문에, **수면 구간이 충분히 길어야** 깊은 수면을 쓸 수 있습니다. WUS와 PDCCH 생략은 짧은 공백을 긴 수면으로 바꿔 줍니다.

??? expert "전문가 노트 — LP-WUS와 설계 트레이드오프"
    **LP-WUS / LP-SS (Rel-18 연구 → Rel-19 규격).** 주 수신기(OFDM 수신 체인)를 완전히 끄고, **초저전력 별도 수신기**(포락선 검출 등)로만 들을 수 있는 OOK 기반 웨이크업 신호를 정의합니다. 대기 전력을 기존 PDCCH 기반 페이징 감시보다 크게 줄여 IoT·웨어러블 대기 시간을 늘립니다. LP-SS는 이 수신기를 위한 동기 신호입니다.

    **지연과의 트레이드오프.** DRX 주기, WUS 오프셋, PDCCH 생략 길이를 늘리면 전력은 줄지만 첫 패킷 지연이 늘어납니다. 서비스(VoNR, 게임, 메신저)별로 QoS를 보고 C-DRX 프로파일을 다르게 주는 것이 일반적입니다.

    **과열 보고.** 단말은 과열 시 UE Assistance Information(`overheatingAssistance`)으로 CC 수·대역폭·레이어를 줄여 달라고 요청할 수 있습니다. FR2 고출력 단말에서 자주 쓰입니다.

    **망 에너지 절감과의 관계.** 단말 전력 절약과 별도로, Rel-18은 **기지국 에너지 절감**(SSB·SIB 생략 셀, 공간·전력 적응, 셀 DTX/DRX)을 다룹니다. → [네트워크 에너지 절감](../../advanced5g/network-energy-saving.md)

## 관련 페이지

- [BWP](../phy/bwp.md)
- [RRC 상태와 INACTIVE](../procedures/rrc-states.md)
- [Paging](../procedures/paging.md)
- [LTE DRX](../../lte/procedures/drx.md)
