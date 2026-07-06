import shutil
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "stylestore.db")


def realizar_backup(carpeta_destino):
    """
    Copia el archivo de base de datos a la carpeta destino,
    añadiendo fecha y hora al nombre (RF14).
    Retorna (True, ruta_completa) o (False, mensaje_error).
    """
    try:
        if not os.path.exists(DB_PATH):
            return False, "No se encontró la base de datos actual"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_backup = f"stylestore_backup_{timestamp}.db"
        ruta_completa = os.path.join(carpeta_destino, nombre_backup)

        shutil.copy2(DB_PATH, ruta_completa)
        return True, ruta_completa
    except Exception as e:
        return False, str(e)


def restaurar_backup(ruta_archivo_backup):
    """
    Reemplaza la base de datos actual con el archivo de backup seleccionado (RF15).
    Valida que el archivo tenga extensión .db antes de continuar.
    Retorna (True, mensaje) o (False, mensaje_error).
    """
    try:
        if not ruta_archivo_backup.lower().endswith(".db"):
            return False, "Error al restaurar: archivo inválido (no es un archivo .db)"

        if not os.path.exists(ruta_archivo_backup):
            return False, "Error al restaurar: el archivo no existe"

        # Validación básica de estructura: intentar abrirlo como SQLite
        import sqlite3
        try:
            conexion_prueba = sqlite3.connect(ruta_archivo_backup)
            cursor = conexion_prueba.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tablas = [fila[0] for fila in cursor.fetchall()]
            conexion_prueba.close()

            tablas_esperadas = {"producto", "cliente", "venta", "proveedor"}
            if not tablas_esperadas.issubset(set(tablas)):
                return False, "Error al restaurar: archivo inválido (no corresponde a StyleStore)"
        except Exception:
            return False, "Error al restaurar: archivo inválido o corrupto"

        shutil.copy2(ruta_archivo_backup, DB_PATH)
        return True, "Base de datos restaurada exitosamente"
    except Exception as e:
        return False, str(e)