from dataclasses import dataclass


@dataclass
class EventoSimulacion:
    tiempo: float
    contenedor_id: str
    accion: str
    origen: str
    destino: str
