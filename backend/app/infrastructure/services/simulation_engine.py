import random
from typing import List, Optional

import simpy

from app.domain.contenedor import Contenedor
from app.domain.enums import TipoCarga
from app.domain.evento import EventoSimulacion
from app.infrastructure.services.visual_service import VisualService

TIEMPO_BUQUE_A_PISO = 2.0
TIEMPO_PISO_A_PATIO = 1.5
COMPRADORES = ["ACME Corp", "Importadora S.A.", "Distribuciones S.A.", "Cliente X"]


class SimulacionEngine:
    def __init__(self, visual_service: VisualService) -> None:
        self._visual = visual_service

    def ejecutar(self, n: int, intervalo: float) -> "_Simulador":
        duracion = (n * intervalo) + 10
        env = simpy.Environment()
        sim = _Simulador(env, self._visual)
        env.process(sim._generador(n, intervalo))
        env.run(until=duracion)
        return sim


class _Simulador:
    def __init__(self, env: simpy.Environment, visual: VisualService) -> None:
        self.env = env
        self._visual = visual
        self.eventos: List[EventoSimulacion] = []
        self.contenedores: List[Contenedor] = []
        self.patio: List[List[Optional[Contenedor]]] = [
            [None for _ in range(4)] for _ in range(10)
        ]

    def _registrar(self, contenedor: Contenedor, accion: str, origen: str, destino: str) -> None:
        self.eventos.append(
            EventoSimulacion(
                tiempo=self.env.now,
                contenedor_id=contenedor.id,
                accion=accion,
                origen=origen,
                destino=destino,
            )
        )

    def _proceso_contenedor(self, contenedor: Contenedor):
        contenedor.posicion_actual = "BUQUE"
        contenedor.estado = "En Buque - Esperando descarga"
        self._registrar(contenedor, "Llegada", "MAR", "BUQUE")
        yield self.env.timeout(random.uniform(0.5, 1.5))

        contenedor.estado = "En tránsito a Piso"
        self._registrar(contenedor, "Iniciando traslado", "BUQUE", "PISO")
        yield self.env.timeout(TIEMPO_BUQUE_A_PISO)

        contenedor.posicion_actual = "PISO"
        contenedor.estado = "En Piso - Verificación"
        self._registrar(contenedor, "Llegó a Piso", "BUQUE", "PISO")
        yield self.env.timeout(random.uniform(1.0, 2.0))

        contenedor.estado = "En tránsito a Patio"
        self._registrar(contenedor, "Iniciando traslado", "PISO", "PATIO")
        yield self.env.timeout(TIEMPO_PISO_A_PATIO)

        if self._colocar_en_patio(contenedor):
            contenedor.posicion_actual = "PATIO"
            contenedor.estado = f"En Patio - C{contenedor.columna}, P{contenedor.piso}"
            self._registrar(
                contenedor,
                f"Almacenado en columna {contenedor.columna}, piso {contenedor.piso}",
                "PISO",
                "PATIO",
            )
        else:
            contenedor.estado = "Patio lleno — NO SE PUEDE ALMACENAR"
            self._registrar(contenedor, "Error almacenamiento", "PISO", "PATIO")

        yield self.env.timeout(0.1)

    def _generador(self, n: int, intervalo: float):
        for i in range(n):
            c = Contenedor(
                id=f"CNT-{i + 1:03d}",
                tiempo_llegada=self.env.now,
                imagen_src=self._visual.get_random(),
                carga_tipo=random.choice(list(TipoCarga)),
                comprador=random.choice(COMPRADORES),
                tamano_pies=random.choice([20, 40]),
            )
            self.contenedores.append(c)
            self.env.process(self._proceso_contenedor(c))
            yield self.env.timeout(intervalo)

    def _colocar_en_patio(self, contenedor: Contenedor) -> bool:
        for col in range(10):
            for piso in range(4):
                if all(self.patio[col][p] is None for p in range(piso + 1, 4)):
                    if self.patio[col][piso] is None:
                        self.patio[col][piso] = contenedor
                        contenedor.columna = col
                        contenedor.piso = piso
                        return True
        return False
