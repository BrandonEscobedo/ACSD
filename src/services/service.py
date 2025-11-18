# app.py
import streamlit as st
import simpy
import time
import random
import base64
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List, Dict

# ----------------- Config Streamlit -----------------
st.set_page_config(page_title="SimPy + Animación (Buque→Patio→Asignación)", layout="wide")

# ----------------- SVG (base64) -----------------
from models.simulation_models import LineasTransportistas
st.set_page_config(page_title="SimPy + Animación", layout="wide")

try:
    svg_bytes = Path("contenedor.svg").read_bytes()
    svg_b64 = base64.b64encode(svg_bytes).decode("utf-8")
    svg_img = f"data:image/svg+xml;base64,{svg_b64}"
except FileNotFoundError:
    svg_img = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100'%3E%3Crect width='100' height='100' fill='%234A90E2'/%3E%3Ctext x='50' y='55' text-anchor='middle' fill='white' font-size='40'%3E📦%3C/text%3E%3C/svg%3E"


# ----------------- Dataclasses -----------------
@dataclass
class Contenedor:
    id: str
    tiempo_llegada: float
    posicion_actual: str = "BUQUE"
    estado: str = "En Buque"

@dataclass
class LineasTransportistas:
    id: int
    nombre: str
    disponible: bool
    porcentaje_cumplimiento: float   # 0..1 (declarado)
    porcentaje_puntualidad: float    # 0..1 (declarado)
    contacto: Optional[str] = None

    # métricas acumuladas durante la simulación
    reprogramaciones: int = 0
    tiempo_espera_total: float = 0.0  # suma de tiempos de espera de contenedores que asignó
    asignaciones: int = 0
    lead_time_total: float = 0.0      # tiempo desde disponibilidad en patio hasta salida con esa línea
    cumplimientos_observados: int = 0 # cantidad de retiros exitosos observados


# ----------------- Zonas para visualización -----------------
ZONAS = {
    "BUQUE": {"label": "🚢 Buque", "color": "#2E86AB"},
    "PISO":  {"label": "📍 Piso",  "color": "#A23B72"},
    "PATIO": {"label": "🏭 Patio", "color": "#F18F01"},
    "CARGADO": {"label": "✅ Cargado", "color": "#2ECC71"},
}

# ----------------- Parámetros temporales (unidades arbitrarias) -----------------
TIEMPO_BUQUE_A_PISO = 1.5
TIEMPO_PISO_A_PATIO = 1.0
TIEMPO_CARGA_BASE = 2.0  # tiempo que ocupa la línea para cargar (simulado)


# ----------------- Simulador con SimPy -----------------
class SimuladorContenedores:
    def __init__(self, env: simpy.Environment, lineas: List[LineasTransportistas]):
        self.env = env
        self.lineas = lineas
        self.contenedores: List[Contenedor] = []
        self.eventos: List[Dict] = []  # lista de dicts: {tiempo, id, accion, origen, destino}
        self.estado_actual: Dict[str, str] = {}

    def log_evento(self, cont: Contenedor, accion: str, origen: str, destino: str):
        evento = {
            "tiempo": float(self.env.now),
            "contenedor_id": cont.id,
            "accion": accion,
            "origen": origen,
            "destino": destino
        }
        self.eventos.append(evento)
        # actualizar estado
        self.estado_actual[cont.id] = destino

    # criterio para elegir mejor linea entre disponibles
    def seleccionar_mejor_linea(self, disponibles: List[LineasTransportistas]) -> LineasTransportistas:
        def score(l: LineasTransportistas):
            # score simple: peso al cumplimiento y puntualidad, penaliza reprogramaciones
            return (l.porcentaje_cumplimiento * 0.55 +
                    l.porcentaje_puntualidad * 0.35 +
                    (1.0 / (1 + l.reprogramaciones)) * 0.10)
        return max(disponibles, key=score)

    def proceso_asignacion_transporte(self, cont: Contenedor):
        # Se intenta asignar una línea cuando el contenedor está en PATIO.
        llegada_patio = self.env.now
        self.log_evento(cont, "Disponible en patio", "PATIO", "PATIO")
        # Intentos hasta que se asigne con éxito
        intentos = 0
        assigned_line: Optional[LineasTransportistas] = None

        while True:
            intentos += 1
            # Filtrar líneas que "estén disponibles" en sentido operativo
            disponibles = [l for l in self.lineas if l.disponible]

            if not disponibles:
                # nadie disponible -> esperar y contar reprogramación tentativa
                for l in self.lineas:
                    l.reprogramaciones += 0  # no incrementar aún, solo esperar
                yield self.env.timeout(1.0)
                continue

            # seleccionar candidato por score
            candidato = self.seleccionar_mejor_linea(disponibles)

            # Simular si la linea cumple en esta ocasión (probabilidad según porcentaje_cumplimiento)
            rnd = random.random()
            cumple = rnd <= candidato.porcentaje_cumplimiento

            if not cumple:
                # fallo: reprogramación
                candidato.reprogramaciones += 1
                self.log_evento(cont, "Fallo en línea (reprogramación)", "PATIO", candidato.nombre)
                # esperar un tiempo antes de volver a intentar (simula llamada / reprogramación)
                yield self.env.timeout(1.0)
                continue

            # Si cumple, asignamos
            assigned_line = candidato
            break

        # registrar métricas de asignación
        espera = self.env.now - llegada_patio
        assigned_line.tiempo_espera_total += espera
        assigned_line.asignaciones += 1
        assigned_line.lead_time_total += espera  # en este modelo lead time = espera hasta cargar
        assigned_line.cumplimientos_observados += 1

        # marcar contenedor como "en carga" y la linea no disponible mientras carga
        assigned_line.disponible = False
        self.log_evento(cont, f"Asignado a {assigned_line.nombre}", "PATIO", assigned_line.nombre)

        # Simular tiempo de carga (puede variar algo)
        tiempo_carga = TIEMPO_CARGA_BASE + random.uniform(-0.5, 0.8)
        yield self.env.timeout(max(0.5, tiempo_carga))

        # carga exitosa → contenedor sale
        cont.posicion_actual = "CARGADO"
        cont.estado = "Cargado y en salida"
        self.log_evento(cont, "Cargado y salió", assigned_line.nombre, "SALIDA")

        # liberar la linea
        assigned_line.disponible = True

    def proceso_contenedor(self, cont: Contenedor):
        # Llega al buque (registro)
        cont.posicion_actual = "BUQUE"
        cont.estado = "En Buque"
        self.log_evento(cont, "En Buque (llegada)", "MAR", "BUQUE")

        # espera en buque (descarga)
        yield self.env.timeout(random.uniform(0.3, 1.0))

        # traslado buque -> piso
        self.log_evento(cont, "Saliendo buque -> piso", "BUQUE", "PISO")
        yield self.env.timeout(TIEMPO_BUQUE_A_PISO)
        cont.posicion_actual = "PISO"
        cont.estado = "En Piso"
        self.log_evento(cont, "En Piso (verificación)", "BUQUE", "PISO")

        # verificación en piso
        yield self.env.timeout(random.uniform(0.5, 1.5))

        # traslado piso -> patio
        self.log_evento(cont, "Saliendo piso -> patio", "PISO", "PATIO")
        yield self.env.timeout(TIEMPO_PISO_A_PATIO)
        cont.posicion_actual = "PATIO"
        cont.estado = "En Patio"
        self.log_evento(cont, "En Patio (listo para asignación)", "PISO", "PATIO")

        # lanza proceso de asignación para esta carga (no bloqueante)
        self.env.process(self.proceso_asignacion_transporte(cont))

    def generador_contenedores(self, num: int, intervalo: float):
        for i in range(num):
            cont = Contenedor(id=f"CNT-{i+1:03d}", tiempo_llegada=self.env.now)
            self.contenedores.append(cont)
            # iniciar su proceso
            self.env.process(self.proceso_contenedor(cont))
            # esperar intervalo hasta siguiente
            yield self.env.timeout(intervalo)

# ----------------- Ejecutar simulación -----------------
def ejecutar_simulacion(num_contenedores: int, intervalo: float, lineas: List[LineasTransportistas]) -> SimuladorContenedores:
    env = simpy.Environment()
    simulador = SimuladorContenedores(env, lineas)
    # iniciar generador
    env.process(simulador.generador_contenedores(num_contenedores, intervalo))
    # calcular duración razonable
    dur = num_contenedores * (intervalo + TIEMPO_BUQUE_A_PISO + TIEMPO_PISO_A_PATIO + TIEMPO_CARGA_BASE) + 5
    env.run(until=dur)
    return simulador

# ----------------- Visual (HTML) -----------------
def crear_escena_html(contenedores_por_zona: Dict[str, List[Contenedor]], cont_activo_id: Optional[str] = None):
    # crea un HTML con tres banderas verticales (BUQUE, PISO, PATIO)
    zonas_html = ""
    zone_width = 1000
    for zona, info in ZONAS.items():
        conts = contenedores_por_zona.get(zona, [])
        count = len(conts)
        zonas_html += f"""
        <div style="position: relative; width: 100%; height: 160px; border-radius: 12px; margin: 12px 0;
                    background: linear-gradient(90deg, {info['color']}22 0%, {info['color']}44 100%);
                    border: 3px solid {info['color']};">
            <div style="position:absolute; left:16px; top:50%; transform: translateY(-50%); font-weight:800; font-size:22px; color:{info['color']}">
                {info['label']}
            </div>
            <div style="position:absolute; right:16px; top:12px; background:{info['color']}; color:white; padding:8px 14px; border-radius:20px; font-weight:700;">
                {count} 📦
            </div>
        """

        # dibujar contenedores en zona (máx 12 mostrados)
        for idx, c in enumerate(conts[:12]):
            is_active = (c.id == cont_activo_id)
            left_px = 120 + idx * 70
            scale = 1.2 if is_active else 1.0
            opacity = 1.0 if is_active else 0.85
            transform = f"translateY(-50%) scale({scale})"
            filter_style = "filter: drop-shadow(0 6px 12px rgba(0,0,0,0.25));"
            zonas_html += f"""
            <img src="{svg_img}" style="
                position:absolute;
                left:{left_px}px;
                top:50%;
                transform:{transform};
                width:48px;
                height:48px;
                opacity:{opacity};
                transition: all 0.35s ease;
                {filter_style}
            "/>
            """

        zonas_html += "</div>"

    html = f"""
    <div style="padding: 18px; border-radius: 14px; background: linear-gradient(#f7fbff, #eef7ff); box-shadow: 0 10px 20px rgba(0,0,0,0.06);">
        {zonas_html}
    </div>
    """
    return html

# ----------------- Métricas -----------------
def calcular_metricas(sim: SimuladorContenedores):
    # métricas globales
    total_reprog = sum(l.reprogramaciones for l in sim.lineas)
    tiempos_espera = []
    lead_times = []
    tasas = []
    detalles = []
    for l in sim.lineas:
        asign = l.asignaciones
        t_espera_prom = (l.tiempo_espera_total / asign) if asign > 0 else 0.0
        lead_prom = (l.lead_time_total / asign) if asign > 0 else 0.0
        tasa_obs = (l.cumplimientos_observados / asign) if asign > 0 else 0.0
        detalles.append({
            "Linea": l.nombre,
            "Asignaciones": asign,
            "Reprogramaciones": l.reprogramaciones,
            "Tiempo promedio espera (u)": round(t_espera_prom, 3),
            "Lead time promedio (u)": round(lead_prom, 3),
            "Tasa cumplimiento observado": round(tasa_obs, 3),
            "Cumplimiento declarado": l.porcentaje_cumplimiento,
            "Puntualidad declarada": l.porcentaje_puntualidad
        })
        if asign > 0:
            tiempos_espera.append(t_espera_prom)
            lead_times.append(lead_prom)
            tasas.append(tasa_obs)

    tiempo_promedio_espera_global = (sum(tiempos_espera) / len(tiempos_espera)) if tiempos_espera else 0.0
    lead_promedio_global = (sum(lead_times) / len(lead_times)) if lead_times else 0.0

    return {
        "total_reprogramaciones": total_reprog,
        "tiempo_promedio_espera_global": round(tiempo_promedio_espera_global, 3),
        "lead_time_promedio_global": round(lead_promedio_global, 3),
        "detalles_lineas": detalles
    }

# ----------------- Streamlit UI -----------------
st.title("🚢 SimPy + Streamlit: Asignación de Líneas Transportistas")
st.markdown("Simulación del flujo **Buque → Piso → Patio → Asignación → Carga → Salida** con métricas por línea transportista.")

# Sidebar config
with st.sidebar:
    st.header("Parámetros")
    num_contenedores = st.slider("Número de contenedores", 1, 12, 5)
    intervalo = st.slider("Intervalo entre llegadas (u)", 0.2, 3.0, 1.0, step=0.1)
    velocidad_anim = st.slider("Velocidad animación (s por evento)", 0.05, 1.0, 0.3, step=0.05)
    st.markdown("---")
    st.markdown("Define líneas transportistas (ejemplo)")
    # Ejemplo por defecto (puedes editar en el código si quieres otros)
    st.info("Se usarán 3 líneas de ejemplo. Cambia en el código si quieres más.")

# crear líneas de ejemplo (podrías exponer en UI)
lineas_default = [
    LineasTransportistas(1, "MAERSK", True, 0.92, 0.88, "555-1001"),
    LineasTransportistas(2, "HAPAG-LLOYD", True, 0.90, 0.92, "555-1002"),
    LineasTransportistas(3, "CMA-CGM", True, 0.85, 0.80, "555-1003"),
]

# botones principales
colA, colB, colC = st.columns([1,1,2])
with colA:
    run_sim = st.button("▶️ Ejecutar Simulación")
with colB:
    rerun = st.button("🔄 Reiniciar")
with colC:
    play_anim = st.button("🎬 Reproducir Animación (si disponible)")

if rerun:
    # limpia estado
    st.experimental_rerun()

# ejecutar la simulación
sim_result = None
if run_sim:
    with st.spinner("Ejecutando SimPy..."):
        # clonar líneas para esta corrida
        lineas = [LineasTransportistas(**vars(l)) for l in lineas_default]
        simulador = ejecutar_simulacion(num_contenedores, intervalo, lineas)
        sim_result = simulador
        st.success("Simulación finalizada.")
        # guardar en session para reusarlo
        st.session_state['simulador'] = simulador

elif 'simulador' in st.session_state:
    sim_result = st.session_state['simulador']

# mostrar métricas si hay resultado
if sim_result:
    metrics = calcular_metricas(sim_result)
    st.markdown("---")
    st.subheader("📈 KPIs generales")
    st.metric("Cantidad total de reprogramaciones", metrics["total_reprogramaciones"])
    st.metric("Tiempo promedio de espera por contenedor (u)", metrics["tiempo_promedio_espera_global"])
    st.metric("Lead time promedio (u)", metrics["lead_time_promedio_global"])
    st.markdown("---")

    # mostrar tabla por línea
    import pandas as pd
    df_lineas = pd.DataFrame(metrics["detalles_lineas"])
    st.subheader("Detalle por Línea Transportista")
    st.dataframe(df_lineas, use_container_width=True)

    # recomendar mejor linea (según score en el simulador)
    mejor = sim_result.seleccionar_mejor_linea(sim_result.lineas)
    st.success(f"Recomendación (mejor línea - según criterio): {mejor.nombre}")

    # botón reproducir animación
    if play_anim:
        # preparar animación: inicializar estructuras
        contenedores_por_zona = {"BUQUE": [], "PISO": [], "PATIO": [], "CARGADO": []}
        placeholder_scene = st.empty()

        # reproducir secuencialmente cada evento
        for ev in sim_result.eventos:
            # buscar contenedor
            cont_obj = next((c for c in sim_result.contenedores if c.id == ev["contenedor_id"]), None)
            if not cont_obj:
                continue

            # limpiar de zonas previas
            for z in contenedores_por_zona.values():
                if cont_obj in z:
                    z.remove(cont_obj)

            # mover a destino del evento
            destino = ev["destino"]
            if destino in contenedores_por_zona:
                contenedores_por_zona[destino].append(cont_obj)
            elif destino == "SALIDA" or destino == "CARGADO" or destino not in contenedores_por_zona:
                # marcar como cargado/salida
                cont_obj.posicion_actual = "CARGADO"
                # agregar a CARGADO para visual
                contenedores_por_zona["CARGADO"].append(cont_obj)

            # renderizar escena y destacar el contenedor actual
            html = crear_escena_html(contenedores_por_zona, cont_activo_id=cont_obj.id)
            # usar components.html para evitar sanitización
            st.components.v1.html(html, height=520)
            time.sleep(velocidad_anim)

        st.success("🎉 Animación completada.")

# vista previa si no se ha corrido
if not sim_result:
    st.markdown("### 👀 Vista previa del sistema")
    preview_conts = [Contenedor(f"CNT-{i+1:03d}", 0) for i in range(3)]
    preview = {"BUQUE": preview_conts[:1], "PISO": preview_conts[1:2], "PATIO": preview_conts[2:]}
    st.components.v1.html(crear_escena_html(preview), height=420)
