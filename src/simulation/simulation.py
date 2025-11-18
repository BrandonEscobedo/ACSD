import streamlit as st
import simpy
import time
import base64
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict
import random
import pandas as pd
from models.simulation_models import Contenedor, EventoSimulacion, LineaTransportista

TIEMPO_BUQUE_A_PISO = 2.0
TIEMPO_PISO_A_PATIO = 1.5

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



# ==================== SIMULACIÓN SIMPY ====================
class SimuladorContenedores:
    def __init__(self, env):
        self.env = env
        self.eventos = []
        self.contenedores = []
        self.estado_actual = {}

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
        contenedor.posicion_actual = "BUQUE"
        contenedor.estado = "En Buque - Esperando descarga"
        self.registrar_evento(contenedor, "Llegada", "MAR", "BUQUE")
        yield self.env.timeout(random.uniform(0.5, 1.5))

        contenedor.estado = "En tránsito a Piso"
        self.registrar_evento(contenedor, "Iniciando traslado", "BUQUE", "PISO")
        yield self.env.timeout(TIEMPO_BUQUE_A_PISO)

        contenedor.posicion_actual = "PISO"
        contenedor.estado = "En Piso - Verificación"
        self.registrar_evento(contenedor, "Llegó a Piso", "BUQUE", "PISO")
        yield self.env.timeout(random.uniform(1.0, 2.0))

        contenedor.estado = "En tránsito a Patio"
        self.registrar_evento(contenedor, "Iniciando traslado", "PISO", "PATIO")
        yield self.env.timeout(TIEMPO_PISO_A_PATIO)

        contenedor.posicion_actual = "PATIO"
        contenedor.estado = "En Patio - Almacenado"
        self.registrar_evento(contenedor, "Llegó a Patio", "PISO", "PATIO")
        yield self.env.timeout(0.1)
        contenedor.estado = "✅ Almacenado"

    def generador_contenedores(self, n, intervalo):
        for i in range(n):
            c = Contenedor(id=f"CNT-{i+1:03d}", tiempo_llegada=self.env.now)
            self.contenedores.append(c)
            self.env.process(self.proceso_contenedor(c))
            yield self.env.timeout(intervalo)


def ejecutar_simulacion(n, intervalo, duracion):
    env = simpy.Environment()
    sim = SimuladorContenedores(env)
    env.process(sim.generador_contenedores(n, intervalo))
    env.run(until=duracion)
    return sim