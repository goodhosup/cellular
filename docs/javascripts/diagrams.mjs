// Mermaid 다이어그램 렌더러
//
// Material 테마의 기본 Mermaid 통합은 다이어그램을 본문 폭에 맞춰 축소합니다.
// 참여자가 많은 시퀀스 다이어그램(예: Attach, 핸드오버)은 원래 너비가 2000 px을 넘어서
// 축소하면 글자가 읽히지 않으므로, 여기서 직접 렌더링합니다.
//
//  - 원본이 본문보다 넓으면 최소 MIN_SCALE 배율을 유지하고 가로 스크롤
//  - 다이어그램을 클릭하면 원본 크기로 전체 화면 보기
//  - 라이트/다크 팔레트 전환 시 다시 렌더링
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";

const MIN_SCALE = 0.75;
let counter = 0;

function isDark() {
  return document.body.getAttribute("data-md-color-scheme") === "slate";
}

function configure() {
  mermaid.initialize({
    startOnLoad: false,
    theme: isDark() ? "dark" : "default",
    fontFamily: '"Noto Sans KR", sans-serif',
    themeVariables: { fontFamily: '"Noto Sans KR", sans-serif' },
    flowchart: { useMaxWidth: true, htmlLabels: true },
    sequence: {
      useMaxWidth: false,
      actorFontSize: 15,
      messageFontSize: 15,
      noteFontSize: 14,
      mirrorActors: false,
    },
    timeline: { useMaxWidth: true },
    stateDiagram: { useMaxWidth: true },
  });
}

function fit(wrapper) {
  const svg = wrapper.querySelector("svg");
  if (!svg) return;
  const vb = svg.viewBox && svg.viewBox.baseVal;
  const natural = vb && vb.width ? vb.width : svg.getBoundingClientRect().width;
  const available = wrapper.clientWidth;
  svg.style.maxWidth = "none";
  svg.style.height = "auto";
  if (natural <= available) {
    svg.style.width = natural + "px";
    wrapper.classList.remove("is-wide");
  } else {
    svg.style.width = Math.max(available, natural * MIN_SCALE) + "px";
    wrapper.classList.add("is-wide");
  }
}

async function renderOne(wrapper) {
  const source = wrapper.dataset.source;
  try {
    const { svg } = await mermaid.render("diagram-" + counter++, source);
    wrapper.innerHTML = svg;
    fit(wrapper);
  } catch (err) {
    wrapper.innerHTML = "";
    const pre = document.createElement("pre");
    pre.className = "diagram-error";
    pre.textContent = "다이어그램 오류: " + (err && err.message ? err.message : err) + "\n\n" + source;
    wrapper.appendChild(pre);
  }
}

function openFullscreen(wrapper) {
  const svg = wrapper.querySelector("svg");
  if (!svg) return;
  const overlay = document.createElement("div");
  overlay.className = "diagram-overlay";
  overlay.setAttribute("role", "dialog");
  overlay.setAttribute("aria-label", "다이어그램 전체 화면 보기");
  const close = document.createElement("button");
  close.className = "diagram-overlay__close";
  close.type = "button";
  close.textContent = "닫기 ✕";
  const body = document.createElement("div");
  body.className = "diagram-overlay__body";
  const clone = svg.cloneNode(true);
  const vb = svg.viewBox && svg.viewBox.baseVal;
  clone.style.maxWidth = "none";
  clone.style.width = vb && vb.width ? vb.width + "px" : "auto";
  clone.style.height = "auto";
  body.appendChild(clone);
  overlay.append(close, body);
  const dismiss = () => {
    overlay.remove();
    document.removeEventListener("keydown", onKey);
  };
  const onKey = (e) => { if (e.key === "Escape") dismiss(); };
  close.addEventListener("click", dismiss);
  overlay.addEventListener("click", (e) => { if (e.target === overlay) dismiss(); });
  document.addEventListener("keydown", onKey);
  document.body.appendChild(overlay);
  close.focus();
}

async function renderAll(root = document) {
  configure();
  const sources = root.querySelectorAll("pre.diagram-src");
  for (const pre of sources) {
    const wrapper = document.createElement("div");
    wrapper.className = "diagram";
    wrapper.dataset.source = pre.textContent;
    wrapper.title = "클릭하면 크게 볼 수 있습니다";
    wrapper.addEventListener("click", () => openFullscreen(wrapper));
    pre.replaceWith(wrapper);
  }
  for (const wrapper of root.querySelectorAll("div.diagram")) {
    await renderOne(wrapper);
  }
}

// 팔레트 전환 시 다시 그리기
new MutationObserver(() => renderAll()).observe(document.body, {
  attributes: true,
  attributeFilter: ["data-md-color-scheme"],
});

let resizeTimer;
window.addEventListener("resize", () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => document.querySelectorAll("div.diagram").forEach(fit), 150);
});

if (typeof document$ !== "undefined") {
  document$.subscribe(() => renderAll());
} else {
  renderAll();
}
