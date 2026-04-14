import streamlit as st
import pandas as pd
import numpy as np
import random 
from dataclasses import dataclass
import random
COSTO_PENALIZACION_DIA = 50.0 
COSTO_POR_HORA_FIJO = 2.08 

st.set_page_config(layout="wide", page_title="MySSD")

with st.sidebar:
    st.title("Panel de  Configuración")
    
    st.header("Parámetros Globales del Escenario")
    
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
        help="Tasa de llegada de contenedores al patio."
    )

    num_lineas = st.number_input(
        "Cantidad de Líneas de Transporte (X)", 
        min_value=1, 
        value=3,
        help="Cuántas líneas transportistas distintas se van a modelar."
    )
    
    st.header("Política de Asignación y Costos")
    
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
        value=int(COSTO_PENALIZACION_DIA)
    )

    st.caption(f"Costo por hora de penalización: ${COSTO_POR_HORA_FIJO:.2f} USD")

    st.header("Configuración de Líneas Transportistas")
    st.caption("Aquí se define el comportamiento de CADA línea.")

    line_configs = []
    
    for i in range(num_lineas):
        with st.expander(f"Parámetros de la Línea {i + 1}", expanded=True if i == 0 else False):
            
            tasa_llegada_linea = st.slider(
                f"Llegadas (Prom/Hora) - Línea {i+1}",
                0.1, 20.0, 5.0, step=0.1, key=f"tasa_llegada_{i}",
                help="Tasa de llegada de camiones específica para esta línea."
            )
            
            prob_falla = st.slider(
                f"Prob. Falla Admin. (%) - Línea {i+1}",
                0.0, 1.0, 0.10, format="%.2f", key=f"falla_{i}",
                help="Probabilidad de fallas de documentación/papelería."
            )
            
            prob_retraso = st.slider(
                f"Prob. Retraso/Ausencia (%) - Línea {i+1}",
                0.0, 1.0, 0.15, format="%.2f", key=f"retraso_{i}",
                help="Probabilidad de fallas mecánicas o ausencia de chofer."
            )
            
            line_configs.append({
                "id": i + 1,
                "tasa_llegada": tasa_llegada_linea,
                "prob_falla": prob_falla,
                "prob_retraso": prob_retraso
            })

    st.header("Controles de Simulación")
    
    status_placeholder = st.empty()
    status_placeholder.warning("Configuración lista. Presione 'Iniciar' para correr el modelo.")
    
    st.button("Iniciar Simulación", use_container_width=True, type="primary")
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("Pausar", use_container_width=True)
    with col2:
        st.button("Resetear", use_container_width=True)


st.title("Dashboard de Simulación Logística")
st.caption(f"Evaluando Política: **{politica_asignacion}**")

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
    # Datos de relleno
    acumulacion = 70 + (np.random.randn(30).cumsum() / 3)
    acumulacion = np.clip(acumulacion, 0, capacidad_patio) 
    

    col_x_patio = "Día de Simulación"
    col_y_patio = "Contenedores en Patio"

    df_patio = pd.DataFrame({
        col_x_patio: dias,
        col_y_patio: acumulacion
    })

    st.line_chart(df_patio, x=col_x_patio, y=col_y_patio)

with fig_col2:
    st.subheader("Eficiencia por Línea Transportista") 
    line_names = [f"Línea {cfg['id']}" for cfg in line_configs]
    
    # Datos de relleno 
    random.seed(42) 
    tasas_falla = np.random.uniform(5, 25, len(line_names)).round(1) 
    

    col_x_eficiencia = "Línea Transportista"
    col_y_eficiencia = "Tasa de Falla Configurada (%)"

    df_eficiencia = pd.DataFrame({
        col_x_eficiencia: line_names,
        col_y_eficiencia: tasas_falla
    })
    st.bar_chart(df_eficiencia, x=col_x_eficiencia, y=col_y_eficiencia)


st.header("Log de Eventos (Bitácora)")
log_container = st.container(height=300)
# Datos de relleno
log_container.write("10:01 AM - Contenedor C-101 (Prioridad: ALTA) llegó.")
log_container.write("10:03 AM - Línea 1 (Confiabilidad: 85%) llegó.")
log_container.write("10:04 AM - ASIGNACIÓN (Política: Prioridad por Conf.): C-101 -> Línea 1.")
log_container.write("10:07 AM - FALLA: Línea 2 sin documentos (Falla Admin).")
log_container.write("10:08 AM - DEVOLUCIÓN: Contenedor C-102 devuelto al patio.")