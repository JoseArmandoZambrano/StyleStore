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


def modificar_proveedor(id_proveedor, nombre, contacto, telefono, correo, direccion):
    """Modifica los datos de un proveedor existente."""
    if not nombre:
        return False, "El nombre es obligatorio"

    conexion = crear_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            UPDATE proveedor
            SET nombre = ?, contacto = ?, telefono = ?, correo = ?, direccion = ?
            WHERE id_proveedor = ?
        """, (nombre, contacto, telefono, correo, direccion, id_proveedor))
        conexion.commit()
        return True, "Proveedor actualizado exitosamente"
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            return False, "El teléfono o correo ya está registrado por otro proveedor"
        return False, str(e)
    finally:
        conexion.close()


def eliminar_proveedor(id_proveedor):
    """Elimina un proveedor. Si tiene productos asociados, no se puede eliminar."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM producto WHERE id_proveedor = ? AND status = 'Activo'", (id_proveedor,))
        total_productos = cursor.fetchone()[0]
        if total_productos > 0:
            return False, f"No se puede eliminar: el proveedor tiene {total_productos} producto(s) activo(s) asociado(s)"

        cursor.execute("DELETE FROM proveedor WHERE id_proveedor = ?", (id_proveedor,))
        conexion.commit()
        return True, "Proveedor eliminado exitosamente"
    except Exception as e:
        return False, str(e)
    finally:
        conexion.close()


def obtener_proveedor_por_id(id_proveedor):
    """Obtiene un solo proveedor por su id, para precargar el formulario de edición."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id_proveedor, nombre, contacto, telefono, correo, direccion
        FROM proveedor WHERE id_proveedor = ?
    """, (id_proveedor,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado


def obtener_proveedores():
    """Retorna una lista de todos los proveedores."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_proveedor, nombre, contacto, telefono, correo, direccion FROM proveedor ORDER BY nombre")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado