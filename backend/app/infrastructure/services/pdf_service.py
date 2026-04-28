import io
from datetime import datetime
from typing import Dict

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.domain.contenedor import Contenedor


class PDFService:
    def generar_reporte_despacho(self, contenedor: Contenedor, linea_info: Dict) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            topMargin=0.75 * inch,
            leftMargin=1 * inch,
            rightMargin=1 * inch,
            bottomMargin=0.75 * inch,
        )
        estilos = getSampleStyleSheet()
        elementos = []

        elementos.append(Paragraph("REPORTE DE DESPACHO DE CARGA", estilos["h1"]))
        elementos.append(Spacer(1, 0.15 * inch))
        elementos.append(
            Paragraph(
                f"<b>Fecha de generación:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                estilos["Normal"],
            )
        )
        elementos.append(Spacer(1, 0.3 * inch))

        elementos.append(Paragraph("INFORMACIÓN DEL CONTENEDOR", estilos["h2"]))
        elementos.append(Spacer(1, 0.1 * inch))

        carga_valor = (
            contenedor.carga_tipo.value
            if hasattr(contenedor.carga_tipo, "value")
            else str(contenedor.carga_tipo)
        )
        datos_contenedor = [
            ["Campo", "Valor"],
            ["ID Contenedor", contenedor.id],
            ["Posición en Patio", f"Columna {contenedor.columna}, Piso {contenedor.piso}"],
            ["Estado", contenedor.estado],
            ["Tiempo de Llegada", f"{contenedor.tiempo_llegada:.2f} unidades"],
            ["Tipo de Carga", carga_valor],
            ["Comprador", contenedor.comprador or "N/A"],
            ["Tamaño", f"{contenedor.tamano_pies} pies"],
        ]

        tabla_contenedor = Table(datos_contenedor, colWidths=[2.5 * inch, 3.5 * inch])
        tabla_contenedor.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E86AB")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#E8F4F8")),
                ]
            )
        )
        elementos.append(tabla_contenedor)
        elementos.append(Spacer(1, 0.4 * inch))

        elementos.append(Paragraph("LÍNEA DE TRANSPORTE ASIGNADA", estilos["h2"]))
        elementos.append(Spacer(1, 0.1 * inch))

        datos_linea = [
            ["Campo", "Valor"],
            ["Nombre de Línea", linea_info.get("línea", "N/A")],
            ["Puntaje", f"{linea_info.get('puntaje', 0):.2f}"],
            ["Cumplimiento", f"{linea_info.get('cumplimiento', 0)}%"],
            ["Lead Time", f"{linea_info.get('lead_time', 0):.1f} horas"],
            ["Contacto", linea_info.get("contacto", "N/A")],
        ]

        tabla_linea = Table(datos_linea, colWidths=[2.5 * inch, 3.5 * inch])
        tabla_linea.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F18F01")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#FEF6E8")),
                ]
            )
        )
        elementos.append(tabla_linea)
        elementos.append(Spacer(1, 0.4 * inch))

        elementos.append(
            Paragraph(
                "<b>Nota:</b> Este documento certifica la asignación de la línea de transporte "
                "para el despacho del contenedor especificado.",
                estilos["Normal"],
            )
        )

        doc.build(elementos)
        buffer.seek(0)
        return buffer.read()
