from fastapi import APIRouter, Depends

from app.api.dependencies import get_simulation_use_case
from app.api.schemas.simulation import (
    ContenedorSchema,
    EventoSchema,
    SimulationRequest,
    SimulationResponse,
)
from app.application.simulation_use_case import SimulationUseCase

router = APIRouter(prefix="/simulation", tags=["simulation"])


@router.post("/run", response_model=SimulationResponse)
def run_simulation(
    req: SimulationRequest,
    use_case: SimulationUseCase = Depends(get_simulation_use_case),
):
    result = use_case.ejecutar(req.n_contenedores, req.intervalo)

    eventos = [
        EventoSchema(
            tiempo=e.tiempo,
            contenedor_id=e.contenedor_id,
            accion=e.accion,
            origen=e.origen,
            destino=e.destino,
        )
        for e in result.eventos
    ]

    contenedores = [
        ContenedorSchema(
            id=c.id,
            tiempo_llegada=c.tiempo_llegada,
            posicion_actual=c.posicion_actual,
            estado=c.estado,
            columna=c.columna,
            piso=c.piso,
            imagen_src=c.imagen_src,
            carga_tipo=c.carga_tipo.value if hasattr(c.carga_tipo, "value") else c.carga_tipo,
            comprador=c.comprador,
            tamano_pies=c.tamano_pies,
        )
        for c in result.contenedores
    ]

    patio = [
        [result.patio[col][piso].id if result.patio[col][piso] else None for piso in range(4)]
        for col in range(10)
    ]

    return SimulationResponse(eventos=eventos, contenedores=contenedores, patio=patio)
