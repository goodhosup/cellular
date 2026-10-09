"""mkdocs.yml의 nav를 읽어 아직 없는 페이지를 '작성 예정' 스텁으로 만든다.

이미 있는 파일은 절대 건드리지 않는다. 목차(nav)가 단일 진실 공급원이므로
새 페이지를 추가할 때는 mkdocs.yml에 한 줄 넣고 이 스크립트를 실행하면 된다.

    python tools/scaffold.py
"""
from __future__ import annotations

import os
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


class _IgnoreTagsLoader(yaml.SafeLoader):
    """mkdocs.yml의 !!python/name 태그를 무시하고 읽기 위한 로더."""


_IgnoreTagsLoader.add_multi_constructor("", lambda loader, suffix, node: None)


def walk(items, trail):
    """nav 트리를 (경로, 제목, 섹션 트레일, 형제 목록)으로 펼친다."""
    for item in items:
        if isinstance(item, str):  # 섹션 인덱스 (제목 없음)
            yield item, trail[-1] if trail else "", trail, items
        else:
            (title, value), = item.items()
            if isinstance(value, str):
                yield value, title, trail, items
            else:
                yield from walk(value, trail + [title])


def children_of(items):
    for item in items:
        if isinstance(item, str):
            continue
        (title, value), = item.items()
        if isinstance(value, str):
            yield title, value
        else:
            first = next((v for v in value if isinstance(v, str)), None)
            if first is None:
                first = next(iter(value[0].values())) if value and isinstance(value[0], dict) else None
            if isinstance(first, str):
                yield title, first


def stub(title: str, trail: list[str]) -> str:
    crumb = " › ".join(trail)
    return f"""# {title}

!!! stub "🚧 작성 예정"
    이 페이지는 아직 작성 중입니다. ({crumb})

    완성되면 아래 구성을 따릅니다.

    - <span class="lv lv1">기초</span> 한눈에 보기 — 개념과 비유
    - <span class="lv lv2">중급</span> 구조와 동작 — 파라미터, 표, 그림
    - <span class="lv lv3">전문가</span> 스펙 디테일 — 수식, 예외 처리, 릴리즈별 변화
"""


def index_stub(title: str, here: str, siblings) -> str:
    lines = [f"# {title}", ""]
    lines.append("이 섹션의 페이지:")
    lines.append("")
    base = os.path.dirname(here)
    for child_title, child_path in children_of(siblings):
        if child_path == here:
            continue
        rel = os.path.relpath(child_path, base or ".")
        lines.append(f"- [{child_title}]({rel})")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    cfg = yaml.load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"), Loader=_IgnoreTagsLoader)
    created = 0
    for path, title, trail, siblings in walk(cfg["nav"], []):
        target = DOCS / path
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        is_index = target.name == "index.md"
        body = index_stub(title, path, siblings) if is_index else stub(title, trail)
        target.write_text(body, encoding="utf-8")
        created += 1
        print(f"  + {path}")
    print(f"스텁 {created}개 생성")


if __name__ == "__main__":
    main()
