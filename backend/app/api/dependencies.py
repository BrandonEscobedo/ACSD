from functools import lru_cache
from pathlib import Path
from typing import List

from app.application.assignment_use_case import AssignmentUseCase
from app.application.report_use_case import ReportUseCase
from app.domain.linea_transportista import LineaTransportista
from app.infrastructure.repositories.linea_repository import LineaTransportistaRepository
from app.infrastructure.services.container_monitor import ContainerMonitor
from app.infrastructure.services.pdf_service import PDFService
from app.infrastructure.services.visual_service import VisualService
from app.infrastructure.services.websocket_manager import WebSocketManager

_BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
_ASSETS_DIR = _BASE_DIR / "assets"
_JSON_PATH = _BASE_DIR / "src" / "data" / "lineas_transportistas.json"

# Singletons — se crean una sola vez al primer acceso
_visual_svc: VisualService | None = None
_ws_manager: WebSocketManager | None = None
_monitor: ContainerMonitor | None = None


@lru_cache(maxsize=1)
def _linea_repository() -> LineaTransportistaRepository:
    return LineaTransportistaRepository(_JSON_PATH)


@lru_cache(maxsize=1)
def _pdf_service() -> PDFService:
    return PDFService()


def get_ws_manager() -> WebSocketManager:
    global _ws_manager
    if _ws_manager is None:
        _ws_manager = WebSocketManager()
    return _ws_manager


def get_monitor() -> ContainerMonitor:
    global _visual_svc, _monitor
    if _monitor is None:
        _visual_svc = VisualService(_ASSETS_DIR)
        _monitor = ContainerMonitor(_visual_svc)
        _monitor.set_ws_manager(get_ws_manager())
    return _monitor


def get_lineas() -> List[LineaTransportista]:
    return _linea_repository().get_all()


def get_assignment_use_case() -> AssignmentUseCase:
    return AssignmentUseCase()


def get_report_use_case() -> ReportUseCase:
    return ReportUseCase(_pdf_service())
