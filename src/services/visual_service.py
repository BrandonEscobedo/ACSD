import base64
import random
from pathlib import Path


class VisualService:
    def __init__(self, assets_dir: Path):
        self.imagenes_cargadas = []

        # Verificación de seguridad: si la ruta no existe, no hace nada
        if not assets_dir or not assets_dir.exists():
            return

        # Escanea TODOS los archivos en la carpeta
        for archivo in assets_dir.iterdir():
            # Solo procesa archivos .svg (ignora mayúsculas/minúsculas)
            if archivo.is_file() and archivo.suffix.lower() == '.svg':
                # Ignora las imágenes por defecto para que no salgan grises
                if archivo.name in ["contenedor.svg", "output.svg", "cont1.svg"]:
                    continue

                try:
                    # Lee y guarda la imagen
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
