from database.db_setup import crear_conexion


def registrar_cliente(nombre, apellido, telefono, correo):
    """Registra un nuevo cliente (RF05). Retorna (True, id) o (False, mensaje_error)."""
    if not nombre:
        return False, "El nombre es obligatorio"

    conexion = crear_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO cliente (nombre, apellido, telefono, correo)
            VALUES (?, ?, ?, ?)
        """, (nombre, apellido, telefono, correo))
        conexion.commit()
        return True, cursor.lastrowid
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            return False, "El teléfono o correo ya está registrado"
        return False, str(e)
    finally:
        conexion.close()


def modificar_cliente(id_cliente, nombre, apellido, telefono, correo):
    """Modifica los datos de un cliente existente."""
    if not nombre:
        return False, "El nombre es obligatorio"

    conexion = crear_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            UPDATE cliente
            SET nombre = ?, apellido = ?, telefono = ?, correo = ?
            WHERE id_cliente = ?
        """, (nombre, apellido, telefono, correo, id_cliente))
        conexion.commit()
        return True, "Cliente actualizado exitosamente"
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            return False, "El teléfono o correo ya está registrado por otro cliente"
        return False, str(e)
    finally:
        conexion.close()


def eliminar_cliente(id_cliente):
    """Elimina un cliente. Si tiene ventas asociadas, no se puede eliminar (integridad referencial)."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM venta WHERE id_cliente = ?", (id_cliente,))
        total_ventas = cursor.fetchone()[0]
        if total_ventas > 0:
            return False, f"No se puede eliminar: el cliente tiene {total_ventas} venta(s) registrada(s)"

        cursor.execute("DELETE FROM cliente WHERE id_cliente = ?", (id_cliente,))
        conexion.commit()
        return True, "Cliente eliminado exitosamente"
    except Exception as e:
        return False, str(e)
    finally:
        conexion.close()


def obtener_cliente_por_id(id_cliente):
    """Obtiene un solo cliente por su id, para precargar el formulario de edición."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id_cliente, nombre, apellido, telefono, correo
        FROM cliente WHERE id_cliente = ?
    """, (id_cliente,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado


def obtener_clientes(texto_busqueda=None):
    """Consulta clientes (RF05), con número de compras realizadas por cada uno."""
    conexion = crear_conexion()
    cursor = conexion.cursor()

    query = """
        SELECT c.id_cliente, c.nombre, c.apellido, c.telefono, c.correo,
               COUNT(v.id_venta) AS total_compras
        FROM cliente c
        LEFT JOIN venta v ON v.id_cliente = c.id_cliente
        WHERE 1=1
    """
    parametros = []

    if texto_busqueda:
        query += " AND (c.nombre LIKE ? OR c.apellido LIKE ? OR c.telefono LIKE ?)"
        like = f"%{texto_busqueda}%"
        parametros.extend([like, like, like])

    query += " GROUP BY c.id_cliente ORDER BY c.nombre"

    cursor.execute(query, parametros)
    resultado = cursor.fetchall()
    conexion.close()
    return resultado


def obtener_historial_compras(id_cliente):
    """Retorna el historial de ventas de un cliente específico (RF06)."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT v.id_venta, v.fecha, v.total, m.tipo_pago
        FROM venta v
        LEFT JOIN metodo_pago m ON v.id_pago = m.id_pago
        WHERE v.id_cliente = ?
        ORDER BY v.fecha DESC
    """, (id_cliente,))
    resultado = cursor.fetchall()
    conexion.close()
    return resultado