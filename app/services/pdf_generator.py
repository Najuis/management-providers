import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Ruta base para guardar los PDFs generados
UPLOAD_DIR = "app/uploads"

def generate_official_pdf(submission_id: int, form_data: dict, risk_level: str, output_path: str):
    """
    Genera el formato oficial LGB-OFC-F-009 con los datos diligenciados.
    """
    # Asegurar que el directorio exista
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # --- ENCABEZADO ---
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 1 * inch, "FORMATO OFICIAL LGB-OFC-F-009")
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, height - 1.3 * inch, "Declaración Jurada de Proveedor")
    
    # Línea separadora
    c.line(50, height - 1.5 * inch, width - 50, height - 1.5 * inch)
    
    # --- DATOS GENERALES ---
    y_pos = height - 2 * inch
    line_height = 0.3 * inch
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y_pos, f"ID Submission: {submission_id}")
    c.drawString(300, y_pos, f"Fecha Generación: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y_pos -= line_height
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y_pos, "DATOS DEL PROVEEDOR:")
    y_pos -= line_height
    
    c.setFont("Helvetica", 10)
    # Nombre o Razón Social
    nombre = form_data.get("business_name") or f"{form_data.get('first_name', '')} {form_data.get('last_name', '')}"
    c.drawString(50, y_pos, f"Nombre/Razón Social: {nombre}")
    y_pos -= line_height
    
    # Tipo de Persona
    tipo_persona = form_data.get("type_person", "Natural")
    c.drawString(50, y_pos, f"Tipo de Persona: {tipo_persona}")
    y_pos -= line_height
    
    # Documento de Identidad
    doc_id = form_data.get("identification_number", "N/A")
    c.drawString(50, y_pos, f"No. Identificación: {doc_id}")
    y_pos -= line_height * 1.5
    
    # --- DATOS ECONÓMICOS Y RIESGO ---
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y_pos, "INFORMACIÓN DE RIESGO LA/FT:")
    y_pos -= line_height
    
    c.setFont("Helvetica", 10)
    c.drawString(50, y_pos, f"Código CIIU: {form_data.get('ciiu_code', 'N/A')}")
    y_pos -= line_height
    c.drawString(50, y_pos, f"País de Origen: {form_data.get('country_origin', 'N/A')}")
    y_pos -= line_height
    
    # CAJA DE NIVEL DE RIESGO (Destacado)
    c.setFillColorRGB(0.9, 0.9, 0.9) # Gris claro de fondo
    c.rect(40, y_pos - 0.4 * inch, 200, 0.6 * inch, fill=1, stroke=0)
    c.setFillColorRGB(0, 0, 0) # Volver a negro
    
    c.setFont("Helvetica-Bold", 12)
    riesgo_text = f"NIVEL DE RIESGO: {risk_level.upper()}"
    c.drawString(50, y_pos - 0.25 * inch, riesgo_text)
    
    y_pos -= 1.2 * inch
    
    # --- FOOTER / FIRMA ---
    c.line(50, y_pos, 300, y_pos)
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, y_pos - 0.2 * inch, "Firma del Representante Legal")
    
    c.save()
    return output_path