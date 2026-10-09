"""docs/reference/glossary.md 의 약어 표에서 includes/abbreviations.md 를 생성한다.

약어 툴팁(pymdownx.snippets auto_append + abbr)의 원본은 약어 사전 페이지이므로,
약어를 추가할 때는 사전 표에 한 줄 넣고 이 스크립트를 실행하면 된다.

    python tools/gen_abbreviations.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GLOSSARY = ROOT / "docs" / "reference" / "glossary.md"
OUT = ROOT / "includes" / "abbreviations.md"

ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*$")


def main() -> None:
    lines = GLOSSARY.read_text(encoding="utf-8").splitlines()
    entries: dict[str, str] = {}
    in_main_table = False
    for line in lines:
        if line.startswith("| 약어 | 풀네임"):
            in_main_table = True
            continue
        if in_main_table and not line.startswith("|"):
            break  # 첫 번째 표(단일 의미 약어)만 사용
        m = ROW.match(line)
        if not (in_main_table and m) or set(m.group(1)) <= {"-"}:
            continue
        abbr, full, desc = m.groups()
        tip = full if not desc else f"{full} — {desc}"
        entries[abbr] = tip.replace("]", ")")
    body = "\n".join(f"*[{k}]: {v}" for k, v in sorted(entries.items(), key=lambda kv: kv[0].lower()))
    OUT.write_text(body + "\n", encoding="utf-8")
    print(f"약어 {len(entries)}개 → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
