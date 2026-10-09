"""diagrams/scripts/ 의 모든 그림 스크립트를 실행해 docs/assets/figures/ 에 SVG를 만든다.

    python tools/build_figures.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "diagrams" / "scripts"


def main() -> int:
    failed = []
    for script in sorted(SCRIPTS.glob("*.py")):
        if script.name == "style.py":
            continue
        print(f"[{script.name}]")
        result = subprocess.run([sys.executable, script.name], cwd=SCRIPTS)
        if result.returncode != 0:
            failed.append(script.name)
    if failed:
        print("실패:", ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
