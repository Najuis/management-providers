from app.models.submission_models import RiskLevel
from typing import Optional
import logging

# ✅ CORREGIDO: __name__ en lugar de name
logger = logging.getLogger(__name__)

def calculate_risk(
    pais_origen_id: int,
    ciudad_id: int,
    codigo_ciiu: str
) -> str:
    """
    Calcular nivel de riesgo basado en:
    - País de origen (peso: 40%)
    - Ciudad (peso: 30%)
    - Actividad económica CIIU (peso: 30%)
    """
    # Validar parámetros
    if not all([pais_origen_id, ciudad_id, codigo_ciiu]):
        logger.warning("Parámetros incompletos para cálculo de riesgo")
        return RiskLevel.MEDIO.value  # Riesgo por defecto si faltan datos
    
    risk_score = 0.0
    
    # FACTOR 1: País de origen (40% del riesgo)
    high_risk_countries = [10, 20, 30, 40, 50]
    medium_risk_countries = [60, 70, 80]
    
    if pais_origen_id in high_risk_countries:
        risk_score += 0.4
    elif pais_origen_id in medium_risk_countries:
        risk_score += 0.2
    
    # FACTOR 2: Ciudad (30% del riesgo)
    high_risk_cities = [5, 15, 25, 35]
    medium_risk_cities = [45, 55]
    
    if ciudad_id in high_risk_cities:
        risk_score += 0.3
    elif ciudad_id in medium_risk_cities:
        risk_score += 0.15
    
    # FACTOR 3: Código CIIU (30% del riesgo)
    high_risk_ciiu = ["0111", "0112", "1011", "4661", "6419", "6499", "7010"]
    medium_risk_ciiu = ["4711", "5210"]
    
    if codigo_ciiu in high_risk_ciiu:
        risk_score += 0.3
    elif codigo_ciiu in medium_risk_ciiu:
        risk_score += 0.15
    
    # Determinar nivel de riesgo
    risk_level = _determine_risk_level(risk_score)
    
    logger.info(
        f"Riesgo calculado: score={risk_score:.2f}, level={risk_level}, "
        f"pais={pais_origen_id}, ciudad={ciudad_id}, ciiu={codigo_ciiu}"
    )
    
    return risk_level


def _determine_risk_level(score: float) -> str:
    """
    Determinar nivel de riesgo basado en el score calculado.
    """
    # ✅ CORREGIDO: Usar los valores correctos del enum
    if score >= 0.75:
        return RiskLevel.EXTREMO.value   # ✅ Era EXTREME
    elif score >= 0.50:
        return RiskLevel.ALTO.value      # ✅ Era HIGH
    elif score >= 0.25:
        return RiskLevel.MEDIO.value     # ✅ Era MEDIUM
    else:
        return RiskLevel.BAJO.value      # ✅ Era LOW


def calculate_risk_detailed(
    pais_origen_id: int,
    ciudad_id: int,
    codigo_ciiu: str
) -> dict:
    """
    Calcular riesgo con detalles (para debugging y auditoría).
    """
    risk_score = 0.0
    factors = {
        'pais': 0.0,
        'ciudad': 0.0,
        'ciiu': 0.0
    }
    
    # País
    high_risk_countries = [10, 20, 30, 40, 50]
    if pais_origen_id in high_risk_countries:
        factors['pais'] = 0.4
        risk_score += 0.4
    
    # Ciudad
    high_risk_cities = [5, 15, 25, 35]
    if ciudad_id in high_risk_cities:
        factors['ciudad'] = 0.3
        risk_score += 0.3
    
    # CIIU
    high_risk_ciiu = ["0111", "0112", "1011", "4661", "6419", "6499"]
    if codigo_ciiu in high_risk_ciiu:
        factors['ciiu'] = 0.3
        risk_score += 0.3
    
    return {
        'score': risk_score, 
        'level': _determine_risk_level(risk_score),
        'factors': factors
    }