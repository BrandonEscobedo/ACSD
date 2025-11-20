import streamlit as st
import time
import base64
from pathlib import Path
import pandas as pd

# Asegúrate de que estas carpetas existan en tu proyecto
# NOTA: Si estás probando esto en un entorno nuevo sin estos módulos, fallará la importación.
try:
    from models.simulation_models import LineaTransportista
    from simulation.simulation import ejecutar_simulacion, simular_asignacion
except ImportError:
    # Mocks para que el código funcione si no tienes los archivos locales a mano
    class LineaTransportista:
        def __init__(self, id, nombre, activo, puntaje, costo, contacto):
            self.id = id
            self.nombre = nombre
            self.activo = activo
            self.puntaje = puntaje
            self.costo = costo
            self.contacto = contacto
            
    def ejecutar_simulacion(num, intervalo, duracion):
        class MockSim:
            def __init__(self):
                self.eventos = []
                self.contenedores = []
                self.patio = [[None for _ in range(4)] for _ in range(10)]
        return MockSim()
        
    def simular_asignacion(cont, lineas):
        return None, []

# Configuración de la página
st.set_page_config(page_title="SimPy + Animación", layout="wide")

# Configuración de Rutas y Assets
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"

# Carga del SVG del contenedor
svg_contenedor_path = ASSETS_DIR / "contenedor.svg"
svg_contenedor_img = ""
if svg_contenedor_path.exists():
    svg_contenedor_bytes = svg_contenedor_path.read_bytes()
    svg_contenedor_b64 = base64.b64encode(svg_contenedor_bytes).decode("utf-8")
    svg_contenedor_img = f"data:image/svg+xml;base64,{svg_contenedor_b64}"
else:
    # Fallback para el SVG del contenedor si no se encuentra
    svg_contenedor_img = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1MCIgaGVpZ2h0PSI1MCI+PHJlY3Qgd2lkdGg9IjUwIiBoZWlnaHQ9IjUwIiBmaWxsPSIjY2NjIi8+PC9zdmc+"

# SVG del loader animado
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

# Datos de demostración
LINEAS_DEMO = [
    LineaTransportista(1, "Maersk Logistics", True, 92, 88, "contacto@maersk.com"),
    LineaTransportista(2, "Hapag-Lloyd Express", True, 80, 75, "service@hapag.com"),
    LineaTransportista(3, "MSC Cargo", False, 85, 70, "ops@msc.com"),
    LineaTransportista(4, "ONE Transport", True, 78, 90, "support@one.com"),
]

TIEMPO_BUQUE_A_PISO = 2.0
TIEMPO_PISO_A_PATIO = 1.5

# Definimos las opciones de velocidad globalmente
OPCIONES_VELOCIDAD = [0.1, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0]

# ==================== FUNCIONES DE VISUALIZACIÓN ====================

def mostrar_loader_overlay(mensaje="Cargando..."):
    """Muestra una pantalla de carga de cuerpo completo con un icono SVG animado."""
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
    """Crea HTML para zonas BUQUE y PISO"""
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
        html += f"""
        <img src="{svg_contenedor_img}" style="
            position:absolute; left:{200 + idx*60}px; top:50%;
            transform:translateY(-50%);
            width:50px; opacity:0.8;
            transition:all .4s ease;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));">
        """
    
    html += "</div>"
    return html


def crear_zona_patio_3d(patio_matriz, contenedor_activo=None, contenedor_seleccionado=None):
    """Crea visualización 3D del patio con columnas y pisos y manejo de clicks"""
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
    <div style="position: relative; width: 100%; min-height: 500px;
        border: 4px solid #F18F01;
        background: linear-gradient(135deg, #F18F0122 0%, #F18F0144 100%);
        border-radius: 20px; margin: 20px 0; padding: 20px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);">
        
        <div style="position: absolute; left: 20px; top: 20px;
            font-weight: bold; font-size: 28px; color: #F18F01;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            🏭 Patio de Almacenamiento
        </div>
        
        <div style="position:absolute; top:20px; right:20px;
            background:#F18F01; color:white; padding:8px 16px;
            border-radius:20px; font-weight:bold; font-size:16px;">
            {sum(1 for col in patio_matriz for cnt in col if cnt is not None)} 📦
        </div>
        
        <div style="margin-top: 100px; display: flex; justify-content: center; gap: 8px;">
    """
    
    for col_idx in range(NUM_COLUMNAS):
        html += f"""
        <div style="display: flex; flex-direction: column-reverse; align-items: center; gap: 4px;">
            <div style="background: #333; color: white; padding: 4px 8px; 
                border-radius: 4px; font-size: 10px; font-weight: bold;">
                C{col_idx}
            </div>
        """
        
        for piso_idx in range(NUM_PISOS):
            contenedor = patio_matriz[col_idx][piso_idx] if col_idx < len(patio_matriz) else None
            
            is_active = (contenedor_activo and contenedor and contenedor.id == contenedor_activo.id)
            is_selected = (contenedor_seleccionado and contenedor and contenedor.id == contenedor_seleccionado.id)
            
            if contenedor is None:
                html += f"""
                <div style="width: 45px; height: 45px; 
                    border: 2px dashed #ccc; border-radius: 6px;
                    background: rgba(255,255,255,0.3);
                    display: flex; align-items: center; justify-content: center;
                    font-size: 9px; color: #999;">
                    P{piso_idx}
                </div>
                """
            else:
                if is_selected:
                    bg_color = "#FF9800"
                    scale = "1.2"
                    shadow = "0 6px 12px rgba(255,152,0,0.6)"
                elif is_active:
                    bg_color = "#4CAF50"
                    scale = "1.15"
                    shadow = "0 6px 12px rgba(76,175,80,0.5)"
                else:
                    bg_color = "#2196F3"
                    scale = "1.0"
                    shadow = "0 3px 6px rgba(0,0,0,0.3)"
                
                html += f"""
                <div onclick="selectContainer('{contenedor.id}')"
                    style="position: relative; width: 45px; height: 45px; 
                    background: {bg_color}; border-radius: 6px;
                    transform: scale({scale}); transition: all 0.3s ease;
                    box-shadow: {shadow}; cursor: pointer;
                    display: flex; align-items: center; justify-content: center;">
                    
                    <img src="{svg_contenedor_img}" style="width: 35px; height: 35px; filter: brightness(1.2); pointer-events: none;">
                    
                    <div style="position: absolute; top: -8px; right: -8px;
                        background: white; color: #333; padding: 2px 6px; border-radius: 10px;
                        font-size: 9px; font-weight: bold; pointer-events: none;">
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
        # Aquí el usuario selecciona el factor (0.1 = lento, 2.0 = rápido)
        velocidad_seleccionada = st.select_slider("Velocidad", options=OPCIONES_VELOCIDAD, value=val_init, key="vel_anim")
    
    with col_ctrl4: placeholder_progreso = st.empty()
    with col_ctrl5: placeholder_info = st.empty()
    placeholder_escena = st.empty()
    
    contenedores_por_zona = {"BUQUE": [], "PISO": [], "PATIO": []}
    patio_temporal = [[None for _ in range(4)] for _ in range(10)]
    
    if 'evento_actual' not in st.session_state: st.session_state.evento_actual = 0
    
    for idx, evento in enumerate(simulador.eventos[st.session_state.evento_actual:], start=st.session_state.evento_actual):
        if not st.session_state.get('animacion_activa', True): break
        
        while st.session_state.animacion_pausada:
            time.sleep(0.5)
            if not st.session_state.get('animacion_activa', True): break
        
        cont = next(c for c in simulador.contenedores if c.id == evento.contenedor_id)
        
        for zona in contenedores_por_zona.values():
            if cont in zona: zona.remove(cont)
        
        if evento.destino in contenedores_por_zona:
            contenedores_por_zona[evento.destino].append(cont)
            if evento.destino == "PATIO" and cont.columna is not None and cont.piso is not None:
                patio_temporal[cont.columna][cont.piso] = cont
        
        html = crear_escena_html_completa(contenedores_por_zona, patio_temporal, cont)
        placeholder_escena.html(html)
        
        progreso = (idx + 1) / len(simulador.eventos) * 100
        placeholder_progreso.progress(progreso / 100, text=f"Evento {idx + 1}/{len(simulador.eventos)}")
        placeholder_info.caption(f"⏱️ {evento.tiempo:.1f}s | {evento.contenedor_id}: {evento.accion}")
        
        st.session_state.evento_actual = idx + 1
        
        # ===========================================================
        # CAMBIO DE LÓGICA: Inversión de velocidad
        # 0.1 seleccionado -> 0.5/0.1 = 5.0 seg (LENTO)
        # 2.0 seleccionado -> 0.5/2.0 = 0.25 seg (RÁPIDO)
        # ===========================================================
        tiempo_espera = 0.5 / velocidad_seleccionada
        time.sleep(tiempo_espera)
    
    st.session_state.evento_actual = 0
    st.session_state.animacion_activa = False


# ==================== INTERFAZ PRINCIPAL ====================
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

col1, col2 = st.columns([1, 3])
with col1:
    if st.button("▶️ Iniciar Simulación", type="primary"):
        st.session_state['simular'] = True
        st.session_state['mostrar_loader'] = True 
with col2:
    if st.button("🔄 Reiniciar"):
        st.session_state['simular'] = False
        st.session_state['mostrar_loader'] = False
        st.session_state['animacion_activa'] = False
        st.session_state['mostrar_panel_interactivo'] = False
        st.session_state['contenedor_seleccionado_id'] = None
        st.rerun()

# ==================== EJECUTAR SIMULACIÓN ====================

if st.session_state.get('mostrar_loader', False):
    mostrar_loader_overlay("Calculando simulación...")
    if 'simulador_resultado' not in st.session_state or not st.session_state.get('simular_finalizado', False):
        with st.spinner("Preparando el entorno SimPy..."):
            duracion_total = (num_contenedores * intervalo) + 10
            simulador = ejecutar_simulacion(num_contenedores, intervalo, duracion_total)
            st.session_state.simulador_resultado = simulador
            st.session_state.simular_finalizado = True
    
    time.sleep(1) # Pequeña pausa para apreciar el loader
    st.session_state['mostrar_loader'] = False 
    st.session_state['mostrar_panel_interactivo'] = True 
    st.rerun() 


if st.session_state.get('simular_finalizado', False):
    simulador = st.session_state.simulador_resultado
    
    st.divider() 
    st.markdown("### Resumen de la Simulación")
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1: st.metric("Cont. Procesados", len(simulador.contenedores))
    with col_m2: 
        en_patio = sum(1 for c in simulador.contenedores if c.posicion_actual == "PATIO")
        st.metric("Cont. en Patio", en_patio)
    with col_m3: st.metric("Ocupación Patio", f"{(en_patio / 40) * 100:.1f}%")
    with col_m4: st.metric("Total Eventos", len(simulador.eventos))
    
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

    if st.session_state.get('mostrar_panel_interactivo', False):
        col_patio, col_panel = st.columns([1, 1])
        
        with col_patio:
            st.markdown("### 🏭 Estado del Patio (Interactivo)")
            if 'contenedor_seleccionado_id' not in st.session_state:
                st.session_state.contenedor_seleccionado_id = None
            
            conts_patio = [c for c in simulador.contenedores if c.posicion_actual == "PATIO"]
            
            if conts_patio:
                st.markdown("#### 🔍 Selección Rápida")
                cols_btns = st.columns(5)
                for idx, cnt in enumerate(conts_patio[:20]):
                    with cols_btns[idx % 5]:
                        if st.button(f"{cnt.id.split('-')[1]}", key=f"btn_quick_{cnt.id}", use_container_width=True,
                                   type="primary" if st.session_state.contenedor_seleccionado_id == cnt.id else "secondary"):
                            st.session_state.contenedor_seleccionado_id = cnt.id
                            st.rerun()
                
                st.markdown("---")
                opciones = ["-- Ninguno --"] + [f"{c.id} (C{c.columna}, P{c.piso})" for c in conts_patio]
                seleccion = st.selectbox("Buscar contenedor:", opciones, key="select_contenedor")
                if seleccion != "-- Ninguno --":
                    new_id = seleccion.split()[0]
                    if new_id != st.session_state.contenedor_seleccionado_id:
                        st.session_state.contenedor_seleccionado_id = new_id
                        st.rerun()

            contenedor_sel = None
            if st.session_state.contenedor_seleccionado_id:
                contenedor_sel = next((c for c in conts_patio if c.id == st.session_state.contenedor_seleccionado_id), None)
            
            html_patio = crear_zona_patio_3d(simulador.patio, None, contenedor_sel)
            st.html(html_patio)

        with col_panel:
            st.markdown("### 📋 Información del Contenedor")
            
            if st.session_state.contenedor_seleccionado_id and contenedor_sel:
                
                if 'ultimo_contenedor_analizado' not in st.session_state:
                    st.session_state.ultimo_contenedor_analizado = None
                
                if st.session_state.ultimo_contenedor_analizado != contenedor_sel.id:
                    st.session_state.analisis_listo = False
                    st.session_state.resultados_analisis = None
                    st.session_state.mejor_opcion = None

                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px; border-radius: 15px; color: white;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2); margin-bottom: 20px;">
                    <h3 style="margin: 0 0 15px 0;">📦 {contenedor_sel.id}</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div><div style="opacity:0.8; font-size:12px;">Posición</div><b>C{contenedor_sel.columna}, P{contenedor_sel.piso}</b></div>
                        <div><div style="opacity:0.8; font-size:12px;">Estado</div><b>{contenedor_sel.estado}</b></div>
                        <div><div style="opacity:0.8; font-size:12px;">Llegada</div>{contenedor_sel.tiempo_llegada:.2f}u</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 🚚 Análisis de Línea Transportista")
                
                if st.button("🚚 Asignar Línea de Transporte", type="primary", use_container_width=True, key="btn_asignar"):
                    st.session_state['mostrar_loader_analisis'] = True 
                    st.rerun() 
                
                if st.session_state.get('mostrar_loader_analisis', False):
                    mostrar_loader_overlay("Analizando líneas transportistas...")
                    time.sleep(3) # Simular tiempo de carga de 3s para ver la animación
                    
                    mejor, resultados = simular_asignacion(contenedor_sel, LINEAS_DEMO)
                    st.session_state.analisis_listo = True
                    st.session_state.resultados_analisis = resultados
                    st.session_state.mejor_opcion = mejor
                    st.session_state.ultimo_contenedor_analizado = contenedor_sel.id
                    
                    st.session_state['mostrar_loader_analisis'] = False 
                    st.rerun() 

                if st.session_state.get('analisis_listo', False) and st.session_state.get('ultimo_contenedor_analizado') == contenedor_sel.id:
                    
                    mejor = st.session_state.mejor_opcion
                    resultados = st.session_state.resultados_analisis
                    
                    st.divider()
                    if mejor:
                        st.success(f"⭐ **Recomendación:** {mejor['línea']}")
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Puntaje", f"{mejor['puntaje']:.2f}")
                        c2.metric("Lead Time", f"{mejor['lead_time']:.1f}h")
                        c3.metric("Cumplimiento", f"{mejor['cumplimiento']}%")
                        
                        st.info(f"📞 {mejor['contacto']}")
                        
                        st.markdown("#### 📊 Detalles")
                        df_resultados = pd.DataFrame(resultados)
                        st.dataframe(df_resultados, use_container_width=True)

                        st.markdown("#### 📈 Comparativa")
                        chart_data = df_resultados.set_index('línea')[['puntaje']]
                        st.bar_chart(chart_data, color="#FF4B4B")

            else:
                st.info("👆 Selecciona un contenedor para ver detalles")
                st.markdown("<div style='text-align:center; font-size:50px; opacity:0.3;'>📦</div>", unsafe_allow_html=True)

else:
    st.info("👈 Configura los parámetros y presiona **Iniciar Simulación**")
    patio_vacio = [[None for _ in range(4)] for _ in range(10)]
    st.html(crear_zona_patio_3d(patio_vacio))