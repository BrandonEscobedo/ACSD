from dataclasses import dataclass
from typing import List, Optional

from app.domain.contenedor import Contenedor
from app.domain.evento import EventoSimulacion
from app.infrastructure.services.simulation_engine import SimulacionEngine


@dataclass
class SimulationResult:
    eventos: List[EventoSimulacion]
    contenedores: List[Contenedor]
    patio: List[List[Optional[Contenedor]]]


class SimulationUseCase:
    def __init__(self, engine: SimulacionEngine) -> None:
        self._engine = engine

    def ejecutar(self, n_contenedores: int, intervalo: float) -> SimulationResult:
        sim = self._engine.ejecutar(n_contenedores, intervalo)
        return SimulationResult(
            eventos=sim.eventos,
            contenedores=sim.contenedores,
            patio=sim.patio,
        )
