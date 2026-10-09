"""export_wikidocs.py가 만든 폴더를 위키독스 API로 올린다.

    export WIKIDOCS_TOKEN=...      # 위키독스 계정설정 > API 토큰 (저장소에 커밋하지 말 것)
    python tools/publish_wikidocs.py --src build/wikidocs                  # 새 책(비공개) 만들고 업로드
    python tools/publish_wikidocs.py --src build/wikidocs --book-id 12345  # 기존 책 갱신

동작
- TOC.md 순서대로 페이지를 만들고(부모–자식 관계 유지), 페이지 ID를 상태 파일
  (<src>/.wikidocs-state.json)에 기록한다. 다시 실행하면 새로 만들지 않고 PATCH로 갱신한다.
- 페이지 본문의 ../assets/*.png 이미지를 그 페이지에 업로드하고, 응답으로 받은 CDN 주소로
  본문을 치환해 저장한다. 같은 페이지·같은 파일(내용 해시 동일)은 다시 올리지 않는다.
- 책은 기본적으로 비공개(open_yn=N)로 만든다. 확인 후 위키독스 책 설정에서 공개로 바꾸면 된다.

API 문서: https://wikidocs.net/178030 , https://wikidocs.net/napi/docs
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

import requests

API = "https://wikidocs.net/napi"
IMG = re.compile(r"!\[([^\]]*)\]\(\.\./assets/([^)]+)\)")


class Client:
    def __init__(self, token: str, delay: float):
        self.s = requests.Session()
        self.s.headers["Authorization"] = f"Token {token}"
        self.delay = delay

    def call(self, method: str, path: str, **kw):
        for attempt in range(6):
            r = self.s.request(method, f"{API}{path}", timeout=60, **kw)
            if r.status_code in (429, 502, 503, 504):
                wait = 5 * (attempt + 1)
                print(f"  … {r.status_code}, {wait}s 후 재시도")
                time.sleep(wait)
                continue
            if r.status_code >= 400:
                raise SystemExit(f"{method} {path} → HTTP {r.status_code}: {r.text[:400]}")
            time.sleep(self.delay)
            return r.json() if r.content else {}
        raise SystemExit(f"{method} {path} 재시도 한도 초과")


def parse_toc(toc_path: Path):
    """TOC.md → [(depth, title, filename)]"""
    items = []
    for line in toc_path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(\s*)- \[(.+)\]\(pages/(.+?\.md)\)\s*$", line)
        if m:
            items.append((len(m.group(1)) // 2, m.group(2), m.group(3)))
    return items


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default="build/wikidocs", help="export_wikidocs.py 출력 폴더")
    ap.add_argument("--book-id", type=int, default=None, help="기존 책 ID (없으면 새 책 생성)")
    ap.add_argument("--open", action="store_true", help="새 책을 공개(Y)로 생성 (기본: 비공개)")
    ap.add_argument("--only", default=None, help="이 문자열이 들어간 파일만 업로드 (시험용)")
    ap.add_argument("--delay", type=float, default=0.3, help="요청 간 대기 (초)")
    opts = ap.parse_args()

    token = os.environ.get("WIKIDOCS_TOKEN")
    if not token:
        raise SystemExit("WIKIDOCS_TOKEN 환경 변수를 설정하세요")
    src = Path(opts.src)
    state_path = src / ".wikidocs-state.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
    state.setdefault("pages", {})
    state.setdefault("images", {})

    def save():
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")

    api = Client(token, opts.delay)
    me = api.call("GET", "/auth/me/")
    print(f"계정: {me.get('username')}")

    # 책
    book_id = opts.book_id or state.get("book_id")
    if not book_id:
        readme = (src / "README.md").read_text(encoding="utf-8").splitlines()
        subject = readme[0].lstrip("# ").strip()
        summary = "\n".join(readme[1:]).strip()
        book = api.call("POST", "/books/create/", data={
            "subject": subject, "summary": summary, "open_yn": "Y" if opts.open else "N", "book_type": "B"})
        book_id = book["id"]
        print(f"새 책 생성: {book_id} ({'공개' if opts.open else '비공개'})")
    state["book_id"] = book_id
    save()

    items = parse_toc(src / "TOC.md")
    parents: list[int | None] = []
    total = len(items)
    for n, (depth, title, filename) in enumerate(items, 1):
        parents = parents[:depth]
        parent_id = parents[-1] if parents else None
        content = (src / "pages" / filename).read_text(encoding="utf-8")
        if opts.only and opts.only not in filename:
            parents.append(state["pages"].get(filename))
            continue

        page_id = state["pages"].get(filename)
        if page_id is None:
            page = api.call("POST", "/pages/create/", json={
                "book_id": book_id, "subject": title, "content": "작성 중…",
                "parent_id": parent_id if parent_id else -1})
            page_id = page["id"]
            state["pages"][filename] = page_id
            save()
            action = "생성"
        else:
            action = "갱신"
        parents.append(page_id)

        # 이미지 업로드 → CDN 주소로 치환
        def upload(m: re.Match) -> str:
            alt, name = m.group(1), m.group(2)
            path = src / "assets" / name
            if not path.exists():
                print(f"  ⚠ 이미지 없음: {name}")
                return m.group(0)
            digest = hashlib.sha1(path.read_bytes()).hexdigest()[:12]
            key = f"{page_id}:{name}"
            cached = state["images"].get(key)
            if cached and cached["hash"] == digest:
                return f"![{alt}]({cached['url']})"
            with path.open("rb") as f:
                res = api.call("POST", "/images/upload/", data={"page_id": page_id},
                               files={"file": (name, f, "image/png")})
            state["images"][key] = {"hash": digest, "url": res["image_url"]}
            save()
            return f"![{alt}]({res['image_url']})"

        content = IMG.sub(upload, content)
        api.call("PATCH", f"/pages/{page_id}/", json={
            "subject": title, "content": content, "parent_id": parent_id if parent_id else -1})
        print(f"[{n:3d}/{total}] {action} {page_id} {title}")

    save()
    print(f"\n완료: https://wikidocs.net/book/{book_id}")


if __name__ == "__main__":
    main()
