from pathlib import Path
import sys


def resource_path(path: Path) -> Path:
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / path
    return path