from database.db_setup import crear_conexion
from datetime import datetime


def registrar_promocion(nombre, tipo_descuento, valor, fecha_inicio, fecha_fin):
    """
    Registra una nueva promoción (RF10).
    tipo_descuento: 'porcentaje' o 'monto_fijo'
    fecha_inicio, fecha_fin: strings 'YYYY-MM-DD'
    Retorna (True, id) o (False, mensaje_error).
    """
    if fecha_fin < fecha_inicio:
        return False, "La fecha de fin debe ser posterior a la fecha de inicio"

    if valor <= 0:
        return False, "El valor del descuento debe ser mayor a cero"

    conexion = crear_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO promocion (nombre, tipo_descuento, valor, fecha_inicio, fecha_fin, estado)
            VALUES (?, ?, ?, ?, ?, 'Activa')
        """, (nombre, tipo_descuento, valor, fecha_inicio, fecha_fin))
        conexion.commit()
        return True, cursor.lastrowid
    except Exception as e:
        return False, str(e)
    finally:
        conexion.close()


def obtener_promociones():
    """Retorna todas las promociones registradas, indicando si están vigentes hoy."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id_promocion, nombre, tipo_descuento, valor, fecha_inicio, fecha_fin, estado
        FROM promocion
        ORDER BY fecha_inicio DESC
    """)
    resultado = cursor.fetchall()
    conexion.close()
    return resultado


def asignar_promocion_a_producto(id_producto, id_promocion):
    """Asocia una promoción vigente a un producto específico."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("UPDATE producto SET id_promocion = ? WHERE id_producto = ?", (id_promocion, id_producto))
        conexion.commit()
        return True, "Promoción asignada al producto"
    except Exception as e:
        return False, str(e)
    finally:
        conexion.close()


def esta_vigente(fecha_inicio, fecha_fin):
    """Verifica si una promoción está vigente en la fecha actual."""
    hoy = datetime.now().strftime("%Y-%m-%d")
    return fecha_inicio <= hoy <= fecha_fin