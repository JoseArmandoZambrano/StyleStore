from database.db_setup import crear_conexion


def registrar_categoria(nombre, descripcion=""):
    """Registra una nueva categoría. Retorna (True, id) o (False, mensaje_error)."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO categoria (nombre, descripcion)
            VALUES (?, ?)
        """, (nombre, descripcion))
        conexion.commit()
        nuevo_id = cursor.lastrowid
        return True, nuevo_id
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            return False, "Esa categoría ya existe"
        return False, str(e)
    finally:
        conexion.close()


def obtener_categorias():
    """Retorna una lista de todas las categorías."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_categoria, nombre, descripcion FROM categoria ORDER BY nombre")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado