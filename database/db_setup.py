import sqlite3
import os

DB_NAME = os.path.join(os.path.dirname(__file__), "..", "stylestore.db")

def crear_conexion():
    """Crea y retorna una conexión a la base de datos SQLite."""
    conexion = sqlite3.connect(DB_NAME)
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion

def crear_tablas():
    """Crea todas las tablas del sistema si no existen."""
    conexion = crear_conexion()
    cursor = conexion.cursor()

    # Tabla PROVEEDOR
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proveedor (
            id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            contacto TEXT,
            telefono TEXT UNIQUE,
            correo TEXT UNIQUE,
            direccion TEXT
        )
    """)

    # Tabla CATEGORIA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categoria (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            descripcion TEXT
        )
    """)

    # Tabla PROMOCION
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS promocion (
            id_promocion INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo_descuento TEXT NOT NULL,   -- 'porcentaje' o 'monto_fijo'
            valor REAL NOT NULL,
            fecha_inicio TEXT NOT NULL,
            fecha_fin TEXT NOT NULL,
            estado TEXT DEFAULT 'Activa'
        )
    """)

    # Tabla PRODUCTO
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS producto (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            id_categoria INTEGER,
            talla TEXT,
            color TEXT,
            precio_compra REAL NOT NULL,
            precio_venta REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            id_proveedor INTEGER,
            id_promocion INTEGER,
            descripcion TEXT,
            status TEXT DEFAULT 'Activo',
            FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria),
            FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor),
            FOREIGN KEY (id_promocion) REFERENCES promocion(id_promocion)
        )
    """)

    # Tabla CLIENTE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT,
            telefono TEXT UNIQUE,
            correo TEXT UNIQUE,
            fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabla METODO_PAGO
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metodo_pago (
            id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_pago TEXT NOT NULL UNIQUE
        )
    """)

    # Tabla VENTA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS venta (
            id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP,
            total REAL NOT NULL,
            id_cliente INTEGER,
            id_pago INTEGER NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
            FOREIGN KEY (id_pago) REFERENCES metodo_pago(id_pago)
        )
    """)

    # Tabla DETALLES_VENTAS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalles_ventas (
            id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
            id_venta INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (id_venta) REFERENCES venta(id_venta),
            FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
        )
    """)

    conexion.commit()

    # Insertar métodos de pago por defecto si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM metodo_pago")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO metodo_pago (tipo_pago) VALUES (?)",
            [("Efectivo",), ("Tarjeta de débito",), ("Tarjeta de crédito",), ("Transferencia",)]
        )
        conexion.commit()

    conexion.close()
    print("Base de datos creada correctamente en:", DB_NAME)


if __name__ == "__main__":
    crear_tablas()