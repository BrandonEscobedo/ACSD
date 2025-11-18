import streamlit as st
import time
import base64
from pathlib import Path
from dataclasses import dataclass
import pandas as pd
from models.simulation_models import LineaTransportista
from simulation.simulation import ejecutar_simulacion, simular_asignacion

st.set_page_config(page_title="SimPy + Animación", layout="wide")

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"

svg_path = ASSETS_DIR / "contenedor.svg"
svg_bytes = svg_path.read_bytes()
svg_b64 = base64.b64encode(svg_bytes).decode("utf-8")
svg_img = f"data:image/svg+xml;base64,{svg_b64}"

LINEAS_DEMO = [
    LineaTransportista(1, "Maersk Logistics", True, 92, 88, "contacto@maersk.com"),
    LineaTransportista(2, "Hapag-Lloyd Express", True, 80, 75, "service@hapag.com"),
    LineaTransportista(3, "MSC Cargo", False, 85, 70, "ops@msc.com"),
    LineaTransportista(4, "ONE Transport", True, 78, 90, "support@one.com"),
]

TIEMPO_BUQUE_A_PISO = 2.0
TIEMPO_PISO_A_PATIO = 1.5


def crear_zona_buque_piso(zona_nombre, zona_info, contenedores):
    """Crea HTML para zonas BUQUE y PISO (sin estructura de matriz)"""
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
        <img src="{svg_img}" style="
            position:absolute; left:{200 + idx*60}px; top:50%;
            transform:translateY(-50%);
            width:50px; opacity:0.8;
            transition:all .4s ease;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));">
        """
    
    html += "</div>"
    return html


def crear_zona_patio_3d(patio_matriz, contenedor_activo=None, contenedor_seleccionado=None):
    """
    Crea visualización 3D del patio con columnas y pisos
    patio_matriz: lista de listas [columna][piso] = Contenedor o None
    """
    NUM_COLUMNAS = 10
    NUM_PISOS = 4
    
    # Generar script JavaScript para manejar clicks
    js_click_handler = """
    <script>
    function selectContainer(containerId) {
        // Enviar mensaje al parent (Streamlit)
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            key: 'selected_container',
            value: containerId
        }, '*');
        
        // Guardar en localStorage para persistencia
        localStorage.setItem('selected_container_id', containerId);
        
        // Recargar para actualizar Streamlit
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
        
        <!-- Encabezado -->
        <div style="position: absolute; left: 20px; top: 20px;
            font-weight: bold; font-size: 28px; color: #F18F01;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            🏭 Patio de Almacenamiento
        </div>
        
        <!-- Contador total -->
        <div style="position:absolute; top:20px; right:20px;
            background:#F18F01; color:white; padding:8px 16px;
            border-radius:20px; font-weight:bold; font-size:16px;">
            {sum(1 for col in patio_matriz for cnt in col if cnt is not None)} 📦
        </div>
        
        <!-- Instrucción -->
        <div style="position:absolute; left:20px; top:60px;
            font-size:12px; color:#666; font-style:italic;">
            💡 Haz click en cualquier contenedor para ver su información
        </div>
        
        <!-- Grid de Columnas y Pisos -->
        <div style="margin-top: 100px; display: flex; justify-content: center; gap: 8px;">
    """
    
    # Iterar por cada columna
    for col_idx in range(NUM_COLUMNAS):
        html += f"""
        <div style="display: flex; flex-direction: column-reverse; align-items: center; gap: 4px;">
            <!-- Etiqueta de columna -->
            <div style="background: #333; color: white; padding: 4px 8px; 
                border-radius: 4px; font-size: 10px; font-weight: bold;">
                C{col_idx}
            </div>
        """
        
        # Iterar por cada piso (de abajo hacia arriba)
        for piso_idx in range(NUM_PISOS):
            contenedor = patio_matriz[col_idx][piso_idx] if col_idx < len(patio_matriz) else None
            
            # Verificar si es el contenedor activo o seleccionado
            is_active = (contenedor_activo and contenedor and 
                        contenedor.id == contenedor_activo.id)
            is_selected = (contenedor_seleccionado and contenedor and 
                          contenedor.id == contenedor_seleccionado.id)
            
            # Colores según estado
            if contenedor is None:
                # Espacio vacío
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
                # Contenedor presente
                if is_selected:
                    bg_color = "#FF9800"  # Naranja para seleccionado
                    scale = "1.2"
                    shadow = "0 6px 12px rgba(255,152,0,0.6)"
                elif is_active:
                    bg_color = "#4CAF50"  # Verde para activo
                    scale = "1.15"
                    shadow = "0 6px 12px rgba(76,175,80,0.5)"
                else:
                    bg_color = "#2196F3"  # Azul normal
                    scale = "1.0"
                    shadow = "0 3px 6px rgba(0,0,0,0.3)"
                
                html += f"""
                <div onclick="selectContainer('{contenedor.id}')"
                    style="position: relative; width: 45px; height: 45px; 
                    background: {bg_color}; border-radius: 6px;
                    transform: scale({scale});
                    transition: all 0.3s ease;
                    box-shadow: {shadow};
                    display: flex; align-items: center; justify-content: center;
                    cursor: pointer;">
                    
                    <img src="{svg_img}" style="width: 35px; height: 35px; 
                        filter: brightness(1.2); pointer-events: none;">
                    
                    <!-- Label del contenedor -->
                    <div style="position: absolute; top: -8px; right: -8px;
                        background: white; color: #333;
                        padding: 2px 6px; border-radius: 10px;
                        font-size: 9px; font-weight: bold;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                        pointer-events: none;">
                        {contenedor.id.split('-')[1]}
                    </div>
                    
                    <!-- Tooltip mejorado -->
                    <div style="position: absolute; bottom: 110%; left: 50%;
                        transform: translateX(-50%);
                        background: rgba(0,0,0,0.9); color: white;
                        padding: 8px 12px; border-radius: 8px;
                        font-size: 11px; white-space: nowrap;
                        opacity: 0; pointer-events: none;
                        transition: opacity 0.2s;
                        z-index: 1000;">
                        <strong>{contenedor.id}</strong><br>
                        📍 C{col_idx}, P{piso_idx}<br>
                        🖱️ Click para detalles
                        <div style="position: absolute; top: 100%; left: 50%;
                            transform: translateX(-50%);
                            border: 5px solid transparent;
                            border-top-color: rgba(0,0,0,0.9);"></div>
                    </div>
                </div>
                <style>
                    div[onclick]:hover > div:last-child {{
                        opacity: 1 !important;
                    }}
                </style>
                """
        
        html += "</div>"  # Cerrar columna
    
    html += """
        </div>
        
        <!-- Leyenda -->
        <div style="margin-top: 20px; display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
            <div style="display: flex; align-items: center; gap: 6px;">
                <div style="width: 18px; height: 18px; background: #FF9800; border-radius: 4px;"></div>
                <span style="font-size: 12px;">Seleccionado</span>
            </div>
            <div style="display: flex; align-items: center; gap: 6px;">
                <div style="width: 18px; height: 18px; background: #4CAF50; border-radius: 4px;"></div>
                <span style="font-size: 12px;">Activo</span>
            </div>
            <div style="display: flex; align-items: center; gap: 6px;">
                <div style="width: 18px; height: 18px; background: #2196F3; border-radius: 4px;"></div>
                <span style="font-size: 12px;">Almacenado</span>
            </div>
            <div style="display: flex; align-items: center; gap: 6px;">
                <div style="width: 18px; height: 18px; border: 2px dashed #ccc; border-radius: 4px;"></div>
                <span style="font-size: 12px;">Vacío</span>
            </div>
        </div>
    </div>
    """
    
    return html


def crear_escena_html_completa(contenedores_por_zona, patio_matriz, contenedor_activo=None, contenedor_seleccionado=None):
    """Crea la escena completa con las 3 zonas"""
    ZONAS = {
        "BUQUE": {"color": "#2E86AB", "label": "🚢 Buque"},
        "PISO": {"color": "#A23B72", "label": "📍 Piso"},
    }
    
    html = "<div style='padding: 20px;'>"
    
    # Zona BUQUE
    html += crear_zona_buque_piso("BUQUE", ZONAS["BUQUE"], contenedores_por_zona.get("BUQUE", []))
    
    # Zona PISO
    html += crear_zona_buque_piso("PISO", ZONAS["PISO"], contenedores_por_zona.get("PISO", []))
    
    # Zona PATIO (con visualización 3D) - ahora acepta contenedor_seleccionado
    html += crear_zona_patio_3d(patio_matriz, contenedor_activo, contenedor_seleccionado)
    
    html += "</div>"
    return html


def animar_simulacion(simulador, velocidad=0.5):
    """Anima la simulación mostrando el patio 3D con controles compactos"""
    
    # Barra de controles compacta en la parte superior
    st.markdown("### 🎬 Visualización en Tiempo Real")
    
    # Controles en una fila horizontal
    col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4, col_ctrl5 = st.columns([1, 1, 1, 2, 2])
    
    # Botones de control
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
        # Selector de velocidad compacto
        velocidad_actual = st.select_slider(
            "Velocidad",
            options=[0.1, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0],
            value=velocidad,
            key="vel_anim"
        )
    
    # Placeholders para progreso e info en las columnas restantes
    with col_ctrl4:
        placeholder_progreso = st.empty()
    
    with col_ctrl5:
        placeholder_info = st.empty()
    
    # Visualización a pantalla completa
    placeholder_escena = st.empty()
    
    contenedores_por_zona = {"BUQUE": [], "PISO": [], "PATIO": []}
    patio_temporal = [[None for _ in range(4)] for _ in range(10)]
    
    # Guardar el estado actual en session_state
    if 'evento_actual' not in st.session_state:
        st.session_state.evento_actual = 0
    
    for idx, evento in enumerate(simulador.eventos[st.session_state.evento_actual:], 
                                  start=st.session_state.evento_actual):
        
        # Verificar si se debe detener
        if not st.session_state.get('animacion_activa', True):
            break
        
        # Verificar pausa
        while st.session_state.animacion_pausada:
            time.sleep(0.5)
            if not st.session_state.get('animacion_activa', True):
                break
        
        cont = next(c for c in simulador.contenedores if c.id == evento.contenedor_id)
        
        # Actualizar zonas
        for zona in contenedores_por_zona.values():
            if cont in zona:
                zona.remove(cont)
        
        if evento.destino in contenedores_por_zona:
            contenedores_por_zona[evento.destino].append(cont)
            
            if evento.destino == "PATIO" and cont.columna is not None and cont.piso is not None:
                patio_temporal[cont.columna][cont.piso] = cont
        
        # Actualizar visualización a pantalla completa
        html = crear_escena_html_completa(contenedores_por_zona, patio_temporal, cont)
        placeholder_escena.html(html)
        
        # Actualizar info en barra superior
        progreso = (idx + 1) / len(simulador.eventos) * 100
        placeholder_progreso.progress(progreso / 100, text=f"Evento {idx + 1}/{len(simulador.eventos)}")
        placeholder_info.caption(f"⏱️ {evento.tiempo:.1f}s | {evento.contenedor_id}: {evento.accion}")
        
        # Guardar estado actual
        st.session_state.evento_actual = idx + 1
        
        time.sleep(velocidad_actual)
    
    # Limpiar estado al finalizar
    st.session_state.evento_actual = 0
    st.session_state.animacion_activa = False


# ==================== INTERFAZ ====================
st.title("🚢 Simulación: Buque → Piso → Patio 3D")
st.markdown("**SimPy + Visualización de Columnas y Pisos**")

with st.sidebar:
    st.header("⚙️ Configuración")
    num_contenedores = st.slider("Número de contenedores", 1, 40, 15)
    intervalo = st.slider("Intervalo entre llegadas", 0.5, 5.0, 1.5)
    velocidad_animacion = st.slider("Velocidad de animación", 0.1, 2.0, 0.3)
    
    st.markdown("---")
    st.markdown("### 📊 Tiempos del Sistema")
    st.info(f"⏱️ Buque → Piso: {TIEMPO_BUQUE_A_PISO}u")
    st.info(f"⏱️ Piso → Patio: {TIEMPO_PISO_A_PATIO}u")
    
    st.markdown("---")
    st.markdown("### 🏭 Capacidad del Patio")
    st.info("📦 10 columnas × 4 pisos = 40 contenedores")

col1, col2 = st.columns([1, 3])
with col1:
    if st.button("▶️ Iniciar Simulación", type="primary"):
        st.session_state['simular'] = True
with col2:
    if st.button("🔄 Reiniciar"):
        st.session_state['simular'] = False
        st.rerun()

# ==================== EJECUTAR SIMULACIÓN ====================
if st.session_state.get('simular', False):
    with st.spinner("🔧 Ejecutando SimPy..."):
        duracion_total = (num_contenedores * intervalo) + 10
        simulador = ejecutar_simulacion(num_contenedores, intervalo, duracion_total)
        st.success(f"✅ Simulación terminada: {len(simulador.eventos)} eventos")
    
    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Procesados", len(simulador.contenedores))
    with col2:
        en_patio = sum(1 for c in simulador.contenedores if c.posicion_actual == "PATIO")
        st.metric("En Patio", en_patio)
    with col3:
        capacidad_usada = (en_patio / 40) * 100
        st.metric("Ocupación", f"{capacidad_usada:.1f}%")
    with col4:
        st.metric("Eventos", len(simulador.eventos))
    
    st.markdown("---")
    
    # Botón de animación
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
    
    # ========== DECIDIR QUÉ MOSTRAR ==========
    if st.session_state.get('animacion_activa', False):
        # Ejecutar animación
        animar_simulacion(simulador, velocidad_animacion)
        # Después de terminar, mostrar panel interactivo
        st.session_state.mostrar_panel_interactivo = True
        st.session_state.animacion_activa = False
        st.rerun()
    
    # ========== VISTA ESTÁTICA INTERACTIVA ==========
    if st.session_state.get('mostrar_panel_interactivo', True):
        # Modo estático interactivo
        
        # ========== LAYOUT CON COLUMNAS: PATIO + PANEL LATERAL ==========
        col_patio, col_panel = st.columns([1, 1])
        
        with col_patio:
            st.markdown("### 🏭 Estado del Patio (Interactivo)")
            
            # Inicializar contenedor seleccionado en session_state
            if 'contenedor_seleccionado_id' not in st.session_state:
                st.session_state.contenedor_seleccionado_id = None
            
            # Contenedores en el patio
            conts_patio = [c for c in simulador.contenedores if c.posicion_actual == "PATIO"]
            
            # Selector de contenedor con botones en grid
            if conts_patio:
                st.markdown("#### 🔍 Selección Rápida")
                
                # Crear grid de botones para selección rápida
                cols_btns = st.columns(5)
                for idx, cnt in enumerate(conts_patio[:20]):  # Mostrar primeros 20
                    with cols_btns[idx % 5]:
                        if st.button(
                            f"{cnt.id.split('-')[1]}", 
                            key=f"btn_{cnt.id}",
                            help=f"{cnt.id} - C{cnt.columna}, P{cnt.piso}",
                            use_container_width=True,
                            type="primary" if st.session_state.contenedor_seleccionado_id == cnt.id else "secondary"
                        ):
                            st.session_state.contenedor_seleccionado_id = cnt.id
                            st.rerun()
                
                st.markdown("---")
                
                # Dropdown tradicional como alternativa
                with st.expander("📋 Selector por Lista", expanded=False):
                    opciones = ["-- Ninguno --"] + [f"{c.id} (C{c.columna}, P{c.piso})" for c in conts_patio]
                    seleccion = st.selectbox(
                        "Buscar contenedor:",
                        opciones,
                        key="select_contenedor",
                        index=0 if not st.session_state.contenedor_seleccionado_id else 
                              next((i+1 for i, c in enumerate(conts_patio) 
                                   if c.id == st.session_state.contenedor_seleccionado_id), 0)
                    )
                    
                    if seleccion != "-- Ninguno --":
                        new_id = seleccion.split()[0]
                        if new_id != st.session_state.contenedor_seleccionado_id:
                            st.session_state.contenedor_seleccionado_id = new_id
                            st.rerun()
                    else:
                        if st.session_state.contenedor_seleccionado_id is not None:
                            st.session_state.contenedor_seleccionado_id = None
                            st.rerun()
            
            # Renderizar patio con contenedor seleccionado
            contenedor_sel = None
            if st.session_state.contenedor_seleccionado_id:
                contenedor_sel = next((c for c in conts_patio 
                                      if c.id == st.session_state.contenedor_seleccionado_id), None)
            
            html_patio = crear_zona_patio_3d(simulador.patio, None, contenedor_sel)
            st.html(html_patio)
            
            # Info rápida
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Total en Patio", len(conts_patio))
            with col_b:
                ocupacion_pct = (len(conts_patio) / 40) * 100
                st.metric("Ocupación", f"{ocupacion_pct:.1f}%")
            with col_c:
                disponibles = 40 - len(conts_patio)
                st.metric("Disponibles", disponibles)
        
        with col_panel:
            st.markdown("### 📋 Información del Contenedor")
            
            if st.session_state.contenedor_seleccionado_id and contenedor_sel:
                # ========== TARJETA DE INFORMACIÓN ==========
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px; border-radius: 15px; color: white;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2); margin-bottom: 20px;">
                    <h3 style="margin: 0 0 15px 0;">📦 {contenedor_sel.id}</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div>
                            <div style="font-size: 12px; opacity: 0.9;">Posición</div>
                            <div style="font-size: 18px; font-weight: bold;">
                                Columna {contenedor_sel.columna}, Piso {contenedor_sel.piso}
                            </div>
                        </div>
                        <div>
                            <div style="font-size: 12px; opacity: 0.9;">Estado</div>
                            <div style="font-size: 14px; font-weight: bold;">
                                {contenedor_sel.estado}
                            </div>
                        </div>
                        <div>
                            <div style="font-size: 12px; opacity: 0.9;">Tiempo Llegada</div>
                            <div style="font-size: 16px;">{contenedor_sel.tiempo_llegada:.2f}u</div>
                        </div>
                        <div>
                            <div style="font-size: 12px; opacity: 0.9;">Posición Actual</div>
                            <div style="font-size: 16px;">{contenedor_sel.posicion_actual}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # ========== ANÁLISIS DE LÍNEA ==========
                st.markdown("### 🚚 Análisis de Línea Transportista")
                
                if st.button("🚚 Asignar Línea de Transporte", type="primary", use_container_width=True):
                    with st.spinner("Analizando líneas disponibles..."):
                        mejor, resultados = simular_asignacion(contenedor_sel, LINEAS_DEMO)
                        
                        st.subheader("📊 Resultados por Línea")
                        df_resultados = pd.DataFrame(resultados)
                        st.dataframe(df_resultados, use_container_width=True)
                        
                        if mejor:
                            st.success(f"⭐ **Línea Recomendada:** {mejor['línea']}")
                            
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                st.metric("🎯 Puntaje", f"{mejor['puntaje']:.2f}")
                            with col_b:
                                st.metric("✅ Cumplimiento", f"{mejor['cumplimiento']}%")
                            with col_c:
                                st.metric("⏱️ Lead Time", f"{mejor['lead_time']:.1f}h")
                            
                            st.info(f"📞 **Contacto:** {mejor['contacto']}")
                            
                            # Gráfico comparativo
                            st.markdown("#### 📈 Comparación de Puntajes")
                            import plotly.express as px
                            fig = px.bar(df_resultados, x='línea', y='puntaje', 
                                        color='puntaje',
                                        color_continuous_scale='Viridis',
                                        title='Puntaje por Línea Transportista')
                            st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("👆 Selecciona un contenedor del patio para ver su información y asignar línea")
                
                # Placeholder visual
                st.markdown("""
                <div style="text-align: center; padding: 40px; background: #f0f0f0; 
                    border-radius: 15px; margin-top: 20px;">
                    <div style="font-size: 80px;">📦</div>
                    <p style="color: #666; margin-top: 20px;">
                        Selecciona un contenedor<br>para ver sus detalles
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    # Tabla de eventos
    with st.expander("📊 Ver Tabla de Eventos"):
        df = pd.DataFrame([{
            "Tiempo": f"{e.tiempo:.2f}",
            "Contenedor": e.contenedor_id,
            "Acción": e.accion,
            "Origen": e.origen,
            "Destino": e.destino
        } for e in simulador.eventos])
        st.dataframe(df, use_container_width=True)

else:
    st.info("👈 Configura los parámetros en el sidebar y presiona **Iniciar Simulación**")
    
    # Inicializar el estado para mostrar panel por defecto
    if 'mostrar_panel_interactivo' not in st.session_state:
        st.session_state.mostrar_panel_interactivo = False
    
    # Vista previa estática del patio
    st.markdown("### 👀 Vista Previa del Patio")
    patio_vacio = [[None for _ in range(4)] for _ in range(10)]
    st.html(crear_zona_patio_3d(patio_vacio))