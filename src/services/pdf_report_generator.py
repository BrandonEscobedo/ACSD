from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import pandas as pd
import io
from typing import List, Dict
from simulation.simulation import SimuladorContenedores 
from models.simulation_models import LineaTransportista
from datetime import datetime


def generar_reporte_despacho_pdf(contenedor, linea_info: Dict) -> io.BytesIO:
    """
    Genera un reporte PDF para el despacho de carga con información del contenedor y línea de transporte.
    
    Args:
        contenedor: Objeto contenedor con información del contenedor
        linea_info: Diccionario con información de la línea de transporte asignada
    
    Returns:
        Buffer de bytes con el PDF generado
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            topMargin=0.75*inch, leftMargin=1*inch,
                            rightMargin=1*inch, bottomMargin=0.75*inch)
    
    elementos = []
    estilos = getSampleStyleSheet()

    # Título principal
    titulo = Paragraph("REPORTE DE DESPACHO DE CARGA", estilos['h1'])
    elementos.append(titulo)
    elementos.append(Spacer(1, 0.15 * inch))
    
    # Fecha y hora
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    fecha_p = Paragraph(f"<b>Fecha de generación:</b> {fecha_actual}", estilos['Normal'])
    elementos.append(fecha_p)
    elementos.append(Spacer(1, 0.3 * inch))
    
    # Sección: Información del Contenedor
    elementos.append(Paragraph("INFORMACIÓN DEL CONTENEDOR", estilos['h2']))
    elementos.append(Spacer(1, 0.1 * inch))
    
    datos_contenedor = [
        ["Campo", "Valor"],
        ["ID Contenedor", contenedor.id],
        ["Posición en Patio", f"Columna {contenedor.columna}, Piso {contenedor.piso}"],
        ["Estado", contenedor.estado],
        ["Tiempo de Llegada", f"{contenedor.tiempo_llegada:.2f} unidades"],
        ["Posición Actual", contenedor.posicion_actual],
        ["Tipo de Carga", getattr(contenedor, 'carga_tipo', 'N/A') or 'N/A'],
        ["Comprador", getattr(contenedor, 'comprador', 'N/A') or 'N/A'],
        ["Tamaño", f"{getattr(contenedor, 'tamano_pies', 'N/A')} pies"]
    ]
    
    tabla_contenedor = Table(datos_contenedor, colWidths=[2.5*inch, 3.5*inch])
    tabla_contenedor.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#E8F4F8')),
    ]))
    elementos.append(tabla_contenedor)
    elementos.append(Spacer(1, 0.4 * inch))
    
    # Sección: Línea de Transporte Asignada
    elementos.append(Paragraph("LÍNEA DE TRANSPORTE ASIGNADA", estilos['h2']))
    elementos.append(Spacer(1, 0.1 * inch))
    
    datos_linea = [
        ["Campo", "Valor"],
        ["Nombre de Línea", linea_info.get('línea', 'N/A')],
        ["Puntaje", f"{linea_info.get('puntaje', 0):.2f}"],
        ["Cumplimiento", f"{linea_info.get('cumplimiento', 0)}%"],
        ["Lead Time", f"{linea_info.get('lead_time', 0):.1f} horas"],
        ["Contacto", linea_info.get('contacto', 'N/A')]
    ]
    
    tabla_linea = Table(datos_linea, colWidths=[2.5*inch, 3.5*inch])
    tabla_linea.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F18F01')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#FEF6E8')),
    ]))
    elementos.append(tabla_linea)
    elementos.append(Spacer(1, 0.4 * inch))
    
    # Nota final
    nota = Paragraph(
        "<b>Nota:</b> Este documento certifica la asignación de la línea de transporte "
        "para el despacho del contenedor especificado.", 
        estilos['Normal']
    )
    elementos.append(nota)

    doc.build(elementos)
    buffer.seek(0)
    return buffer


def generar_reporte_simulacion_pdf(
    simulador: SimuladorContenedores, 
    lineas_demo: List[LineaTransportista]
) -> io.BytesIO:
    
    # Obtener datos de contenedores y líneas asignadas
    datos_contenedores = []
    for contenedor in simulador.contenedores:
        datos_contenedores.append({
            "Contenedor ID": contenedor.id,
            "Línea Asignada": contenedor.linea_asignada if hasattr(contenedor, 'linea_asignada') else "N/A"
        })
    
    df_contenedores = pd.DataFrame(datos_contenedores)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            topMargin=0.75*inch, leftMargin=1*inch,
                            rightMargin=1*inch, bottomMargin=0.75*inch)
    
    elementos = []
    estilos = getSampleStyleSheet()

    # Título principal
    titulo = Paragraph("REPORTE DE ASIGNACIÓN DE CONTENEDORES", estilos['h1'])
    elementos.append(titulo)
    elementos.append(Spacer(1, 0.25 * inch))
    
    # Tabla de contenedores y líneas asignadas
    elementos.append(Paragraph("## CONTENEDORES Y LÍNEAS DE TRANSPORTE ASIGNADAS", estilos['h2']))
    elementos.append(Spacer(1, 0.1 * inch))

    data_contenedores = [df_contenedores.columns.tolist()] + df_contenedores.values.tolist()
    
    tabla_contenedores = Table(data_contenedores, colWidths=[2.5*inch, 3.5*inch], repeatRows=1)
    tabla_contenedores.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    elementos.append(tabla_contenedores)

    doc.build(elementos)
    buffer.seek(0)
    return buffer
