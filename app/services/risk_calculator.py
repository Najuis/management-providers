from typing import Dict, Any
from app.models.submission_models import RiskLevel

# Listas de ejemplo para crear y cargar esto desde tu Excel/BD real en producción)
PAISES_ALTO_RIESGO = ["IR", "KP", "SY", "VE", "MM", "AF"] # lo que que comenta Mila Ejemplo simplificado
CIUU_ALTO_RIESGO = ["6419", "6420", "6430", "7010"] # Actividades financieras sensibles
CIUU_MEDIO_RIESGO = ["4610", "4620", "6810"] # Comercio mayorista, bienes raíces

def calculate_risk(form_data: Dict[str, Any]) -> RiskLevel:
    """
    Calcula el nivel de riesgo LA/FT basado en CIIU y País de Origen.
    Recibe el diccionario de datos del formulario.
    """
    ciiu_code = str(form_data.get("ciiu_code", ""))
    country = str(form_data.get("country_origin", "")).upper()
    
    # Lógica de evaluación (Matriz de Riesgo Simplificada)
    # 1. Verificar País de Alto Riesgo
    if country in PAISES_ALTO_RIESGO:
        return RiskLevel.ALTO
    
    # 2. Verificar Actividad Económica (CIIU)
    if ciiu_code in CIUU_ALTO_RIESGO:
        # Si es actividad sensible, verificar si hay otros mitigantes (ej: antigüedad)
        # Por ahora, lo marcamos como ALTO por precaución basado sobre los conceptos de la matriz queb me paso Mila
        return RiskLevel.ALTO
    
    if ciiu_code in CIUU_MEDIO_RIESGO:
        return RiskLevel.MEDIO
    
    # 3. Default: Riesgo Bajo
    return RiskLevel.BAJO