import json
from typing import List
from models.simulation_models import LineasTransportistas

class LineaTransportistaServicio:
    def __init__(self, ruta_json: str):
        self.ruta_json = ruta_json

    def listar_lineas(self) -> List[LineasTransportistas]:
        try:
            with open(self.ruta_json, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
        except FileNotFoundError:
            print(f"Archivo {self.ruta_json} No encontrado.")
            return []
        except json.JSONDecodeError as ex:
            print(f"Error de formato JSON: {ex}")
            return []

        lineas = []
        for item in datos:
            try:
                linea = LineasTransportistas(**item)
                lineas.append(linea)
            except TypeError as ex:
                print(f"Error al crear LineaTransportista: {ex} - Datos: {item}")
        return lineas