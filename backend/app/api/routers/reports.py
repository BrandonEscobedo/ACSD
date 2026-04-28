from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.responses import Response

from app.api.dependencies import get_report_use_case
from app.api.schemas.assignment import ReportRequest
from app.application.report_use_case import ReportUseCase
from app.domain.contenedor import Contenedor
from app.domain.enums import TipoCarga

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/dispatch")
def dispatch_report(
    req: ReportRequest,
    use_case: ReportUseCase = Depends(get_report_use_case),
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
    pdf_bytes = use_case.generar_despacho(contenedor, req.linea_info)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Despacho_{req.contenedor.id}_{timestamp}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
