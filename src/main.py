"""
Script de Ejecución Rápida - Proyecto Modelo Relacional
Julian Barbieri

Ejecuta todo el flujo: ETL → Validación → Análisis → Exportación
"""

import sys
from pathlib import Path

# Configuración de rutas
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

# Importaciones
import src.config as config
from src.data_processing import DataProcessor
from src.validation import DataValidator
from src.analysis import DataAnalyzer

def main():
    """Función principal que ejecuta el flujo completo."""
    
    print("\n" + "="*70)
    print("PROYECTO MODELO RELACIONAL - ANÁLISIS DE VENTAS")
    print("="*70 + "\n")
    
    # 1. PROCESAMIENTO (ETL)
    print("🔄 ETAPA 1: PROCESAMIENTO DE DATOS")
    print("-" * 70)
    processor = DataProcessor(str(config.INPUT_FILE), encoding=config.ENCODING)
    tablas = processor.procesar_todo()
    
    # 2. VALIDACIÓN
    print("\n✅ ETAPA 2: VALIDACIÓN DE INTEGRIDAD")
    print("-" * 70)
    validator = DataValidator(tablas)
    es_valido, errores, advertencias = validator.validar_todo()
    
    # 3. ANÁLISIS
    print("\n📊 ETAPA 3: ANÁLISIS Y KPIs")
    print("-" * 70)
    analyzer = DataAnalyzer(tablas)
    kpis = analyzer.ejecutar_analisis_completo()
    
    # 4. RESUMEN EJECUTIVO
    print("\n" + analyzer.obtener_resumen_ejecutivo())
    
    # 5. EXPORTACIÓN
    print("\n💾 ETAPA 4: EXPORTACIÓN DE RESULTADOS")
    print("-" * 70)
    
    # Excel
    processor.exportar_excel(str(config.OUTPUT_EXCEL))
    print(f"✅ Archivo Excel: {config.OUTPUT_EXCEL}")
    
    # KPIs a CSV
    for nombre, df in kpis.items():
        import pandas as pd
        if isinstance(df, pd.DataFrame) and not df.empty:
            csv_path = config.REPORTS_DIR / f"kpi_{nombre}.csv"
            df.to_csv(csv_path, index=False)
            print(f"✅ KPI guardado: {csv_path.name}")
    
    # Resumen
    print("\n" + "="*70)
    print("✅ PROCESAMIENTO COMPLETADO EXITOSAMENTE")
    print("="*70)
    print(f"""
📁 UBICACIONES IMPORTANTES:
  • Datos procesados: {config.OUTPUT_EXCEL}
  • Reportes: {config.REPORTS_DIR}
  • Documentación: {config.BASE_DIR}/README.md
  
📚 DOCUMENTACIÓN:
  • Diccionario de datos: reports/data_dictionary.md
  • Diagrama ER: reports/ER_diagram.md
  
🚀 PRÓXIMOS PASOS:
  1. Revisar README.md para instrucciones detalladas
  2. Ejecutar los notebooks en orden:
     - 01_EDA.ipynb (Análisis Exploratorio)
     - 02_Modelo_Relacional_Profesional.ipynb (Procesamiento)
     - 03_Dashboard_Insights.ipynb (Visualizaciones)
  3. Importar {config.OUTPUT_EXCEL} en Power BI
  4. Crear dashboard interactivo
    """)
    
    return tablas, kpis

if __name__ == "__main__":
    tablas, kpis = main()
