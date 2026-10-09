# NR-U (비면허 대역)

!!! spec "스펙 · 릴리즈"
    채널 접속: TS 37.213 (공유 스펙트럼 채널 접속 절차) · 물리계층: TS 38.211/213/214 Rel-16 (interlace, RB set, 발견 버스트) · 연구: TR 38.889 · 60 GHz: TR 38.808, Rel-17
    Rel-16 NR-U (5 GHz n46, 6 GHz n96) → Rel-17 52.6–71 GHz 비면허, 6 GHz 유럽 n102 → Rel-18 사이드링크 비면허(SL-U)

!!! basic "한눈에 보기"
    **NR-U**는 Wi-Fi가 쓰는 5 GHz, 6 GHz 같은 **비면허 대역**에서 NR을 쓰는 기술입니다. LTE LAA와 달리 다음이 가능합니다.

    - 면허 대역 도움 없이 **단독(standalone)**으로 동작 → 공장·건물 사설망
    - 상향·하향 모두 지원

    비면허 대역의 규칙은 같습니다. **먼저 들어 보고(LBT) 비어 있을 때만** 보냅니다. 그래서 NR-U는 "보내려던 때 못 보낼 수 있다"는 가정 아래 여러 절차를 바꿨습니다.

## 배치 시나리오 { .l2 }

| 시나리오 | 앵커 | 비면허 셀 |
|---|---|---|
| A | NR 면허 PCell | NR-U SCell (CA) |
| B | LTE 면허 | NR-U PSCell (EN-DC) |
| **C** | 없음 | **NR-U 단독** (PCell) |
| D | NR-U 단독 하향 | 면허 대역 상향 |
| E | NR 면허 | NR-U PSCell (NR-DC) |

## 채널 접속 유형 (TS 37.213) { .l2 }

| 유형 | 감지 | 쓰임 |
|---|---|---|
| **Type 1** | 랜덤 백오프 (CW, 우선순위 클래스 1–4) | COT 시작 |
| Type 2A | 25 µs 단일 감지 | COT 안에서 공유, 발견 버스트 |
| Type 2B | 16 µs | COT 안 짧은 간격 |
| Type 2C | **감지 없음** (갭 ≤ 16 µs, 전송 ≤ 584 µs) | COT 안 즉시 응답 (예: HARQ-ACK) |

**COT 공유**: 기지국이 Type 1로 확보한 채널 점유 시간(COT) 안에서 단말은 짧은 LBT(2A/2B/2C)만으로 상향을 보낼 수 있습니다. DCI 2_0이 COT 길이와 가용 RB 집합을 알려 줍니다.

## LBT를 고려한 설계 변경 { .l2 }

| 영역 | 변경 |
|---|---|
| 대역폭 | 20 MHz LBT 단위 = **RB set**. 넓은 캐리어는 RB set별로 LBT, 가용 set만 사용 |
| 상향 자원 | **interlace** (15 kHz: 10개, 30 kHz: 5개) — 대역 전체에 분산 → 점유 대역폭(OCB) 규제 충족 |
| 발견 버스트 | SSB + CORESET#0 + SIB1을 짧은 창(최대 5 ms)에 묶어 Type 2A로 전송, SSB 후보 위치 증가 |
| HARQ | Type-3 코드북(일괄 보고), NFI(새 피드백 지시), 비수치 K1(나중에 보고 시점 지시) |
| Configured Grant | 단말이 HARQ ID·RV·NDI를 **CG-UCI**로 직접 알림, 재전송 타이머 |
| RACH | 긴 RAR 창(최대 40 ms), PRACH 시퀀스 길이 571/1151 |
| 실패 처리 | 연속 UL LBT 실패 감지 → BWP 전환 / 보고 (MAC) |
| 페이징·RLM | LBT 실패를 고려한 측정 (RSSI, 채널 점유율 보고) |

??? expert "전문가 노트 — 우선순위 클래스, 60 GHz, 공존"
    **채널 접속 우선순위 (DL, TS 37.213 Table 4.1.1-1).** \(p\) = 1: \(m_p\)=1, CW 3–7, MCOT 2 ms / \(p\) = 2: 1, 7–15, 3 ms / \(p\) = 3: 3, 15–63, 8 or 10 ms / \(p\) = 4: 7, 15–1023, 8 or 10 ms. LAA와 같은 값으로 Wi-Fi(EDCA)와 공정성을 맞춥니다. 에너지 감지 임계값은 출력·대역폭에 따라 계산합니다(20 MHz, 23 dBm 기준 약 −72 dBm).

    **6 GHz.** 미국 5925–7125 MHz(n96), 유럽 5945–6425 MHz(n102). 국가별로 LBT 의무·출력(LPI 실내 저출력, VLP) 규정이 다릅니다.

    **52.6–71 GHz 비면허 (Rel-17).** 60 GHz 대역은 지역에 따라 LBT가 필수가 아니므로 **LBT 켜기/끄기 모드**를 둡니다. 빔이 좁아 간섭이 국지적이라 **방향성 LBT**(빔 방향으로 감지)를 지원합니다. 480/960 kHz numerology와 함께 씁니다.

    **Wi-Fi와의 공존.** 3GPP 평가 기준은 "NR-U가 Wi-Fi 노드 하나를 대체했을 때 다른 Wi-Fi의 성능이 나빠지지 않을 것"입니다. 같은 대역의 Wi-Fi 6E/7과 함께 운용되므로 LBT 파라미터 준수가 핵심입니다.

## 관련 페이지

- [LTE LAA·eLAA](../../lte/advanced/laa.md)
- [FR1·FR2와 밴드](../spectrum/bands.md)
- [SSB 구조](../phy/ssb.md)
- [Sidelink와 NR V2X](sidelink.md) — SL-U
