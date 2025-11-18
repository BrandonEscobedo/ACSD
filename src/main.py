import streamlit as st
import time
import base64
from pathlib import Path
from dataclasses import dataclass
import pandas as pd
from models.simulation_models import  LineaTransportista 
from simulation.simulation import ejecutar_simulacion, simular_asignacion
from pathlib import Path
st.set_page_config(page_title="SimPy + Animación", layout="wide")

BASE_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = BASE_DIR / "assets"

svg_path = ASSETS_DIR / "contenedor.svg"
svg = svg_path.read_text(encoding="utf-8")
svg_bytes = Path(svg_path).read_bytes()
svg_b64 = base64.b64encode(svg_bytes).decode("utf-8")
svg_img = f"data:image/svg+xml;base64,{svg_b64}"

LINEAS_DEMO = [
    LineaTransportista(1, "Maersk Logistics", True, 92, 88, "contacto@maersk.com"),
    LineaTransportista(2, "Hapag-Lloyd Express", True, 80, 75, "service@hapag.com"),
    LineaTransportista(3, "MSC Cargo", False, 85, 70, "ops@msc.com"),
    LineaTransportista(4, "ONE Transport", True, 78, 90, "support@one.com"),
]

ZONAS = {
    "BUQUE": {"x": 0, "y": 60, "color": "#2E86AB", "label": "🚢 Buque"},
    "PISO": {"x": 180, "y": 60, "color": "#A23B72", "label": "📍 Piso"},
    "PATIO": {"x": 360, "y": 60, "color": "#F18F01", "label": "🏭 Patio"},
}

TIEMPO_BUQUE_A_PISO = 2.0
TIEMPO_PISO_A_PATIO = 1.5

st.markdown("""
<style>
/*
Target CUALQUIER SVG que tenga el ID 'stElementToolbarButtonIcon'
Y que esté DENTRO de un botón con el ID 'stBaseButton-elementToolbar'
*/
button[data-testid="stBaseButton-elementToolbar"] svg[data-testid="stElementToolbarButtonIcon"] {
    /* Hacemos el ícono (el dibujo SVG) un 80% más grande */
    transform: scale(1.8) !important;
    transform-origin: center center !important;
}

/* Y hacemos el ÁREA CLICKEABLE (el botón) más grande */
button[data-testid="stBaseButton-elementToolbar"] {
    padding: 0.5rem !important; /* Más relleno = botón más grande */
}
</style>
""", unsafe_allow_html=True)
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

def renderizar_patio(patio, svg_img, ancho=60, alto=45):
    """
    patio = matriz [10 columnas][4 pisos]
    piso 0 = abajo, piso 3 = arriba
    """
    html = """
    <div style="padding:20px;">
        <h3 style="text-align:center;">🏭 Patio – Vista por Columnas y Pisos</h3>
        <div style="display:flex; flex-direction:row; gap:15px; justify-content:center;">
    """

    for col in range(10):
        html += "<div style='display:flex; flex-direction:column-reverse; gap:8px;'>"

        # pisos 0 a 3 (pero se dibujan de abajo hacia arriba)
        for piso in range(4):
            cont = patio[col][piso]
            if cont is None:
                html += f"""
                <div style="
                    width:{ancho}px; height:{alto}px;
                    border:2px dashed #999;
                    border-radius:6px;
                    background:#f0f0f0;
                    display:flex; justify-content:center; align-items:center;
                    font-size:12px; color:#666;">
                    {piso}
                </div>
                """
            else:
                html += f"""
                <div style="
                    width:{ancho}px; height:{alto}px;
                    border:3px solid #2E86AB;
                    border-radius:6px;
                    background:#d7ecfa;
                    display:flex; justify-content:center; align-items:center;">
                    <img src="{svg_img}" style="width:40px;">
                </div>
                """

        # etiqueta columna
        html += f"<div style='text-align:center; font-weight:bold;'>{col}</div>"
        html += "</div>"

    html += "</div></div>"

    return html

# ==================== ejecutar simulacion ====================
if st.session_state.get('simular', False):
    with st.spinner("Ejecutando SimPy..."):
        duracion_total = (num_contenedores * intervalo) + 10
        simulador = ejecutar_simulacion(num_contenedores, intervalo, duracion_total)
        st.subheader("🏭 Estado del Patio (10 columnas × 4 pisos)")
        html_patio = renderizar_patio(simulador.patio, svg_img)
        st.markdown(html_patio, unsafe_allow_html=True)
        st.success(f"Simulación terminada: {len(simulador.eventos)} eventos")

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

    # ========== ASIGNACIÓN DE lineas ==========
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
