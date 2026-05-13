"""
Módulo de procesamiento y transformación de datos (ETL)
Julian Barbieri - Proyecto Modelo Relacional - 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Dict, Tuple

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Clase para procesar y transformar datos de ventas en modelo relacional.
    """
    
    def __init__(self, input_file: str, encoding: str = "latin-1"):
        """
        Inicializa el procesador de datos.
        
        Args:
            input_file: Ruta del archivo CSV de entrada
            encoding: Codificación del archivo
        """
        self.input_file = input_file
        self.encoding = encoding
        self.df = None
        self.tablas = {}
        
    def cargar_datos(self) -> pd.DataFrame:
        """Carga el archivo CSV."""
        logger.info(f"Cargando datos desde {self.input_file}")
        self.df = pd.read_csv(self.input_file, encoding=self.encoding)
        logger.info(f"Datos cargados: {self.df.shape[0]} filas, {self.df.shape[1]} columnas")
        return self.df
    
    def crear_tabla_ciudades(self) -> pd.DataFrame:
        """Crea tabla de dimensión Ciudades."""
        logger.info("Creando tabla: Ciudades")
        ciudades = self.df['CiudadSucursal'].unique()
        ciudades_df = pd.DataFrame(ciudades, columns=['Ciudad'])
        ciudades_df['CiudadID'] = ciudades_df.index + 1
        ciudades_df = ciudades_df[['CiudadID', 'Ciudad']]
        self.tablas['ciudades'] = ciudades_df
        logger.info(f"  ✓ {len(ciudades_df)} ciudades")
        return ciudades_df
    
    def crear_tabla_sucursales(self, ciudades_df: pd.DataFrame) -> pd.DataFrame:
        """Crea tabla de dimensión Sucursales."""
        logger.info("Creando tabla: Sucursales")
        sucursales = self.df[['SucursalNombre', 'CiudadSucursal']].drop_duplicates().reset_index(drop=True)
        sucursales['SucursalID'] = sucursales.index + 1
        
        sucursales = sucursales.merge(
            ciudades_df,
            left_on='CiudadSucursal',
            right_on='Ciudad',
            how='left'
        )
        sucursales = sucursales[['SucursalID', 'SucursalNombre', 'CiudadID']]
        self.tablas['sucursales'] = sucursales
        logger.info(f"  ✓ {len(sucursales)} sucursales")
        return sucursales
    
    def crear_tabla_productos(self) -> pd.DataFrame:
        """Crea tabla de dimensión Productos."""
        logger.info("Creando tabla: Productos")
        
        # Consolidar productos de 3 columnas
        p1 = self.df[['NombreProducto1', 'MarcaProducto1']].rename(
            columns={'NombreProducto1': 'NombreProducto', 'MarcaProducto1': 'MarcaProducto'}
        )
        p2 = self.df[['NombreProducto2', 'MarcaProducto2']].rename(
            columns={'NombreProducto2': 'NombreProducto', 'MarcaProducto2': 'MarcaProducto'}
        )
        p3 = self.df[['NombreProducto3', 'MarcaProducto3']].rename(
            columns={'NombreProducto3': 'NombreProducto', 'MarcaProducto3': 'MarcaProducto'}
        )
        
        productos = pd.concat([p1, p2, p3], ignore_index=True)
        
        # Limpieza
        productos = productos.dropna(subset=['NombreProducto']).copy()
        productos['NombreProducto'] = productos['NombreProducto'].astype(str).str.strip()
        productos['MarcaProducto'] = productos['MarcaProducto'].astype(str).str.strip()
        productos = productos.drop_duplicates().reset_index(drop=True)
        
        # Crear IDs
        productos['ProductoID'] = productos.index + 1
        productos = productos[['ProductoID', 'NombreProducto', 'MarcaProducto']]
        
        self.tablas['productos'] = productos
        logger.info(f"  ✓ {len(productos)} productos únicos")
        return productos
    
    def crear_tabla_clientes(self) -> pd.DataFrame:
        """Crea tabla de dimensión Clientes."""
        logger.info("Creando tabla: Clientes")
        
        clientes = (
            self.df[[
                'ClienteNombre', 'GeneroCliente', 'EdadCliente',
                'EmailCliente', 'TelefonoCliente', 'DireccionCliente'
            ]]
            .drop_duplicates()
            .reset_index(drop=True)
        )
        
        clientes['ClienteID'] = clientes.index + 1
        clientes = clientes[[
            'ClienteID', 'ClienteNombre', 'GeneroCliente', 'EdadCliente',
            'EmailCliente', 'TelefonoCliente', 'DireccionCliente'
        ]]
        
        self.tablas['clientes'] = clientes
        logger.info(f"  ✓ {len(clientes)} clientes únicos")
        return clientes
    
    def crear_tabla_vendedores(self) -> pd.DataFrame:
        """Crea tabla de dimensión Vendedores."""
        logger.info("Creando tabla: Vendedores")
        
        vendedores = self.df['VendedorNombre'].unique()
        vendedores_df = pd.DataFrame(vendedores, columns=['Vendedor'])
        vendedores_df['VendedorID'] = vendedores_df.index + 1
        vendedores_df = vendedores_df[['VendedorID', 'Vendedor']]
        
        self.tablas['vendedores'] = vendedores_df
        logger.info(f"  ✓ {len(vendedores_df)} vendedores")
        return vendedores_df
    
    def crear_tabla_facturas(
        self, 
        ciudades_df: pd.DataFrame,
        sucursales_df: pd.DataFrame,
        clientes_df: pd.DataFrame,
        vendedores_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Crea tabla de hechos Facturas."""
        logger.info("Creando tabla: Facturas")
        
        # Base de facturas
        facturas = (
            self.df[[
                'VentaID', 'Anio', 'Mes', 'Dia', 'HoraVenta', 'MetodoPago',
                'DescuentoVenta', 'TotalVenta', 'ClienteNombre', 'GeneroCliente',
                'EdadCliente', 'EmailCliente', 'TelefonoCliente', 'DireccionCliente',
                'VendedorNombre', 'SucursalNombre', 'CiudadSucursal'
            ]]
            .drop_duplicates(subset=['VentaID'])
            .reset_index(drop=True)
        )
        
        # Mapeos de IDs
        facturas = facturas.merge(
            clientes_df,
            on=['ClienteNombre', 'GeneroCliente', 'EdadCliente', 'EmailCliente',
                'TelefonoCliente', 'DireccionCliente'],
            how='left'
        )
        
        facturas = facturas.merge(
            vendedores_df,
            left_on='VendedorNombre',
            right_on='Vendedor',
            how='left'
        )
        
        facturas = facturas.merge(
            ciudades_df,
            left_on='CiudadSucursal',
            right_on='Ciudad',
            how='left'
        )
        
        facturas = facturas.merge(
            sucursales_df[['SucursalID', 'SucursalNombre', 'CiudadID']],
            on=['SucursalNombre', 'CiudadID'],
            how='left'
        )
        
        # Selección final
        facturas = facturas.rename(columns={'VentaID': 'FacturaID'})
        facturas = facturas[[
            'FacturaID', 'Dia', 'Mes', 'Anio', 'HoraVenta', 'MetodoPago',
            'SucursalID', 'VendedorID', 'ClienteID', 'DescuentoVenta', 'TotalVenta'
        ]].drop_duplicates().reset_index(drop=True)
        
        self.tablas['facturas'] = facturas
        logger.info(f"  ✓ {len(facturas)} facturas")
        return facturas
    
    def crear_tabla_detalles(self, productos_df: pd.DataFrame) -> pd.DataFrame:
        """Crea tabla de detalles de facturas."""
        logger.info("Creando tabla: DetalleFacturas")
        
        # Consolidar 3 líneas de productos
        detalles = []
        
        for i, nombre_col, marca_col, cant_col, precio_col, subtotal_col in [
            (1, 'NombreProducto1', 'MarcaProducto1', 'CantidadProducto1', 
             'PrecioUnitarioProducto1', 'SubtotalProducto1'),
            (2, 'NombreProducto2', 'MarcaProducto2', 'CantidadProducto2',
             'PrecioUnitarioProducto2', 'SubtotalProducto2'),
            (3, 'NombreProducto3', 'MarcaProducto3', 'CantidadProducto3',
             'PrecioUnitarioProducto3', 'SubtotalProducto3'),
        ]:
            det = self.df[['VentaID', nombre_col, marca_col, cant_col, precio_col, subtotal_col]].copy()
            det.rename(columns={
                'VentaID': 'FacturaID',
                nombre_col: 'NombreProducto',
                marca_col: 'MarcaProducto',
                cant_col: 'Cantidad',
                precio_col: 'PrecioUnitario',
                subtotal_col: 'Subtotal'
            }, inplace=True)
            det['ProductoNro'] = i
            detalles.append(det)
        
        detalle_facturas = pd.concat(detalles, ignore_index=True)
        
        # Limpieza
        detalle_facturas = detalle_facturas.dropna(subset=['NombreProducto']).copy()
        detalle_facturas = detalle_facturas[detalle_facturas['Cantidad'].fillna(0) > 0]
        
        # Mapeo de ProductoID
        detalle_facturas = detalle_facturas.merge(
            productos_df[['ProductoID', 'NombreProducto', 'MarcaProducto']],
            on=['NombreProducto', 'MarcaProducto'],
            how='left'
        )
        
        # Crear IDs
        detalle_facturas = detalle_facturas.reset_index(drop=True)
        detalle_facturas['DetalleID'] = detalle_facturas.index + 1
        
        detalle_facturas = detalle_facturas[[
            'DetalleID', 'FacturaID', 'ProductoNro', 'ProductoID',
            'Cantidad', 'PrecioUnitario', 'Subtotal'
        ]]
        
        self.tablas['detalle_facturas'] = detalle_facturas
        logger.info(f"  ✓ {len(detalle_facturas)} líneas de detalle")
        return detalle_facturas
    
    def procesar_todo(self) -> Dict[str, pd.DataFrame]:
        """Ejecuta todo el flujo de procesamiento."""
        logger.info("=" * 60)
        logger.info("INICIANDO PROCESAMIENTO DE DATOS")
        logger.info("=" * 60)
        
        # Cargar datos
        self.cargar_datos()
        
        # Crear tablas dimensionales
        ciudades = self.crear_tabla_ciudades()
        sucursales = self.crear_tabla_sucursales(ciudades)
        productos = self.crear_tabla_productos()
        clientes = self.crear_tabla_clientes()
        vendedores = self.crear_tabla_vendedores()
        
        # Crear tablas de hechos
        facturas = self.crear_tabla_facturas(ciudades, sucursales, clientes, vendedores)
        detalles = self.crear_tabla_detalles(productos)
        
        logger.info("=" * 60)
        logger.info("✓ PROCESAMIENTO COMPLETADO EXITOSAMENTE")
        logger.info("=" * 60)
        
        return self.tablas
    
    def exportar_excel(self, output_file: str) -> None:
        """Exporta todas las tablas a un archivo Excel."""
        logger.info(f"Exportando a {output_file}")
        
        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            self.tablas['ciudades'].to_excel(writer, sheet_name="Ciudades", index=False)
            self.tablas['sucursales'].to_excel(writer, sheet_name="Sucursales", index=False)
            self.tablas['vendedores'].to_excel(writer, sheet_name="Vendedores", index=False)
            self.tablas['clientes'].to_excel(writer, sheet_name="Clientes", index=False)
            self.tablas['productos'].to_excel(writer, sheet_name="Productos", index=False)
            self.tablas['facturas'].to_excel(writer, sheet_name="Facturas", index=False)
            self.tablas['detalle_facturas'].to_excel(writer, sheet_name="DetalleFacturas", index=False)
        
        logger.info(f"✓ Archivo Excel creado exitosamente")
    
    def exportar_parquet(self, output_dir: str) -> None:
        """Exporta todas las tablas en formato Parquet."""
        logger.info(f"Exportando a Parquet en {output_dir}")
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        for nombre_tabla, df in self.tablas.items():
            filepath = Path(output_dir) / f"{nombre_tabla}.parquet"
            df.to_parquet(filepath, index=False)
            logger.info(f"  ✓ {nombre_tabla}.parquet")


def limpiar_columnas_numericas(df: pd.DataFrame, columnas: list) -> pd.DataFrame:
    """
    Limpia y convierte columnas a tipo numérico.
    
    Args:
        df: DataFrame
        columnas: Lista de nombres de columnas a limpiar
    
    Returns:
        DataFrame con columnas limpias
    """
    df_clean = df.copy()
    
    for col in columnas:
        if col in df_clean.columns:
            df_clean[col] = (
                df_clean[col]
                .astype(str)
                .str.replace(',', '', regex=False)
                .str.replace('$', '', regex=False)
                .str.strip()
            )
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)
    
    return df_clean
