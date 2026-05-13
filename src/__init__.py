"""
Paquete de procesamiento, validación y análisis de datos
Julian Barbieri - Proyecto Modelo Relacional - 2026
"""

from .data_processing import DataProcessor, limpiar_columnas_numericas
from .validation import DataValidator
from .analysis import DataAnalyzer

__all__ = [
    'DataProcessor',
    'DataValidator',
    'DataAnalyzer',
    'limpiar_columnas_numericas',
]
