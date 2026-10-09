# Cellular Handbook — LTE · 5G NR · 6G

4G LTE부터 5G NR, 5G-Advanced, 6G 개념까지 다루는 한글 이동통신 핸드북입니다.
각 페이지는 **기초 → 중급 → 전문가** 순서로 깊어집니다.

## 로컬 실행

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python tools/build_figures.py   # 그림 생성
.venv/bin/mkdocs serve                    # http://127.0.0.1:8000
```

## 폴더 구조

| 경로 | 내용 |
|---|---|
| `mkdocs.yml` | 사이트 설정과 **전체 목차(nav)** — 페이지 추가는 여기서 시작 |
| `docs/` | 본문 마크다운 |
| `docs/assets/figures/` | 스크립트로 생성한 SVG 그림 (직접 수정하지 않음) |
| `diagrams/scripts/` | 그림 생성 스크립트 (matplotlib). 공통 색·스타일은 `style.py` |
| `diagrams/drawio/` | 아키텍처 그림 원본 (.drawio) |
| `includes/abbreviations.md` | 사이트 전체 약어 툴팁 (`tools/gen_abbreviations.py`가 약어 사전에서 생성) |
| `tools/scaffold.py` | nav에 있는데 파일이 없는 페이지를 스텁으로 생성 |
| `tools/build_figures.py` | 모든 그림 스크립트 실행 |
| `tools/gen_abbreviations.py` | `docs/reference/glossary.md` 표 → 약어 툴팁 파일 생성 |
| `docs/javascripts/diagrams.mjs` | Mermaid 렌더러 (큰 다이어그램 가독성, 다크 모드, 전체 화면) |
| `docs/javascripts/calculators.js` | 레퍼런스 > 계산기 페이지 스크립트 |

## 페이지 작성 규칙

1. 맨 위에 `!!! spec` 박스로 관련 3GPP 스펙 번호·절과 적용 릴리즈를 적습니다.
2. 본문은 세 단계로 씁니다.
    - `!!! basic` — 개념과 비유 (수식 없이)
    - 본문 `## 제목 { .l2 }` (헤딩 옆에 중급 배지) — 구조, 파라미터 표, 그림
    - `??? expert` — 접히는 전문가 노트 (스펙 수식, 예외 처리, 릴리즈별 차이)
3. 절차는 Mermaid 시퀀스 다이어그램으로, 그리드·프레임은 `diagrams/scripts/`의 스크립트로 그립니다.
4. 다른 사이트나 3GPP 스펙의 그림·문장을 복사하지 않습니다. 스펙은 번호와 절만 인용합니다.

## 배포

`main` 브랜치에 push하면 GitHub Actions(`.github/workflows/deploy.yml`)가 그림을 생성하고 사이트를 빌드해 GitHub Pages에 올립니다.
저장소의 **Settings → Pages → Source**를 `GitHub Actions`로 설정하세요.
사이트 주소: https://goodhosup.github.io/cellular/
