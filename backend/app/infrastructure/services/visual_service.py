import base64
import random
from pathlib import Path
from typing import List

_SKIP = {"contenedor.svg", "output.svg", "cont1.svg"}


class VisualService:
    def __init__(self, assets_dir: Path) -> None:
        self._images: List[str] = []
        self._load(assets_dir)

    def _load(self, assets_dir: Path) -> None:
        if not assets_dir or not assets_dir.exists():
            return
        for file in assets_dir.iterdir():
            if file.is_file() and file.suffix.lower() == ".svg" and file.name not in _SKIP:
                try:
                    content = file.read_bytes()
                    if content:
                        b64 = base64.b64encode(content).decode("utf-8")
                        self._images.append(f"data:image/svg+xml;base64,{b64}")
                except Exception:
                    pass

    def get_random(self) -> str:
        return random.choice(self._images) if self._images else ""
