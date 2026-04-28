import asyncio
import random
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Dict, List, Optional

from app.domain.contenedor import Contenedor
from app.domain.enums import TipoCarga
from app.infrastructure.services.visual_service import VisualService

if TYPE_CHECKING:
    from app.infrastructure.services.websocket_manager import WebSocketManager

_COMPRADORES = ["ACME Corp", "Importadora S.A.", "Distribuciones S.A.", "Cliente X"]


@dataclass
class MonitorConfig:
    arrival_interval: float = 5.0
    buque_time: float = 8.0
    piso_time: float = 6.0
    max_containers: int = 40
    auto_advance: bool = True


class ContainerMonitor:
    def __init__(self, visual_service: VisualService) -> None:
        self._visual = visual_service
        self.containers: Dict[str, Contenedor] = {}
        self.buque: List[str] = []
        self.piso: List[str] = []
        self.patio: List[List[Optional[str]]] = [[None] * 4 for _ in range(10)]
        self.events: deque = deque(maxlen=100)
        self.auto_running: bool = False
        self.config: MonitorConfig = MonitorConfig()
        self._counter: int = 0
        self._ws_manager: Optional["WebSocketManager"] = None
        self._auto_task: Optional[asyncio.Task] = None
        self._advance_tasks: Dict[str, asyncio.Task] = {}

    # ── Public setup ──────────────────────────────────────────────────────────

    def set_ws_manager(self, ws_manager: "WebSocketManager") -> None:
        self._ws_manager = ws_manager

    # ── State serialization ───────────────────────────────────────────────────

    def get_state(self) -> dict:
        return {
            "type": "full_state",
            "buque": [self._ser(self.containers[cid]) for cid in self.buque if cid in self.containers],
            "piso":  [self._ser(self.containers[cid]) for cid in self.piso  if cid in self.containers],
            "patio": [[self.patio[col][piso] for piso in range(4)] for col in range(10)],
            "containers": {cid: self._ser(c) for cid, c in self.containers.items()},
            "events": list(self.events),
            "auto_running": self.auto_running,
            "config": {
                "arrival_interval": self.config.arrival_interval,
                "buque_time": self.config.buque_time,
                "piso_time": self.config.piso_time,
                "max_containers": self.config.max_containers,
                "auto_advance": self.config.auto_advance,
            },
        }

    def _ser(self, c: Contenedor) -> dict:
        return {
            "id": c.id,
            "tiempo_llegada": c.tiempo_llegada,
            "posicion_actual": c.posicion_actual,
            "estado": c.estado,
            "columna": c.columna,
            "piso": c.piso,
            "imagen_src": c.imagen_src,
            "carga_tipo": c.carga_tipo.value if hasattr(c.carga_tipo, "value") else c.carga_tipo,
            "comprador": c.comprador,
            "tamano_pies": c.tamano_pies,
        }

    # ── Internal helpers ──────────────────────────────────────────────────────

    async def _broadcast(self) -> None:
        if self._ws_manager:
            await self._ws_manager.broadcast(self.get_state())

    def _log(self, container_id: str, accion: str, origen: str, destino: str) -> None:
        self.events.appendleft({
            "timestamp": datetime.now().isoformat(),
            "container_id": container_id,
            "accion": accion,
            "origen": origen,
            "destino": destino,
        })

    def _make_container(self) -> Contenedor:
        self._counter += 1
        return Contenedor(
            id=f"CNT-{self._counter:03d}",
            tiempo_llegada=datetime.now().timestamp(),
            imagen_src=self._visual.get_random(),
            carga_tipo=random.choice(list(TipoCarga)),
            comprador=random.choice(_COMPRADORES),
            tamano_pies=random.choice([20, 40]),
            posicion_actual="BUQUE",
            estado="En Buque — esperando descarga",
        )

    def _place_in_patio(self, contenedor: Contenedor) -> bool:
        for col in range(10):
            for piso in range(4):
                if all(self.patio[col][p] is None for p in range(piso + 1, 4)):
                    if self.patio[col][piso] is None:
                        self.patio[col][piso] = contenedor.id
                        contenedor.columna = col
                        contenedor.piso = piso
                        return True
        return False

    # ── Zone transitions ──────────────────────────────────────────────────────

    def _arrive_in_buque(self, cont: Contenedor) -> None:
        self.containers[cont.id] = cont
        self.buque.append(cont.id)
        self._log(cont.id, "Llegada", "MAR", "BUQUE")

    async def move_to_piso(self, container_id: str) -> bool:
        if container_id not in self.buque:
            return False
        cont = self.containers[container_id]
        self.buque.remove(container_id)
        self.piso.append(container_id)
        cont.posicion_actual = "PISO"
        cont.estado = "En Piso — verificación"
        self._log(container_id, "Trasladado a Piso", "BUQUE", "PISO")
        await self._broadcast()
        return True

    async def move_to_patio(self, container_id: str) -> bool:
        if container_id not in self.piso:
            return False
        cont = self.containers[container_id]
        if not self._place_in_patio(cont):
            cont.estado = "⚠ Patio lleno"
            self._log(container_id, "Error — patio lleno", "PISO", "PATIO")
            await self._broadcast()
            return False
        self.piso.remove(container_id)
        cont.posicion_actual = "PATIO"
        cont.estado = f"Almacenado — C{cont.columna} P{cont.piso}"
        self._log(container_id, f"Almacenado C{cont.columna} P{cont.piso}", "PISO", "PATIO")
        await self._broadcast()
        return True

    async def remove_from_patio(self, container_id: str) -> bool:
        cont = self.containers.get(container_id)
        if not cont or cont.posicion_actual != "PATIO":
            return False
        col, piso = cont.columna, cont.piso
        if any(self.patio[col][p] is not None for p in range(piso + 1, 4)):
            return False
        self.patio[col][piso] = None
        del self.containers[container_id]
        self._log(container_id, "Retirado del patio", "PATIO", "SALIDA")
        await self._broadcast()
        return True

    # ── Auto-advance task ─────────────────────────────────────────────────────

    async def _auto_advance(self, container_id: str) -> None:
        try:
            await asyncio.sleep(self.config.buque_time)
            await self.move_to_piso(container_id)
            await asyncio.sleep(self.config.piso_time)
            await self.move_to_patio(container_id)
        except asyncio.CancelledError:
            pass
        finally:
            self._advance_tasks.pop(container_id, None)

    # ── Public operations ─────────────────────────────────────────────────────

    async def add_container(self) -> Contenedor:
        cont = self._make_container()
        self._arrive_in_buque(cont)
        await self._broadcast()
        if self.config.auto_advance:
            task = asyncio.create_task(self._auto_advance(cont.id))
            self._advance_tasks[cont.id] = task
        return cont

    async def advance_container(self, container_id: str) -> bool:
        if container_id in self.buque:
            return await self.move_to_piso(container_id)
        if container_id in self.piso:
            return await self.move_to_patio(container_id)
        return False

    async def start_auto(self) -> None:
        if self.auto_running:
            return
        self.auto_running = True
        self._log("SYSTEM", "Modo automático iniciado", "—", "—")
        self._auto_task = asyncio.create_task(self._generator_loop())
        await self._broadcast()

    async def stop_auto(self) -> None:
        if not self.auto_running:
            return
        self.auto_running = False
        if self._auto_task:
            self._auto_task.cancel()
            self._auto_task = None
        self._log("SYSTEM", "Modo automático detenido", "—", "—")
        await self._broadcast()

    async def _generator_loop(self) -> None:
        try:
            while self.auto_running:
                if self.config.max_containers == 0 or len(self.containers) < self.config.max_containers:
                    cont = self._make_container()
                    self._arrive_in_buque(cont)
                    await self._broadcast()
                    task = asyncio.create_task(self._auto_advance(cont.id))
                    self._advance_tasks[cont.id] = task
                await asyncio.sleep(self.config.arrival_interval)
        except asyncio.CancelledError:
            pass

    async def reset(self) -> None:
        await self.stop_auto()
        for task in self._advance_tasks.values():
            task.cancel()
        self._advance_tasks.clear()
        self.containers.clear()
        self.buque.clear()
        self.piso.clear()
        self.patio = [[None] * 4 for _ in range(10)]
        self.events.clear()
        self._counter = 0
        self._log("SYSTEM", "Sistema reiniciado", "—", "—")
        await self._broadcast()
