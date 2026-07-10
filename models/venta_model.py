from database.db_setup import crear_conexion


def obtener_producto_para_venta(id_producto):
    """Obtiene los datos necesarios de un producto para agregarlo al carrito."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id_producto, sku, nombre, precio_venta, stock
        FROM producto
        WHERE id_producto = ? AND status = 'Activo'
    """, (id_producto,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado


def obtener_metodos_pago():
    """Retorna la lista de métodos de pago disponibles."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_pago, tipo_pago FROM metodo_pago ORDER BY id_pago")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado


def registrar_venta(carrito, id_cliente, id_pago):
    """
    Registra una venta completa (RF07).
    carrito: lista de dicts [{id_producto, sku, nombre, cantidad, precio_unitario, subtotal}, ...]
    Retorna (True, id_venta, total) o (False, mensaje_error).
    """
    if not carrito:
        return False, "El carrito está vacío", None

    conexion = crear_conexion()
    cursor = conexion.cursor()

    try:
        for item in carrito:
            cursor.execute("SELECT stock, nombre FROM producto WHERE id_producto = ?", (item["id_producto"],))
            fila = cursor.fetchone()
            if fila is None:
                conexion.close()
                return False, f"El producto {item['nombre']} ya no existe", None
            stock_actual, nombre = fila
            if stock_actual < item["cantidad"]:
                conexion.close()
                return False, f"Stock insuficiente para {nombre}", None

        total = sum(item["subtotal"] for item in carrito)

        cursor.execute("""
            INSERT INTO venta (total, id_cliente, id_pago)
            VALUES (?, ?, ?)
        """, (total, id_cliente, id_pago))
        id_venta = cursor.lastrowid

        for item in carrito:
            cursor.execute("""
                INSERT INTO detalles_ventas (id_venta, id_producto, cantidad, precio_unitario, subtotal)
                VALUES (?, ?, ?, ?, ?)
            """, (id_venta, item["id_producto"], item["cantidad"], item["precio_unitario"], item["subtotal"]))

            cursor.execute("""
                UPDATE producto SET stock = stock - ? WHERE id_producto = ?
            """, (item["cantidad"], item["id_producto"]))

        conexion.commit()
        return True, id_venta, total

    except Exception as e:
        conexion.rollback()
        return False, str(e), None
    finally:
        conexion.close()


def obtener_ventas(fecha_inicio=None, fecha_fin=None):
    """Lista todas las ventas registradas, con nombre de cliente y método de pago."""
    conexion = crear_conexion()
    cursor = conexion.cursor()

    query = """
        SELECT v.id_venta, v.fecha,
               COALESCE(c.nombre || ' ' || c.apellido, 'Sin cliente') AS cliente,
               v.total, m.tipo_pago,
               (SELECT COUNT(*) FROM detalles_ventas d WHERE d.id_venta = v.id_venta) AS items
        FROM venta v
        LEFT JOIN cliente c ON v.id_cliente = c.id_cliente
        LEFT JOIN metodo_pago m ON v.id_pago = m.id_pago
        WHERE 1=1
    """
    parametros = []
    if fecha_inicio and fecha_fin:
        query += " AND date(v.fecha) BETWEEN date(?) AND date(?)"
        parametros.extend([fecha_inicio, fecha_fin])

    query += " ORDER BY v.id_venta DESC"

    cursor.execute(query, parametros)
    resultado = cursor.fetchall()
    conexion.close()
    return resultado


def obtener_detalle_venta(id_venta):
    """Retorna los productos incluidos en una venta específica."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT d.id_detalle, p.nombre, d.cantidad, d.precio_unitario, d.subtotal, d.id_producto
        FROM detalles_ventas d
        JOIN producto p ON d.id_producto = p.id_producto
        WHERE d.id_venta = ?
    """, (id_venta,))
    resultado = cursor.fetchall()
    conexion.close()
    return resultado


def reembolsar_venta(id_venta):
    """
    Reembolsa una venta completa: regresa el stock de cada producto
    y elimina el registro de la venta y sus detalles.
    Retorna (True, mensaje) o (False, mensaje_error).
    """
    conexion = crear_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT id_venta FROM venta WHERE id_venta = ?", (id_venta,))
        if cursor.fetchone() is None:
            conexion.close()
            return False, "La venta no existe o ya fue reembolsada"

        cursor.execute("""
            SELECT id_producto, cantidad FROM detalles_ventas WHERE id_venta = ?
        """, (id_venta,))
        items = cursor.fetchall()

        for id_producto, cantidad in items:
            cursor.execute("""
                UPDATE producto SET stock = stock + ? WHERE id_producto = ?
            """, (cantidad, id_producto))

        cursor.execute("DELETE FROM detalles_ventas WHERE id_venta = ?", (id_venta,))
        cursor.execute("DELETE FROM venta WHERE id_venta = ?", (id_venta,))

        conexion.commit()
        return True, f"Venta #{id_venta} reembolsada exitosamente. El inventario fue restaurado."
    except Exception as e:
        conexion.rollback()
        return False, str(e)
    finally:
        conexion.close()