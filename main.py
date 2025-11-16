import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="Simulación Logística (v2.2 - Completo)")

with st.sidebar:
    st.title("Panel de Configuración")
    
    st.header("1. Parámetros Globales del Escenario")
    
    capacidad_patio = st.number_input(
        "Capacidad del Patio (N contenedores)", 
        min_value=1, 
        value=90
    )
    
    tasa_llegada_contenedores = st.number_input(
        "Llegada de Contenedores (Prom/Hora)", 
        min_value=0.1, 
        value=5.0,
        step=0.1,
        help="Tasa de llegada de contenedores al patio. Usará una distribución de probabilidad (ej. Exponencial)."
    )

    num_lineas = st.number_input(
        "Cantidad de Líneas de Transporte (X)", 
        min_value=1, 
        value=3,
        help="Cuántas líneas transportistas distintas se van a modelar."
    )
    
    st.header("2. Política de Asignación y Costos")
    
    politica_asignacion = st.selectbox(
        "Política de Asignación",
        ("Por Orden de Llegada (FIFO)", 
         "Prioridad por Confiabilidad", 
         "Por Tipo de Carga (Prioridad)") 
    )

    sla_maximo = st.number_input(
        "SLA Máximo (horas)", 
        min_value=1, 
        value=72
    )
    
    penalizacion_sla = st.number_input(
        "Penalización por Día ($ USD)", 
        min_value=0, 
        value=50
    )

    st.header("3. Configuración de Líneas Transportistas")
    st.caption("Aquí se define el comportamiento de CADA línea.")

    line_configs = []
    
    for i in range(num_lineas):
        with st.expander(f"Parámetros de la Línea {i + 1}"):
            
            tasa_llegada_linea = st.slider(
                f"Llegadas (Prom/Hora) - Línea {i+1}",
                0.1, 20.0, 5.0, step=0.1, key=f"tasa_llegada_{i}",
                help="Tasa de llegada de camiones específica para esta línea."
            )
            
            prob_falla = st.slider(
                f"Prob. Falla Admin. (%) - Línea {i+1}",
                0.0, 1.0, 0.10, format="%.2f", key=f"falla_{i}",
                help="Probabilidad de fallas de documentación, etc. [cite: 80]"
            )
            
            prob_retraso = st.slider(
                f"Prob. Retraso/Ausencia (%) - Línea {i+1}",
                0.0, 1.0, 0.15, format="%.2f", key=f"retraso_{i}",
                help="Probabilidad de que el camión llegue tarde o no llegue[cite: 79]."
            )
            
            line_configs.append({
                "id": i + 1,
                "tasa_llegada": tasa_llegada_linea,
                "prob_falla": prob_falla,
                "prob_retraso": prob_retraso
            })

    st.header("4. Controles de Simulación")
    st.button("Iniciar Simulación", use_container_width=True, type="primary")
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("Pausar", use_container_width=True)
    with col2:
        st.button("Resetear", use_container_width=True)


st.title("Dashboard de Simulación Logística")
st.caption(f"Evaluando Política: {politica_asignacion}")

st.header("Métricas Clave (KPIs)")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Costo Total de Almacenamiento", value="$ 12,550") 
with col2:
    st.metric(label="Tiempo Prom. Espera (hrs)", value="8.2 hrs") 
with col3:
    st.metric(label="Tasa de Cumplimiento (SLA)", value="85%", delta="-2%") 

col4, col5, col6 = st.columns(3)
with col4:
    st.metric(label="Acumulación en Patio", value=f"78 / {capacidad_patio}") 
with col5:
    st.metric(label="Total Fallas (Reprogramaciones)", value="112") 
with col6:
    st.metric(label="Utilización de Líneas", value="75%") 

st.divider()

st.header("Flujo del Proceso y Gráficos")
fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.subheader("Acumulación en Patio (vs. Tiempo)")
    dias = np.arange(1, 31)
    acumulacion = 70 + (np.random.randn(30).cumsum() / 3)
    acumulacion = np.clip(acumulacion, 0, capacidad_patio) 
    
    # --- INICIO DE LA CORRECCIÓN ---
    # Definimos los nombres de las columnas como variables
    col_x_patio = "Día de Simulación"
    col_y_patio = "Contenedores en Patio"

    df_patio = pd.DataFrame({
        col_x_patio: dias,
        col_y_patio: acumulacion
    })
    # Usamos las variables para llamar al gráfico
    st.line_chart(df_patio, x=col_x_patio, y=col_y_patio)
    # --- FIN DE LA CORRECCIÓN ---

with fig_col2:
    st.subheader("Eficiencia por Línea Transportista") 
    line_names = [f"Línea {cfg['id']}" for cfg in line_configs]
    tasas_falla = [cfg['prob_falla'] + cfg['prob_retraso'] for cfg in line_configs]
    
    # --- INICIO DE LA CORRECCIÓN ---
    # Aplicamos la misma buena práctica aquí
    col_x_eficiencia = "Línea Transportista"
    col_y_eficiencia = "Tasa de Falla Configurada (%)"

    df_eficiencia = pd.DataFrame({
        col_x_eficiencia: line_names,
        col_y_eficiencia: tasas_falla
    })
    # Usamos las variables
    st.bar_chart(df_eficiencia, x=col_x_eficiencia, y=col_y_eficiencia)
    # --- FIN DE LA CORRECCIÓN ---


st.header("Log de Eventos (Bitácora)")
log_container = st.container(height=300)
log_container.write("10:01 AM - Contenedor C-101 (Prioridad: ALTA) llegó.")
log_container.write("10:03 AM - Línea 1 (Confiabilidad: 85%) llegó.")
log_container.write("10:04 AM - ASIGNACIÓN (Política: Prioridad por Conf.): C-101 -> Línea 1.")
log_container.write("10:07 AM - FALLA: Línea 2 sin documentos (Falla Admin).")
log_container.write("10:08 AM - DEVOLUCIÓN: Contenedor C-102 devuelto al patio.")