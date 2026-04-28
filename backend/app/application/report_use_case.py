from typing import Dict

from app.domain.contenedor import Contenedor
from app.infrastructure.services.pdf_service import PDFService


class ReportUseCase:
    def __init__(self, pdf_service: PDFService) -> None:
        self._pdf = pdf_service

    def generar_despacho(self, contenedor: Contenedor, linea_info: Dict) -> bytes:
        return self._pdf.generar_reporte_despacho(contenedor, linea_info)
