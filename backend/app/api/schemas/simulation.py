from typing import List, Optional
from pydantic import BaseModel, Field


class SimulationRequest(BaseModel):
    n_contenedores: int = Field(ge=1, le=40)
    intervalo: float = Field(ge=0.5, le=5.0)


class EventoSchema(BaseModel):
    tiempo: float
    contenedor_id: str
    accion: str
    origen: str
    destino: str


class ContenedorSchema(BaseModel):
    id: str
    tiempo_llegada: float
    posicion_actual: str
    estado: str
    columna: Optional[int]
    piso: Optional[int]
    imagen_src: str
    carga_tipo: str
    comprador: Optional[str]
    tamano_pies: int


class SimulationResponse(BaseModel):
    eventos: List[EventoSchema]
    contenedores: List[ContenedorSchema]
    patio: List[List[Optional[str]]]
