from dataclasses import dataclass
from .base import Entity


@dataclass
class LineaTransportista(Entity):
    id: int
    nombre: str
    disponible: bool
    porcentaje_cumplimiento: float
    porcentaje_puntualidad: float
    contacto: str = ""
