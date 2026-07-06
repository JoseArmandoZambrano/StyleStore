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
        # 1. Verificar stock disponible de cada producto (RF07 - restricción)
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

        # 2. Calcular total
        total = sum(item["subtotal"] for item in carrito)

        # 3. Registrar la venta
        cursor.execute("""
            INSERT INTO venta (total, id_cliente, id_pago)
            VALUES (?, ?, ?)
        """, (total, id_cliente, id_pago))
        id_venta = cursor.lastrowid

        # 4. Registrar detalles y descontar inventario
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