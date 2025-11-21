import simpy
from dataclasses import dataclass
from typing import List
import random
from pathlib import Path
from services.visual_service import VisualService
from models.simulation_models import Contenedor, EventoSimulacion, LineaTransportista, TipoCarga
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

# ==================== Funciones de Asignación y Patio ====================

def calcular_probabilidad_sin_eir(contenedor: Contenedor, linea_info: dict) -> tuple[bool, float]:
    """
    Calcula la probabilidad de que la carga NO traiga papelería EIR.
    Retorna (tiene_eir: bool, probabilidad_fallo: float)
    """
    # Factores base de riesgo (mientras peores los indicadores, mayor probabilidad de fallo)
    riesgo_cumplimiento = (100 - linea_info["cumplimiento"]) / 100  # 0 a 1
    riesgo_puntualidad = (100 - linea_info["puntualidad"]) / 100   # 0 a 1
    riesgo_reprogramaciones = min(linea_info["reprogramaciones"] / 5, 1.0)  # normalizado
    riesgo_lead_time = max(0, (linea_info["lead_time"] - 2) / 6)  # lead_time bajo = más riesgo inverso
    
    # Lead time bajo incrementa el riesgo (procesos apresurados)
    if linea_info["lead_time"] < 3:
        riesgo_lead_time = 0.4  # alto riesgo si es muy rápido
    elif linea_info["lead_time"] < 5:
        riesgo_lead_time = 0.2  # riesgo moderado
    else:
        riesgo_lead_time = 0.05  # bajo riesgo si hay tiempo suficiente
    
    # Puntaje bajo = mayor riesgo
    riesgo_puntaje = max(0, 1 - (linea_info["puntaje"] / 100))
    
    # Factores del contenedor
    riesgo_tipo_carga = 0.0
    if contenedor.carga_tipo == TipoCarga.PELIGROSA:
        riesgo_tipo_carga = 0.15  # carga peligrosa tiene más requisitos documentales
    elif contenedor.carga_tipo == TipoCarga.REFRIGERADA:
        riesgo_tipo_carga = 0.12  # requiere documentación especial
    elif contenedor.carga_tipo == TipoCarga.FRAGIL:
        riesgo_tipo_carga = 0.10  # carga frágil requiere documentación especial
    elif contenedor.carga_tipo == TipoCarga.NODRIZA:
        riesgo_tipo_carga = 0.08  # nodriza tiene requisitos adicionales
    else:  # SECA
        riesgo_tipo_carga = 0.05  # carga seca tiene menos riesgo
    
    # Contenedores de 40 pies tienen más documentación
    riesgo_tamano = 0.08 if contenedor.tamano_pies == 40 else 0.03
    
    # Algunos compradores pueden ser más propensos a errores documentales
    riesgo_comprador = 0.0
    if "S.A." in contenedor.comprador:
        riesgo_comprador = 0.05  # empresas establecidas son más formales
    elif "Corp" in contenedor.comprador:
        riesgo_comprador = 0.03
    else:
        riesgo_comprador = 0.10  # clientes menos conocidos tienen más riesgo
    
    # Cálculo de probabilidad total de fallo (que NO tenga EIR)
    probabilidad_fallo = (
        riesgo_cumplimiento * 0.25 +
        riesgo_puntualidad * 0.20 +
        riesgo_reprogramaciones * 0.15 +
        riesgo_lead_time * 0.15 +
        riesgo_puntaje * 0.10 +
        riesgo_tipo_carga * 0.08 +
        riesgo_tamano * 0.04 +
        riesgo_comprador * 0.03
    )
    
    # Limitar entre 0.02 (2% mínimo) y 0.65 (65% máximo)
    probabilidad_fallo = max(0.02, min(probabilidad_fallo, 0.65))
    
    # Determinar aleatoriamente si tiene o no EIR
    tiene_eir = random.random() > probabilidad_fallo
    
    return tiene_eir, probabilidad_fallo


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

        linea_info = {
            "línea": linea.nombre,
            "cumplimiento": linea.porcentaje_cumplimiento,
            "puntualidad": linea.porcentaje_puntualidad,
            "reprogramaciones": reprogramaciones,
            "espera_promedio": espera,
            "lead_time": lead_time,
            "puntaje": puntaje,
            "contacto": linea.contacto
        }
        
        # Calcular probabilidad de papelería EIR
        tiene_eir, prob_fallo = calcular_probabilidad_sin_eir(contenedor, linea_info)
        
        # Agregar información de EIR al resultado
        linea_info["tiene_eir"] = tiene_eir
        linea_info["probabilidad_sin_eir"] = round(prob_fallo * 100, 2)  # en porcentaje
        linea_info["estado_documental"] = "✓ EIR Completo" if tiene_eir else "✗ SIN EIR"
        
        # Si no tiene EIR, reducir el puntaje para la asignación
        if not tiene_eir:
            linea_info["puntaje"] = puntaje * 0.6  # penalización del 40%
            linea_info["observaciones"] = "⚠ Requiere completar documentación EIR"
        else:
            linea_info["observaciones"] = "Documentación completa"
        
        resultados.append(linea_info)

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
            # Asignar campos adicionales: tipo de carga, comprador y tamaño
            comprador_random = random.choice(["ACME Corp", "Importadora S.A.", "Distribuciones S.A.", "Cliente X"])
            tipo_carga_random = random.choice(list(TipoCarga))
            tamano_random = random.choice([20, 40])

            c = Contenedor(
                id=f"CNT-{i+1:03d}",
                tiempo_llegada=self.env.now,
                imagen_src=img_random,
                carga_tipo=tipo_carga_random,
                comprador=comprador_random,
                tamano_pies=tamano_random
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