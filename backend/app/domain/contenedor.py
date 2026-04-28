from dataclasses import dataclass, field
from typing import Optional
from .base import Entity
from .enums import TipoCarga


@dataclass
class Contenedor(Entity):
    id: str
    tiempo_llegada: float
    posicion_actual: str = "BUQUE"
    estado: str = "En Buque"
    columna: Optional[int] = None
    piso: Optional[int] = None
    imagen_src: str = ""
    carga_tipo: TipoCarga = TipoCarga.SECA
    carga_descripcion: Optional[str] = None
    comprador: Optional[str] = None
    tamano_pies: int = 20
