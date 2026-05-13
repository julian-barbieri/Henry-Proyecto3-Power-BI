# Diccionario de Datos - Proyecto Modelo Relacional

**Documento:** Diccionario de Datos Completo  
**Autor:** Julian Barbieri  
**Fecha:** Mayo 2026  
**Versión:** 1.0

---

## 📑 Tabla de Contenidos

1. [Tablas Dimensionales](#tablas-dimensionales)
2. [Tablas de Hechos](#tablas-de-hechos)
3. [Convenciones de Nomenclatura](#convenciones)
4. [Tipos de Datos](#tipos-de-datos)
5. [Relaciones](#relaciones)
6. [Restricciones](#restricciones)

---

## <a name="tablas-dimensionales"></a>Tablas Dimensionales

### 1. CIUDADES

**Descripción:** Ubicaciones geográficas donde operan las sucursales.

**Clave Primaria:** `CiudadID`

| Campo    | Tipo         | Nulo | Descripción         | Rango/Validación |
| -------- | ------------ | ---- | ------------------- | ---------------- |
| CiudadID | INT          | NO   | ID único de ciudad  | 1-100            |
| Ciudad   | VARCHAR(100) | NO   | Nombre de la ciudad | Texto único      |

**Ejemplos:**

- Bogotá
- Medellín
- Cali
- Pereira

---

### 2. SUCURSALES

**Descripción:** Puntos de venta ubicados en diferentes ciudades.

**Clave Primaria:** `SucursalID`  
**Clave Foránea:** `CiudadID` → `Ciudades.CiudadID`

| Campo          | Tipo         | Nulo | Descripción          | Rango/Validación         |
| -------------- | ------------ | ---- | -------------------- | ------------------------ |
| SucursalID     | INT          | NO   | ID único de sucursal | 1-100                    |
| SucursalNombre | VARCHAR(100) | NO   | Nombre descriptivo   | Texto único              |
| CiudadID       | INT          | NO   | Referencia a ciudad  | Debe existir en Ciudades |

**Ejemplos:**

- Techcore Bogotá #1
- Techcore Medellín #2
- Techcore Cali

---

### 3. PRODUCTOS

**Descripción:** Catálogo de productos disponibles para venta (laptops y accesorios).

**Clave Primaria:** `ProductoID`

| Campo          | Tipo         | Nulo | Descripción          | Rango/Validación |
| -------------- | ------------ | ---- | -------------------- | ---------------- |
| ProductoID     | INT          | NO   | ID único de producto | 1-1000           |
| NombreProducto | VARCHAR(150) | NO   | Nombre del producto  | Texto único      |
| MarcaProducto  | VARCHAR(100) | NO   | Marca del fabricante | Texto            |

**Ejemplos:**

- Apple MacBook Pro 16 (Apple)
- Dell XPS 13 (Dell)
- Lenovo ThinkPad X1 Carbon (Lenovo)
- HP Spectre x360 (HP)

**Marcas disponibles:**
Apple, Dell, Lenovo, HP, Asus, MSI, Samsung, Acer, Microsoft

---

### 4. CLIENTES

**Descripción:** Base de clientes que realizan compras.

**Clave Primaria:** `ClienteID`

| Campo            | Tipo         | Nulo | Descripción          | Rango/Validación                |
| ---------------- | ------------ | ---- | -------------------- | ------------------------------- |
| ClienteID        | INT          | NO   | ID único de cliente  | 1-10000                         |
| ClienteNombre    | VARCHAR(150) | NO   | Nombre completo      | Texto                           |
| GeneroCliente    | CHAR(1)      | SÍ   | Género del cliente   | 'M' = Masculino, 'F' = Femenino |
| EdadCliente      | INT          | SÍ   | Edad en años         | 18-100                          |
| EmailCliente     | VARCHAR(150) | SÍ   | Email para contacto  | Formato email válido            |
| TelefonoCliente  | VARCHAR(20)  | SÍ   | Teléfono de contacto | Formato internacional           |
| DireccionCliente | VARCHAR(200) | SÍ   | Domicilio            | Texto                           |

**Notas:**

- Email puede estar vacío en algunos registros
- Edad es aproximada en ciertos casos
- Algunos clientes no tienen datos de contacto completos

---

### 5. VENDEDORES

**Descripción:** Personal de ventas que realiza las transacciones.

**Clave Primaria:** `VendedorID`

| Campo      | Tipo         | Nulo | Descripción          | Rango/Validación |
| ---------- | ------------ | ---- | -------------------- | ---------------- |
| VendedorID | INT          | NO   | ID único de vendedor | 1-100            |
| Vendedor   | VARCHAR(150) | NO   | Nombre del vendedor  | Texto único      |

---

## <a name="tablas-de-hechos"></a>Tablas de Hechos

### 6. FACTURAS

**Descripción:** Transacciones de ventas (cabecera).

**Clave Primaria:** `FacturaID`  
**Claves Foráneas:**

- `ClienteID` → `Clientes.ClienteID`
- `VendedorID` → `Vendedores.VendedorID`
- `SucursalID` → `Sucursales.SucursalID`

| Campo          | Tipo          | Nulo | Descripción             | Rango/Validación                                                                             |
| -------------- | ------------- | ---- | ----------------------- | -------------------------------------------------------------------------------------------- |
| FacturaID      | INT           | NO   | ID único de factura     | 1-100000                                                                                     |
| Dia            | INT           | NO   | Día del mes             | 1-31                                                                                         |
| Mes            | INT           | NO   | Mes del año             | 1-12                                                                                         |
| Anio           | INT           | NO   | Año de venta            | 2014-2025                                                                                    |
| HoraVenta      | TIME          | SÍ   | Hora de la transacción  | HH:MM:SS                                                                                     |
| MetodoPago     | VARCHAR(50)   | SÍ   | Forma de pago           | Tarjeta Crédito, Tarjeta Débito, Efectivo, Transferencia, Billetera Digital, No especificado |
| SucursalID     | INT           | NO   | ID de sucursal          | Debe existir en Sucursales                                                                   |
| VendedorID     | INT           | NO   | ID de vendedor          | Debe existir en Vendedores                                                                   |
| ClienteID      | INT           | NO   | ID de cliente           | Debe existir en Clientes                                                                     |
| DescuentoVenta | DECIMAL(5,2)  | SÍ   | % de descuento aplicado | 0-100                                                                                        |
| TotalVenta     | DECIMAL(15,2) | NO   | Monto total de la venta | > 0                                                                                          |

**Notas:**

- TotalVenta es la suma de subtotales menos descuentos
- MetodoPago puede estar vacío
- Fecha completa se forma con Dia, Mes, Anio

---

### 7. DETALLEFACTURAS

**Descripción:** Línea de productos vendidos por factura (detalles de transacciones).

**Clave Primaria:** `DetalleID`  
**Claves Foráneas:**

- `FacturaID` → `Facturas.FacturaID`
- `ProductoID` → `Productos.ProductoID`

| Campo          | Tipo          | Nulo | Descripción                | Rango/Validación          |
| -------------- | ------------- | ---- | -------------------------- | ------------------------- |
| DetalleID      | INT           | NO   | ID único de línea          | 1-1000000                 |
| FacturaID      | INT           | NO   | ID de factura padre        | Debe existir en Facturas  |
| ProductoNro    | INT           | NO   | Número de línea en factura | 1-3                       |
| ProductoID     | INT           | NO   | ID de producto             | Debe existir en Productos |
| Cantidad       | INT           | NO   | Unidades vendidas          | > 0                       |
| PrecioUnitario | DECIMAL(15,2) | NO   | Precio por unidad          | > 0                       |
| Subtotal       | DECIMAL(15,2) | NO   | Cantidad × PrecioUnitario  | > 0                       |

**Notas:**

- Una factura puede tener de 1 a 3 líneas de productos
- ProductoNro indica el orden dentro de la factura
- Subtotal es calculado: Cantidad × PrecioUnitario

---

## <a name="convenciones"></a>Convenciones de Nomenclatura

### Tablas

- **Singular en inglés:** `Factura` → `facturas`
- **Plural para tablas:** `clientes`, `productos`, `vendedores`
- **Sin prefijos innecesarios:** No usar `tbl_` o `tb_`

### Columnas

- **PascalCase:** `ClienteNombre`, `SucursalID`, `TotalVenta`
- **IDs siempre al final:** `XxxID` donde Xxx es el nombre de la tabla
- **Métodos de pago:** `MetodoPago` (no `PaymentMethod`)

### Claves

- **Primaria (PK):** `{Tabla}ID` (e.j., `ClienteID`)
- **Foránea (FK):** Mismo nombre que en tabla referenciada

---

## <a name="tipos-de-datos"></a>Tipos de Datos

| Tipo SQL      | Python/Pandas | Rango                          | Uso                   |
| ------------- | ------------- | ------------------------------ | --------------------- |
| INT           | int64         | -2,147,483,648 a 2,147,483,647 | IDs, cantidades, años |
| DECIMAL(15,2) | float64       | Hasta 15 dígitos, 2 decimales  | Moneda                |
| VARCHAR(n)    | object        | Hasta n caracteres             | Texto                 |
| CHAR(1)       | object        | Exactamente 1 carácter         | Género, tipo          |
| DATE          | datetime64    | Rango de fechas SQL            | Fechas                |
| TIME          | object        | HH:MM:SS                       | Horas                 |
| NUMERIC(5,2)  | float64       | Porcentajes                    | Descuentos, impuestos |

---

## <a name="relaciones"></a>Relaciones

### Diagrama de Relaciones

```
┌──────────────┐
│   CIUDADES   │
│  (PK: CiudadID)
└──────┬───────┘
       │ 1
       │
       │ N
┌──────▼───────────┐
│  SUCURSALES      │
│ (PK: SucursalID) │
│ (FK: CiudadID)   │
└──────┬───────────┘
       │ 1
       │
       ├─────────────────────┐
       │ N                   │
       │                     │
    ┌──▼─────────────┐   ┌──────────────┐
    │   FACTURAS     │   │  VENDEDORES  │
    │ (PK: FacturaID)├──→│(PK: VendedorID)
    │ (FK: SucursalID) │
    │ (FK: VendedorID) │
    │ (FK: ClienteID)  │
    └──┬──────────────┘
       │ 1            ┌──────────────┐
       │              │  CLIENTES    │
       │             │(PK: ClienteID)
       │              └──────────────┘
       │ N
       │
┌──────▼─────────────────┐
│ DETALLEFACTURAS        │
│ (PK: DetalleID)        │
│ (FK: FacturaID)        │
│ (FK: ProductoID)       │
└────────┬───────────────┘
         │ N
         │
         │ 1
      ┌──▼───────────┐
      │  PRODUCTOS   │
      │(PK: ProductoID)
      └──────────────┘
```

### Cardinalidad

| Relación                    | Tipo | Descripción                             |
| --------------------------- | ---- | --------------------------------------- |
| Ciudades → Sucursales       | 1:N  | Una ciudad tiene múltiples sucursales   |
| Sucursales → Facturas       | 1:N  | Una sucursal procesa múltiples facturas |
| Vendedores → Facturas       | 1:N  | Un vendedor realiza múltiples facturas  |
| Clientes → Facturas         | 1:N  | Un cliente realiza múltiples compras    |
| Facturas → DetalleFacturas  | 1:N  | Una factura tiene múltiples líneas      |
| Productos → DetalleFacturas | 1:N  | Un producto aparece en múltiples líneas |

---

## <a name="restricciones"></a>Restricciones y Validaciones

### Restricciones de Integridad

1. **Valores No Nulos (NOT NULL):**
   - Todas las claves primarias y foráneas
   - NombreProducto, MarcaProducto
   - ClienteNombre
   - SucursalNombre, Ciudad
   - Cantidad, PrecioUnitario, Subtotal
   - TotalVenta

2. **Valores Positivos:**
   - Cantidad > 0
   - PrecioUnitario > 0
   - Subtotal > 0
   - TotalVenta > 0

3. **Únicos (UNIQUE):**
   - CiudadID (en Ciudades)
   - SucursalID (en Sucursales)
   - ProductoID (en Productos)
   - ClienteID (en Clientes)
   - VendedorID (en Vendedores)
   - FacturaID (en Facturas)
   - DetalleID (en DetalleFacturas)

4. **Integridad Referencial:**
   - CiudadID en Sucursales debe existir en Ciudades
   - SucursalID en Facturas debe existir en Sucursales
   - VendedorID en Facturas debe existir en Vendedores
   - ClienteID en Facturas debe existir en Clientes
   - FacturaID en DetalleFacturas debe existir en Facturas
   - ProductoID en DetalleFacturas debe existir en Productos

### Validaciones Lógicas

1. **Fecha válida:** 1 ≤ Día ≤ 31, 1 ≤ Mes ≤ 12
2. **Año válido:** 2014 ≤ Año ≤ 2025
3. **Descuento válido:** 0 ≤ DescuentoVenta ≤ 100
4. **Edad válida:** 18 ≤ EdadCliente ≤ 120
5. **Cálculo consistente:** Subtotal = Cantidad × PrecioUnitario

---

## 📊 Estadísticas

| Métrica    | Valor     | Notas                                 |
| ---------- | --------- | ------------------------------------- |
| Ciudades   | 5         | Bogotá, Medellín, Cali, Pereira, etc. |
| Sucursales | 7         | 1-2 sucursales por ciudad             |
| Vendedores | 18        | Personal activo                       |
| Clientes   | 1,200+    | Base histórica                        |
| Productos  | 40+       | Marcas variadas                       |
| Facturas   | 1,000+    | Desde 2014                            |
| Detalles   | 2,000+    | Múltiples líneas por factura          |
| Período    | 2014-2025 | 11 años de datos                      |

---

## 📝 Notas Importantes

1. **Datos Históricos:** La base contiene ventas desde 2014, con variaciones en completitud
2. **Clientes Duplicados:** Algunos clientes pueden tener registros similares
3. **Productos Dinámicos:** Catálogo de productos cambia según disponibilidad
4. **Métodos de Pago:** La categoría "No especificado" indica datos incompletos
5. **Horas de Venta:** Algunas transacciones usan un valor por defecto (1899-12-30)

---

**Versión:** 1.0  
**Última Actualización:** Mayo 2026  
**Responsable:** Julian Barbieri
