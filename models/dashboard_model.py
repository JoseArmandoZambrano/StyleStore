from database.db_setup import crear_conexion
from datetime import datetime


def obtener_estadisticas():
    """Retorna los conteos generales para las tarjetas del Home."""
    conexion = crear_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM producto WHERE status = 'Activo'")
    total_productos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM cliente")
    total_clientes = cursor.fetchone()[0]

    hoy = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT COUNT(*), COALESCE(SUM(total), 0) FROM venta WHERE date(fecha) = date(?)", (hoy,))
    ventas_hoy, ingresos_hoy = cursor.fetchone()

    conexion.close()
    return {
        "productos": total_productos,
        "clientes": total_clientes,
        "ventas_hoy": ventas_hoy,
        "ingresos_hoy": ingresos_hoy or 0,
    }


def obtener_ventas_recientes(limite=5):
    """Retorna las últimas ventas registradas, para la tabla de 'Recent sales'."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT v.id_venta,
               COALESCE(c.nombre || ' ' || c.apellido, 'Sin cliente') AS cliente,
               (SELECT COUNT(*) FROM detalles_ventas d WHERE d.id_venta = v.id_venta) AS items,
               v.total, m.tipo_pago
        FROM venta v
        LEFT JOIN cliente c ON v.id_cliente = c.id_cliente
        LEFT JOIN metodo_pago m ON v.id_pago = m.id_pago
        ORDER BY v.id_venta DESC
        LIMIT ?
    """, (limite,))
    resultado = cursor.fetchall()
    conexion.close()
    return resultado


def contar_bajo_stock(umbral=5):
    """Cuenta cuántos productos activos tienen stock igual o menor al umbral."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM producto WHERE status = 'Activo' AND stock <= ?", (umbral,))
    resultado = cursor.fetchone()[0]
    conexion.close()
    return resultado