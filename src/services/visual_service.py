import base64
import random
from pathlib import Path


class VisualService:
    def __init__(self, assets_dir: Path):
        self.imagenes_cargadas = []

        if not assets_dir or not assets_dir.exists():
            return

        for archivo in assets_dir.iterdir():
            if archivo.is_file() and archivo.suffix.lower() == '.svg':
                if archivo.name in ["contenedor.svg", "output.svg", "cont1.svg"]:
                    continue

                try:
                    contenido = archivo.read_bytes()
                    if contenido:
                        b64 = base64.b64encode(contenido).decode("utf-8")
                        src = f"data:image/svg+xml;base64,{b64}"
                        self.imagenes_cargadas.append(src)
                except:
                    pass

    def obtener_imagen_random(self) -> str:
        if not self.imagenes_cargadas:
            return ""
        return random.choice(self.imagenes_cargadas)
