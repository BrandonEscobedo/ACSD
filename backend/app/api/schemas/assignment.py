from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from .simulation import ContenedorSchema


class AssignmentRequest(BaseModel):
    contenedor: ContenedorSchema


class LineResultSchema(BaseModel):
    línea: str
    cumplimiento: float
    puntualidad: float
    reprogramaciones: int
    espera_promedio: float
    lead_time: float
    puntaje: float
    contacto: str
    tiene_eir: bool
    probabilidad_sin_eir: float
    estado_documental: str
    observaciones: str


class AssignmentResponse(BaseModel):
    mejor: Optional[LineResultSchema]
    resultados: List[LineResultSchema]


class ReportRequest(BaseModel):
    contenedor: ContenedorSchema
    linea_info: Dict[str, Any]
