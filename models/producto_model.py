from database.db_setup import crear_conexion
import random
import string


def generar_sku():
    """Genera un SKU aleatorio único, ej: PRD-7X9K2A"""
    letras_numeros = string.ascii_uppercase + string.digits
    codigo = "".join(random.choices(letras_numeros, k=6))
    return f"PRD-{codigo}"


def registrar_producto(nombre, id_categoria, talla, color, precio_compra,
                        precio_venta, cantidad_inicial, id_proveedor, descripcion=""):
    """Registra un nuevo producto (RF01). Retorna (True, sku) o (False, mensaje_error)."""
    if not nombre or precio_venta is None or cantidad_inicial is None:
        return False, "Faltan campos obligatorios"

    conexion = crear_conexion()
    cursor = conexion.cursor()
    sku = generar_sku()
    try:
        cursor.execute("""
            INSERT INTO producto
            (sku, nombre, id_categoria, talla, color, precio_compra, precio_venta,
             stock, id_proveedor, descripcion, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Activo')
        """, (sku, nombre, id_categoria, talla, color, precio_compra,
              precio_venta, cantidad_inicial, id_proveedor, descripcion))
        conexion.commit()
        return True, sku
    except Exception as e:
        return False, str(e)
    finally:
        conexion.close()


def modificar_producto(id_producto, nombre, id_categoria, talla, color,
                        precio_compra, precio_venta, id_proveedor, descripcion):
    """Modifica un producto existente (RF02). El SKU no se puede modificar."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            UPDATE producto
            SET nombre = ?, id_categoria = ?, talla = ?, color = ?,
                precio_compra = ?, precio_venta = ?, id_proveedor = ?, descripcion = ?
            WHERE id_producto = ?
        """, (nombre, id_categoria, talla, color, precio_compra,
              precio_venta, id_proveedor, descripcion, id_producto))
        conexion.commit()
        return True, "Producto actualizado exitosamente"
    except Exception as e:
        return False, str(e)
    finally:
        conexion.close()


def eliminar_producto(id_producto):
    """Baja lógica de un producto (RF03): cambia status a Inactivo."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("UPDATE producto SET status = 'Inactivo' WHERE id_producto = ?", (id_producto,))
        conexion.commit()
        return True, "Producto dado de baja correctamente"
    except Exception as e:
        return False, str(e)
    finally:
        conexion.close()


def obtener_productos(solo_activos=True, id_categoria=None, texto_busqueda=None):
    """Consulta productos (RF04), con filtros opcionales de categoría y texto."""
    conexion = crear_conexion()
    cursor = conexion.cursor()

    query = """
        SELECT p.id_producto, p.sku, p.nombre, c.nombre AS categoria, p.talla,
               p.color, p.precio_venta, p.stock, p.status, p.id_categoria, p.id_proveedor,
               p.precio_compra, p.descripcion
        FROM producto p
        LEFT JOIN categoria c ON p.id_categoria = c.id_categoria
        WHERE 1=1
    """
    parametros = []

    if solo_activos:
        query += " AND p.status = 'Activo'"
    if id_categoria:
        query += " AND p.id_categoria = ?"
        parametros.append(id_categoria)
    if texto_busqueda:
        query += " AND (p.nombre LIKE ? OR p.sku LIKE ?)"
        like = f"%{texto_busqueda}%"
        parametros.extend([like, like])

    query += " ORDER BY p.nombre"

    cursor.execute(query, parametros)
    resultado = cursor.fetchall()
    conexion.close()
    return resultado


def obtener_producto_por_id(id_producto):
    """Obtiene un solo producto por su id, útil para cargar el formulario de edición."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id_producto, sku, nombre, id_categoria, talla, color,
               precio_compra, precio_venta, stock, id_proveedor, descripcion, status
        FROM producto WHERE id_producto = ?
    """, (id_producto,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado