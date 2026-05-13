# Diagrama Entidad-Relación (ER)

**Documento:** Diseño del Modelo Relacional  
**Autor:** Julian Barbieri  
**Fecha:** Mayo 2026  
**Versión:** 1.0

---

## 📊 Diagrama ER Conceptual

```
                          ┌─────────────────────┐
                          │     CIUDADES        │
                          ├─────────────────────┤
                          │ PK: CiudadID (INT)  │
                          │    Ciudad (VARCHAR) │
                          └──────────┬──────────┘
                                     │
                                     │ 1:N
                                     │
                          ┌──────────▼──────────┐
                          │    SUCURSALES      │
                          ├────────────────────┤
                          │PK: SucursalID (INT)│
                          │SucursalNombre(VAR) │
                          │FK: CiudadID (INT)  │
                          └──┬───────────┬─────┘
                             │           │
                     1:N      │           │       1:N
                             │           │
         ┌───────────┐   ┌────▼─────┐   └─────────────┐
         │VENDEDORES │   │ FACTURAS  │               │
         ├───────────┤   ├───────────┤               │
         │PK: VID    │   │PK: FID    │               │
         │Vendedor   │───│FK: VID ◄──┤               │
         │(VARCHAR)  │   │FK: CID    │               │
         └───────────┘   │FK: SID    │               │
                         │Dia(INT)   │               │
                         │Mes(INT)   │               │
                         │Anio(INT)  │               │
                         │HoraVenta  │               │
                         │Metodo Pago│               │
                         │Descuento  │               │
                         │TotalVenta │               │
                         └────┬──────┘               │
                              │                     │
                              │ 1:N                 │
                              │                     │
         ┌───────────┐    ┌───▼──────────┐  ┌──────▼──────┐
         │ CLIENTES  │    │DETALLFACTURAS│  │ CLIENTES    │
         ├───────────┤    ├──────────────┤  ├─────────────┤
         │PK: CID    │───◄│FK: FID       │  │ PK: CID     │
         │ClienteNom │    │FK: PID       │  │ ClienteNom  │
         │Genero     │    │DetalleID(PK) │  │ Genero      │
         │Edad       │    │ProductoNro   │  │ Edad        │
         │Email      │    │Cantidad      │  │ Email       │
         │Telefono   │    │PrecioUnit.   │  │ Telefono    │
         │Direccion  │    │Subtotal      │  │ Direccion   │
         └───────────┘    └────┬─────────┘  └─────────────┘
                                │
                                │ N:1
                                │
                        ┌───────▼────────┐
                        │   PRODUCTOS    │
                        ├────────────────┤
                        │ PK: PID (INT)  │
                        │NombreProducto  │
                        │MarcaProducto   │
                        └────────────────┘
```

---

## 📑 Especificación Detallada del Modelo

### Entidad: CIUDADES

```
CIUDADES
├─ Atributo Clave: CiudadID (INT)
├─ Atributo: Ciudad (VARCHAR(100))
└─ Relaciones:
   └─ 1:N con SUCURSALES
```

**Propósito:** Mantener la lista de ubicaciones geográficas.

---

### Entidad: SUCURSALES

```
SUCURSALES
├─ Atributo Clave: SucursalID (INT)
├─ Atributos:
│  ├─ SucursalNombre (VARCHAR(100))
│  └─ CiudadID (INT, FK → CIUDADES)
└─ Relaciones:
   ├─ N:1 con CIUDADES (ubicación)
   └─ 1:N con FACTURAS (procesa)
```

**Propósito:** Representar los puntos de venta, ligados a ubicaciones.

---

### Entidad: VENDEDORES

```
VENDEDORES
├─ Atributo Clave: VendedorID (INT)
├─ Atributo: Vendedor (VARCHAR(150))
└─ Relaciones:
   └─ 1:N con FACTURAS (realiza)
```

**Propósito:** Mantener el registro del personal de ventas.

---

### Entidad: CLIENTES

```
CLIENTES
├─ Atributo Clave: ClienteID (INT)
├─ Atributos:
│  ├─ ClienteNombre (VARCHAR(150))
│  ├─ GeneroCliente (CHAR(1))
│  ├─ EdadCliente (INT)
│  ├─ EmailCliente (VARCHAR(150))
│  ├─ TelefonoCliente (VARCHAR(20))
│  └─ DireccionCliente (VARCHAR(200))
└─ Relaciones:
   └─ 1:N con FACTURAS (realiza compras)
```

**Propósito:** Mantener información demográfica y de contacto de clientes.

---

### Entidad: PRODUCTOS

```
PRODUCTOS
├─ Atributo Clave: ProductoID (INT)
├─ Atributos:
│  ├─ NombreProducto (VARCHAR(150))
│  └─ MarcaProducto (VARCHAR(100))
└─ Relaciones:
   └─ 1:N con DETALLEFACTURAS (se vende en)
```

**Propósito:** Mantener el catálogo de productos disponibles.

---

### Entidad (Tabla de Hechos): FACTURAS

```
FACTURAS
├─ Atributo Clave: FacturaID (INT)
├─ Atributos (Dimensionales):
│  ├─ SucursalID (INT, FK → SUCURSALES)
│  ├─ VendedorID (INT, FK → VENDEDORES)
│  ├─ ClienteID (INT, FK → CLIENTES)
│  └─ MetodoPago (VARCHAR(50))
├─ Atributos (Temporales):
│  ├─ Dia (INT)
│  ├─ Mes (INT)
│  ├─ Anio (INT)
│  └─ HoraVenta (TIME)
├─ Atributos (Medidas):
│  ├─ DescuentoVenta (NUMERIC(5,2))
│  └─ TotalVenta (DECIMAL(15,2))
└─ Relaciones:
   ├─ N:1 con SUCURSALES (ocurre en)
   ├─ N:1 con VENDEDORES (vendido por)
   ├─ N:1 con CLIENTES (comprado por)
   └─ 1:N con DETALLEFACTURAS (contiene)
```

**Propósito:** Registrar transacciones de venta (tabla de hechos).

---

### Entidad (Tabla de Detalles): DETALLEFACTURAS

```
DETALLEFACTURAS
├─ Atributo Clave: DetalleID (INT)
├─ Atributos (Foráneos):
│  ├─ FacturaID (INT, FK → FACTURAS)
│  └─ ProductoID (INT, FK → PRODUCTOS)
├─ Atributos (Contextuales):
│  └─ ProductoNro (INT)
├─ Atributos (Medidas):
│  ├─ Cantidad (INT)
│  ├─ PrecioUnitario (DECIMAL(15,2))
│  └─ Subtotal (DECIMAL(15,2))
└─ Relaciones:
   ├─ N:1 con FACTURAS (pertenece a)
   └─ N:1 con PRODUCTOS (es de)
```

**Propósito:** Registrar líneas de detalle de cada transacción.

---

## 🔄 Flujo de Datos

```
CLIENTE REALIZA COMPRA
        │
        ▼
┌───────────────────────────────────┐
│  CREA FACTURA (FACTURAS)          │
│  ├─ Ref: Cliente                  │
│  ├─ Ref: Vendedor                 │
│  ├─ Ref: Sucursal                 │
│  ├─ Fecha/Hora                    │
│  ├─ Método de Pago                │
│  └─ Total                         │
└───────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────┐
│  AGREGA PRODUCTOS                 │
│  (DETALLEFACTURAS)                │
│  ├─ Producto 1: 2 unidades × $X   │
│  ├─ Producto 2: 1 unidad × $Y     │
│  └─ Producto 3: 3 unidades × $Z   │
└───────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────┐
│  PROCESA EN SUCURSAL               │
│  ├─ Ubicación geográfica (Ciudad) │
│  └─ Personal (Vendedor)           │
└───────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────┐
│  TOTAL VENTA = SUM(Subtotales)    │
│  - Descuentos                     │
└───────────────────────────────────┘
```

---

## 📋 Matriz de Cardinalidad

| Tabla 1    | Relación | Tabla 2         | Descripción                             |
| ---------- | -------- | --------------- | --------------------------------------- |
| Ciudades   | 1:N      | Sucursales      | Una ciudad tiene varias sucursales      |
| Sucursales | 1:N      | Facturas        | Una sucursal procesa muchas facturas    |
| Vendedores | 1:N      | Facturas        | Un vendedor hace muchas ventas          |
| Clientes   | 1:N      | Facturas        | Un cliente realiza múltiples compras    |
| Facturas   | 1:N      | DetalleFacturas | Una factura tiene múltiples líneas      |
| Productos  | 1:N      | DetalleFacturas | Un producto aparece en múltiples líneas |

---

## 🔐 Integridad Referencial

### Restricciones de Clave Foránea

```sql
-- Sucursales debe referenciar Ciudades
ALTER TABLE sucursales
ADD FOREIGN KEY (CiudadID)
REFERENCES ciudades(CiudadID);

-- Facturas debe referenciar Sucursales, Vendedores, Clientes
ALTER TABLE facturas
ADD FOREIGN KEY (SucursalID)
REFERENCES sucursales(SucursalID);

ALTER TABLE facturas
ADD FOREIGN KEY (VendedorID)
REFERENCES vendedores(VendedorID);

ALTER TABLE facturas
ADD FOREIGN KEY (ClienteID)
REFERENCES clientes(ClienteID);

-- DetalleFacturas debe referenciar Facturas, Productos
ALTER TABLE detalle_facturas
ADD FOREIGN KEY (FacturaID)
REFERENCES facturas(FacturaID);

ALTER TABLE detalle_facturas
ADD FOREIGN KEY (ProductoID)
REFERENCES productos(ProductoID);
```

---

## 📊 Diagrama Lógico (SQL DDL)

```sql
CREATE TABLE ciudades (
    CiudadID INT PRIMARY KEY AUTO_INCREMENT,
    Ciudad VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE sucursales (
    SucursalID INT PRIMARY KEY AUTO_INCREMENT,
    SucursalNombre VARCHAR(100) NOT NULL UNIQUE,
    CiudadID INT NOT NULL,
    FOREIGN KEY (CiudadID) REFERENCES ciudades(CiudadID)
);

CREATE TABLE vendedores (
    VendedorID INT PRIMARY KEY AUTO_INCREMENT,
    Vendedor VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE clientes (
    ClienteID INT PRIMARY KEY AUTO_INCREMENT,
    ClienteNombre VARCHAR(150) NOT NULL,
    GeneroCliente CHAR(1),
    EdadCliente INT,
    EmailCliente VARCHAR(150),
    TelefonoCliente VARCHAR(20),
    DireccionCliente VARCHAR(200)
);

CREATE TABLE productos (
    ProductoID INT PRIMARY KEY AUTO_INCREMENT,
    NombreProducto VARCHAR(150) NOT NULL,
    MarcaProducto VARCHAR(100) NOT NULL
);

CREATE TABLE facturas (
    FacturaID INT PRIMARY KEY AUTO_INCREMENT,
    Dia INT NOT NULL,
    Mes INT NOT NULL,
    Anio INT NOT NULL,
    HoraVenta TIME,
    MetodoPago VARCHAR(50),
    SucursalID INT NOT NULL,
    VendedorID INT NOT NULL,
    ClienteID INT NOT NULL,
    DescuentoVenta NUMERIC(5,2),
    TotalVenta DECIMAL(15,2) NOT NULL,
    FOREIGN KEY (SucursalID) REFERENCES sucursales(SucursalID),
    FOREIGN KEY (VendedorID) REFERENCES vendedores(VendedorID),
    FOREIGN KEY (ClienteID) REFERENCES clientes(ClienteID)
);

CREATE TABLE detalle_facturas (
    DetalleID INT PRIMARY KEY AUTO_INCREMENT,
    FacturaID INT NOT NULL,
    ProductoNro INT NOT NULL,
    ProductoID INT NOT NULL,
    Cantidad INT NOT NULL,
    PrecioUnitario DECIMAL(15,2) NOT NULL,
    Subtotal DECIMAL(15,2) NOT NULL,
    FOREIGN KEY (FacturaID) REFERENCES facturas(FacturaID),
    FOREIGN KEY (ProductoID) REFERENCES productos(ProductoID)
);
```

---

## ✅ Propiedades del Diseño

### Normalización

- **1FN (Primera Forma Normal):** ✓ Todos los atributos son atómicos
- **2FN (Segunda Forma Normal):** ✓ No hay dependencias parciales
- **3FN (Tercera Forma Normal):** ✓ No hay dependencias transitivas
- **BCNF (Boyce-Codd):** ✓ Todos los determinantes son claves candidatas

### Características

- **Sin datos redundantes:** ✓ Cada hecho se registra una sola vez
- **Integridad referencial:** ✓ Relaciones bien definidas
- **Escalable:** ✓ Estructura soporta crecimiento
- **Flexible:** ✓ Permite analítica desde múltiples ángulos

---

## 📈 Variaciones del Modelo

### Opción 1: Tabla de Fechas (Date Dimension)

```
FECHAS
├─ FechaID (INT, PK)
├─ Fecha (DATE)
├─ Dia (INT)
├─ Mes (INT)
├─ Anio (INT)
├─ NombreMes (VARCHAR)
├─ Trimestre (INT)
├─ DiaSemana (INT)
└─ Semana (INT)
```

**Ventaja:** Facilita análisis temporal sin parsear Dia/Mes/Anio.

### Opción 2: Tabla de Métodos de Pago (Payment Methods)

```
METODOS_PAGO
├─ MetodoPagoID (INT, PK)
├─ MetodoPago (VARCHAR)
├─ Comisión (NUMERIC)
└─ Habilitado (BOOLEAN)
```

**Ventaja:** Control de métodos de pago y comisiones.

---

**Versión:** 1.0  
**Última Actualización:** Mayo 2026  
**Responsable:** Julian Barbieri
