# 공통 기초

LTE와 NR이 함께 쓰는 무선 통신 원리입니다. LTE·NR 페이지에서 "왜 이렇게 설계했는가"를 이해하려면 이 섹션의 <span class="lv lv1">기초</span> 부분만이라도 먼저 읽어 두세요.

| 페이지 | 핵심 질문 | LTE·NR에서 연결되는 곳 |
|---|---|---|
| [무선 전파와 채널](radio-channel.md) | 전파는 왜 약해지고 일그러지는가 | 참조신호 밀도, CP 길이, SCS 선택 |
| [디지털 변조 (QAM)](modulation.md) | 비트를 어떻게 전파에 싣는가 | MCS 표, CQI |
| [OFDM 원리](ofdm.md) | 넓은 대역을 어떻게 다중경로에 강하게 쓰는가 | 프레임 구조, 리소스 그리드 |
| [OFDMA와 DFT-s-OFDM](ofdma-scfdma.md) | 여러 사용자를 어떻게 나누고, 단말 전력은 어떻게 아끼는가 | LTE UL SC-FDMA, NR transform precoding |
| [채널 코딩](channel-coding.md) | 오류를 어떻게 고치는가 | Turbo / LDPC / Polar |
| [HARQ](harq.md) | 깨진 패킷을 어떻게 효율적으로 다시 보내는가 | HARQ 프로세스, ACK/NACK 타이밍 |
| [MIMO 기초](mimo.md) | 안테나 여러 개로 어떻게 더 빠르게 보내는가 | 전송 모드, CSI 보고 |
| [빔포밍](beamforming.md) | 에너지를 어떻게 한 방향으로 모으는가 | NR 빔 관리, SSB 스윕 |
| [듀플렉싱](duplexing.md) | 송신과 수신을 어떻게 나누는가 | FDD/TDD 프레임 |
| [셀룰러 개념과 간섭](cellular-concept.md) | 같은 주파수를 어떻게 여러 셀이 나눠 쓰는가 | ICIC, CoMP, 핸드오버 |
