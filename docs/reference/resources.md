# 참고 자료

!!! basic "이 페이지의 용도"
    더 깊이 공부하거나 원문을 확인할 때 쓸 수 있는 **공식 자료와 공개 학습 자료**를 모았습니다. 이 핸드북의 정의·수치는 아래 1차 자료(3GPP 규격, ITU-R 문서)를 기준으로 작성했습니다.

## 1차 자료 (표준 원문) { .l2 }

| 자료 | 주소 | 내용 |
|---|---|---|
| 3GPP Specifications | [3gpp.org — Specifications](https://www.3gpp.org/specifications-technologies) | 모든 TS/TR, 릴리즈별 버전 |
| 3GPP 아카이브 (FTP) | [3gpp.org/ftp/Specs/archive](https://www.3gpp.org/ftp/Specs/archive/) | 시리즈·번호·버전별 zip |
| 3GPP Portal | [portal.3gpp.org](https://portal.3gpp.org/) | 작업 항목(WI/SI), CR 목록, 회의 문서 |
| 3GPP 릴리즈 소개 | [3gpp.org — Releases](https://www.3gpp.org/specifications-technologies/releases) | 릴리즈 일정과 개요 |
| ETSI 규격 (무료 PDF) | [etsi.org — Standards search](https://www.etsi.org/standards) | `ETSI TS 138 211` 형태 번호로 같은 규격 |
| ITU-R IMT | [itu.int — IMT-2020 / IMT-2030](https://www.itu.int/en/ITU-R/study-groups/rsg5/rwp5d/imt-2030/Pages/default.aspx) | WP 5D, M.2160 등 |
| O-RAN Alliance | [o-ran.org — Specifications](https://www.o-ran.org/specifications) | Open Fronthaul, RIC, E2 규격 |
| GSMA | [gsma.com](https://www.gsma.com/) | VoLTE/VoNR 프로파일(IR.92 등), 슬라이스 템플릿(NG.116) |

## 원문을 읽는 순서 추천 { .l2 }

| 목표 | 먼저 읽을 문서 | 그다음 |
|---|---|---|
| LTE 전체 구조 | TS 36.300 | 36.211 → 36.213 → 36.321 → 36.331 |
| NR 전체 구조 | TS 38.300 | 38.211 → 38.213/38.214 → 38.321 → 38.331 |
| 5G 핵심망 | TS 23.501 | 23.502 → 24.501 |
| 새 기능 배경 | 해당 기능의 TR (연구 보고서) | 해당 릴리즈의 TS 변경 (CR) |
| 릴리즈 요약 | TR 21.9xx (Release Description) | |

## 공개 학습 자료 { .l2 }

| 자료 | 특징 |
|---|---|
| [ShareTechnote](https://www.sharetechnote.com/) | LTE/NR 프로토콜·물리계층 노트, 로그 예시가 풍부 (영문) — 이 핸드북의 구성에 영감을 준 사이트 |
| 3GPP 기술 소개 페이지 | 기능별 개요 글 (예: NR, 5G System Overview) |
| 각 제조사·칩셋 업체 백서 | 기능별 실무 관점 (상업적 관점이 섞여 있음에 유의) |
| 학술 교과서 | 이론 기초: 무선 통신, OFDM, MIMO, 채널 코딩 교재 |

!!! warning "자료 사용 시 주의"
    2차 자료(블로그, 백서, 이 핸드북 포함)는 특정 릴리즈·가정에 기반하거나 오류가 있을 수 있습니다. 구현·시험·논문에 쓸 수치는 반드시 **해당 릴리즈 최신 버전의 3GPP 원문**으로 확인하세요.

## 이 핸드북에 기여하기 { .l2 }

- 각 페이지 오른쪽 위의 편집 아이콘으로 GitHub에서 수정 제안을 할 수 있습니다.
- 그림은 `diagrams/scripts/`의 Python 스크립트로 생성합니다. 수치를 바꾸려면 스크립트를 고친 뒤 `python tools/build_figures.py`를 실행하세요.
- 약어는 [약어 사전](glossary.md) 표에 추가하고 `python tools/gen_abbreviations.py`를 실행하면 사이트 전체 툴팁에 반영됩니다.
