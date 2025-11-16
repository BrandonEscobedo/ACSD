import streamlit as st
import simpy
import random
import pandas as pd
import time
import io

# --- Configuración de la Página de Streamlit ---
st.set_page_config(
    page_title="Simulador de Patio de Contenedores",
    layout="wide"
)

# --- Variables Globales para Resultados ---
TIEMPOS_ESPERA_TOTAL = []
CAMIONES_PROCESADOS = 0

# --- Constantes y Tiempos de Distribución (Ajustables) ---
CAPACIDAD_PATIO = 100                     # Espacio máximo para contenedores
NUM_LINEAS_TRANSPORTISTAS = 5           # Cantidad de líneas de transporte
TIEMPO_ENTRE_LLEGADA_CONTENEDOR = 10      # Media de minutos entre llegadas
TIEMPO_ENTRE_LLEGADA_TRANSPORTISTA = 5    # Media de minutos entre llegadas de la *misma* línea
TIEMPO_ASIGNACION_CARGA = 20              # Minutos que tarda la grúa en cargar
TIEMPO_DEVOLUCION_PATIO = 10              # Minutos que tarda la grúa en devolver al patio (falla)


# --- Clase del Entorno de Simulación ---
class PatioContenedores(object):
    """
    Representa el entorno de simulación del patio de contenedores.
    Contiene las grúas (recurso) y el inventario de contenedores.
    """
    def __init__(self, env, num_gruas, capacidad_patio, prob_falla):
        self.env = env
        self.gruas = simpy.Resource(env, capacity=num_gruas)
        self.inventario_contenedores = simpy.Container(env, init=0, capacity=capacidad_patio)
        self.capacidad_patio = capacidad_patio
        self.prob_falla = prob_falla
        self.log_buffer = io.StringIO()

    def log(self, mensaje):
        """Función para registrar eventos en un buffer en memoria."""
        self.log_buffer.write(f'{self.env.now:.2f} min: {mensaje}\n')
        
    def asignar_contenedor(self, transportista):
        """Proceso que simula la carga y despacho del contenedor."""
        global CAMIONES_PROCESADOS
        
        # 1. Verificar si hay contenedores disponibles en el patio
        if self.inventario_contenedores.level > 0:
            yield self.inventario_contenedores.get(1) # Toma un contenedor del inventario
            
            self.log(f'{transportista} busca asignar contenedor. Contenedores disponibles: {self.inventario_contenedores.level}')
            
            # 2. Simular la operación de carga con una grúa
            with self.gruas.request() as req:
                yield req
                
                # Simular la posible falla del transportista
                if random.random() < self.prob_falla:
                    # FALLA: No cumple con requisitos
                    self.log(f'¡FALLA! {transportista} no cumple requisitos.')
                    
                    # Simular la devolución del contenedor al patio
                    yield self.env.timeout(TIEMPO_DEVOLUCION_PATIO)
                    yield self.inventario_contenedores.put(1) # Devuelve el contenedor
                    self.log(f'Contenedor devuelto al patio.')
                    return False # El transportista NO fue procesado exitosamente
                
                else:
                    # ÉXITO: Transportista apto, procede la carga
                    self.log(f'{transportista} OK. Grúa inicia carga.')
                    yield self.env.timeout(TIEMPO_ASIGNACION_CARGA) # Tiempo de carga
                    self.log(f'Carga completa. {transportista} despachado.')
                    CAMIONES_PROCESADOS += 1
                    return True # El transportista FUE procesado exitosamente
        else:
            # No hay contenedores disponibles
            self.log(f'{transportista} llegó, pero el patio está vacío. Espera...')
            return False

# --- Procesos de Simulación ---

def generador_contenedores(env, patio):
    """Simula la llegada continua de contenedores al patio."""
    i = 0
    while True:
        i += 1
        # Tiempo entre llegadas (distribución exponencial)
        yield env.timeout(random.expovariate(1.0 / TIEMPO_ENTRE_LLEGADA_CONTENEDOR))
        
        if patio.inventario_contenedores.capacity - patio.inventario_contenedores.level > 0:
             yield patio.inventario_contenedores.put(1)
             patio.log(f'Contenedor C-{i} agregado al inventario. Stock: {patio.inventario_contenedores.level}')
        else:
            patio.log(f'ADVERTENCIA: Contenedor C-{i} PERDIDO. Patio está LLENO.')

def generador_transportistas(env, patio):
    """Simula la llegada de transportistas y su intento de despacho."""
    global TIEMPOS_ESPERA_TOTAL
    
    i = 0
    while True:
        i += 1
        linea_id = random.randint(1, NUM_LINEAS_TRANSPORTISTAS)
        nombre_transportista = f'T-{i}/Línea {linea_id}'
        
        # Tiempo de espera hasta la llegada del siguiente transportista
        yield env.timeout(random.expovariate(1.0 / TIEMPO_ENTRE_LLEGADA_TRANSPORTISTA))
        
        tiempo_llegada = env.now
        
        # Proceso del transportista: intenta el despacho
        despacho_exitoso = yield env.process(patio.asignar_contenedor(nombre_transportista))
        
        tiempo_salida = env.now
        tiempo_en_patio = tiempo_salida - tiempo_llegada
        TIEMPOS_ESPERA_TOTAL.append(tiempo_en_patio)
        
        if despacho_exitoso:
            patio.log(f'{nombre_transportista} PROCESADO. Tiempo total en patio: {tiempo_en_patio:.2f} min.')
        else:
            patio.log(f'{nombre_transportista} NO procesado. Tiempo total en patio: {tiempo_en_patio:.2f} min.')
        
        

# --- Función Principal de Ejecución ---

def ejecutar_simulacion(num_gruas, prob_falla, tiempo_simular):
    """Inicializa y ejecuta la simulación."""
    
    # Reiniciar variables globales
    global TIEMPOS_ESPERA_TOTAL, CAMIONES_PROCESADOS
    TIEMPOS_ESPERA_TOTAL = []
    CAMIONES_PROCESADOS = 0
    
    # 1. Configurar el entorno
    random.seed(42) # Semilla para resultados reproducibles
    env = simpy.Environment()
    patio = PatioContenedores(env, num_gruas, CAPACIDAD_PATIO, prob_falla)

    # 2. Iniciar procesos
    env.process(generador_contenedores(env, patio))
    env.process(generador_transportistas(env, patio))

    # 3. Ejecutar la simulación
    patio.log(f"--- INICIO DE SIMULACIÓN ({tiempo_simular} minutos) ---")
    env.run(until=tiempo_simular)
    patio.log("--- FIN DE SIMULACIÓN ---")

    # 4. Calcular y devolver resultados
    if not TIEMPOS_ESPERA_TOTAL:
        tiempo_promedio = 0
        tiempo_maximo = 0
    else:
        tiempo_promedio = sum(TIEMPOS_ESPERA_TOTAL) / len(TIEMPOS_ESPERA_TOTAL)
        tiempo_maximo = max(TIEMPOS_ESPERA_TOTAL)
        
    resultados = {
        "tiempo_promedio": round(tiempo_promedio, 2),
        "tiempo_maximo": round(tiempo_maximo, 2),
        "camiones_procesados": CAMIONES_PROCESADOS,
        "log_simulacion": patio.log_buffer.getvalue()
    }
    
    return resultados

# ----------------------------------------------------
#               INTERFAZ DE USUARIO (Streamlit)
# ----------------------------------------------------

st.title("Simulador de Patio de Contenedores")

st.markdown("""
Este modelo de simulación discreta reproduce la asignación y despacho de contenedores,
analizando el tiempo de espera y la eficiencia operativa en el patio logístico.
""")
st.markdown("---")


# Sección 1: Parámetros de Simulación (Sidebar)
st.header("⚙️ Parámetros de Simulación")

with st.form("parametros_form"):
    
    # Número de Grúas
    numero_gruas = st.slider(
        "Número de Grúas (Recursos de Carga):",
        min_value=1,
        max_value=10,
        value=2,
        step=1
    )
    
    # Probabilidad de Falla
    probabilidad_falla = st.slider(
        "Probabilidad de Falla (Transportista B, 0.0-1.0):",
        min_value=0.0,
        max_value=1.0,
        value=0.25,
        step=0.01
    )
    
    # Tiempo a Simular
    tiempo_simular = st.number_input(
        "Tiempo a Simular (minutos):",
        min_value=60,
        max_value=10000,
        value=480,
        step=60
    )
    
    # Botón de Ejecución
    submitted = st.form_submit_button("▶️ Ejecutar Simulación")

# ------------------ Lógica de Ejecución ------------------

if submitted:
    # Mostrar un spinner mientras se ejecuta la simulación
    with st.spinner('Ejecutando simulación de eventos discretos...'):
        resultados = ejecutar_simulacion(numero_gruas, probabilidad_falla, tiempo_simular)
        
    st.markdown("---")
    st.header("📊 Resultados de la Simulación")

    # Sección 2: Resultados (Métricas principales)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Tiempo Promedio en Patio",
            value=f"{resultados['tiempo_promedio']} min",
            delta=None
        )
        st.caption("Promedio de tiempo que un transportista pasa en el patio.")

    with col2:
        st.metric(
            label="Tiempo Máximo en Patio",
            value=f"{resultados['tiempo_maximo']} min",
            delta=None
        )
        st.caption("El tiempo más largo que un transportista esperó o fue procesado.")

    with col3:
        st.metric(
            label="Camiones Procesados",
            value=f"{resultados['camiones_procesados']} unidades",
            delta=None
        )
        st.caption("Número de transportistas que salieron exitosamente con su carga.")
        
    st.markdown("---")
    
    # Sección 3: Datos de Detalle y Log
    st.subheader("Análisis Detallado")
    
    if TIEMPOS_ESPERA_TOTAL:
        # Crear un DataFrame para estadísticas rápidas
        df_tiempos = pd.DataFrame(TIEMPOS_ESPERA_TOTAL, columns=['Tiempo en Patio (min)'])
        
        st.write("Distribución de Tiempos en Patio:")
        st.bar_chart(df_tiempos)

        with st.expander("Ver estadísticas de tiempo"):
            st.dataframe(df_tiempos.describe())

    # Mostrar el Log de Eventos
    with st.expander("Ver Log Completo de Eventos de la Simulación"):
        st.text_area("Registro de Eventos (Tiempo: Evento)", resultados['log_simulacion'], height=300)