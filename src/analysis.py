"""
Módulo de análisis y generación de KPIs
Julian Barbieri - Proyecto Modelo Relacional - 2026
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, Tuple
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataAnalyzer:
    """
    Clase para realizar análisis profundo de datos de ventas y generar KPIs.
    """
    
    def __init__(self, tablas: Dict[str, pd.DataFrame]):
        """
        Inicializa el analizador.
        
        Args:
            tablas: Diccionario con todas las tablas del modelo
        """
        self.tablas = tablas
        self.kpis = {}
        self.detalle_facturas_clean = None
        self._preparar_datos()
    
    def _preparar_datos(self) -> None:
        """Prepara los datos para análisis."""
        if 'detalle_facturas' in self.tablas:
            self.detalle_facturas_clean = self.tablas['detalle_facturas'].copy()
            
            # Limpiar columnas numéricas
            for col in ['Cantidad', 'PrecioUnitario', 'Subtotal']:
                if col in self.detalle_facturas_clean.columns:
                    self.detalle_facturas_clean[col] = pd.to_numeric(
                        self.detalle_facturas_clean[col], errors='coerce'
                    ).fillna(0)
    
    def calcular_kpis_generales(self) -> Dict:
        """Calcula KPIs generales del negocio."""
        logger.info("Calculando KPIs generales...")
        
        kpis = {}
        
        if self.detalle_facturas_clean is not None:
            kpis['total_ingresos'] = self.detalle_facturas_clean['Subtotal'].sum()
            kpis['numero_transacciones'] = self.tablas['facturas'].shape[0]
            kpis['ticket_promedio'] = kpis['total_ingresos'] / kpis['numero_transacciones'] if kpis['numero_transacciones'] > 0 else 0
            kpis['cantidad_total_vendida'] = self.detalle_facturas_clean['Cantidad'].sum()
            kpis['numero_clientes_unicos'] = self.tablas['clientes'].shape[0]
            kpis['numero_productos'] = self.tablas['productos'].shape[0]
            kpis['numero_sucursales'] = self.tablas['sucursales'].shape[0]
        
        self.kpis['generales'] = kpis
        return kpis
    
    def calcular_kpis_por_marca(self) -> pd.DataFrame:
        """Calcula KPIs por marca de producto."""
        logger.info("Calculando KPIs por marca...")
        
        if self.detalle_facturas_clean is None:
            return pd.DataFrame()
        
        resultado = (
            self.detalle_facturas_clean
            .merge(
                self.tablas['productos'][['ProductoID', 'MarcaProducto']],
                on='ProductoID',
                how='left'
            )
            .groupby('MarcaProducto', as_index=False)
            .agg(
                ingresos_totales=('Subtotal', 'sum'),
                cantidad_vendida=('Cantidad', 'sum'),
                numero_transacciones=('FacturaID', 'count'),
                precio_promedio=('PrecioUnitario', 'mean'),
                cantidad_promedio=('Cantidad', 'mean'),
            )
            .sort_values('ingresos_totales', ascending=False)
        )
        
        # Calcular participación de mercado
        resultado['participacion_mercado_%'] = (
            resultado['ingresos_totales'] / resultado['ingresos_totales'].sum() * 100
        ).round(2)
        
        self.kpis['por_marca'] = resultado
        return resultado
    
    def calcular_kpis_por_producto(self) -> pd.DataFrame:
        """Calcula KPIs por producto individual."""
        logger.info("Calculando KPIs por producto...")
        
        if self.detalle_facturas_clean is None:
            return pd.DataFrame()
        
        resultado = (
            self.detalle_facturas_clean
            .merge(
                self.tablas['productos'][['ProductoID', 'NombreProducto', 'MarcaProducto']],
                on='ProductoID',
                how='left'
            )
            .groupby(['NombreProducto', 'MarcaProducto'], as_index=False)
            .agg(
                ingresos_totales=('Subtotal', 'sum'),
                cantidad_vendida=('Cantidad', 'sum'),
                numero_transacciones=('FacturaID', 'count'),
                precio_promedio=('PrecioUnitario', 'mean'),
            )
            .sort_values('ingresos_totales', ascending=False)
        )
        
        self.kpis['por_producto'] = resultado
        return resultado
    
    def calcular_kpis_por_sucursal(self) -> pd.DataFrame:
        """Calcula KPIs por sucursal."""
        logger.info("Calculando KPIs por sucursal...")
        
        if 'facturas' not in self.tablas:
            return pd.DataFrame()
        
        resultado = (
            self.tablas['facturas']
            .merge(
                self.tablas['sucursales'][['SucursalID', 'SucursalNombre']],
                on='SucursalID',
                how='left'
            )
            .groupby('SucursalNombre', as_index=False)
            .agg(
                ingresos_totales=('TotalVenta', lambda x: pd.to_numeric(x, errors='coerce').sum()),
                numero_transacciones=('FacturaID', 'count'),
                numero_clientes_unicos=('ClienteID', 'nunique'),
                ticket_promedio=('TotalVenta', lambda x: pd.to_numeric(x, errors='coerce').mean()),
            )
            .sort_values('ingresos_totales', ascending=False)
        )
        
        self.kpis['por_sucursal'] = resultado
        return resultado
    
    def calcular_kpis_por_cliente(self) -> pd.DataFrame:
        """Calcula KPIs por cliente (RFM y CLV)."""
        logger.info("Calculando KPIs por cliente...")
        
        if 'facturas' not in self.tablas:
            return pd.DataFrame()
        
        # Análisis RFM (Recency, Frequency, Monetary)
        resultado = (
            self.tablas['facturas']
            .copy()
            .assign(
                fecha=pd.to_datetime(
                    self.tablas['facturas']['Anio'].astype(str) + '-' +
                    self.tablas['facturas']['Mes'].astype(str).str.zfill(2) + '-' +
                    self.tablas['facturas']['Dia'].astype(str).str.zfill(2),
                    format='%Y-%m-%d',
                    errors='coerce'
                ),
                monto=pd.to_numeric(
                    self.tablas['facturas']['TotalVenta'], errors='coerce'
                )
            )
            .groupby('ClienteID', as_index=False)
            .agg(
                numero_compras=('FacturaID', 'count'),
                ingreso_total=('monto', 'sum'),
                ingreso_promedio=('monto', 'mean'),
                primera_compra=('fecha', 'min'),
                ultima_compra=('fecha', 'max'),
            )
            .merge(
                self.tablas['clientes'][['ClienteID', 'ClienteNombre', 'GeneroCliente', 'EdadCliente']],
                on='ClienteID',
                how='left'
            )
            .sort_values('ingreso_total', ascending=False)
        )
        
        # Calcular recency en días
        fecha_actual = pd.Timestamp.now()
        resultado['dias_desde_ultima_compra'] = (
            fecha_actual - pd.to_datetime(resultado['ultima_compra'])
        ).dt.days
        
        self.kpis['por_cliente'] = resultado
        return resultado
    
    def calcular_kpis_por_vendedor(self) -> pd.DataFrame:
        """Calcula KPIs por vendedor."""
        logger.info("Calculando KPIs por vendedor...")
        
        if 'facturas' not in self.tablas:
            return pd.DataFrame()
        
        resultado = (
            self.tablas['facturas']
            .merge(
                self.tablas['vendedores'][['VendedorID', 'Vendedor']],
                on='VendedorID',
                how='left'
            )
            .groupby('Vendedor', as_index=False)
            .agg(
                ingresos_totales=('TotalVenta', lambda x: pd.to_numeric(x, errors='coerce').sum()),
                numero_transacciones=('FacturaID', 'count'),
                numero_clientes_unicos=('ClienteID', 'nunique'),
                ticket_promedio=('TotalVenta', lambda x: pd.to_numeric(x, errors='coerce').mean()),
            )
            .sort_values('ingresos_totales', ascending=False)
        )
        
        self.kpis['por_vendedor'] = resultado
        return resultado
    
    def calcular_kpis_temporal(self) -> pd.DataFrame:
        """Calcula KPIs por período temporal (mes, trimestre)."""
        logger.info("Calculando KPIs temporal...")
        
        if 'facturas' not in self.tablas:
            return pd.DataFrame()
        
        resultado = (
            self.tablas['facturas']
            .copy()
            .assign(
                periodo=lambda x: x['Anio'].astype(str) + '-' + x['Mes'].astype(str).str.zfill(2)
            )
            .groupby(['Anio', 'Mes', 'periodo'], as_index=False)
            .agg(
                ingresos_totales=('TotalVenta', lambda x: pd.to_numeric(x, errors='coerce').sum()),
                numero_transacciones=('FacturaID', 'count'),
                numero_clientes_unicos=('ClienteID', 'nunique'),
                ticket_promedio=('TotalVenta', lambda x: pd.to_numeric(x, errors='coerce').mean()),
            )
            .sort_values(['Anio', 'Mes'])
        )
        
        self.kpis['temporal'] = resultado
        return resultado
    
    def calcular_kpis_metodo_pago(self) -> pd.DataFrame:
        """Calcula KPIs por método de pago."""
        logger.info("Calculando KPIs por método de pago...")
        
        if 'facturas' not in self.tablas:
            return pd.DataFrame()
        
        resultado = (
            self.tablas['facturas']
            .copy()
            .assign(
                monto=pd.to_numeric(
                    self.tablas['facturas']['TotalVenta'], errors='coerce'
                )
            )
            .groupby('MetodoPago', as_index=False)
            .agg(
                ingresos_totales=('monto', 'sum'),
                numero_transacciones=('FacturaID', 'count'),
                valor_promedio=('monto', 'mean'),
            )
            .sort_values('ingresos_totales', ascending=False)
        )
        
        # Calcular participación
        resultado['participacion_%'] = (
            resultado['ingresos_totales'] / resultado['ingresos_totales'].sum() * 100
        ).round(2)
        
        self.kpis['por_metodo_pago'] = resultado
        return resultado
    
    def analizar_segmentacion_clientes(self) -> Dict:
        """Segmenta clientes por nivel de gasto."""
        logger.info("Analizando segmentación de clientes...")
        
        if 'por_cliente' not in self.kpis or self.kpis['por_cliente'].empty:
            return {}
        
        clientes_df = self.kpis['por_cliente'].copy()
        
        # Definir segmentos por deciles de gasto
        try:
            clientes_df['segmento'] = pd.qcut(
                clientes_df['ingreso_total'],
                q=4,
                labels=['Bajo', 'Medio', 'Alto', 'VIP'],
                duplicates='drop'
            )
        except ValueError:
            # Si hay duplicados y los labels no coinciden, usar labels automáticos
            clientes_df['segmento'] = pd.qcut(
                clientes_df['ingreso_total'],
                q=4,
                duplicates='drop'
            )
        
        segmentacion = (
            clientes_df
            .groupby('segmento', as_index=False)
            .agg(
                numero_clientes=('ClienteID', 'count'),
                ingreso_total=('ingreso_total', 'sum'),
                ingreso_promedio=('ingreso_total', 'mean'),
                numero_compras_promedio=('numero_compras', 'mean'),
            )
        )
        
        self.kpis['segmentacion_clientes'] = segmentacion
        return segmentacion.to_dict('records')
    
    def ejecutar_analisis_completo(self) -> Dict:
        """Ejecuta todos los análisis."""
        logger.info("=" * 60)
        logger.info("INICIANDO ANÁLISIS COMPLETO")
        logger.info("=" * 60)
        
        self.calcular_kpis_generales()
        self.calcular_kpis_por_marca()
        self.calcular_kpis_por_producto()
        self.calcular_kpis_por_sucursal()
        self.calcular_kpis_por_cliente()
        self.calcular_kpis_por_vendedor()
        self.calcular_kpis_temporal()
        self.calcular_kpis_metodo_pago()
        self.analizar_segmentacion_clientes()
        
        logger.info("=" * 60)
        logger.info("✓ ANÁLISIS COMPLETADO")
        logger.info("=" * 60)
        
        return self.kpis
    
    def obtener_resumen_ejecutivo(self) -> str:
        """Genera un resumen ejecutivo textual."""
        resumen = "\n" + "=" * 70 + "\n"
        resumen += "RESUMEN EJECUTIVO - ANÁLISIS DE VENTAS\n"
        resumen += "=" * 70 + "\n\n"
        
        if 'generales' in self.kpis:
            kpis = self.kpis['generales']
            resumen += "📊 KPIs GENERALES:\n"
            resumen += f"  • Ingresos Totales: ${kpis.get('total_ingresos', 0):,.2f}\n"
            resumen += f"  • Número de Transacciones: {kpis.get('numero_transacciones', 0):,}\n"
            resumen += f"  • Ticket Promedio: ${kpis.get('ticket_promedio', 0):,.2f}\n"
            resumen += f"  • Cantidad Total Vendida: {kpis.get('cantidad_total_vendida', 0):,.0f} unidades\n"
            resumen += f"  • Clientes Únicos: {kpis.get('numero_clientes_unicos', 0):,}\n"
            resumen += f"  • Productos: {kpis.get('numero_productos', 0):,}\n"
            resumen += f"  • Sucursales: {kpis.get('numero_sucursales', 0):,}\n\n"
        
        if 'por_marca' in self.kpis and not self.kpis['por_marca'].empty:
            top_marca = self.kpis['por_marca'].iloc[0]
            resumen += "🏆 MARCA LÍDER:\n"
            resumen += f"  • {top_marca['MarcaProducto']}: ${top_marca['ingresos_totales']:,.2f}\n"
            resumen += f"  • Participación: {top_marca['participacion_mercado_%']}%\n\n"
        
        if 'por_producto' in self.kpis and not self.kpis['por_producto'].empty:
            top_prod = self.kpis['por_producto'].iloc[0]
            resumen += "⭐ PRODUCTO TOP:\n"
            resumen += f"  • {top_prod['NombreProducto']}: ${top_prod['ingresos_totales']:,.2f}\n\n"
        
        if 'por_sucursal' in self.kpis and not self.kpis['por_sucursal'].empty:
            top_suc = self.kpis['por_sucursal'].iloc[0]
            resumen += "🏪 SUCURSAL LÍDER:\n"
            resumen += f"  • {top_suc['SucursalNombre']}: ${top_suc['ingresos_totales']:,.2f}\n\n"
        
        resumen += "=" * 70 + "\n"
        
        return resumen
