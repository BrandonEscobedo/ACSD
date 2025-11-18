from enum import Enum
from typing import List, Optional
from dataclasses import dataclass, field
class Prioridad(Enum):
    """Niveles de prioridad para contenedores"""
    ALTA = 3
    MEDIA = 2
    BAJA = 1


class EstadoContenedor(Enum):
    """Estados posibles de un contenedor"""
    EN_PATIO = "En Patio"
    ASIGNADO = "Asignado a Camión"
    EN_VERIFICACION = "En Verificación"
    CARGANDO = "Cargando"
    DESPACHADO = "Despachado"
    REPROGRAMADO = "Reprogramado"

 
class TipoCarga(Enum):
    """Tipos de carga (opcional para extensión futura)"""
    SECA = "Carga Seca"
    REFRIGERADA = "Refrigerada"
    PELIGROSA = "Peligrosa"
    FRAGIL = "Frágil"
    NODRIZA = "Nodriza"

@dataclass
class LineaTransportista:
    id: int
    nombre: str
    disponible: bool
    porcentaje_cumplimiento: float
    porcentaje_puntualidad: float
    contacto: str = ""

@dataclass
class EventoSimulacion:
    tiempo: float
    contenedor_id: str
    accion: str
    origen: str
    destino: str

    def __repr__(self):
        return f"t={self.tiempo:.1f} | {self.contenedor_id}: {self.accion} ({self.origen}→{self.destino})"

@dataclass
class Contenedor:
    id: str
    tiempo_llegada: float
    posicion_actual: str = "BUQUE"
    estado: str = "En Buque"

    def __repr__(self):
        return f"{self.id} [{self.estado}]"