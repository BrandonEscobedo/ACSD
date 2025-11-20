import json
from typing import List
from models.simulation_models import LineaTransportista # Corregido a LineaTransportista

class LineaTransportistaServicio:
    """Clase para cargar y gestionar las líneas transportistas desde un archivo JSON."""
    
    def __init__(self, ruta_json: str):
        self.ruta_json = ruta_json

    def listar_lineas(self) -> List[LineaTransportista]:
        """Carga los datos del JSON y los convierte a objetos LineaTransportista."""
        try:
            # La ruta_json ya viene corregida desde main.py para usar sys._MEIPASS
            with open(self.ruta_json, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
        except FileNotFoundError:
            # Este error ocurrirá si PyInstaller falló en copiar el JSON o si la ruta es incorrecta.
            print(f"Error: Archivo de líneas transportistas NO encontrado en {self.ruta_json}.")
            return []
        except json.JSONDecodeError as ex:
            print(f"Error de formato JSON: {ex} en {self.ruta_json}")
            return []

        lineas = []
        for item in datos:
            try:
                # Nota: Tu dataclass es 'LineaTransportista'
                linea = LineaTransportista(**item) 
                lineas.append(linea)
            except TypeError as ex:
                print(f"Error al crear LineaTransportista: {ex} - Datos: {item}")
        return lineas