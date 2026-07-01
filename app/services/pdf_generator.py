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
    doc_table = Table(doc_info, colWidths=[2*inch, 3*inch])
    doc_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e2e8f0')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(doc_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # ============================================
    # SECCIÓN 1: INFORMACIÓN GENERAL
    # ============================================
    elements.append(Paragraph("1. INFORMACIÓN GENERAL", section_style))
    general_data = [
        ["Campo", "Valor"],
        ["Fecha", str(data.get('fecha', ''))],
        ["Tipo de Cliente", data.get('tipo_cliente', '')],
        ["Tipo de Vinculación", data.get('tipo_vinculacion', '')],
        ["Ciudad", str(data.get('ciudad_id', ''))],
        ["Oficina/Almacén", data.get('oficina', '')],
        ["Tipo de Persona", data.get('tipo_persona', '')],
    ]
    
    table = Table(general_data, colWidths=[2.5*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.2*inch))
    
    # ============================================
    # SECCIÓN 2: INFORMACIÓN DE IDENTIFICACIÓN
    # ============================================
    elements.append(Paragraph("2. INFORMACIÓN DE IDENTIFICACIÓN", section_style))
    id_data = [
        ["Campo", "Valor"],
        ["Tipo de Persona", data.get('tipo_persona', '')],
        ["Nombres", data.get('nombres', '')],
        ["Apellidos", data.get('apellidos', '')],
        ["Razón Social", data.get('razon_social', '')],
        ["Tipo de Identificación", data.get('tipo_id', '')],
        ["Número de Identificación", data.get('numero_id', '')],
        ["Fecha de Expedición", str(data.get('fecha_expedicion', ''))],
        ["Estructura Jurídica", data.get('estructura_juridica', '')],
    ]
    
    table2 = Table(id_data, colWidths=[2.5*inch, 4*inch])
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    elements.append(table2)
    elements.append(Spacer(1, 0.2*inch))
    
    # ============================================
    # SECCIÓN 3: ACTIVIDAD ECONÓMICA
    # ============================================
    elements.append(Paragraph("3. ACTIVIDAD ECONÓMICA Y RIESGO", section_style))
    economic_data = [
        ["Campo", "Valor"],
        ["Código CIIU", data.get('codigo_ciiu', '')],
        ["País de Origen", str(data.get('pais_origen_id', ''))],
        ["País de Residencia", str(data.get('pais_residencia_id', ''))],
        ["Zona", data.get('zona', '')],
        ["Nivel de Riesgo", data.get('risk_level', 'No calculado')],
    ]
    
    table3 = Table(economic_data, colWidths=[2.5*inch, 4*inch])
    table3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    elements.append(table3)
    elements.append(Spacer(1, 0.2*inch))
    
    # ============================================
    # SECCIÓN 4: INFORMACIÓN FINANCIERA
    # ============================================
    elements.append(Paragraph("4. INFORMACIÓN FINANCIERA Y TRIBUTARIA", section_style))
    financial_data = [
        ["Campo", "Valor"],
        ["Régimen Tributario", data.get('regimen_tributario', '')],
        ["Total Ingresos", f"${data.get('total_ingresos', 0):,.2f}" if data.get('total_ingresos') else "N/A"],
        ["Total Egresos", f"${data.get('total_egresos', 0):,.2f}" if data.get('total_egresos') else "N/A"],
    ]
    
    table4 = Table(financial_data, colWidths=[2.5*inch, 4*inch])
    table4.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    elements.append(table4)
    elements.append(Spacer(1, 0.2*inch))
    
    # ============================================
    # SECCIÓN 5: AUTORIZACIONES
    # ============================================
    elements.append(Paragraph("5. AUTORIZACIONES Y DECLARACIONES", section_style))
    
    auth_style = ParagraphStyle(
        'AuthText',
        parent=styles['Normal'],
        fontSize=9,
        leftIndent=20,
        spaceAfter=5
    )
    
    auth_items = [
        ("✓", "Autorizo el manejo de mi información según Ley 1581 de 2012"),
        ("✓" if data.get('aut_datos') else "☐", "Autorizo el manejo de datos personales"),
        ("✓" if data.get('aut_laft') else "☐", "Declaro cumplimiento con la Política LAFT/FPADM"),
        ("✓" if data.get('aut_anticorrupcion') else "", "Me adhiero a la Política Anticorrupción y Antisoborno"),
        ("✓" if data.get('aut_etica') else "", "Me adhiero a la Política de Transparencia y Ética Empresarial"),
    ]
    
    for check, text in auth_items:
        elements.append(Paragraph(f"{check}  {text}", auth_style))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # ============================================
    # PIE DE PÁGINA
    # ============================================
    elements.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    elements.append(Paragraph("Documento generado automáticamente por el Sistema de Gestión de Proveedores", footer_style))
    elements.append(Paragraph("Lagobo Distribuciones S.A.S. - Todos los derechos reservados", footer_style))
    
    # ============================================
    # GENERAR PDF
    # ============================================
    try:
        doc.build(elements)
        return output_path
    except Exception as e:
        raise Exception(f"Error al generar el PDF: {str(e)}")


def generate_status_pdf(submission_data: dict, output_path: str):
    """
    Generar PDF de estado de solicitud (para confirmación)
    """
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1e40af')
    )
    
    elements.append(Paragraph("CONFIRMACIÓN DE SOLICITUD", title_style))
    elements.append(Spacer(1, 0.5*inch))
    
    status_data = [
        ["Campo", "Valor"],
        ["ID de Solicitud", str(submission_data.get('id', ''))],
        ["Estado", submission_data.get('status', 'Pendiente')],
        ["Nivel de Riesgo", submission_data.get('risk_level', 'No calculado')],
        ["Fecha de envío", str(submission_data.get('submitted_at', datetime.now()))],
    ]
    
    table = Table(status_data, colWidths=[2.5*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    elements.append(table)
    
    doc.build(elements)
    return output_path