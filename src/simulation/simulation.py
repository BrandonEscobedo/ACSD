import simpy
from dataclasses import dataclass
from typing import List
import random
from pathlib import Path
from services.visual_service import VisualService
from models.simulation_models import Contenedor, EventoSimulacion, LineaTransportista
import sys # <--- Importar sys

# -------------------------------------------------------------------
# LÓGICA DE RUTA CORREGIDA
if getattr(sys, 'frozen', False):
    # En el .exe, los assets están en la raíz del directorio temporal.
    BASE_DIR = Path(getattr(sys, '_MEIPASS', Path('.')))
else:
    # En desarrollo, la base es la carpeta raíz del proyecto (un nivel arriba de simulation/)
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

ASSETS_DIR = BASE_DIR / "assets"
# -------------------------------------------------------------------

visual_service = VisualService(ASSETS_DIR)

TIEMPO_BUQUE_A_PISO = 2.0
TIEMPO_PISO_A_PATIO = 1.5

# ==================== Funciones de Asignación y Patio (SIN CAMBIOS) ====================

def simular_asignacion(contenedor: Contenedor, lineas: List[LineaTransportista]):
    resultados = []

    for linea in lineas:
        if not linea.disponible:
            continue

        lead_time = random.uniform(2, 8)
        espera = random.uniform(1, 5)
        reprogramaciones = int((100 - linea.porcentaje_cumplimiento) / 25)

        puntaje = (
            (linea.porcentaje_cumplimiento * 0.5) +
            (linea.porcentaje_puntualidad * 0.3) +
            ((10 - lead_time) * 2)
        )

        resultados.append({
            "línea": linea.nombre,
            "cumplimiento": linea.porcentaje_cumplimiento,
            "puntualidad": linea.porcentaje_puntualidad,
            "reprogramaciones": reprogramaciones,
            "espera_promedio": espera,
            "lead_time": lead_time,
            "puntaje": puntaje,
            "contacto": linea.contacto
        })

    mejor = max(resultados, key=lambda x: x["puntaje"]) if resultados else None
    return mejor, resultados


def colocar_en_patio(contenedor, patio):
    for col in range(10):  # 10 columnas
        for piso in range(4):  # 4 niveles
            # solo se puede colocar si todo arriba está vacío
            if all(patio[col][p] is None for p in range(piso + 1, 4)):
                if patio[col][piso] is None:
                    patio[col][piso] = contenedor
                    contenedor.columna = col
                    contenedor.piso = piso
                    return True
    return False  # patio lleno


def retirar_de_patio(contenedor, patio):
    col = contenedor.columna
    piso = contenedor.piso

    # No puedes sacar si hay contenedores arriba
    if any(patio[col][p] is not None for p in range(piso + 1, 4)):
        return False  # no se puede retirar

    patio[col][piso] = None
    contenedor.columna = None
    contenedor.piso = None
    return True

# ==================== SIMULACIÓN SIMPY (SIN CAMBIOS) ====================


class SimuladorContenedores:
    def __init__(self, env):
        self.env = env
        self.eventos = []
        self.contenedores = []
        self.estado_actual = {}

        # patio = 10 columnas × 4 pisos (nivel 0 abajo, 3 arriba)
        self.patio = [[None for _ in range(4)] for _ in range(10)]

    def registrar_evento(self, contenedor, accion, origen, destino):
        evento = EventoSimulacion(
            tiempo=self.env.now,
            contenedor_id=contenedor.id,
            accion=accion,
            origen=origen,
            destino=destino
        )
        self.eventos.append(evento)
        self.estado_actual[contenedor.id] = destino

    def proceso_contenedor(self, contenedor):
        # ========================= BUQUE =========================
        contenedor.posicion_actual = "BUQUE"
        contenedor.estado = "En Buque - Esperando descarga"
        self.registrar_evento(contenedor, "Llegada", "MAR", "BUQUE")
        yield self.env.timeout(random.uniform(0.5, 1.5))

        # ================== BUQUE → PISO ==================
        contenedor.estado = "En tránsito a Piso"
        self.registrar_evento(
            contenedor, "Iniciando traslado", "BUQUE", "PISO")
        yield self.env.timeout(TIEMPO_BUQUE_A_PISO)

        contenedor.posicion_actual = "PISO"
        contenedor.estado = "En Piso - Verificación"
        self.registrar_evento(contenedor, "Llegó a Piso", "BUQUE", "PISO")
        yield self.env.timeout(random.uniform(1.0, 2.0))

        # ================== PISO → PATIO ==================
        contenedor.estado = "En tránsito a Patio"
        self.registrar_evento(
            contenedor, "Iniciando traslado", "PISO", "PATIO")
        yield self.env.timeout(TIEMPO_PISO_A_PATIO)

        # ---------- AQUI SE AGREGA LA LÓGICA DE PISOS ----------
        colocado = colocar_en_patio(contenedor, self.patio)

        if colocado:
            contenedor.posicion_actual = "PATIO"
            contenedor.estado = f"En Patio - C{contenedor.columna}, P{contenedor.piso}"
            self.registrar_evento(
                contenedor,
                f"Almacenado en columna {contenedor.columna}, piso {contenedor.piso}",
                "PISO",
                "PATIO"
            )
        else:
            contenedor.estado = "⚠ Patio lleno — NO SE PUEDE ALMACENAR"
            self.registrar_evento(
                contenedor, "Error almacenamiento", "PISO", "PATIO")

        yield self.env.timeout(0.1)

    def generador_contenedores(self, n, intervalo):
        for i in range(n):
            img_random = visual_service.obtener_imagen_random()
            c = Contenedor(
                id=f"CNT-{i+1:03d}",
                tiempo_llegada=self.env.now,
                imagen_src=img_random
            )
            self.contenedores.append(c)
            self.env.process(self.proceso_contenedor(c))
            yield self.env.timeout(intervalo)


def ejecutar_simulacion(n, intervalo, duracion):
    env = simpy.Environment()
    sim = SimuladorContenedores(env)
    env.process(sim.generador_contenedores(n, intervalo))
    env.run(until=duracion)
    return sim