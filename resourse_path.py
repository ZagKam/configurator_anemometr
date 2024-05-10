from pathlib import Path
import os


def resource_path(path: Path) -> Path:
    if os.getenv("_MEIPASS"):
        return Path(os.getenv("_MEIPASS") / path)
    return path