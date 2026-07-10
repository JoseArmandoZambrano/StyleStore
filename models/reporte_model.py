from database.db_setup import crear_conexion
import csv


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


def exportar_ventas_a_csv(ventas, ruta_archivo):
    """
    Exporta la lista de ventas a un archivo CSV en la ruta indicada.
    Retorna (True, ruta) o (False, mensaje_error).
    """
    try:
        with open(ruta_archivo, mode="w", newline="", encoding="utf-8-sig") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["ID Venta", "Fecha", "Cliente", "Total", "Método de pago"])
            total_acumulado = 0
            for id_venta, fecha, cliente, total, metodo_pago in ventas:
                escritor.writerow([id_venta, fecha, cliente, f"{total:.2f}", metodo_pago or "-"])
                total_acumulado += total
            escritor.writerow([])
            escritor.writerow(["", "", "TOTAL ACUMULADO:", f"{total_acumulado:.2f}", ""])
        return True, ruta_archivo
    except Exception as e:
        return False, str(e)


def exportar_bajo_stock_a_csv(productos, ruta_archivo):
    """
    Exporta el reporte de bajo stock a un archivo CSV en la ruta indicada.
    Retorna (True, ruta) o (False, mensaje_error).
    """
    try:
        with open(ruta_archivo, mode="w", newline="", encoding="utf-8-sig") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["SKU", "Nombre", "Categoría", "Talla", "Color", "Stock", "Proveedor"])
            for sku, nombre, categoria, talla, color, stock, proveedor in productos:
                escritor.writerow([sku, nombre, categoria or "-", talla or "-", color or "-", stock, proveedor or "-"])
        return True, ruta_archivo
    except Exception as e:
        return False, str(e)