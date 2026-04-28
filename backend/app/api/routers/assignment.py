from typing import List

from fastapi import APIRouter, Depends

from app.api.dependencies import get_assignment_use_case, get_lineas
from app.api.schemas.assignment import AssignmentRequest, AssignmentResponse
from app.application.assignment_use_case import AssignmentUseCase
from app.domain.contenedor import Contenedor
from app.domain.enums import TipoCarga
from app.domain.linea_transportista import LineaTransportista

router = APIRouter(prefix="/assignment", tags=["assignment"])


@router.post("", response_model=AssignmentResponse)
def assign_line(
    req: AssignmentRequest,
    use_case: AssignmentUseCase = Depends(get_assignment_use_case),
    lineas: List[LineaTransportista] = Depends(get_lineas),
):
    contenedor = Contenedor(
        id=req.contenedor.id,
        tiempo_llegada=req.contenedor.tiempo_llegada,
        posicion_actual=req.contenedor.posicion_actual,
        estado=req.contenedor.estado,
        columna=req.contenedor.columna,
        piso=req.contenedor.piso,
        imagen_src=req.contenedor.imagen_src,
        carga_tipo=TipoCarga(req.contenedor.carga_tipo),
        comprador=req.contenedor.comprador,
        tamano_pies=req.contenedor.tamano_pies,
    )
    result = use_case.ejecutar(contenedor, lineas)
    return AssignmentResponse(mejor=result.mejor, resultados=result.resultados)
