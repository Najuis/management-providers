from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import os
import json


def generate_official_pdf(data: dict, output_path: str):
    """
    Generar PDF oficial del formulario de vinculación de terceros.
    
    Args:
        data: Diccionario con los datos del formulario
        output_path: Ruta donde se guardará el PDF
    
    Returns:
        str: Ruta del PDF generado
    """
    # Validar datos de entrada
    if not data:
        data = {}
    
    # Crear directorio de salida si no existe
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Configurar documento
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # ============================================
    # ESTILOS PERSONALIZADOS
    # ============================================
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1e40af')
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#64748b')
    )
    
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=12,
        spaceBefore=15,
        spaceAfter=8,
        textColor=colors.HexColor('#1e40af'),
        borderWidth=1,
        borderColor=colors.HexColor('#1e40af'),
        borderPadding=5
    )
    
    # ============================================
    # ENCABEZADO
    # ============================================
    elements.append(Paragraph("FORMULARIO DE VINCULACIÓN DE TERCEROS", title_style))
    elements.append(Paragraph("Mayoreo e Institucional", subtitle_style))
    elements.append(Paragraph("Lagobo Distribuciones S.A.S.", subtitle_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Información del documento
    doc_info = [
        ["Código:", "LGB-OFC-F-008"],
        ["Fecha de generación:", datetime.now().strftime("%d/%m/%Y %H:%M")],
        ["Versión:", "1.0"],
    ]
    doc_table = Table(doc_info, colWidths