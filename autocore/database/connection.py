import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "autocore.db"


def obtener_conexion():
    """Abre una conexion con la base de datos SQLite de AutoCore."""
    return sqlite3.connect(DB_PATH)


def crear_tabla_clientes():
    """Crea la tabla clientes si todavia no existe."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            correo TEXT,
            direccion TEXT
        )
        """
    )

    conexion.commit()
    conexion.close()
