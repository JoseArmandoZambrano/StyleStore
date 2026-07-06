from database.db_setup import crear_conexion


def registrar_proveedor(nombre, contacto, telefono, correo, direccion):
    """Registra un nuevo proveedor. Retorna (True, id) o (False, mensaje_error)."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO proveedor (nombre, contacto, telefono, correo, direccion)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, contacto, telefono, correo, direccion))
        conexion.commit()
        nuevo_id = cursor.lastrowid
        return True, nuevo_id
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            return False, "El teléfono o correo ya está registrado"
        return False, str(e)
    finally:
        conexion.close()


def obtener_proveedores():
    """Retorna una lista de todos los proveedores."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_proveedor, nombre, contacto, telefono, correo, direccion FROM proveedor ORDER BY nombre")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado