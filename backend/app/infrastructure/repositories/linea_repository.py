import json
from pathlib import Path
from typing import List

from app.domain.linea_transportista import LineaTransportista


class LineaTransportistaRepository:
    def __init__(self, json_path: Path) -> None:
        self._path = json_path

    def get_all(self) -> List[LineaTransportista]:
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        lineas: List[LineaTransportista] = []
        for item in data:
            try:
                lineas.append(LineaTransportista(**item))
            except TypeError:
                continue
        return lineas
