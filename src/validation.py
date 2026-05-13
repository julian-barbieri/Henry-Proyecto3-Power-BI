"""
Módulo de validación de integridad de datos
Julian Barbieri - Proyecto Modelo Relacional - 2026
"""

import pandas as pd
import logging
from typing import Dict, List, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataValidator:
    """
    Clase para validar la integridad referencial y calidad de datos.
    """
    
    def __init__(self, tablas: Dict[str, pd.DataFrame]):
        """
        Inicializa el validador.
        
        Args:
            tablas: Diccionario con todas las tablas del modelo
        """
        self.tablas = tablas
        self.errores = []
        self.advertencias = []
    
    def validar_todo(self) -> Tuple[bool, List[str], List[str]]:
        """Ejecuta todas las validaciones."""
        logger.info("=" * 60)
        logger.info("INICIANDO VALIDACIONES")
        logger.info("=" * 60)
        
        # Validaciones de estructura
        self.validar_columnas_requeridas()
        self.validar_tipos_datos()
        self.validar_valores_nulos()
        
        # Validaciones de integridad referencial
        self.validar_integridad_sucursales_ciudades()
        self.validar_integridad_facturas()
        self.validar_integridad_detalles()
        
        # Validaciones de datos
        self.validar_valores_negativos()
        self.validar_duplicados()
        
        # Reporte
        self._reportar_resultados()
        
        return len(self.errores) == 0, self.errores, self.advertencias
    
    def validar_columnas_requeridas(self) -> None:
        """Valida que existan las columnas requeridas."""
        logger.info("Validando columnas requeridas...")
        
        columnas_requeridas = {
            'ciudades': ['CiudadID', 'Ciudad'],
            'sucursales': ['SucursalID', 'SucursalNombre', 'CiudadID'],
            'productos': ['ProductoID', 'NombreProducto', 'MarcaProducto'],
            'clientes': ['ClienteID', 'ClienteNombre'],
            'vendedores': ['VendedorID', 'Vendedor'],
            'facturas': ['FacturaID', 'ClienteID', 'VendedorID', 'SucursalID'],
            'detalle_facturas': ['DetalleID', 'FacturaID', 'ProductoID'],
        }
        
        for tabla, columnas in columnas_requeridas.items():
            if tabla not in self.tablas:
                self.errores.append(f"Tabla '{tabla}' no encontrada")
                continue
            
            df = self.tablas[tabla]
            for col in columnas:
                if col not in df.columns:
                    self.errores.append(f"Tabla '{tabla}': columna '{col}' faltante")
    
    def validar_tipos_datos(self) -> None:
        """Valida tipos de datos."""
        logger.info("Validando tipos de datos...")
        
        tipos_esperados = {
            'ciudades': {'CiudadID': 'int64', 'Ciudad': 'object'},
            'sucursales': {'SucursalID': 'int64', 'CiudadID': 'int64'},
            'productos': {'ProductoID': 'int64'},
            'clientes': {'ClienteID': 'int64'},
            'vendedores': {'VendedorID': 'int64'},
            'facturas': {'FacturaID': 'int64', 'ClienteID': 'int64', 'VendedorID': 'int64', 'SucursalID': 'int64'},
            'detalle_facturas': {'DetalleID': 'int64', 'FacturaID': 'int64', 'ProductoID': 'int64'},
        }
        
        for tabla, tipos in tipos_esperados.items():
            if tabla not in self.tablas:
                continue
            
            df = self.tablas[tabla]
            for col, tipo in tipos.items():
                if col in df.columns and str(df[col].dtype) != tipo:
                    self.advertencias.append(
                        f"Tabla '{tabla}': columna '{col}' es {df[col].dtype}, "
                        f"esperaba {tipo}"
                    )
    
    def validar_valores_nulos(self) -> None:
        """Valida valores nulos en columnas críticas."""
        logger.info("Validando valores nulos...")
        
        columnas_criticas = {
            'ciudades': ['CiudadID', 'Ciudad'],
            'productos': ['ProductoID', 'NombreProducto'],
            'clientes': ['ClienteID', 'ClienteNombre'],
            'facturas': ['FacturaID', 'ClienteID', 'VendedorID'],
            'detalle_facturas': ['DetalleID', 'FacturaID', 'ProductoID'],
        }
        
        for tabla, columnas in columnas_criticas.items():
            if tabla not in self.tablas:
                continue
            
            df = self.tablas[tabla]
            for col in columnas:
                if col in df.columns:
                    nulos = df[col].isnull().sum()
                    if nulos > 0:
                        self.errores.append(
                            f"Tabla '{tabla}': {nulos} valores nulos en '{col}'"
                        )
    
    def validar_integridad_sucursales_ciudades(self) -> None:
        """Valida que cada SucursalID tenga un CiudadID válido."""
        logger.info("Validando integridad: Sucursales → Ciudades...")
        
        if 'sucursales' not in self.tablas or 'ciudades' not in self.tablas:
            return
        
        ciudades_validas = set(self.tablas['ciudades']['CiudadID'])
        ciudades_en_sucursales = set(self.tablas['sucursales']['CiudadID'].dropna())
        
        invalidas = ciudades_en_sucursales - ciudades_validas
        if invalidas:
            self.errores.append(
                f"Sucursales: CiudadID inválidos: {invalidas}"
            )
    
    def validar_integridad_facturas(self) -> None:
        """Valida integridad referencial de la tabla Facturas."""
        logger.info("Validando integridad: Facturas...")
        
        if 'facturas' not in self.tablas:
            return
        
        facturas = self.tablas['facturas']
        
        # Validar ClienteID
        if 'clientes' in self.tablas:
            clientes_validos = set(self.tablas['clientes']['ClienteID'])
            clientes_en_facturas = set(facturas['ClienteID'].dropna())
            invalidos = clientes_en_facturas - clientes_validos
            if invalidos:
                self.errores.append(f"Facturas: ClienteID inválidos: {len(invalidos)}")
        
        # Validar VendedorID
        if 'vendedores' in self.tablas:
            vendedores_validos = set(self.tablas['vendedores']['VendedorID'])
            vendedores_en_facturas = set(facturas['VendedorID'].dropna())
            invalidos = vendedores_en_facturas - vendedores_validos
            if invalidos:
                self.errores.append(f"Facturas: VendedorID inválidos: {len(invalidos)}")
        
        # Validar SucursalID
        if 'sucursales' in self.tablas:
            sucursales_validas = set(self.tablas['sucursales']['SucursalID'])
            sucursales_en_facturas = set(facturas['SucursalID'].dropna())
            invalidas = sucursales_en_facturas - sucursales_validas
            if invalidas:
                self.errores.append(f"Facturas: SucursalID inválidos: {len(invalidas)}")
    
    def validar_integridad_detalles(self) -> None:
        """Valida integridad referencial de Detalles."""
        logger.info("Validando integridad: DetalleFacturas...")
        
        if 'detalle_facturas' not in self.tablas:
            return
        
        detalles = self.tablas['detalle_facturas']
        
        # Validar FacturaID
        if 'facturas' in self.tablas:
            facturas_validas = set(self.tablas['facturas']['FacturaID'])
            facturas_en_detalles = set(detalles['FacturaID'].dropna())
            invalidas = facturas_en_detalles - facturas_validas
            if invalidas:
                self.errores.append(f"Detalles: FacturaID inválidos: {len(invalidas)}")
        
        # Validar ProductoID
        if 'productos' in self.tablas:
            productos_validos = set(self.tablas['productos']['ProductoID'])
            productos_en_detalles = set(detalles['ProductoID'].dropna())
            invalidos = productos_en_detalles - productos_validos
            if invalidos:
                self.errores.append(f"Detalles: ProductoID inválidos: {len(invalidos)}")
    
    def validar_valores_negativos(self) -> None:
        """Valida que valores monetarios no sean negativos."""
        logger.info("Validando valores negativos...")
        
        columnas_monetarias = ['Cantidad', 'PrecioUnitario', 'Subtotal', 'TotalVenta']
        
        if 'detalle_facturas' in self.tablas:
            df = self.tablas['detalle_facturas']
            for col in columnas_monetarias:
                if col in df.columns:
                    negativos = (pd.to_numeric(df[col], errors='coerce') < 0).sum()
                    if negativos > 0:
                        self.advertencias.append(
                            f"DetalleFacturas: {negativos} valores negativos en '{col}'"
                        )
        
        if 'facturas' in self.tablas:
            df = self.tablas['facturas']
            if 'TotalVenta' in df.columns:
                negativos = (pd.to_numeric(df['TotalVenta'], errors='coerce') < 0).sum()
                if negativos > 0:
                    self.advertencias.append(f"Facturas: {negativos} valores negativos en 'TotalVenta'")
    
    def validar_duplicados(self) -> None:
        """Valida que no haya registros duplicados en claves primarias."""
        logger.info("Validando registros duplicados...")
        
        claves_primarias = {
            'ciudades': ['CiudadID'],
            'sucursales': ['SucursalID'],
            'productos': ['ProductoID'],
            'clientes': ['ClienteID'],
            'vendedores': ['VendedorID'],
            'facturas': ['FacturaID'],
            'detalle_facturas': ['DetalleID'],
        }
        
        for tabla, columnas in claves_primarias.items():
            if tabla not in self.tablas:
                continue
            
            df = self.tablas[tabla]
            duplicados = df[columnas].duplicated().sum()
            if duplicados > 0:
                self.errores.append(
                    f"Tabla '{tabla}': {duplicados} registros duplicados en clave primaria"
                )
    
    def _reportar_resultados(self) -> None:
        """Reporta los resultados de las validaciones."""
        logger.info("=" * 60)
        logger.info("RESULTADOS DE VALIDACIÓN")
        logger.info("=" * 60)
        
        if not self.errores and not self.advertencias:
            logger.info("✓ Todas las validaciones pasaron correctamente")
        else:
            if self.errores:
                logger.error(f"❌ {len(self.errores)} ERRORES encontrados:")
                for i, error in enumerate(self.errores, 1):
                    logger.error(f"  {i}. {error}")
            
            if self.advertencias:
                logger.warning(f"⚠️  {len(self.advertencias)} ADVERTENCIAS:")
                for i, advertencia in enumerate(self.advertencias, 1):
                    logger.warning(f"  {i}. {advertencia}")
        
        logger.info("=" * 60)
