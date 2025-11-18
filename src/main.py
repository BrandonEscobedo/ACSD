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
from simulation.simulation import ejecutar_simulacion, simular_asignacion
from pathlib import Path
st.set_page_config(page_title="SimPy + Animación", layout="wide")

BASE_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = BASE_DIR / "assets"

svg_path = ASSETS_DIR / "contenedor.svg"
svg = svg_path.read_text(encoding="utf-8")

try:
    svg_bytes = Path(svg_path).read_bytes()
    svg_b64 = base64.b64encode(svg_bytes).decode("utf-8")
    svg_img = f"data:image/svg+xml;base64,{svg_b64}"
except FileNotFoundError:
    svg_img = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100'%3E%3Crect width='100' height='100' fill='%234A90E2'/%3E%3Ctext x='50' y='55' text-anchor='middle' fill='white' font-size='40'%3E📦%3C/text%3E%3C/svg%3E"


LINEAS_DEMO = [
    LineaTransportista(1, "Maersk Logistics", True, 92, 88, "contacto@maersk.com"),
    LineaTransportista(2, "Hapag-Lloyd Express", True, 80, 75, "service@hapag.com"),
    LineaTransportista(3, "MSC Cargo", False, 85, 70, "ops@msc.com"),
    LineaTransportista(4, "ONE Transport", True, 78, 90, "support@one.com"),
]




# ==================== CONFIG ZONAS ====================
ZONAS = {
    "BUQUE": {"x": 0, "y": 60, "color": "#2E86AB", "label": "🚢 Buque"},
    "PISO": {"x": 180, "y": 60, "color": "#A23B72", "label": "📍 Piso"},
    "PATIO": {"x": 360, "y": 60, "color": "#F18F01", "label": "🏭 Patio"},
}

TIEMPO_BUQUE_A_PISO = 2.0
TIEMPO_PISO_A_PATIO = 1.5




# ==================== VISUALIZACIÓN ====================
def crear_escena_html(contenedores_por_zona, contenedor_activo=None):
    zonas_html = ""
    for zona_nombre, zona_info in ZONAS.items():
        conts = contenedores_por_zona.get(zona_nombre, [])
        zonas_html += f"""
        <div style="position: relative; width: 100%; height: 200px;
            border: 4px solid {zona_info['color']};
            background: linear-gradient(90deg,{zona_info['color']}22,{zona_info['color']}44);
            border-radius: 20px; margin: 20px 0;">
            <div style="position: absolute; left: 20px; top: 50%; transform: translateY(-50%);
                font-weight: bold; font-size: 32px; color: {zona_info['color']};">
                {zona_info['label']}
            </div>
            <div style="position:absolute; top:20px; right:20px;
                background:{zona_info['color']}; color:white; padding:10px 20px;
                border-radius:25px; font-weight:bold;">
                {len(conts)} 📦
            </div>
        """

        for idx, cnt in enumerate(conts[:15]):
            active = (contenedor_activo and cnt.id == contenedor_activo.id)
            zonas_html += f"""
            <img src="{svg_img}" style="
                position:absolute; left:{200 + idx*60}px; top:50%;
                transform:translateY(-50%) scale({1.3 if active else 1});
                width:50px; opacity:{1 if active else 0.7};
                transition:all .4s ease;">
            """

        zonas_html += "</div>"

    return f"<div style='padding:30px;'>{zonas_html}</div>"


def animar_simulacion(simulador, velocidad=0.5):
    col1, col2 = st.columns([2, 1])
    with col1:
        placeholder = st.empty()

    contenedores_por_zona = {"BUQUE": [], "PISO": [], "PATIO": []}

    for evento in simulador.eventos:
        cont = next(c for c in simulador.contenedores if c.id == evento.contenedor_id)

        for zona in contenedores_por_zona.values():
            if cont in zona:
                zona.remove(cont)

        if evento.destino in contenedores_por_zona:
            contenedores_por_zona[evento.destino].append(cont)

        html = crear_escena_html(contenedores_por_zona, cont)
        placeholder.html(html)
        time.sleep(velocidad)


# ==================== INTERFAZ STREAMLIT ====================
st.title("🚢 Simulación: Buque → Piso → Patio")
st.markdown("SimPy + Animación + Asignación de Línea Transportista")

with st.sidebar:
    st.header("⚙️ Configuración")
    num_contenedores = st.slider("Número de contenedores", 1, 10, 5)
    intervalo = st.slider("Intervalo entre llegadas", 0.5, 5.0, 1.5)
    velocidad_animacion = st.slider("Velocidad de animación", 0.1, 2.0, 0.5)

    st.markdown("---")
    st.info(f"⏱️ Buque → Piso: {TIEMPO_BUQUE_A_PISO}u")
    st.info(f"⏱️ Piso → Patio: {TIEMPO_PISO_A_PATIO}u")

col1, col2 = st.columns([1, 3])
with col1:
    if st.button("▶️ Iniciar Simulación"):
        st.session_state['simular'] = True
with col2:
    if st.button("🔄 Reiniciar"):
        st.session_state['simular'] = False
        st.rerun()


# ==================== EJECUTAR SIMULACIÓN ====================
if st.session_state.get('simular', False):
    with st.spinner("Ejecutando SimPy..."):
        duracion_total = (num_contenedores * intervalo) + 10
        simulador = ejecutar_simulacion(num_contenedores, intervalo, duracion_total)
        st.success(f"Simulación terminada: {len(simulador.eventos)} eventos")

    st.metric("Procesados", len(simulador.contenedores))
    st.metric("Final en Patio", sum(1 for c in simulador.contenedores if c.posicion_actual == "PATIO"))
    st.metric("Eventos", len(simulador.eventos))

    st.markdown("---")

    if st.button("🎬 Reproducir Animación"):
        animar_simulacion(simulador, velocidad_animacion)

    with st.expander("📊 Eventos"):
        df = pd.DataFrame([{
            "Tiempo": e.tiempo,
            "Contenedor": e.contenedor_id,
            "Acción": e.accion,
            "Origen": e.origen,
            "Destino": e.destino
        } for e in simulador.eventos])
        st.dataframe(df)

    # ========== ASIGNACIÓN DE LÍNEAS ==========
    st.header("🚚 Asignación de Línea Transportista")

    conts_patio = [c for c in simulador.contenedores if c.posicion_actual == "PATIO"]

    if not conts_patio:
        st.info("Aún no llegan contenedores al patio.")
    else:
        seleccion = st.selectbox("Selecciona un contenedor:", [c.id for c in conts_patio])
        elegido = next(c for c in conts_patio if c.id == seleccion)

        if st.button("🚚 Simular Asignación"):
            mejor, resultados = simular_asignacion(elegido, LINEAS_DEMO)

            st.subheader("Resultados por Línea")
            st.dataframe(pd.DataFrame(resultados))

            if mejor:
                st.success(f"⭐ Línea Recomendada: **{mejor['línea']}**")
                st.write(f"🎯 Puntaje: `{mejor['puntaje']:.2f}`")
                st.write(f"📞 Contacto: {mejor['contacto']}")

else:
    st.info("Configura la simulación y presiona Iniciar.")
