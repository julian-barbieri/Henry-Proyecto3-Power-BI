# Sales Analytics Pipeline — ETL + Modelo Relacional + Power BI

**Autor:** Julian Barbieri | [julianbarbieri01@gmail.com](mailto:julianbarbieri01@gmail.com)  
**Contexto:** Henry Data Science Bootcamp — Proyecto M3  
**Stack:** Python · Pandas · Power BI · Excel · Jupyter

---

## ¿Qué hace este proyecto?

Pipeline de datos end-to-end que transforma un dataset crudo de ventas en un **modelo relacional normalizado**, valida su integridad de forma automática, calcula **50+ KPIs de negocio** y los expone en un **dashboard interactivo de Power BI**.

El dataset contiene más de **2.000 líneas de transacciones** distribuidas en 7 tablas relacionales, cubriendo clientes, productos, sucursales, vendedores y facturas.

---

## Resultados clave

| Métrica | Valor |
|---|---|
| Tablas generadas | 7 (5 dimensiones + 2 hechos) |
| KPIs computados | 50+ |
| Registros procesados | ~2.000+ líneas de detalle |
| Clientes analizados | 1.200+ |
| Validaciones automáticas | Esquema · Nulos · PKs · FKs · Lógica de negocio |
| Formatos de salida | Excel · Parquet · CSV · Power BI (.pbix) |

---

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Lenguaje | Python 3.10 |
| Transformación | Pandas, NumPy |
| Validación | Lógica propia (DataValidator) |
| Análisis / KPIs | DataAnalyzer con RFM + CLV |
| Visualización | Power BI Desktop |
| Notebooks | Jupyter Lab |
| Formato de salida | Excel (openpyxl), Parquet (pyarrow) |

---

## Arquitectura del pipeline

```
data/raw/ventasTransformed.csv
        │
        ▼
  DataProcessor              ← ETL: normalización + construcción del modelo relacional
        │
        ▼
  DataValidator              ← Integridad referencial, nulos, PKs, lógica de negocio
        │
        ▼
  DataAnalyzer               ← 50+ KPIs: RFM, CLV, tendencias, segmentación
        │
        ├── data/processed/modeloVentas.xlsx
        ├── reports/kpi_*.csv
        └── PowerBI/*.pbix   ← Dashboard interactivo
```

---

## Modelo relacional

```
Ciudades (1) ─────── (N) Sucursales
                           │
Vendedores (1) ──────┐    │
                     ├──── (N) Facturas (1) ─────── (N) DetalleFacturas
Clientes (1) ────────┘                                      │
                                                     (N) Productos
```

Todas las claves son enteros secuenciales; integridad referencial verificada en cada ejecución.

---

## KPIs calculados

**Negocio general**
- Ingresos totales, ticket promedio, cantidad vendida, clientes únicos

**Por dimensión**
- Marca: participación de mercado, ingresos, volumen
- Producto: ranking top 10, desempeño individual
- Sucursal: ingresos por ubicación, eficiencia por vendedor
- Cliente: segmentación RFM (Recency, Frequency, Monetary) y CLV estimado

**Temporales**
- Ingresos mensuales, tendencias anuales, estacionalidad

**Segmentación**
- Clientes VIP vs. regulares · Métodos de pago · Distribución por género y edad

---

## Estructura del proyecto

```
ProyectoM3_JulianBarbieri/
├── src/
│   ├── config.py              # Rutas y parámetros centralizados
│   ├── data_processing.py     # Clase DataProcessor (ETL)
│   ├── validation.py          # Clase DataValidator
│   ├── analysis.py            # Clase DataAnalyzer (KPIs)
│   └── main.py                # Orquestador principal
├── notebooks/
│   ├── 01_EDA.ipynb           # Análisis exploratorio
│   ├── 02_Modelo_Relacional.ipynb
│   └── 03_Dashboard_Insights.ipynb
├── data/
│   ├── raw/                   # CSV original
│   └── processed/             # Excel + Parquet de salida
├── reports/                   # KPI CSVs + diccionario de datos + diagrama ER
├── PowerBI/                   # Archivos .pbix
└── requirements.txt
```

---

## Inicio rápido

```bash
# 1. Crear entorno e instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar el pipeline completo
python src/main.py
```

O ejecutar los notebooks en orden: `01_EDA` → `02_Modelo_Relacional` → `03_Dashboard_Insights`.

---

## Decisiones de diseño

- **Configuración centralizada** en `src/config.py`: cambiar rutas o encoding en un solo lugar.
- **Encoding `latin-1`** en la lectura del CSV: requerido por el dataset fuente; cualquier cambio rompe el loader.
- **IDs enteros secuenciales** (no UUIDs): simplifica los JOINs y es consistente con el modelo estrella de Power BI.
- **Separación ETL / Validación / Análisis** en clases independientes: permite testear y extender cada capa sin acoplar lógica.
