from services.linea_transportista_service import LineaTransportistaServicio
from dataclasses import asdict

def main():
    servicio = LineaTransportistaServicio('data/lineas_transportistas.json')
    lineas = servicio.listar_lineas()
    for linea in lineas:
        print(asdict(linea))

if __name__ == "__main__":
    main()
"""
Simulación de Contenedores: Buque → Piso → Patio
Integración SimPy + Streamlit con animación visual
"""

import streamlit as st
import simpy
import time
import base64
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict
import random

# ==================== CONFIGURACIÓN ====================
st.set_page_config(page_title="SimPy + Animación", layout="wide")

# Cargar SVG (manejo de errores si no existe)
try:
    svg_bytes = Path("contenedor.svg").read_bytes()
    svg_b64 = base64.b64encode(svg_bytes).decode("utf-8")
    svg_img = f"data:image/svg+xml;base64,{svg_b64}"
except FileNotFoundError:
    # SVG de respaldo simple
    svg_img = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100'%3E%3Crect width='100' height='100' fill='%234A90E2'/%3E%3Ctext x='50' y='55' text-anchor='middle' fill='white' font-size='40'%3E📦%3C/text%3E%3C/svg%3E"


# ==================== CLASES DE DATOS ====================
@dataclass
class Contenedor:
    id: str
    tiempo_llegada: float
    posicion_actual: str = "BUQUE"
    estado: str = "En Buque"
    
    def __repr__(self):
        return f"{self.id} [{self.estado}]"


@dataclass
class EventoSimulacion:
    tiempo: float
    contenedor_id: str
    accion: str
    origen: str
    destino: str
    
    def __repr__(self):
        return f"t={self.tiempo:.1f} | {self.contenedor_id}: {self.accion} ({self.origen}→{self.destino})"


# ==================== CONFIGURACIÓN DE ZONAS ====================
ZONAS = {
    "BUQUE": {"x": 0, "y": 60, "color": "#2E86AB", "label": "🚢 Buque"},
    "PISO": {"x": 180, "y": 60, "color": "#A23B72", "label": "📍 Piso"},
    "PATIO": {"x": 360, "y": 60, "color": "#F18F01", "label": "🏭 Patio"}
}

# Tiempos de traslado (en unidades de simulación)
TIEMPO_BUQUE_A_PISO = 2.0
TIEMPO_PISO_A_PATIO = 1.5


# ==================== SIMULACIÓN SIMPY ====================
class SimuladorContenedores:
    def __init__(self, env):
        self.env = env
        self.eventos = []
        self.contenedores = []
        self.estado_actual = {}  # {contenedor_id: zona}
    
    def registrar_evento(self, contenedor: Contenedor, accion: str, origen: str, destino: str):
        """Registra un evento en el log"""
        evento = EventoSimulacion(
            tiempo=self.env.now,
            contenedor_id=contenedor.id,
            accion=accion,
            origen=origen,
            destino=destino
        )
        self.eventos.append(evento)
        self.estado_actual[contenedor.id] = destino
    
    def proceso_contenedor(self, contenedor: Contenedor):
        """Proceso completo de un contenedor: BUQUE → PISO → PATIO"""
        
        # 1. INICIO: En el buque
        contenedor.posicion_actual = "BUQUE"
        contenedor.estado = "En Buque - Esperando descarga"
        self.registrar_evento(contenedor, "Llegada", "MAR", "BUQUE")
        
        # Esperar un poco en el buque (descarga)
        yield self.env.timeout(random.uniform(0.5, 1.5))
        
        # 2. TRASLADO: BUQUE → PISO
        contenedor.estado = "En tránsito a Piso"
        self.registrar_evento(contenedor, "Iniciando traslado", "BUQUE", "PISO")
        yield self.env.timeout(TIEMPO_BUQUE_A_PISO)
        
        contenedor.posicion_actual = "PISO"
        contenedor.estado = "En Piso - Verificación"
        self.registrar_evento(contenedor, "Llegó a Piso", "BUQUE", "PISO")
        
        # Tiempo de verificación en piso
        yield self.env.timeout(random.uniform(1.0, 2.0))
        
        # 3. TRASLADO: PISO → PATIO
        contenedor.estado = "En tránsito a Patio"
        self.registrar_evento(contenedor, "Iniciando traslado", "PISO", "PATIO")
        yield self.env.timeout(TIEMPO_PISO_A_PATIO)
        
        contenedor.posicion_actual = "PATIO"
        contenedor.estado = "En Patio - Almacenado"
        self.registrar_evento(contenedor, "Llegó a Patio", "PISO", "PATIO")
        
        # Final: Contenedor almacenado
        yield self.env.timeout(0.1)
        contenedor.estado = "✅ Almacenado"
    
    def generador_contenedores(self, num_contenedores: int, intervalo: float):
        """Genera contenedores que llegan al buque"""
        for i in range(num_contenedores):
            contenedor = Contenedor(
                id=f"CNT-{i+1:03d}",
                tiempo_llegada=self.env.now
            )
            self.contenedores.append(contenedor)
            
            # Iniciar proceso del contenedor
            self.env.process(self.proceso_contenedor(contenedor))
            
            # Esperar antes de generar el siguiente
            yield self.env.timeout(intervalo)


def ejecutar_simulacion(num_contenedores: int, intervalo: float, duracion: float):
    """Ejecuta la simulación SimPy"""
    env = simpy.Environment()
    simulador = SimuladorContenedores(env)
    
    # Iniciar generador de contenedores
    env.process(simulador.generador_contenedores(num_contenedores, intervalo))
    
    # Correr simulación
    env.run(until=duracion)
    
    return simulador


# ==================== VISUALIZACIÓN ====================
def crear_escena_html(contenedores_por_zona: Dict[str, List[Contenedor]], contenedor_activo=None):
    """Crea el HTML de la escena con todas las zonas en layout vertical"""
    
    zonas_html = ""
    for zona_nombre, zona_info in ZONAS.items():
        contenedores_en_zona = contenedores_por_zona.get(zona_nombre, [])
        num_contenedores = len(contenedores_en_zona)
        
        zonas_html += f"""
        <div style="
            position: relative;
            width: 100%;
            height: 200px;
            border: 4px solid {zona_info['color']};
            background: linear-gradient(90deg, {zona_info['color']}22 0%, {zona_info['color']}44 100%);
            border-radius: 20px;
            margin: 20px 0;
            display: block;
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        ">
            <div style="
                position: absolute;
                left: 20px;
                top: 50%;
                transform: translateY(-50%);
                font-weight: bold;
                color: {zona_info['color']};
                font-size: 32px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            ">
                {zona_info['label']}
            </div>
            <div style="
                position: absolute;
                top: 20px;
                right: 20px;
                background: {zona_info['color']};
                color: white;
                padding: 10px 20px;
                border-radius: 25px;
                font-weight: bold;
                font-size: 18px;
                box-shadow: 0 3px 6px rgba(0,0,0,0.2);
            ">
                {num_contenedores} 📦
            </div>
        """
        
        # Dibujar contenedores en esta zona (distribuidos horizontalmente)
        for idx, cnt in enumerate(contenedores_en_zona[:15]):  # Max 15 visibles
            is_active = contenedor_activo and cnt.id == contenedor_activo.id
            zonas_html += f"""
            <img src="{svg_img}" style="
                position: absolute;
                left: {200 + (idx * 60)}px;
                top: 50%;
                transform: translateY(-50%) scale({1.3 if is_active else 1.0});
                width: 50px;
                height: 50px;
                opacity: {1.0 if is_active else 0.7};
                transition: all 0.4s ease;
                filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3)) {('hue-rotate(120deg) brightness(1.3)' if is_active else '')};
            ">
            """
        
        zonas_html += "</div>"
    
    html_completo = f"""
    <div style="
        background: linear-gradient(to bottom, #e3f2fd 0%, #bbdefb 100%);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        min-height: 700px;
    ">
        {zonas_html}
    </div>
    """
    
    return html_completo


def animar_simulacion(simulador: SimuladorContenedores, velocidad: float = 0.5):
    """Anima los eventos de la simulación paso a paso"""
    
    # Crear contenedores de placeholders
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎬 Visualización en Tiempo Real")
        placeholder_escena = st.empty()
    
    with col2:
    
        contenedores_por_zona = {"BUQUE": [], "PISO": [], "PATIO": []}
    
    for evento in simulador.eventos:
        # Actualizar posiciones
        contenedor = next(c for c in simulador.contenedores if c.id == evento.contenedor_id)
        
        # Remover de zona origen
        for zona in contenedores_por_zona.values():
            if contenedor in zona:
                zona.remove(contenedor)
        
        # Agregar a zona destino
        if evento.destino in contenedores_por_zona:
            contenedores_por_zona[evento.destino].append(contenedor)
        
        # Renderizar escena
        html = crear_escena_html(contenedores_por_zona, contenedor)
        placeholder_escena.html(html)
        
     
        
        time.sleep(velocidad)


# ==================== INTERFAZ STREAMLIT ====================
st.title("🚢 Simulación: Buque → Piso → Patio")
st.markdown("**Simulación de flujo de contenedores con SimPy + Animación**")

# Sidebar: Configuración
with st.sidebar:
    st.header("⚙️ Configuración")
    
    num_contenedores = st.slider("Número de contenedores", 1, 10, 5)
    intervalo = st.slider("Intervalo entre llegadas (unidades)", 0.5, 5.0, 1.5)
    velocidad_animacion = st.slider("Velocidad de animación (s)", 0.1, 2.0, 0.5)
    
    st.markdown("---")
    st.markdown("### 📊 Tiempos del Sistema")
    st.info(f"⏱️ Buque → Piso: {TIEMPO_BUQUE_A_PISO}u")
    st.info(f"⏱️ Piso → Patio: {TIEMPO_PISO_A_PATIO}u")

# Botón principal
col1, col2 = st.columns([1, 3])
with col1:
    if st.button("▶️ Iniciar Simulación", type="primary", use_container_width=True):
        st.session_state['simular'] = True

with col2:
    if st.button("🔄 Reiniciar", use_container_width=True):
        st.session_state['simular'] = False
        st.rerun()

# Ejecutar simulación
if st.session_state.get('simular', False):
    with st.spinner("🔧 Ejecutando simulación SimPy..."):
        # Calcular duración total necesaria
        duracion_total = (num_contenedores * intervalo) + TIEMPO_BUQUE_A_PISO + TIEMPO_PISO_A_PATIO + 5
        
        simulador = ejecutar_simulacion(num_contenedores, intervalo, duracion_total)
        
        st.success(f"✅ Simulación completada: {len(simulador.eventos)} eventos generados")
    
    # Mostrar estadísticas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Contenedores Procesados", len(simulador.contenedores))
    with col2:
        en_patio = sum(1 for c in simulador.contenedores if c.posicion_actual == "PATIO")
        st.metric("En Patio Final", en_patio)
    with col3:
        st.metric("Eventos Totales", len(simulador.eventos))
    
    st.markdown("---")
    
    # Animación
    if st.button("🎬 Reproducir Animación", type="primary"):
        animar_simulacion(simulador, velocidad_animacion)
    
    # Tabla de eventos
    with st.expander("📊 Ver tabla completa de eventos"):
        import pandas as pd
        df = pd.DataFrame([
            {
                'Tiempo': f"{e.tiempo:.2f}",
                'Contenedor': e.contenedor_id,
                'Acción': e.accion,
                'Origen': e.origen,
                'Destino': e.destino
            }
            for e in simulador.eventos
        ])
        st.dataframe(df, use_container_width=True)

else:
    st.info("👈 Configura los parámetros y presiona **Iniciar Simulación**")
    
    # Vista previa estática
    st.markdown("### 👀 Vista Previa del Sistema")
    contenedores_demo = [Contenedor(f"CNT-{i:03d}", 0) for i in range(3)]
    demo_zonas = {
        "BUQUE": contenedores_demo[:1],
        "PISO": contenedores_demo[1:2],
        "PATIO": contenedores_demo[2:]
    }
    st.html(crear_escena_html(demo_zonas))
