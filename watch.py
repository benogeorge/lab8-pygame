from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path


WATCH_INTERVAL = 0.5


def latest_mtime(source_dir: Path) -> float:
    return max(path.stat().st_mtime for path in source_dir.glob("*.py"))


def main() -> None:
    source_dir = Path(__file__).resolve().parent
    source_path = source_dir / "main.py"

    while True:
        child = subprocess.Popen([sys.executable, str(source_path)], env=os.environ.copy())
        last_mtime = latest_mtime(source_dir)

        try:
            while child.poll() is None:
                time.sleep(WATCH_INTERVAL)
                if latest_mtime(source_dir) != last_mtime:
                    child.terminate()
                    child.wait(timeout=5)
                    break
            else:
                return
        except KeyboardInterrupt:
            child.terminate()
            child.wait(timeout=5)
            return


if __name__ == "__main__":
    main()
