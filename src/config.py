"""
Configuración centralizada del proyecto
Julian Barbieri - Proyecto Modelo Relacional - 2026
"""

import os
from pathlib import Path

# Rutas del proyecto
BASE_DIR = Path(__file__).parent.parent  # Raíz del proyecto
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REPORTS_DIR = BASE_DIR / "reports"
SRC_DIR = BASE_DIR / "src"

# Archivos de entrada/salida
INPUT_FILE = PROCESSED_DATA_DIR / "ventasTransformed.csv"
OUTPUT_EXCEL = PROCESSED_DATA_DIR / "modeloVentas.xlsx"
OUTPUT_PARQUET = PROCESSED_DATA_DIR / "modeloVentas.parquet"

# Encoding
ENCODING = "latin-1"

# Configuración de pandas/display
PANDAS_DISPLAY_OPTIONS = {
    'display.max_columns': None,
    'display.max_rows': 100,
    'display.width': None,
    'display.max_colwidth': None,
}

# Tablas del modelo relacional
DIMENSION_TABLES = ['ciudades', 'sucursales', 'vendedores', 'clientes', 'productos']
FACT_TABLES = ['facturas', 'detalle_facturas']

# Configuración de validación
NUMERIC_COLUMNS = ['Cantidad', 'PrecioUnitario', 'Subtotal']
REQUIRED_COLUMNS = {
    'ciudades': ['CiudadID', 'Ciudad'],
    'sucursales': ['SucursalID', 'SucursalNombre', 'CiudadID'],
    'productos': ['ProductoID', 'NombreProducto', 'MarcaProducto'],
    'clientes': ['ClienteID', 'ClienteNombre'],
    'vendedores': ['VendedorID', 'Vendedor'],
    'facturas': ['FacturaID', 'ClienteID', 'VendedorID', 'SucursalID'],
    'detalle_facturas': ['DetalleID', 'FacturaID', 'ProductoID'],
}

# Análisis y reportes
FIGSIZE_DEFAULT = (12, 6)
FIGSIZE_LARGE = (16, 10)
DCOLOR_PALETTE = "Set2"
