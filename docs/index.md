---
hide:
  - navigation
---

# Cellular Handbook

**4G LTE부터 5G NR, 5G-Advanced, 그리고 6G까지.**
처음 공부하는 사람은 개념부터, 현업 엔지니어는 스펙 디테일까지 한 페이지 안에서 단계적으로 읽을 수 있도록 만든 한글 이동통신 핸드북입니다.

## 이 핸드북을 읽는 법

모든 페이지는 같은 틀을 따르고, 난이도를 신호 막대 아이콘으로 구분합니다.

| 표시 | 대상 | 내용 |
|---|---|---|
| <span class="lv lv1">기초</span> | 처음 공부하는 사람, 비전공자 | 개념, 비유, "왜 이렇게 만들었나" — 수식 없이 |
| <span class="lv lv2">중급</span> | 전공자, 신입 엔지니어 | 구조, 파라미터 표, 그림, 동작 순서 |
| <span class="lv lv3">전문가</span> | 프로토콜·물리계층 엔지니어 | 스펙 수식, 예외 처리, 릴리즈별 변화, 실무 팁 (접힌 상자) |

!!! spec "스펙 박스"
    각 페이지 맨 위의 이 상자에는 관련 3GPP 문서 번호와 절(clause), 적용 릴리즈가 적혀 있습니다.

    본문을 읽다가 원문을 확인하고 싶을 때 바로 찾아갈 수 있습니다.

약어 위에 마우스를 올리면 풀네임이 툴팁으로 나옵니다. 예: PDCCH, SSB, HARQ

## 섹션

<div class="grid cards" markdown>

-   :material-flag-checkered: **시작하기**

    ---

    세대별 변천, 3GPP 릴리즈 타임라인, 스펙 문서 읽는 법, 수준별 학습 로드맵

    [:octicons-arrow-right-24: 시작하기](getting-started/index.md)

-   :material-sine-wave: **공통 기초**

    ---

    OFDM, QAM, 채널 코딩, HARQ, MIMO, 빔포밍 — LTE와 NR이 함께 쓰는 원리

    [:octicons-arrow-right-24: 공통 기초](basics/index.md)

-   :material-numeric-4-box: **LTE (4G)**

    ---

    E-UTRAN/EPC 아키텍처, 프로토콜 스택, 물리계층, 절차, LTE-Advanced Pro까지

    [:octicons-arrow-right-24: LTE](lte/index.md)

-   :material-numeric-5-box: **NR (5G)**

    ---

    NG-RAN/5GC, Numerology, SSB, 빔 관리, 초기 접속, RedCap·NTN 등 Rel-15~17

    [:octicons-arrow-right-24: NR](nr/index.md)

-   :material-rocket-launch: **5G-Advanced**

    ---

    Rel-18~20 — AI/ML 무선 인터페이스, 네트워크 에너지 절감, XR, Ambient IoT

    [:octicons-arrow-right-24: 5G-Advanced](advanced5g/index.md)

-   :material-crystal-ball: **6G 맛보기**

    ---

    IMT-2030 비전, 3GPP 6G 일정, 후보 기술 (ISAC, AI-native, FR3, NTN 통합)

    [:octicons-arrow-right-24: 6G](sixg/index.md)

</div>

## 진행 현황

- [x] 사이트 뼈대, 목차, 그림 파이프라인
- [x] 시작하기 · 공통 기초
- [x] LTE (4G) 전체 — 아키텍처, 프로토콜, 물리계층, 절차, 고급 기능, 측정 (44페이지)
- [x] NR (5G) 전체 — 아키텍처, 프로토콜, 물리계층, 빔 관리, 절차, 주파수, 고급 기능, 측정 (49페이지)
- [x] 5G-Advanced — Rel-18/19/20, AI/ML, 망 에너지 절감, XR, Ambient IoT
- [x] 6G 맛보기 — IMT-2030, 3GPP 일정, 후보 기술
- [x] 레퍼런스 — 비교표, 스펙 인덱스, 약어 사전, 계산기, 참고 자료

!!! note "출처와 저작권"
    본문과 그림은 직접 작성했습니다. 3GPP 기술 규격(TS/TR)은 문서 번호와 절만 출처로 인용하며, 규격 원문의 그림이나 표를 복제하지 않습니다.
    정확한 값은 항상 해당 릴리즈의 최신 버전 규격으로 확인하세요.
