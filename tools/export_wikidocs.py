"""MkDocs 문서(docs/)를 위키독스 '깃허브 연동 책' 구조로 내보낸다.

출력 구조 (위키독스 깃허브 연동 책 규칙, https://wikidocs.net/321336):

    <out>/
    ├── README.md          책 요약 (첫 # 제목 제외한 내용)
    ├── TOC.md             목차 (2칸 들여쓰기 = 하위 페이지)
    ├── pages/*.md         페이지 본문
    ├── assets/*.png       그림 (matplotlib 그림 + 미리 렌더링한 Mermaid 다이어그램)
    └── assets-src/mermaid/*.mmd   Mermaid 원본 (렌더링 입력)

변환 규칙 요약
- !!! / ??? 박스        → 위키독스 팁 블록 [[TIP("제목")]] … [[/TIP]]
- 헤딩 { .l2 }           → 제목 뒤에 (🔵 중급) 표시
- <span class="lv …">   → 🟢/🔵/🔴 표시
- \\( \\), \\[ \\]         → $ $, $$ $$ (위키독스 마크다운의 백슬래시 처리를 고려해 이스케이프)
- <figure> SVG 그림      → ../assets/<이름>.png + 캡션
- ```mermaid            → ../assets/mmd-<해시>.png (기본) 또는 <pre class="mermaid"> (--mermaid html)
- 내부 링크              → 굵은 글씨(기본) 또는 웹 사이트 주소(--link-mode site)
- 페이지 제목            → 위키독스가 제목순으로 정렬하므로 01, 01-02 같은 번호를 붙임

사용 예

    python tools/export_wikidocs.py --out ../cellular-wikidocs            # 내보내기 + 그림 PNG
    python tools/export_wikidocs.py --out ../cellular-wikidocs --render   # + Mermaid PNG 렌더링 (Playwright)
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

BOX_ICON = {
    "spec": "📘", "basic": "🟢", "expert": "🔴", "intermediate": "🔵",
    "note": "📝", "tip": "💡", "warning": "⚠️", "stub": "🚧",
}
LEVEL_MARK = {"1": "🟢 기초", "2": "🔵 중급", "3": "🔴 전문가"}
# Python-Markdown이 백슬래시 이스케이프로 처리하는 문자
MD_ESCAPABLE = set("\\`*_{}[]()>#+-.!")


class _IgnoreTagsLoader(yaml.SafeLoader):
    pass


_IgnoreTagsLoader.add_multi_constructor("", lambda loader, suffix, node: None)


# --------------------------------------------------------------------------- 목차 트리
@dataclass
class Node:
    title: str
    src: str | None = None          # docs/ 기준 경로 (없으면 [[SubPages]]만 있는 묶음 페이지)
    children: list["Node"] = field(default_factory=list)
    code: str = ""
    filename: str = ""


def build_tree(nav) -> list[Node]:
    def walk(items) -> list[Node]:
        nodes = []
        for item in items:
            if isinstance(item, str):           # 섹션 인덱스 (상위에서 처리)
                continue
            (title, value), = item.items()
            if isinstance(value, str):
                nodes.append(Node(title, value))
            else:
                index = next((v for v in value if isinstance(v, str)), None)
                nodes.append(Node(title, index, walk(value)))
        return nodes

    return walk(nav)


def slug_from(node: Node) -> str:
    src = node.src
    if src is None:
        first = node
        while first.children and first.src is None:
            first = first.children[0]
        src = str(Path(first.src or "section").parent / "index.md") if first.src else "section"
    s = re.sub(r"(/index)?\.md$", "", src).replace("/", "-")
    return re.sub(r"[^A-Za-z0-9-]+", "-", s).strip("-") or "home"


def number(nodes: list[Node], prefix: str = "") -> None:
    for i, node in enumerate(nodes):
        n = i if not prefix else i + 1      # 최상위는 00(홈)부터
        node.code = f"{n:02d}" if not prefix else f"{prefix}-{n:02d}"
        node.filename = f"{node.code}-{slug_from(node)}.md"
        number(node.children, node.code)


def label(node: Node) -> str:
    return f"{node.code}. {node.title}"


def flatten(nodes: list[Node]):
    for node in nodes:
        yield node
        yield from flatten(node.children)


# --------------------------------------------------------------------------- 수식
def escape_math(tex: str) -> str:
    """위키독스(Python-Markdown → MathJax) 에서 원래 TeX가 보존되도록 이스케이프."""
    out = []
    i = 0
    while i < len(tex):
        ch = tex[i]
        if ch == "\\" and i + 1 < len(tex):
            nxt = tex[i + 1]
            if nxt in MD_ESCAPABLE:
                out.append("\\\\" + ("\\" + nxt if nxt in "\\*_`" else nxt))
                i += 2
                continue
            out.append("\\")
            i += 1
            continue
        if ch in "*_":
            out.append("\\" + ch)
        elif ch in "|<>":
            cmd = {"|": "\\vert", "<": "\\lt", ">": "\\gt"}[ch]
            nxt = tex[i + 1] if i + 1 < len(tex) else ""
            out.append(cmd + (" " if nxt.isalpha() else ""))
        else:
            out.append(ch)
        i += 1
    return "".join(out)


INLINE_MATH = re.compile(r"\\\((.+?)\\\)")


def convert_inline_math(line: str) -> str:
    return INLINE_MATH.sub(lambda m: "$" + escape_math(m.group(1).strip()) + "$", line)


# --------------------------------------------------------------------------- 변환기
class Converter:
    def __init__(self, src: str, out_assets: Path, mermaid_src: Path, opts, pages_by_src: dict[str, Node]):
        self.src = src
        self.out_assets = out_assets
        self.mermaid_src = mermaid_src
        self.opts = opts
        self.pages_by_src = pages_by_src
        self.mermaid_count = 0
        self.figures: set[str] = set()

    # ---- 링크
    def resolve(self, target: str) -> str | None:
        path, _, _anchor = target.partition("#")
        if not path:
            return self.src
        base = Path(self.src).parent
        resolved = os.path.normpath(str(base / path)).replace("\\", "/")
        return resolved

    def link(self, m: re.Match) -> str:
        text, target = m.group(1), m.group(2)
        if re.match(r"^[a-z]+://", target) or target.startswith("mailto:"):
            return m.group(0)
        resolved = self.resolve(target)
        if self.opts.link_mode == "site" and self.opts.site_url and resolved:
            url = re.sub(r"(index)?\.md$", "", resolved)
            anchor = target.partition("#")[2]
            return f"[{text}]({self.opts.site_url.rstrip('/')}/{url}{'#' + anchor if anchor else ''})"
        node = self.pages_by_src.get(resolved or "")
        if node is not None and self.opts.link_mode == "text":
            return f"**{text}**"
        return f"**{text}**"

    def inline(self, line: str) -> str:
        line = re.sub(r':(material|octicons|fontawesome)-[a-z0-9-]+:\s?', "", line)
        line = re.sub(r'<span class="lv lv([123])">[^<]*</span>', lambda m: LEVEL_MARK[m.group(1)], line)
        line = re.sub(r"<code>(.*?)</code>", r"`\1`", line)
        line = re.sub(r"\{\s*\.[\w-]+(\s+\.[\w-]+)*\s*\}", "", line)
        line = re.sub(r"!\[([^\]]*)\]\(([^)]+?)\.svg\)", self.image, line)
        line = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)", self.link, line)
        line = re.sub(r"^(\s*)- \[x\] ", r"\1- ✅ ", line)
        line = re.sub(r"^(\s*)- \[ \] ", r"\1- ⬜ ", line)
        return convert_inline_math(line)

    def image(self, m: re.Match) -> str:
        alt, path = m.group(1), m.group(2)
        name = Path(path).name
        self.figures.add(name)
        return f"![{alt}](../assets/{name}.png)"

    # ---- 블록
    def convert(self, text: str, top: bool = True) -> str:
        lines = text.split("\n")
        if top and lines and lines[0].strip() == "---":     # front matter
            end = lines.index("---", 1)
            lines = lines[end + 1:]
        out: list[str] = []
        i = 0
        removed_h1 = not top
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # 첫 H1 제거 (위키독스는 페이지 제목을 따로 표시)
            if not removed_h1 and re.match(r"^# \S", line):
                removed_h1 = True
                i += 1
                continue

            # 코드 블록
            fence = re.match(r"^(\s*)```(\w*)", line)
            if fence:
                indent, lang = fence.group(1), fence.group(2)
                body = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    body.append(lines[i][len(indent):] if lines[i].startswith(indent) else lines[i])
                    i += 1
                i += 1
                if lang == "mermaid":
                    out.extend(indent + l for l in self.mermaid("\n".join(body)).split("\n"))
                else:
                    out.append(f"{indent}```{lang}")
                    out.extend(indent + l for l in body)
                    out.append(f"{indent}```")
                continue

            # 박스 (admonition)
            adm = re.match(r'^(\s*)(!!!|\?\?\?\+?) (\w+)(?: "(.*)")?\s*$', line)
            if adm:
                indent, kind, title = adm.group(1), adm.group(3), adm.group(4) or adm.group(3)
                body, i = self.take_block(lines, i + 1, len(indent) + 4)
                inner = self.convert("\n".join(body), top=False).strip("\n")
                icon = BOX_ICON.get(kind, "📌")
                out.append(f'{indent}[[TIP("{icon} {title}")]]')
                out.extend(indent + l if l else "" for l in inner.split("\n"))
                out.append(f"{indent}[[/TIP]]")
                out.append("")
                continue

            # 그림 블록
            if stripped.startswith("<figure"):
                block = []
                while i < len(lines) and "</figure>" not in lines[i]:
                    block.append(lines[i])
                    i += 1
                i += 1
                joined = " ".join(block)
                img = re.search(r"!\[([^\]]*)\]\(([^)]+)\)", joined)
                cap = re.search(r"<figcaption>(.*?)(</figcaption>|$)", joined)
                if img:
                    out.append(self.inline(img.group(0)))
                    out.append("")
                if cap:
                    caption = self.inline(re.sub(r"<[^>]+>", "", cap.group(1)).strip())
                    out.append(f"*그림. {caption}*")
                out.append("")
                continue

            # 표시 수식 \[ … \]
            if stripped.startswith("\\["):
                indent = line[: len(line) - len(line.lstrip())]
                body = []
                first = stripped[2:]
                if "\\]" in first:
                    body.append(first.split("\\]")[0])
                    i += 1
                else:
                    if first:
                        body.append(first)
                    i += 1
                    while i < len(lines) and "\\]" not in lines[i]:
                        body.append(lines[i].strip())
                        i += 1
                    last = lines[i].split("\\]")[0].strip() if i < len(lines) else ""
                    if last:
                        body.append(last)
                    i += 1
                out.append(f"{indent}$$")
                out.extend(indent + escape_math(b) for b in body if b.strip())
                out.append(f"{indent}$$")
                continue

            # HTML 래퍼 제거
            if re.match(r"^\s*</?div\b[^>]*>\s*$", line) or stripped.startswith("<script"):
                i += 1
                continue
            # 카드 그리드 안의 구분선 '---'
            if stripped == "---" and line.startswith("    "):
                i += 1
                continue

            # 헤딩 레벨 표시
            head = re.match(r"^(#{2,6}) (.*?)\s*\{\s*\.l([123])\s*\}\s*$", line)
            if head:
                out.append(f"{head.group(1)} {self.inline(head.group(2))} ({LEVEL_MARK[head.group(3)]})")
                i += 1
                continue

            out.append(self.inline(line))
            i += 1
        return "\n".join(out)

    @staticmethod
    def take_block(lines, start, indent):
        body = []
        i = start
        while i < len(lines):
            l = lines[i]
            if l.strip() == "":
                body.append("")
            elif len(l) - len(l.lstrip()) >= indent:
                body.append(l[indent:])
            else:
                break
            i += 1
        while body and body[-1] == "":
            body.pop()
        return body, i

    def mermaid(self, src: str) -> str:
        self.mermaid_count += 1
        if self.opts.mermaid == "html":
            return f'<pre class="mermaid">\n{src}\n</pre>'
        digest = hashlib.sha1(src.encode("utf-8")).hexdigest()[:10]
        name = f"mmd-{digest}"
        (self.mermaid_src / f"{name}.mmd").write_text(src + "\n", encoding="utf-8")
        return f"![다이어그램](../assets/{name}.png)"


MERMAID_SCRIPT = """
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
mermaid.initialize({ startOnLoad: true });
</script>
"""


def calculators_page(opts) -> str:
    url = (opts.site_url or "").rstrip("/") + "/reference/calculators/"
    return (
        '[[TIP("📘 계산기 안내")]]\n'
        "계산기는 브라우저에서 동작하는 스크립트가 필요해서 위키독스에서는 제공하지 않습니다.\n"
        f"웹 버전에서 사용하세요: {url}\n"
        "[[/TIP]]\n\n"
        "웹 버전 계산기 목록\n\n"
        "- NR 최대 데이터율 (TS 38.306 §4.1.2)\n"
        "- NR-ARFCN ↔ 주파수 (TS 38.101-1 §5.4.2.1)\n"
        "- GSCN ↔ SSB 기준 주파수 (TS 38.101-1 Table 5.4.3.1-1)\n"
        "- LTE EARFCN → 주파수 (TS 36.101 Table 5.7.3-1)\n"
        "- NR TBS (TS 38.214 §5.1.3.2)\n\n"
        "공식과 계산 예는 **처리량 계산**, **TBS와 MCS**, **NR-ARFCN과 GSCN** 페이지에 있습니다.\n"
    )


# --------------------------------------------------------------------------- 실행
def render_figures(assets: Path, dpi: int) -> None:
    env = dict(os.environ, FIG_PREVIEW_DIR=str(assets), FIG_PNG_DPI=str(dpi))
    subprocess.run([sys.executable, str(ROOT / "tools" / "build_figures.py")], env=env, check=True,
                   stdout=subprocess.DEVNULL)


MERMAID_PAGE = """<!doctype html><html><head><meta charset="utf-8">
<style>
  html, body { margin: 0; background: #ffffff; }
  #c { position: absolute; left: 0; top: 0; z-index: 10; overflow: hidden;
       box-sizing: content-box; padding: 16px; background: #ffffff;
       font-family: "Noto Sans KR", "Noto Sans CJK KR", "NanumGothic", sans-serif; }
</style>
<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
  const font = '"Noto Sans KR", "Noto Sans CJK KR", "NanumGothic", sans-serif';
  mermaid.initialize({
    startOnLoad: false, theme: "default", fontFamily: font, themeVariables: { fontFamily: font },
    flowchart: { useMaxWidth: false }, sequence: { useMaxWidth: false, mirrorActors: false,
      actorFontSize: 15, messageFontSize: 15, noteFontSize: 14 },
    gantt: { useMaxWidth: false }, timeline: { useMaxWidth: false }, state: { useMaxWidth: false },
  });
  window.renderOne = async (id, src) => {
    const { svg } = await mermaid.render(id, src);
    // mermaid.render가 남긴 임시 요소 제거 (캡처 영역에 겹치지 않도록)
    document.querySelectorAll("body > :not(#c)").forEach((e) => e.remove());
    const c = document.getElementById("c");
    c.innerHTML = svg;
    const s = c.querySelector("svg");
    const vb = s.viewBox.baseVal;
    s.style.maxWidth = "none";
    s.style.display = "block";
    s.setAttribute("width", vb.width);
    s.setAttribute("height", vb.height);
    c.style.width = vb.width + "px";
    c.style.height = vb.height + "px";
    return [vb.width, vb.height];
  };
  window.ready = true;
</script></head><body><div id="c"></div></body></html>"""


def find_chromium() -> str | None:
    for name in (os.environ.get("CHROMIUM_PATH"), "chromium", "chromium-browser", "google-chrome", "google-chrome-stable"):
        if name and (shutil.which(name) or Path(name).exists()):
            return shutil.which(name) or name
    return None  # Playwright 내장 브라우저 사용 (playwright install chromium 필요)


def render_mermaid(src_dir: Path, assets: Path, force: bool) -> list[str]:
    """Mermaid 원본을 헤드리스 Chromium(Playwright)으로 PNG 렌더링한다."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit("Playwright가 필요합니다: pip install playwright")
    todo = [m for m in sorted(src_dir.glob("*.mmd")) if force or not (assets / f"{m.stem}.png").exists()]
    if not todo:
        return []
    # 일부 환경(GPU 텍스처 최대 4096 px)에서는 그보다 큰 캡처가 반복 패턴으로 깨지므로
    # 캡처 결과가 MAX_PX를 넘지 않도록 다이어그램마다 배율을 정한다.
    MAX_PX = 4000
    done = []
    with sync_playwright() as p:
        exe = find_chromium()
        args = ["--no-sandbox", "--disable-gpu"]
        browser = p.chromium.launch(executable_path=exe, args=args) if exe else p.chromium.launch(args=args)
        probe = browser.new_page(viewport={"width": 3200, "height": 2400})
        probe.set_content(MERMAID_PAGE)
        probe.wait_for_function("window.ready === true", timeout=60000)
        pages: dict[float, object] = {}
        for k, mmd in enumerate(todo):
            src = mmd.read_text(encoding="utf-8")
            w, h = probe.evaluate("([id, src]) => window.renderOne(id, src)", [f"p{k}", src])
            scale = max(1.0, min(2.0, MAX_PX / (w + 32), MAX_PX / (h + 32)))
            scale = round(scale * 4) / 4          # 1.0, 1.25, … 2.0 단위로 묶어 페이지 재사용
            if scale not in pages:
                pg = browser.new_page(viewport={"width": 3200, "height": 2400}, device_scale_factor=scale)
                pg.set_content(MERMAID_PAGE)
                pg.wait_for_function("window.ready === true", timeout=60000)
                pages[scale] = pg
            pg = pages[scale]
            pg.evaluate("([id, src]) => window.renderOne(id, src)", [f"d{k}", src])
            pg.locator("#c").screenshot(path=str(assets / f"{mmd.stem}.png"))
            done.append(mmd.stem)
        browser.close()
    return done


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "build" / "wikidocs"), help="출력 폴더 (위키독스 연동 저장소)")
    ap.add_argument("--mermaid", choices=["png", "html"], default="png",
                    help="png: 이미지로 미리 렌더링(권장) / html: <pre class=mermaid> (책 설정에서 HTML 사용 필요)")
    ap.add_argument("--render", action="store_true", help="Mermaid PNG 렌더링 (Playwright + Chromium)")
    ap.add_argument("--force-render", action="store_true", help="이미 있는 Mermaid PNG도 다시 렌더링")
    ap.add_argument("--link-mode", choices=["text", "site"], default="text",
                    help="내부 링크를 굵은 글씨(text) 또는 웹 사이트 주소(site)로")
    ap.add_argument("--site-url", default=None, help="웹 사이트 주소 (기본: mkdocs.yml의 site_url)")
    ap.add_argument("--dpi", type=int, default=150, help="그림 PNG 해상도")
    ap.add_argument("--no-figures", action="store_true", help="matplotlib 그림 PNG 생성을 건너뜀")
    opts = ap.parse_args()

    cfg = yaml.load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"), Loader=_IgnoreTagsLoader)
    opts.site_url = opts.site_url or cfg.get("site_url")
    out = Path(opts.out).resolve()
    pages_dir, assets, mermaid_src = out / "pages", out / "assets", out / "assets-src" / "mermaid"
    for d in (pages_dir, mermaid_src):
        if d.exists():
            shutil.rmtree(d)        # 생성물만 지움 (.git 등 다른 파일은 유지)
        d.mkdir(parents=True)
    assets.mkdir(parents=True, exist_ok=True)

    tree = build_tree(cfg["nav"])
    number(tree)
    pages_by_src = {n.src: n for n in flatten(tree) if n.src}

    # 페이지 변환
    used_mermaid: set[str] = set()
    figures: set[str] = set()
    for node in flatten(tree):
        if node.src == "reference/calculators.md":
            body = calculators_page(opts)
        elif node.src == "index.md":
            node.title = "이 책에 대하여"
            body = (ROOT / "tools" / "wikidocs_intro.md").read_text(encoding="utf-8").replace("{site_url}", opts.site_url or "")
        elif node.src:
            conv = Converter(node.src, assets, mermaid_src, opts, pages_by_src)
            body = conv.convert((DOCS / node.src).read_text(encoding="utf-8")).strip("\n") + "\n"
            figures |= conv.figures
            if opts.mermaid == "html" and conv.mermaid_count:
                body += MERMAID_SCRIPT
        else:
            body = f"{node.title} 장의 페이지입니다.\n"
        if node.children:
            body += "\n## 이 장의 페이지\n\n[[SubPages]]\n"
        if body.count("\n## ") >= 4 and "[TOC]" not in body:
            # 첫 팁 블록(스펙 박스) 뒤에 페이지 목차 삽입
            idx = body.find("[[/TIP]]")
            pos = idx + len("[[/TIP]]") if idx >= 0 else 0
            body = body[:pos] + "\n\n[TOC]\n" + body[pos:]
        (pages_dir / node.filename).write_text(body, encoding="utf-8")
    used_mermaid = {p.stem for p in mermaid_src.glob("*.mmd")}

    # TOC.md, README.md
    toc = ["# 목차", ""]
    for node in tree:
        def emit(n: Node, depth: int):
            toc.append(f"{'  ' * depth}- [{label(n)}](pages/{n.filename})")
            for c in n.children:
                emit(c, depth + 1)
        emit(node, 0)
    (out / "TOC.md").write_text("\n".join(toc) + "\n", encoding="utf-8")
    (out / "README.md").write_text(
        f"# {cfg['site_name']}\n\n{cfg.get('site_description', '')}\n\n"
        "각 페이지는 🟢 기초 → 🔵 중급 → 🔴 전문가 순서로 깊어집니다. "
        "📘 박스에는 관련 3GPP 규격 번호와 절, 적용 릴리즈를 적었습니다.\n\n"
        f"웹 버전 (검색·계산기·확대 가능한 다이어그램): {opts.site_url}\n",
        encoding="utf-8")

    # 그림
    if not opts.no_figures:
        render_figures(assets, opts.dpi)
    # 사용하지 않는 오래된 Mermaid PNG 정리
    for png in assets.glob("mmd-*.png"):
        if png.stem not in used_mermaid:
            png.unlink()
    rendered = render_mermaid(mermaid_src, assets, opts.force_render) if opts.render and opts.mermaid == "png" else []

    missing_fig = sorted(f for f in figures if not (assets / f"{f}.png").exists())
    missing_mmd = sorted(m for m in used_mermaid if not (assets / f"{m}.png").exists())
    n_pages = sum(1 for _ in flatten(tree))
    print(f"페이지 {n_pages}개 → {pages_dir}")
    print(f"그림 {len(figures)}종, Mermaid {len(used_mermaid)}개 (이번에 렌더링 {len(rendered)}개)")
    if missing_fig:
        print("⚠ PNG 없는 그림:", ", ".join(missing_fig))
    if missing_mmd and opts.mermaid == "png":
        print(f"⚠ 아직 렌더링되지 않은 Mermaid {len(missing_mmd)}개 — --render 옵션으로 생성하세요")


if __name__ == "__main__":
    main()
