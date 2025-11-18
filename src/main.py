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


def crear_zona_patio_3d(patio_matriz, contenedor_activo=None):
    """
    Crea visualización 3D del patio con columnas y pisos
    patio_matriz: lista de listas [columna][piso] = Contenedor o None
    """
    NUM_COLUMNAS = 10
    NUM_PISOS = 4
    
    html = f"""
    <div style="position: relative; width: 100%; min-height: 500px;
        border: 4px solid #F18F01;
        background: linear-gradient(135deg, #F18F0122 0%, #F18F0144 100%);
        border-radius: 20px; margin: 20px 0; padding: 20px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);">
        
        <!-- Encabezado -->
        <div style="position: absolute; left: 20px; top: 20px;
            font-weight: bold; font-size: 32px; color: #F18F01;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            🏭 Patio de Almacenamiento
        </div>
        
        <!-- Contador total -->
        <div style="position:absolute; top:20px; right:20px;
            background:#F18F01; color:white; padding:10px 20px;
            border-radius:25px; font-weight:bold; font-size:18px;">
            {sum(1 for col in patio_matriz for cnt in col if cnt is not None)} 📦
        </div>
        
        <!-- Grid de Columnas y Pisos -->
        <div style="margin-top: 80px; display: flex; justify-content: center; gap: 10px;">
    """
    
    # Iterar por cada columna
    for col_idx in range(NUM_COLUMNAS):
        html += f"""
        <div style="display: flex; flex-direction: column-reverse; align-items: center; gap: 5px;">
            <!-- Etiqueta de columna -->
            <div style="background: #333; color: white; padding: 5px 10px; 
                border-radius: 5px; font-size: 12px; font-weight: bold;">
                C{col_idx}
            </div>
        """
        
        # Iterar por cada piso (de abajo hacia arriba)
        for piso_idx in range(NUM_PISOS):
            contenedor = patio_matriz[col_idx][piso_idx] if col_idx < len(patio_matriz) else None
            
            # Verificar si es el contenedor activo
            is_active = (contenedor_activo and contenedor and 
                        contenedor.id == contenedor_activo.id)
            
            # Colores según estado
            if contenedor is None:
                # Espacio vacío
                html += f"""
                <div style="width: 55px; height: 55px; 
                    border: 2px dashed #ccc; border-radius: 8px;
                    background: rgba(255,255,255,0.3);
                    display: flex; align-items: center; justify-content: center;
                    font-size: 10px; color: #999;">
                    P{piso_idx}
                </div>
                """
            else:
                # Contenedor presente
                bg_color = "#4CAF50" if is_active else "#2196F3"
                scale = "1.15" if is_active else "1.0"
                shadow = "0 6px 12px rgba(76,175,80,0.5)" if is_active else "0 3px 6px rgba(0,0,0,0.3)"
                
                html += f"""
                <div style="position: relative; width: 55px; height: 55px; 
                    background: {bg_color}; border-radius: 8px;
                    transform: scale({scale});
                    transition: all 0.3s ease;
                    box-shadow: {shadow};
                    display: flex; align-items: center; justify-content: center;
                    cursor: pointer;">
                    
                    <img src="{svg_img}" style="width: 40px; height: 40px; 
                        filter: brightness(1.2);">
                    
                    <!-- Tooltip con info -->
                    <div style="position: absolute; bottom: 100%; left: 50%;
                        transform: translateX(-50%);
                        background: rgba(0,0,0,0.9); color: white;
                        padding: 5px 10px; border-radius: 5px;
                        font-size: 11px; white-space: nowrap;
                        opacity: 0; pointer-events: none;
                        transition: opacity 0.2s;">
                        {contenedor.id}<br>
                        C{col_idx} P{piso_idx}
                    </div>
                </div>
                """
        
        html += "</div>"  # Cerrar columna
    
    html += """
        </div>
        
        <!-- Leyenda -->
        <div style="margin-top: 30px; display: flex; justify-content: center; gap: 20px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 20px; height: 20px; background: #4CAF50; border-radius: 4px;"></div>
                <span style="font-size: 14px;">Contenedor Activo</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 20px; height: 20px; background: #2196F3; border-radius: 4px;"></div>
                <span style="font-size: 14px;">Almacenado</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 20px; height: 20px; border: 2px dashed #ccc; border-radius: 4px;"></div>
                <span style="font-size: 14px;">Espacio Vacío</span>
            </div>
        </div>
    </div>
    """
    
    return html


def crear_escena_html_completa(contenedores_por_zona, patio_matriz, contenedor_activo=None):
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
    
    # Zona PATIO (con visualización 3D)
    html += crear_zona_patio_3d(patio_matriz, contenedor_activo)
    
    html += "</div>"
    return html


def animar_simulacion(simulador, velocidad=0.5):
    """Anima la simulación mostrando el patio 3D"""
    st.markdown("### 🎬 Visualización en Tiempo Real")
    placeholder = st.empty()
    
    contenedores_por_zona = {"BUQUE": [], "PISO": [], "PATIO": []}
    
    for evento in simulador.eventos:
        cont = next(c for c in simulador.contenedores if c.id == evento.contenedor_id)
        
        # Remover de zona anterior
        for zona in contenedores_por_zona.values():
            if cont in zona:
                zona.remove(cont)
        
        # Agregar a zona destino
        if evento.destino in contenedores_por_zona:
            contenedores_por_zona[evento.destino].append(cont)
        
        # Renderizar con matriz del patio
        html = crear_escena_html_completa(
            contenedores_por_zona, 
            simulador.patio,
            cont
        )
        placeholder.html(html)
        time.sleep(velocidad)


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
    if st.button("🎬 Reproducir Animación", type="primary"):
        animar_simulacion(simulador, velocidad_animacion)
    
    # Mostrar estado final del patio
    with st.expander("🏭 Ver Estado Final del Patio"):
        html_final = crear_zona_patio_3d(simulador.patio)
        st.html(html_final)
    
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
    
    # Mapa de calor del patio
    with st.expander("🔥 Mapa de Ocupación por Columna"):
        ocupacion = []
        for col_idx, columna in enumerate(simulador.patio):
            espacios_ocupados = sum(1 for piso in columna if piso is not None)
            ocupacion.append({
                "Columna": f"C{col_idx}",
                "Ocupados": espacios_ocupados,
                "Disponibles": 4 - espacios_ocupados,
                "Ocupación %": (espacios_ocupados / 4) * 100
            })
        
        df_ocupacion = pd.DataFrame(ocupacion)
        st.dataframe(df_ocupacion, use_container_width=True)
    
    # ========== ASIGNACIÓN DE LÍNEAS ==========
    st.markdown("---")
    st.header("🚚 Asignación de Línea Transportista")
    
    conts_patio = [c for c in simulador.contenedores if c.posicion_actual == "PATIO"]
    
    if not conts_patio:
        st.info("⏳ Aún no hay contenedores en el patio.")
    else:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            seleccion = st.selectbox(
                "Selecciona un contenedor:",
                [f"{c.id} (C{c.columna}, P{c.piso})" for c in conts_patio]
            )
            contenedor_id = seleccion.split()[0]
            elegido = next(c for c in conts_patio if c.id == contenedor_id)
            
            st.info(f"📍 Posición: Columna {elegido.columna}, Piso {elegido.piso}")
        
        with col2:
            if st.button("🚚 Simular Asignación de Línea"):
                mejor, resultados = simular_asignacion(elegido, LINEAS_DEMO)
                
                st.subheader("📊 Resultados por Línea")
                st.dataframe(pd.DataFrame(resultados), use_container_width=True)
                
                if mejor:
                    st.success(f"⭐ **Línea Recomendada:** {mejor['línea']}")
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Puntaje", f"{mejor['puntaje']:.2f}")
                    with col_b:
                        st.metric("Cumplimiento", f"{mejor['cumplimiento']}%")
                    with col_c:
                        st.metric("Lead Time", f"{mejor['lead_time']:.1f}h")
                    
                    st.write(f"📞 **Contacto:** {mejor['contacto']}")

else:
    st.info("👈 Configura los parámetros en el sidebar y presiona **Iniciar Simulación**")
    
    # Vista previa estática del patio
    st.markdown("### 👀 Vista Previa del Patio")
    patio_vacio = [[None for _ in range(4)] for _ in range(10)]
    st.html(crear_zona_patio_3d(patio_vacio))