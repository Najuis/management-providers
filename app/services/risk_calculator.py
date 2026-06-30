from app.models.submission_models import RiskLevel
from typing import Optional
import logging

# Configurar logging
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
    
    Args:
        pais_origen_id: ID del país de origen
        ciudad_id: ID de la ciudad
        codigo_ciiu: Código CIIU de la actividad económica
    
    Returns:
        str: Nivel de riesgo ('bajo', 'medio', 'alto', 'extremo')
    
    Example:
        >>> calculate_risk(10, 5, "0111")
        'extremo'
    """
    # Validar parámetros
    if not all([pais_origen_id, ciudad_id, codigo_ciiu]):
        logger.warning("Parámetros incompletos para cálculo de riesgo")
        return RiskLevel.MEDIO.value  # Riesgo por defecto si faltan datos
    
    risk_score = 0.0
    
    # ============================================
    # FACTOR 1: País de origen (40% del riesgo)
    # ============================================
    # TODO: En producción, estos IDs deben venir de una tabla en BD
    # Ejemplo: SELECT id FROM countries WHERE risk_level = 'high'
    high_risk_countries = [10, 20, 30, 40, 50]
    medium_risk_countries = [60, 70, 80]
    
    if pais_origen_id in high_risk_countries:
        risk_score += 0.4
    elif pais_origen_id in medium_risk_countries:
        risk_score += 0.2
    
    # ============================================
    # FACTOR 2: Ciudad (30% del riesgo)
    # ============================================
    # TODO: En producción, estos IDs deben venir de una tabla en BD
    high_risk_cities = [5, 15, 25, 35]
    medium_risk_cities = [45, 55]
    
    if ciudad_id in high_risk_cities:
        risk_score += 0.3
    elif ciudad_id in medium_risk_cities:
        risk_score += 0.15
    
    # ============================================
    # FACTOR 3: Código CIIU (30% del riesgo)
    # ============================================
    # TODO: En producción, estos códigos deben venir de una tabla en BD
    # Actividades de alto riesgo financiero/lavado de activos
    high_risk_ciiu = [
        "0111",  # Cultivo de cereales
        "0112",  # Cultivo de arroz
        "1011",  # Procesamiento de carne
        "4661",  # Comercio al por mayor de combustibles
        "6419",  # Otros intermediarios monetarios
        "6499",  # Otros servicios financieros
        "7010",  # Actividades de consultoría de gestión
    ]
    
    medium_risk_ciiu = [
        "4711",  # Comercio al por menor
        "5210",  # Almacenamiento y depósito
    ]
    
    if codigo_ciiu in high_risk_ciiu:
        risk_score += 0.3
    elif codigo_ciiu in medium_risk_ciiu:
        risk_score += 0.15
    
    # ============================================
    # DETERMINAR NIVEL DE RIESGO
    # ============================================
    risk_level = _determine_risk_level(risk_score)
    
    logger.info(
        f"Riesgo calculado: score={risk_score:.2f}, level={risk_level}, "
        f"pais={pais_origen_id}, ciudad={ciudad_id}, ciiu={codigo_ciiu}"
    )
    
    return risk_level


def _determine_risk_level(score: float) -> str:
    """
    Determinar nivel de riesgo basado en el score calculado.
    
    Umbrales:
    - Extremo: score >= 0.75
    - Alto: score >= 0.50
    - Medio: score >= 0.25
    - Bajo: score < 0.25
    """
    if score >= 0.75:
        return RiskLevel.EXTREME.value
    elif score >= 0.50:
        return RiskLevel.HIGH.value
    elif score >= 0.25:
        return RiskLevel.MEDIUM.value
    else:
        return RiskLevel.LOW.value


def calculate_risk_detailed(
    pais_origen_id: int,
    ciudad_id: int,
    codigo_ciiu: str
) -> dict:
    """
    Calcular riesgo con detalles (para debugging y auditoría).
    
    Returns:
        dict: Diccionario con score, level y factores
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