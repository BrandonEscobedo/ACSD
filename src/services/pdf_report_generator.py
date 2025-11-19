from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import pandas as pd
import io
from typing import Dict, List
from simulation.simulation import SimuladorContenedores 
from models.simulation_models import LineaTransportista 

def calcular_metricas_para_reporte(
    sim: SimuladorContenedores, 
    lineas_demo: List[LineaTransportista]
) -> tuple[Dict, pd.DataFrame, pd.DataFrame]:
    
    total_contenedores = len(sim.contenedores)
    contenedores_almacenados = sum(1 for c in sim.contenedores if c.posicion_actual == "PATIO")
    
    kpis = {
        "Contenedores Procesados": total_contenedores,
        "Almacenados en Patio": contenedores_almacenados,
        "Reprogramaciones Totales": 0, 
    }
    
    detalles_lineas = []
    for l in lineas_demo:
        detalles_lineas.append({
            "Línea": l.nombre,
            "Asignaciones": 0,
            "Reprogramaciones": 0,
            "T. Espera Prom. (u)": 0.0,
            "Lead Time Prom. (u)": 0.0,
            "Tasa Cumplimiento Obs.": l.porcentaje_cumplimiento,
            "Puntualidad Declarada": l.porcentaje_puntualidad
        })
    
    df_lineas = pd.DataFrame(detalles_lineas)
    
    eventos_dict = [e.__dict__ for e in sim.eventos]
    df_eventos = pd.DataFrame(eventos_dict)
    
    return kpis, df_lineas, df_eventos

def generar_reporte_simulacion_pdf(
    simulador: SimuladorContenedores, 
    lineas_demo: List[LineaTransportista]
) -> io.BytesIO:
    
    kpis, df_lineas, df_eventos = calcular_metricas_para_reporte(
        simulador, 
        lineas_demo
    )

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            topMargin=0.75*inch, leftMargin=1*inch,
                            rightMargin=1*inch, bottomMargin=0.75*inch)
    
    elementos = []
    estilos = getSampleStyleSheet()

    # Título principal sin emojis
    titulo = Paragraph("REPORTE DE SIMULACIÓN DE ALMACENAMIENTO Y FLUJO", estilos['h1'])
    elementos.append(titulo)
    elementos.append(Spacer(1, 0.25 * inch))
    
    # Encabezado de KPIs sin emojis
    elementos.append(Paragraph("## INDICADORES CLAVE DE RENDIMIENTO (KPIs)", estilos['h2']))
    elementos.append(Spacer(1, 0.1 * inch))
    
    kpi_data = [["Métrica", "Valor"]]
    for k, v in kpis.items():
        kpi_data.append([k, str(v)])
        
    tabla_kpis = Table(kpi_data, colWidths=[2.5*inch, 2.5*inch])
    tabla_kpis.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    elementos.append(tabla_kpis)
    elementos.append(Spacer(1, 0.5 * inch))

    # Encabezado de Líneas Transportistas sin emojis
    elementos.append(Paragraph("## DETALLE DE LÍNEAS TRANSPORTISTAS (DATOS DECLARADOS)", estilos['h2']))
    elementos.append(Spacer(1, 0.1 * inch))

    df_lineas_clean = df_lineas[['Línea', 'Tasa Cumplimiento Obs.', 'Puntualidad Declarada']]
    data_lineas = [df_lineas_clean.columns.tolist()] + df_lineas_clean.values.tolist()
    
    tabla_detalle = Table(data_lineas, colWidths=[2.0*inch, 1.5*inch, 1.5*inch], repeatRows=1)
    tabla_detalle.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F18F01')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    elementos.append(tabla_detalle)
    elementos.append(Spacer(1, 0.5 * inch))

    # Encabezado de Log de Eventos sin emojis
    elementos.append(Paragraph("## LOG DE EVENTOS DE LA SIMULACIÓN", estilos['h2']))
    elementos.append(Spacer(1, 0.1 * inch))

    df_eventos_clean = df_eventos[['tiempo', 'contenedor_id', 'accion', 'origen', 'destino']]
    data_eventos = [df_eventos_clean.columns.tolist()] + df_eventos_clean.values.tolist()

    tabla_eventos = Table(data_eventos, repeatRows=1)
    tabla_eventos.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#A23B72')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
    ]))
    elementos.append(tabla_eventos)

    doc.build(elementos)
    buffer.seek(0)
    return buffer