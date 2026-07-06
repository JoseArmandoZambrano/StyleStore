from database.db_setup import crear_conexion


def reporte_ventas_por_periodo(fecha_inicio, fecha_fin):
    """
    Genera el reporte de ventas dentro de un rango de fechas (RF12).
    Las fechas deben tener formato 'YYYY-MM-DD'.
    """
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT v.id_venta, v.fecha, 
               COALESCE(c.nombre || ' ' || c.apellido, 'Sin cliente') AS cliente,
               v.total, m.tipo_pago
        FROM venta v
        LEFT JOIN cliente c ON v.id_cliente = c.id_cliente
        LEFT JOIN metodo_pago m ON v.id_pago = m.id_pago
        WHERE date(v.fecha) BETWEEN date(?) AND date(?)
        ORDER BY v.fecha DESC
    """, (fecha_inicio, fecha_fin))
    resultado = cursor.fetchall()
    conexion.close()
    return resultado


def reporte_bajo_stock(umbral=5):
    """Genera el reporte de productos con stock igual o menor al umbral (RF13)."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT p.sku, p.nombre, c.nombre AS categoria, p.talla, p.color,
               p.stock, prov.nombre AS proveedor
        FROM producto p
        LEFT JOIN categoria c ON p.id_categoria = c.id_categoria
        LEFT JOIN proveedor prov ON p.id_proveedor = prov.id_proveedor
        WHERE p.status = 'Activo' AND p.stock <= ?
        ORDER BY p.stock ASC
    """, (umbral,))
    resultado = cursor.fetchall()
    conexion.close()
    return resultado