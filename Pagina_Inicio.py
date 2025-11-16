import streamlit as st
import simpy
import random
import pandas as pd
import numpy as np
import io

# --- Configuración de la Página de Streamlit (Diseño Ejecutivo) ---
st.set_page_config(
    page_title="Plataforma de Simulación De Cadena De Suministros (Simulación Avanzada)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Variables Globales y Definiciones de Líneas ---
LOG_EVENTOS = []
REGISTRO_VIAJES = []

# Definición de Líneas Transportistas (Base)
LINEAS_TRANSPORTISTAS = {
    'Línea A (Premium)': {'puntualidad_media': 5, 'prob_falla': 0.10}, 
    'Línea B (Estándar)': {'puntualidad_media': 10, 'prob_falla': 0.25}, 
    'Línea C (Económica)': {'puntualidad_media': 15, 'prob_falla': 0.40}, 
}
LINEAS_COLORES = {
    'Línea A (Premium)': '#28a745',
    'Línea B (Estándar)': '#ffc107',
    'Línea C (Económica)': '#dc3545',
}

# --- Clase del Entorno de Simulación (PatioContenedores) ---
class PatioContenedores(object):
    """Implementa el entorno de simulación discreta."""
    def __init__(self, env, num_gruas, capacidad_patio, params, df_flota_usuario):
        self.env = env
        self.gruas = simpy.Resource(env, capacity=num_gruas)
        self.inventario_contenedores = simpy.Container(env, init=0, capacity=capacidad_patio)
        self.params = params
        self.lineas = list(LINEAS_TRANSPORTISTAS.keys())
        self.contenedores_perdidos = 0
        self.total_contenedores_llegados = 0
        
        # Flota y Rutas Personalizadas
        self.df_flota = df_flota_usuario 
        self.conductores_disponibles = self.df_flota['Conductor'].unique() if not self.df_flota.empty else ['Conductor Genérico']

    def registrar_evento(self, tipo, detalle, transportista_id='N/A'):
        """Método para registrar eventos estructurados en el log."""
        LOG_EVENTOS.append({
            'tiempo': self.env.now,
            'tipo_evento': tipo,
            'detalle': detalle,
            'transportista_id': transportista_id,
            'contenedores_patio': self.inventario_contenedores.level
        })

    def asignar_contenedor(self, linea_nombre, linea_params):
        """Proceso de Asignación y Despacho/Devolución."""
        
        # Seleccionar un conductor/camión/ruta al azar de la flota definida por el usuario
        if not self.df_flota.empty:
            flota_row = self.df_flota.sample(n=1).iloc[0]
            ruta_destino = flota_row['Ruta Destino']
            transportista_id = f"{flota_row['Placa']}/{flota_row['Conductor']}"
            costo_conductor = flota_row['Costo Conductor/Viaje ($)']
            plazo_ruta_min = flota_row['Plazo Estimado (min)']
        else:
            ruta_destino = "Ruta Predeterminada"
            transportista_id = f"CAM-GEN/CD-GEN"
            costo_conductor = 100
            plazo_ruta_min = 120 

        if self.inventario_contenedores.level > 0:
            yield self.inventario_contenedores.get(1) 
            self.registrar_evento('Solicitud', f'Camión {transportista_id} solicita contenedor para {ruta_destino}.', transportista_id)
            
            with self.gruas.request() as req:
                tiempo_llegada_a_cola = self.env.now
                yield req
                tiempo_inicio_carga = self.env.now
                tiempo_espera_grua = tiempo_inicio_carga - tiempo_llegada_a_cola
                
                if random.random() < linea_params['prob_falla']:
                    self.registrar_evento('Falla', f'Camión {transportista_id} FALLA.', transportista_id)
                    yield self.env.timeout(self.params['tiempo_devolucion']) 
                    yield self.inventario_contenedores.put(1)
                    return False, tiempo_espera_grua, 0, ruta_destino, 0, 0, transportista_id.split('/')[1], transportista_id.split('/')[0]
                
                else:
                    tiempo_carga = random.expovariate(1.0 / self.params['tasa_carga']) 
                    yield self.env.timeout(tiempo_carga)
                    self.registrar_evento('Despacho', f'Camión {transportista_id} despachado a {ruta_destino}.', transportista_id)
                    
                    return True, tiempo_espera_grua, tiempo_carga, ruta_destino, costo_conductor, plazo_ruta_min, transportista_id.split('/')[1], transportista_id.split('/')[0]
        else:
            self.registrar_evento('Espera', f'Camión {transportista_id} llegó, patio vacío.', transportista_id)
            return False, 0, 0, 'N/A', 0, 0, transportista_id.split('/')[1], transportista_id.split('/')[0]

# --- Procesos de Simulación ---

def generador_contenedores(env, patio):
    """Generación de contenedores."""
    i = 0
    while True:
        i += 1
        patio.total_contenedores_llegados += 1
        yield env.timeout(random.expovariate(1.0 / patio.params['tasa_llegada_contenedores']))
        
        if patio.inventario_contenedores.capacity - patio.inventario_contenedores.level > 0:
             yield patio.inventario_contenedores.put(1)
             patio.registrar_evento('Inventario', f'Contenedor C-{i} agregado.', f'C-{i}')
        else:
            patio.contenedores_perdidos += 1
            patio.registrar_evento('Inventario', f'ADVERTENCIA: Contenedor C-{i} PERDIDO. Patio LLENO.', f'C-{i}')

def generador_transportistas(env, patio):
    """Generación de transportistas, cálculo de tiempos y costos."""
    
    i = 0
    while True:
        i += 1
        linea_nombre = random.choice(patio.lineas)
        linea_params = LINEAS_TRANSPORTISTAS[linea_nombre]
        
        yield env.timeout(random.expovariate(1.0 / linea_params['puntualidad_media']))
        tiempo_llegada = env.now
        
        exito, t_espera_grua, t_carga, ruta_destino, costo_conductor, plazo_ruta_min, conductor, placa = yield env.process(patio.asignar_contenedor(linea_nombre, linea_params))
        
        tiempo_salida = env.now
        tiempo_total_patio = tiempo_salida - tiempo_llegada
        
        # Cálculo Financiero
        tiempo_base_min = patio.params['tiempo_patio_base'] * 60
        costo_por_min_extra = patio.params['costo_exceso_horas'] / 60 
        tiempo_exceso = max(0, tiempo_total_patio - tiempo_base_min)
        costo_demurrage = tiempo_exceso * costo_por_min_extra
        
        # Registro de Viaje
        REGISTRO_VIAJES.append({
            'camion_id': placa,
            'conductor': conductor,
            'linea_transportista': linea_nombre,
            'exitoso': exito,
            'tiempo_total_patio': tiempo_total_patio,
            'tiempo_espera_grua': t_espera_grua,
            'tiempo_carga_despacho': t_carga,
            'tiempo_exceso': tiempo_exceso,
            'costo_demurrage': costo_demurrage,
            'ruta_destino': ruta_destino,
            'costo_conductor': costo_conductor,
            'plazo_ruta_min': plazo_ruta_min
        })
        
# --- Función Principal de Ejecución ---

def ejecutar_simulacion(params, df_flota_usuario):
    """Orquesta la inicialización y ejecución."""
    
    global LOG_EVENTOS, REGISTRO_VIAJES
    LOG_EVENTOS = []
    REGISTRO_VIAJES = []
    
    random.seed(42) 
    env = simpy.Environment()
    
    patio = PatioContenedores(env, params['num_gruas'], params['capacidad_patio'], params, df_flota_usuario)

    env.process(generador_contenedores(env, patio))
    env.process(generador_transportistas(env, patio))

    patio.registrar_evento('Sistema', f"Inicio Simulación ({params['tiempo_simular']} min).", None)
    env.run(until=params['tiempo_simular'])
    patio.registrar_evento('Sistema', f"Fin Simulación.", None)
    
    df_log = pd.DataFrame(LOG_EVENTOS)
    df_viajes = pd.DataFrame(REGISTRO_VIAJES)
    
    if not df_viajes.empty:
        df_viajes['stock_final'] = patio.inventario_contenedores.level
        df_viajes['contenedores_perdidos'] = patio.contenedores_perdidos
    
    return df_log, df_viajes

# --- LAYOUT Y WIDGETS DE STREAMLIT ---

# Inicializar o cargar el DataFrame de Flota en el estado de la sesión
if 'df_flota' not in st.session_state:
    st.session_state.df_flota = pd.DataFrame({
        'Conductor': ['J. Pérez', 'M. Garcí­a'],
        'Placa': ['ABC-123', 'DEF-456'],
        'Ruta Destino': ['Laredo-Customs', 'Puerto Progreso'],
        'Costo Conductor/Viaje ($)': [100, 150],
        'Plazo Estimado (min)': [120, 240]
    })
    
if 'df_viajes_hist' not in st.session_state:
    st.session_state.df_viajes_hist = pd.DataFrame()

def agregar_flota_row():
    """Función para agregar una fila al DataFrame de la flota."""
    nueva_fila = pd.DataFrame({
        'Conductor': ['Nuevo Conductor'],
        'Placa': ['XXX-999'],
        'Ruta Destino': ['Ruta Genérica'],
        'Costo Conductor/Viaje ($)': [120],
        'Plazo Estimado (min)': [180]
    })
    st.session_state.df_flota = pd.concat([st.session_state.df_flota, nueva_fila], ignore_index=True)

def reset_parametros():
    """Reinicia parámetros y el historial de viajes."""
    keys = ['num_gruas', 'capacidad_patio', 'tasa_llegada_contenedores', 
            'tasa_carga', 'tiempo_devolucion', 'tiempo_patio_base', 
            'costo_exceso_horas', 'tiempo_simular']
    for key in keys:
        if key in st.session_state:
            del st.session_state[key]
    # Reinicia la tabla de la flota
    st.session_state.df_flota = pd.DataFrame({
        'Conductor': ['J. Pérez', 'M. Garcí­a'],
        'Placa': ['ABC-123', 'DEF-456'],
        'Ruta Destino': ['Laredo-Customs', 'Puerto Progreso'],
        'Costo Conductor/Viaje ($)': [100, 150],
        'Plazo Estimado (min)': [120, 240]
    })
    st.session_state.df_viajes_hist = pd.DataFrame()
    st.experimental_rerun() 

# --- Cabecera Principal ---
st.markdown("<h1 style='text-align: center; color: #1e8449;'> Plataforma de Simulación Para Cadena De Suministros </h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #6c757d;'> Modelo de Simulación Discreta para la Cadena de Suministro </h4>", unsafe_allow_html=True)
st.markdown("---")

# --- MÓDULO PRINCIPAL DE CONFIGURACIÓN DE FLOTA Y RUTAS ---

st.header("📋 1. Configuración de Flota, Rutas y Costos Variables")
st.markdown("**Instrucciones:** Utilice la tabla para definir, **editar o eliminar** la información detallada de cada unidad de transporte y la ruta asociada. Asegúrese de que los datos de **Placa**, **Conductor**, **Costo** y **Plazo Estimado** sean correctos.")

col_table, col_button = st.columns([4, 1])

with col_table:
    # Editar, Eliminar y Agregar Datos (Control Total sobre la Flota)
    st.session_state.df_flota = st.data_editor(
        st.session_state.df_flota,
        num_rows="dynamic", # Permite agregar y eliminar filas
        use_container_width=True,
        key='data_editor_flota'
    )
    
with col_button:
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("➕ Agregar Nueva Unidad/Ruta", on_click=agregar_flota_row, use_container_width=True)

st.markdown("---")

# --- PANEL LATERAL DE PARÁMETROS FIJOS ---
with st.sidebar:
    st.header("⚙️ Parámetros Fijos del Patio")

    # --- Parámetros Operacionales ---
    with st.expander("Parámetros Operacionales", expanded=True):
        st.subheader("Capacidad y Tiempos")
        num_gruas = st.slider("Número de Grúas:", 1, 5, 2, key='num_gruas')
        capacidad_patio = st.number_input("Capacidad Máxima del Patio (N Cont.):", 50, 500, 100, step=10, key='capacidad_patio')
        
        st.subheader("Tasas de Flujo")
        tasa_llegada_contenedores = st.number_input("Tasa de Llegada Contenedores (Media min):", 5, 60, 10, key='tasa_llegada_contenedores')
        tasa_carga = st.number_input("Tasa de Carga (Media min):", 5, 60, 20, key='tasa_carga')
        tiempo_devolucion = st.number_input("Tiempo de Re-Acomodo por Falla (min):", 5, 30, 10, key='tiempo_devolucion')

    st.markdown("---")

    # --- Parámetros Financieros ---
    with st.expander("Parámetros Financieros (Demurrage)", expanded=True):
        st.subheader("Cálculo de Costos por Permanencia")
        tiempo_patio_base = st.number_input("Tiempo Base Libre de Patio (horas):", 1, 12, 4, key='tiempo_patio_base')
        costo_exceso_horas = st.number_input("Costo de Almacenaje (USD/hora):", 0.0, 50.0, 15.0, step=1.0, key='costo_exceso_horas')
        
    st.markdown("---")
    
    # --- Parámetros de Control ---
    st.subheader("Control de Simulación")
    tiempo_simular = st.number_input("Duración de la Simulación (minutos):", 60, 10000, 480, step=60, key='tiempo_simular')
    
    # Botón de Ejecución (Principal)
    submitted = st.button("🚀 INICIAR ANÁLISIS DE SIMULACIÓN", type="primary", use_container_width=True)
    
    # Botón para Resetear (Botón necesario para la página correcta)
    st.button("🔄 Resetear Todo (Parámetros e Historial)", on_click=reset_parametros, use_container_width=True)
    
# --- Lógica de Presentación ---

if submitted:
    
    # 1. Validación de Flota
    if st.session_state.df_flota.empty:
        st.error("Debe definir al menos una unidad de transporte en la tabla de configuración (Sección 1).")
        st.stop()
        
    params = {
        'num_gruas': num_gruas,
        'capacidad_patio': capacidad_patio,
        'tasa_llegada_contenedores': tasa_llegada_contenedores,
        'tasa_carga': tasa_carga,
        'tiempo_devolucion': st.session_state.get('tiempo_devolucion', 10),
        'tiempo_patio_base': tiempo_patio_base,
        'costo_exceso_horas': costo_exceso_horas,
        'tiempo_simular': tiempo_simular,
    }
    
    with st.spinner('Ejecutando modelo de simulación de eventos discretos...'):
        df_log, df_viajes = ejecutar_simulacion(params, st.session_state.df_flota)
        
    st.success('✅ Análisis completado. Resultados listos para la toma de decisiones.')
    st.markdown("---")
    
    if df_viajes.empty:
        st.error("La simulación no generó viajes exitosos. Ajuste los parámetros de flujo.")
        st.stop()
        
    # Guardar el historial de viajes para el análisis futuro
    st.session_state.df_viajes_hist = pd.concat([st.session_state.df_viajes_hist, df_viajes], ignore_index=True)

    df_exitosos = df_viajes[df_viajes['exitoso'] == True].copy()
    
    # --- Cálculo de KPIs ---
    stock_final = df_viajes.iloc[0]['stock_final'] if not df_viajes.empty else 0
    camiones_procesados = len(df_exitosos)
    tiempo_promedio_patio = df_exitosos['tiempo_total_patio'].mean() if not df_exitosos.empty else 0
    total_costo_conductor = df_exitosos['costo_conductor'].sum() if not df_exitosos.empty else 0
    total_viajes = len(df_viajes)
    tasa_falla_op = 1 - (camiones_procesados / total_viajes) if total_viajes > 0 else 0
    total_demurrage = df_viajes['costo_demurrage'].sum()
    
    # --- Dashboard de Indicadores Clave (KPIs) ---
    
    st.header("2. 📊 Dashboard Ejecutivo de Desempeño")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"**Tiempo Promedio en Patio** 🕒")
        st.info(f"{tiempo_promedio_patio:.2f} min")
    with col2:
        st.markdown(f"**Costo Total Demurrage** 💰")
        st.warning(f"${total_demurrage:,.0f} USD")
    with col3:
        st.markdown(f"**Costo Total Conductores** 💵")
        st.metric(label="Total Operacional", value=f"${total_costo_conductor:,.0f} USD")
    with col4:
        st.markdown(f"**Tasa de Falla Operacional** 📉")
        st.error(f"{tasa_falla_op:.2%}")
    with col5:
        st.markdown(f"**Acumulación Final (Stock)** 📦")
        st.metric(label="Contenedores", value=f"{stock_final}")

    st.markdown("---")

    # --- Análisis de Eficiencia por Conductor (Mejor Conductor) ---
    
    st.header("3. 🏆 Benchmarking y Mejor Conductor/Ruta")
    
    if not st.session_state.df_viajes_hist.empty:
        df_hist = st.session_state.df_viajes_hist[st.session_state.df_viajes_hist['exitoso'] == True]
        
        # Mejor Conductor/Placa (Menor tiempo de Patio)
        df_conductor_ranking = df_hist.groupby(['conductor', 'camion_id']).agg(
            tiempo_promedio_patio=('tiempo_total_patio', 'mean'),
            viajes_completados=('conductor', 'count')
        ).reset_index().sort_values(by='tiempo_promedio_patio', ascending=True)
        
        mejor_conductor = df_conductor_ranking.iloc[0]
        
        col_con, col_ruta = st.columns(2)
        
        with col_con:
            st.subheader("Mejor Conductor (Menor Tiempo en Patio) 🥇")
            st.success(f"**{mejor_conductor['conductor']}** (Placa: {mejor_conductor['camion_id']})")
            st.metric(label="T. Patio Promedio", value=f"{mejor_conductor['tiempo_promedio_patio']:.2f} min")
            st.caption("Basado en el historial acumulado de viajes.")
            
        with col_ruta:
            st.subheader("Ruta Más Rápida de Exportación 🌍")
            df_ruta_ranking = df_hist.groupby('ruta_destino')['tiempo_total_patio'].mean().reset_index().sort_values(by='tiempo_total_patio', ascending=True)
            mejor_ruta = df_ruta_ranking.iloc[0]
            st.info(f"**{mejor_ruta['ruta_destino']}**")
            st.metric(label="T. Patio Promedio", value=f"{mejor_ruta['tiempo_total_patio']:.2f} min")
            st.caption("Indica dónde se logra el despacho más eficiente.")

    st.markdown("---")

# --- MÓDULO DE SIMULACIÓN DE CASO ESPECÍFICO (IMPORTACIÓN/EXPORTACIÓN) ---

st.header("4. 🔍 Simulación Predictiva de Ruta Específica")
st.markdown("**Objetivo:** Simular qué conductor y qué línea de transporte (tasa de falla) son óptimos para una nueva ruta Importación/Exportación, minimizando el tiempo total de permanencia en patio.")

with st.form("simulacion_ruta_especifica"):
    col_input, col_plazo = st.columns(2)
    
    with col_input:
        nueva_ruta = st.text_input("📍 Nombre del Lugar/Ruta (Importación/Exportación):", "Puerto Lázaro Cárdenas - Export")
    
    with col_plazo:
        plazo_simulado = st.number_input("⏰ Plazo Estimado de la Ruta (minutos):", min_value=30, value=300)
    
    simular_conductor = st.form_submit_button("🧪 Simular Mejor Conductor para esta Ruta")
    
if simular_conductor:
    if st.session_state.df_viajes_hist.empty:
        st.warning("Debe ejecutar la simulación principal (Sección 2) al menos una vez para generar el historial de conductores.")
    else:
        st.subheader(f"Resultados de Simulación para: **{nueva_ruta}**")
        
        # 1. Analizar el rendimiento histórico de cada conductor en patio
        df_hist_con = st.session_state.df_viajes_hist[st.session_state.df_viajes_hist['exitoso'] == True]
        
        # Calcular el Tiempo Promedio de Carga/Espera en Patio de CADA CONDUCTOR
        df_desempeno_conductor = df_hist_con.groupby(['conductor', 'camion_id']).agg(
            t_patio_promedio=('tiempo_total_patio', 'mean'),
            viajes_completados=('conductor', 'count')
        ).reset_index()
        
        # 2. Calcular el Tiempo Total estimado para la nueva ruta (Patio + Plazo de Ruta)
        df_desempeno_conductor['t_total_estimado_min'] = df_desempeno_conductor['t_patio_promedio'] + plazo_simulado
        
        # 3. Clasificar y presentar al mejor conductor
        df_mejor_conductor = df_desempeno_conductor.sort_values(by='t_total_estimado_min', ascending=True)
        
        mejor_con = df_mejor_conductor.iloc[0]
        
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.success("Conductor Recomendado (Menor Tiempo Total)")
            st.metric(
                label=f"{mejor_con['conductor']} (Placa: {mejor_con['camion_id']})",
                value=f"{mejor_con['t_total_estimado_min']:.2f} min"
            )
            st.caption(f"Tiempo Total = (T. Patio Promedio Histórico: {mejor_con['t_patio_promedio']:.2f} min) + (Plazo de Ruta: {plazo_simulado} min)")
        
        with col_res2:
            st.warning("Conductor Menos Recomendado (Mayor Tiempo Total)")
            peor_con = df_mejor_conductor.iloc[-1]
            st.metric(
                label=f"{peor_con['conductor']} (Placa: {peor_con['camion_id']})",
                value=f"{peor_con['t_total_estimado_min']:.2f} min"
            )
            st.caption("Esta métrica ayuda a prevenir retrasos en rutas críticas.")
            
        with st.expander("Tabla Detallada de Rendimiento Estimado"):
            st.dataframe(df_mejor_conductor)


st.markdown("---")