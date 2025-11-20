import streamlit as st
import time
import base64
from pathlib import Path
import pandas as pd
from models.simulation_models import LineaTransportista
from simulation.simulation import ejecutar_simulacion, simular_asignacion
from services.linea_transportista_service import LineaTransportistaServicio # Nuevo import
import sys  # Importado para PyInstaller

# ==================== CONFIGURACIÓN DE RUTAS ====================

# Determina la ruta base de los recursos, ya sea en el entorno
# empaquetado (_MEIPASS) o en desarrollo.
if getattr(sys, 'frozen', False):
    # En el .exe, los recursos se copian a la raíz de _MEIPASS.
    BASE_RESOURCES_PATH = Path(getattr(sys, '_MEIPASS', Path('.')))
else:
    # En desarrollo, la base es la carpeta raíz del proyecto (un nivel arriba de src/)
    BASE_RESOURCES_PATH = Path(__file__).resolve().parent.parent

ASSETS_DIR = BASE_RESOURCES_PATH / "assets"
# El archivo JSON fue copiado a la subcarpeta 'data' del ejecutable.
JSON_PATH = BASE_RESOURCES_PATH / "data" / "lineas_transportistas.json"

# ==================== FIN CONFIGURACIÓN DE RUTAS ====================

st.set_page_config(page_title="SimPy + Animación", layout="wide")

# ==================== ASSETS Y CONFIGURACIÓN GLOBAL ====================

OPCIONES_VELOCIDAD = [0.1, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0]

# --- CARGA DE IMAGEN CONTENEDOR ---
try:
    archivos_svg = list(ASSETS_DIR.glob("*.svg"))
    svg_img = "" # Inicializar
    
    # Intentamos cargar el primer SVG válido
    for svg_path in archivos_svg:
        try:
            svg_bytes = svg_path.read_bytes()
            if svg_bytes:
                svg_b64 = base64.b64encode(svg_bytes).decode("utf-8")
                svg_img = f"data:image/svg+xml;base64,{svg_b64}"
                break
        except Exception:
            continue
            
    if not svg_img:
        svg_img = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1MCIgaGVpZ2h0PSI1MCI+PHJlY3Qgd2lkdGg9IjUwIiBoZWlnaHQ9IjUwIiBmaWxsPSIjY2NjIi8+PC9zdmc+"
        
except Exception as e:
    print(f"⚠️ Advertencia: No se pudo cargar imagen default ({e})")
    svg_img = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1MCIgaGVpZ2h0PSI1MCI+PHJlY3Qgd2lkdGg9IjUwIiBoZWlnaHQ9IjUwIiBmaWxsPSIjY2NjIi8+PC9zdmc+"

# --- CARGA DEL LOADER ANIMADO (Sin cambios) ---
loader_svg = """
<svg version="1.1" id="L2" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
  viewBox="0 0 100 100" enable-background="new 0 0 100 100" xml:space="preserve">
  <circle fill="none" stroke="#fff" stroke-width="4" stroke-miterlimit="10" cx="50" cy="50" r="48"/>
  <line fill="none" stroke-linecap="round" stroke="#fff" stroke-width="4" stroke-miterlimit="10" x1="50" y1="50" x2="85" y2="50.5">
    <animateTransform 
       attributeName="transform" 
       attributeType="XML" 
       type="rotate"
       from="0 50 50"
       to="360 50 50"
       dur="2s" 
       repeatCount="indefinite" />
  </line>
  <line fill="none" stroke-linecap="round" stroke="#fff" stroke-width="4" stroke-miterlimit="10" x1="50" y1="50" x2="49.5" y2="72">
    <animateTransform 
       attributeName="transform" 
       attributeType="XML" 
       type="rotate"
       from="0 50 50"
       to="360 50 50"
       dur="2s" 
       repeatCount="indefinite" />
  </line>
</svg>
"""
loader_b64 = base64.b64encode(loader_svg.encode('utf-8')).decode("utf-8")
loader_img = f"data:image/svg+xml;base64,{loader_b64}"

# --- CARGA DE LÍNEAS TRANSPORTISTAS USANDO EL SERVICIO ---
try:
    # Usamos la ruta JSON corregida (JSON_PATH)
    linea_servicio = LineaTransportistaServicio(str(JSON_PATH))
    LINEAS_DEMO = linea_servicio.listar_lineas()
    if not LINEAS_DEMO:
        st.warning("⚠️ No se pudieron cargar las líneas del JSON. Usando valores por defecto.")
        LINEAS_DEMO = [
            LineaTransportista(1, "Maersk Logistics", True, 92, 88, "contacto@maersk.com"),
            LineaTransportista(2, "Hapag-Lloyd Express", True, 80, 75, "service@hapag.com"),
            LineaTransportista(3, "MSC Cargo", False, 85, 70, "ops@msc.com"),
            LineaTransportista(4, "ONE Transport", True, 78, 90, "support@one.com"),
        ]
except Exception as e:
    # Esto atraparía FileNotFoundError si la ruta de PyInstaller falla catastróficamente
    st.error(f"Error fatal al cargar servicio de líneas: {e}")
    LINEAS_DEMO = []


TIEMPO_BUQUE_A_PISO = 2.0
TIEMPO_PISO_A_PATIO = 1.5

# ==================== FUNCIONES DE UTILERÍA (SIN CAMBIOS) ====================

def mostrar_loader_overlay(mensaje="Cargando..."):
    html_loader = f"""
    <div id="loader-overlay" style="
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(8px);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 99999;
        color: white;
        font-size: 24px;
        text-shadow: 0 0 10px rgba(0,255,255,0.5);
    ">
        <img src="{loader_img}" style="width: 120px; height: 120px; margin-bottom: 20px;">
        <p style="font-weight: bold;">{mensaje}</p>
    </div>
    """
    st.markdown(html_loader, unsafe_allow_html=True)

def crear_zona_buque_piso(zona_nombre, zona_info, contenedores):
    html = f"""
    <div style="position: relative; width: 100%; height: 200px;
        border: 4px solid {zona_info['color']};
        background: linear-gradient(90deg,{zona_info['color']}22,{zona_info['color']}44);
        border-radius: 20px; margin: 20px 0; box-shadow: 0 6px 12px rgba(0,0,0,0.15);">
        <div style="position: absolute; left: 20px; top: 50%; transform: translateY(-50%);
            font-weight: bold; font-size: 32px; color: {zona_info['color']};
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            {zona_info['label']}
        </div>
        <div style="position:absolute; top:20px; right:20px;
            background:{zona_info['color']}; color:white; padding:10px 20px;
            border-radius:25px; font-weight:bold; font-size:18px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.2);">
            {len(contenedores)} 📦
        </div>
    """
    for idx, cnt in enumerate(contenedores[:15]):
        src_final = cnt.imagen_src if hasattr(cnt, 'imagen_src') and cnt.imagen_src else svg_img
        html += f"""
        <img src="{src_final}" style="
            position:absolute; left:{200 + idx*60}px; top:50%;
            transform:translateY(-50%);
            width:50px; opacity:0.9;
            transition:all .4s ease;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));">
        """
    html += "</div>"
    return html

def crear_zona_patio_3d(patio_matriz, contenedor_activo=None, contenedor_seleccionado=None):
    NUM_COLUMNAS = 10
    NUM_PISOS = 4

    js_click_handler = """
    <script>
    function selectContainer(containerId) {
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            key: 'selected_container',
            value: containerId
        }, '*');
        localStorage.setItem('selected_container_id', containerId);
        window.parent.location.reload();
    }
    </script>
    """

    html = f"""
    {js_click_handler}
    <div style="position: relative; width: 100%; min-height: 550px;
        border: 4px solid #F18F01;
        background: linear-gradient(135deg, #F18F0122 0%, #F18F0144 100%);
        border-radius: 20px; margin: 20px 0; padding: 20px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        overflow-x: auto;"> <div style="position: sticky; left: 0; top: 0; z-index: 20;">
            <div style="font-weight: bold; font-size: 28px; color: #F18F01;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1); display: inline-block;">
                🏭 Patio de Almacenamiento
            </div>
            <div style="float: right; background:#F18F01; color:white; padding:8px 16px;
                border-radius:20px; font-weight:bold; font-size:16px;">
                {sum(1 for col in patio_matriz for cnt in col if cnt is not None)} 📦
            </div>
        </div>
        
        <div style="margin-top: 60px; display: flex; justify-content: center; gap: 12px; min-width: max-content; padding-bottom: 20px;">
    """

    for col_idx in range(NUM_COLUMNAS):
        html += f"""
        <div style="display: flex; flex-direction: column-reverse; align-items: center; gap: 6px;">
            <div style="background: #333; color: white; padding: 4px 8px; 
                border-radius: 4px; font-size: 12px; font-weight: bold;">
                C{col_idx}
            </div>
        """
        for piso_idx in range(NUM_PISOS):
            contenedor = patio_matriz[col_idx][piso_idx] if col_idx < len(patio_matriz) else None

            is_active = (contenedor_activo and contenedor and contenedor.id == contenedor_activo.id)
            is_selected = (contenedor_seleccionado and contenedor and contenedor.id == contenedor_seleccionado.id)

            if contenedor is None:
                html += f"""
                <div style="width: 60px; height: 60px; 
                    border: 2px dashed #ccc; border-radius: 8px;
                    background: rgba(255,255,255,0.3);
                    display: flex; align-items: center; justify-content: center;
                    font-size: 11px; color: #999;">
                    P{piso_idx}
                </div>
                """
            else:
                src_patio = contenedor.imagen_src if hasattr(contenedor, 'imagen_src') and contenedor.imagen_src else svg_img

                if is_selected:
                    border_style = "3px solid #FF9800"
                    shadow = "0 0 15px rgba(255,152,0,0.8)"
                    scale = "1.15"
                    z_index = "10"
                elif is_active:
                    border_style = "3px solid #4CAF50"
                    shadow = "0 0 15px rgba(76,175,80,0.8)"
                    scale = "1.10"
                    z_index = "5"
                else:
                    border_style = "2px solid #2196F3"
                    shadow = "0 3px 6px rgba(0,0,0,0.2)"
                    scale = "1.0"
                    z_index = "1"

                bg_color = "transparent"

                html += f"""
                <div onclick="selectContainer('{contenedor.id}')"
                    style="position: relative; width: 60px; height: 60px; 
                    background: {bg_color}; border-radius: 8px;
                    transform: scale({scale});
                    border: {border_style};       
                    transition: all 0.3s ease;
                    box-shadow: {shadow};
                    display: flex; align-items: center; justify-content: center;
                    cursor: pointer; z-index: {z_index};">
                    
                    <img src="{src_patio}" style="width: 50px; height: 50px; 
                        filter: brightness(1.1) drop-shadow(0 2px 4px rgba(0,0,0,0.3)); 
                        pointer-events: none;">
                    
                    <div style="position: absolute; top: -10px; right: -10px;
                        background: white; color: #333;
                        padding: 2px 8px; border-radius: 10px;
                        font-size: 10px; font-weight: bold;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                        pointer-events: none;">
                        {contenedor.id.split('-')[1]}
                    </div>
                </div>
                """
        html += "</div>"
    html += "</div></div>"
    return html

def crear_escena_html_completa(contenedores_por_zona, patio_matriz, contenedor_activo=None, contenedor_seleccionado=None):
    ZONAS = {
        "BUQUE": {"color": "#2E86AB", "label": "🚢 Buque"},
        "PISO": {"color": "#A23B72", "label": "📍 Piso"},
    }
    html = "<div style='padding: 20px;'>"
    html += crear_zona_buque_piso("BUQUE", ZONAS["BUQUE"], contenedores_por_zona.get("BUQUE", []))
    html += crear_zona_buque_piso("PISO", ZONAS["PISO"], contenedores_por_zona.get("PISO", []))
    html += crear_zona_patio_3d(patio_matriz, contenedor_activo, contenedor_seleccionado)
    html += "</div>"
    return html

def animar_simulacion(simulador, velocidad_inicial=0.5):
    st.markdown("### 🎬 Visualización en Tiempo Real")
    col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4, col_ctrl5 = st.columns([1, 1, 1, 2, 2])

    if 'animacion_pausada' not in st.session_state:
        st.session_state.animacion_pausada = False

    with col_ctrl1:
        if st.session_state.animacion_pausada:
            if st.button("▶️ Reanudar", use_container_width=True, type="primary"):
                st.session_state.animacion_pausada = False
                st.rerun()
        else:
            if st.button("⏸️ Pausar", use_container_width=True):
                st.session_state.animacion_pausada = True
                st.rerun()
    with col_ctrl2:
        if st.button("⏹️ Detener", use_container_width=True):
            st.session_state.animacion_activa = False
            st.rerun()
    
    with col_ctrl3:
        val_init = velocidad_inicial if velocidad_inicial in OPCIONES_VELOCIDAD else 0.5
        velocidad_seleccionada = st.select_slider("Velocidad", options=OPCIONES_VELOCIDAD, value=val_init, key="vel_anim")

    placeholder_progreso = col_ctrl4.empty()
    placeholder_info = col_ctrl5.empty()
    placeholder_escena = st.empty()

    contenedores_por_zona = {"BUQUE": [], "PISO": [], "PATIO": []}
    patio_temporal = [[None for _ in range(4)] for _ in range(10)]

    if 'evento_actual' not in st.session_state:
        st.session_state.evento_actual = 0

    # ==============================================================================
    #  CORRECCIÓN DE ELEMENTOS DESAPARECIDOS: RECONSTRUCCIÓN DE ESTADO (FAST-FORWARD)
    # ==============================================================================
    
    if st.session_state.evento_actual > 0:
        for i in range(st.session_state.evento_actual):
            evt_pasado = simulador.eventos[i]
            c_pasado = next(c for c in simulador.contenedores if c.id == evt_pasado.contenedor_id)
            
            for zona in contenedores_por_zona.values():
                if c_pasado in zona: zona.remove(c_pasado)
            
            if evt_pasado.destino in contenedores_por_zona:
                contenedores_por_zona[evt_pasado.destino].append(c_pasado)
                if evt_pasado.destino == "PATIO" and c_pasado.columna is not None and c_pasado.piso is not None:
                    patio_temporal[c_pasado.columna][c_pasado.piso] = c_pasado

    # ==============================================================================
    #  BUCLE DE ANIMACIÓN VISIBLE (Desde el evento actual en adelante)
    # ==============================================================================

    for idx, evento in enumerate(simulador.eventos[st.session_state.evento_actual:], start=st.session_state.evento_actual):
        if not st.session_state.get('animacion_activa', True): break
        while st.session_state.animacion_pausada:
            time.sleep(0.5)
            if not st.session_state.get('animacion_activa', True): break

        cont = next(c for c in simulador.contenedores if c.id == evento.contenedor_id)
        
        # 1. Quitar de zona anterior
        for zona in contenedores_por_zona.values():
            if cont in zona: zona.remove(cont)
        
        # 2. Poner en zona nueva
        if evento.destino in contenedores_por_zona:
            contenedores_por_zona[evento.destino].append(cont)
            if evento.destino == "PATIO" and cont.columna is not None and cont.piso is not None:
                patio_temporal[cont.columna][cont.piso] = cont

        # 3. Renderizar
        html = crear_escena_html_completa(contenedores_por_zona, patio_temporal, cont)
        placeholder_escena.html(html)
        
        progreso = (idx + 1) / len(simulador.eventos) * 100
        placeholder_progreso.progress(progreso / 100, text=f"Evento {idx + 1}/{len(simulador.eventos)}")
        placeholder_info.caption(f"⏱️ {evento.tiempo:.1f}s | {evento.contenedor_id}: {evento.accion}")
        
        st.session_state.evento_actual = idx + 1
        
        # Control de velocidad
        tiempo_espera = 0.5 / velocidad_seleccionada
        time.sleep(tiempo_espera)

    st.session_state.evento_actual = 0
    st.session_state.animacion_activa = False


# ==================== INTERFAZ ====================
st.title("🚢 Simulación: Buque → Piso → Patio 3D")

with st.sidebar:
    st.header("⚙️ Configuración")
    num_contenedores = st.slider("Número de contenedores", 1, 40, 15)
    intervalo = st.slider("Intervalo entre llegadas", 0.5, 5.0, 1.5)
    velocidad_animacion = st.select_slider(
        "Velocidad de animación", 
        options=OPCIONES_VELOCIDAD, 
        value=0.3
    )
    st.markdown("---")
    st.info(f"⏱️ Buque → Piso: {TIEMPO_BUQUE_A_PISO}u")
    st.info(f"⏱️ Piso → Patio: {TIEMPO_PISO_A_PATIO}u")
    st.info("📦 10 columnas × 4 pisos = 40 contenedores")

# Estado inicial
if 'simulador_persistente' not in st.session_state:
    st.session_state.simulador_persistente = None
if 'simular' not in st.session_state:
    st.session_state.simular = False

col1, col2 = st.columns([1, 3])
with col1:
    if st.button("▶️ Iniciar Simulación", type="primary"):
        st.session_state['simular'] = True
        st.session_state['mostrar_loader'] = True
        st.rerun()

with col2:
    if st.button("🔄 Reiniciar"):
        st.session_state['simular'] = False
        st.session_state.simulador_persistente = None
        st.session_state['mostrar_loader'] = False
        if 'asignacion_resultados' in st.session_state: del st.session_state['asignacion_resultados']
        st.rerun()

# ==================== LÓGICA PRINCIPAL CON LOADER ====================

# 1. Si hay que mostrar loader (INICIO), lo mostramos
if st.session_state.get('mostrar_loader', False):
    mostrar_loader_overlay("Calculando simulación...")
    duracion_total = (num_contenedores * intervalo) + 10
    st.session_state.simulador_persistente = ejecutar_simulacion(num_contenedores, intervalo, duracion_total)
    st.session_state.evento_actual = 0
    time.sleep(1)
    st.session_state['mostrar_loader'] = False
    st.rerun()

# 2. Si ya tenemos datos persistentes, mostramos la interfaz
if st.session_state.get('simular', False) and st.session_state.simulador_persistente:
    
    simulador = st.session_state.simulador_persistente
    st.success(f"✅ Simulación terminada: {len(simulador.eventos)} eventos. Líneas cargadas: {len(LINEAS_DEMO)}")

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Procesados", len(simulador.contenedores))
    en_patio = sum(1 for c in simulador.contenedores if c.posicion_actual == "PATIO")
    with col2: st.metric("En Patio", en_patio)
    with col3: st.metric("Ocupación", f"{(en_patio / 40) * 100:.1f}%")
    with col4: st.metric("Eventos", len(simulador.eventos))

    st.markdown("---")

    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        if st.button("🎬 Reproducir Animación", type="primary", use_container_width=True):
            st.session_state.animacion_activa = True
            st.session_state.animacion_pausada = False
            st.session_state.evento_actual = 0
            st.session_state.mostrar_panel_interactivo = False
            st.rerun()

    with col_btn2:
        if st.button("📸 Ver Panel Interactivo", use_container_width=True):
            st.session_state.mostrar_panel_interactivo = True
            st.session_state.animacion_activa = False
            st.rerun()

    with col_btn3:
        if st.button("🔄 Reset Vista", use_container_width=True):
            st.session_state.mostrar_panel_interactivo = False
            st.session_state.animacion_activa = False
            st.session_state.contenedor_seleccionado_id = None
            st.rerun()

    st.markdown("---")

    if st.session_state.get('animacion_activa', False):
        animar_simulacion(simulador, velocidad_animacion)
        st.session_state.mostrar_panel_interactivo = True
        st.session_state.animacion_activa = False
        st.rerun()

    if st.session_state.get('mostrar_panel_interactivo', True):
        col_patio, col_panel = st.columns([3, 1])

        with col_patio:
            st.markdown("### 🏭 Estado del Patio (Interactivo)")
            if 'contenedor_seleccionado_id' not in st.session_state:
                st.session_state.contenedor_seleccionado_id = None

            conts_patio = [c for c in simulador.contenedores if c.posicion_actual == "PATIO"]

            if conts_patio:
                st.markdown("####  Selección Rápida")
                lista_opciones_dropdown = ["-- Ninguno --"] + [f"{c.id} (C{c.columna}, P{c.piso})" for c in conts_patio]

                def on_click_boton(id_cnt, str_para_dropdown):
                    st.session_state.contenedor_seleccionado_id = id_cnt
                    st.session_state.select_contenedor_key = str_para_dropdown

                cols_btns = st.columns(5)
                for idx, cnt in enumerate(conts_patio):
                    with cols_btns[idx % 5]:
                        str_valor_dropdown = f"{cnt.id} (C{cnt.columna}, P{cnt.piso})"
                        st.button(
                            f"{cnt.id.split('-')[1]}",
                            key=f"btn_{cnt.id}",
                            help=f"{cnt.id} - C{cnt.columna}, P{cnt.piso}",
                            use_container_width=True,
                            type="primary" if st.session_state.contenedor_seleccionado_id == cnt.id else "secondary",
                            on_click=on_click_boton,
                            args=(cnt.id, str_valor_dropdown)
                        )

                st.markdown("---")

                def on_change_dropdown():
                    seleccion = st.session_state.select_contenedor_key
                    if seleccion != "-- Ninguno --":
                        st.session_state.contenedor_seleccionado_id = seleccion.split()[0]
                    else:
                        st.session_state.contenedor_seleccionado_id = None

                with st.expander(" Selector por Lista", expanded=False):
                    if "select_contenedor_key" not in st.session_state:
                        st.session_state.select_contenedor_key = "-- Ninguno --"
                    st.selectbox("Buscar contenedor:", options=lista_opciones_dropdown, key="select_contenedor_key", on_change=on_change_dropdown)

            contenedor_sel = None
            if st.session_state.contenedor_seleccionado_id:
                contenedor_sel = next((c for c in conts_patio if c.id == st.session_state.contenedor_seleccionado_id), None)

            html_patio = crear_zona_patio_3d(simulador.patio, None, contenedor_sel)
            st.html(html_patio)

            col_a, col_b, col_c = st.columns(3)
            with col_a: st.metric("Total en Patio", len(conts_patio))
            with col_b: st.metric("Ocupación", f"{(len(conts_patio) / 40) * 100:.1f}%")
            with col_c: st.metric("Disponibles", 40 - len(conts_patio))

        with col_panel:
            st.markdown("###  Información del Contenedor")
            if st.session_state.contenedor_seleccionado_id and contenedor_sel:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px; border-radius: 15px; color: white;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2); margin-bottom: 20px;">
                    <h3 style="margin: 0 0 15px 0;">📦 {contenedor_sel.id}</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div><div style="font-size: 12px; opacity: 0.9;">Posición</div><div style="font-size: 18px; font-weight: bold;">C{contenedor_sel.columna}, P{contenedor_sel.piso}</div></div>
                        <div><div style="font-size: 12px; opacity: 0.9;">Estado</div><div style="font-size: 14px; font-weight: bold;">{contenedor_sel.estado}</div></div>
                        <div><div style="font-size: 12px; opacity: 0.9;">Tiempo Llegada</div><div style="font-size: 16px;">{contenedor_sel.tiempo_llegada:.2f}u</div></div>
                        <div><div style="font-size: 12px; opacity: 0.9;">Posición Actual</div><div style="font-size: 16px;">{contenedor_sel.posicion_actual}</div></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("###  Análisis de Línea Transportista")

                # 1. Botón activa estado de carga
                if st.button(" Asignar Línea de Transporte", type="primary", use_container_width=True):
                    st.session_state['cargando_asignacion'] = True
                    st.rerun()

                # 2. Si está en carga, muestra loader y calcula
                if st.session_state.get('cargando_asignacion', False):
                    mostrar_loader_overlay("Analizando líneas de transporte...")
                    time.sleep(2) # Simular tiempo de análisis
                    
                    mejor, resultados = simular_asignacion(contenedor_sel, LINEAS_DEMO)
                    
                    # Guardamos resultado vinculado al contenedor ID
                    st.session_state.asignacion_resultados = {
                        'id_contenedor': contenedor_sel.id,
                        'mejor': mejor,
                        'resultados': resultados
                    }
                    st.session_state['cargando_asignacion'] = False
                    st.rerun()

                # 3. Si hay resultados guardados para ESTE contenedor, los mostramos
                if 'asignacion_resultados' in st.session_state and \
                   st.session_state.asignacion_resultados.get('id_contenedor') == contenedor_sel.id:
                    
                    res_data = st.session_state.asignacion_resultados
                    mejor = res_data['mejor']
                    resultados = res_data['resultados']

                    st.subheader("📊 Resultados por Línea")
                    df_resultados = pd.DataFrame(resultados)
                    st.dataframe(df_resultados, use_container_width=True)
                    
                    if mejor:
                        st.success(f"⭐ **Línea Recomendada:** {mejor['línea']}")
                        col_a, col_b, col_c = st.columns(3)
                        with col_a: st.metric("🎯 Puntaje", f"{mejor['puntaje']:.2f}")
                        with col_b: st.metric("✅ Cumplimiento", f"{mejor['cumplimiento']}%")
                        with col_c: st.metric("⏱️ Lead Time", f"{mejor['lead_time']:.1f}h")
                        st.info(f"📞 **Contacto:** {mejor['contacto']}")
                        
                        import plotly.express as px
                        st.markdown("#### 📈 Comparación de Puntajes")
                        fig = px.bar(df_resultados, x='línea', y='puntaje', color='puntaje', title='Puntaje por Línea')
                        st.plotly_chart(fig, use_container_width=True)

            else:
                st.info(" Selecciona un contenedor del patio para ver su información y asignar línea")
                st.markdown("""<div style="text-align: center; padding: 40px; background: #f0f0f0; border-radius: 15px; margin-top: 20px;"><div style="font-size: 80px;">📦</div><p style="color: #666;">Selecciona un contenedor</p></div>""", unsafe_allow_html=True)

    with st.expander("📊 Ver Tabla de Eventos"):
        df = pd.DataFrame([{ "Tiempo": f"{e.tiempo:.2f}", "Contenedor": e.contenedor_id, "Acción": e.accion, "Origen": e.origen, "Destino": e.destino } for e in simulador.eventos])
        st.dataframe(df, use_container_width=True)

else:
    st.info(" Configura los parámetros en el sidebar y presiona **Iniciar Simulación**")
    if 'mostrar_panel_interactivo' not in st.session_state:
        st.session_state.mostrar_panel_interactivo = False
    st.markdown("### 👀 Vista Previa del Patio")
    patio_vacio = [[None for _ in range(4)] for _ in range(10)]
    st.html(crear_zona_patio_3d(patio_vacio))
    
if __name__ == '__main__':
    import sys
    import os
    
    # Verificamos si estamos corriendo en modo servidor de Streamlit
    if not st.runtime.exists():
        try:
            from streamlit.web import cli as st_cli
            
            # Lógica para encontrar el archivo main.py
            if getattr(sys, 'frozen', False):
                # Si es un .exe, el archivo estará en la carpeta temporal (_MEIPASS)
                # Nota: Asumiremos que copiaremos main.py a la raíz del paquete
                script_path = os.path.join(sys._MEIPASS, "main.py")
            else:
                # En desarrollo, usamos la ruta normal
                script_path = __file__
            
            # Configuramos los argumentos para simular "streamlit run ..."
            # Agregamos flags para evitar advertencias extras
            sys.argv = [
                "streamlit", 
                "run", 
                script_path, 
                "--global.developmentMode=false", 
                "--server.headless=true"
            ]
            
            print(f"🚀 Iniciando Streamlit desde: {script_path}")
            st_cli.main()
            
        except Exception as e:
            print(f"Error fatal al iniciar Streamlit: {e}")
            # Mantiene la consola abierta si hay error para poder leerlo
            input("Presiona Enter para salir...")