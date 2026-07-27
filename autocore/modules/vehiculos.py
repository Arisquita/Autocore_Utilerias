from database.connection import obtener_conexion
from modules.clientes import buscar_cliente_por_id


# Este modulo administra vehiculos asociados a clientes ya registrados.
def crear_tabla_vehiculos():
    """Crea la tabla vehiculos si todavia no existe."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS vehiculos (
            id_vehiculo INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            anio INTEGER,
            placas TEXT NOT NULL,
            color TEXT,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        )
        """
    )

    conexion.commit()
    conexion.close()


def validar_cliente_existente(id_cliente):
    """Verifica que el vehiculo pertenezca a un cliente existente."""
    if id_cliente is None:
        return False, "El ID del cliente es obligatorio."

    try:
        id_cliente = int(id_cliente)
    except (TypeError, ValueError):
        return False, "El ID del cliente debe ser un numero entero."

    if buscar_cliente_por_id(id_cliente) is None:
        return False, "No existe un cliente con ese ID."

    return True, ""


def validar_vehiculo(id_cliente, marca, modelo, placas, anio=None):
    es_cliente_valido, mensaje = validar_cliente_existente(id_cliente)
    if not es_cliente_valido:
        return False, mensaje

    if not marca or not marca.strip():
        return False, "La marca es obligatoria."

    if not modelo or not modelo.strip():
        return False, "El modelo es obligatorio."

    if not placas or not placas.strip():
        return False, "Las placas son obligatorias."

    if anio not in (None, ""):
        try:
            int(anio)
        except (TypeError, ValueError):
            return False, "El anio debe ser un numero entero."

    return True, ""


def registrar_vehiculo(id_cliente, marca, modelo, anio=None, placas="", color=""):
    es_valido, mensaje = validar_vehiculo(id_cliente, marca, modelo, placas, anio)
    if not es_valido:
        return False, mensaje

    anio_guardado = None if anio in (None, "") else int(anio)

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO vehiculos (id_cliente, marca, modelo, anio, placas, color)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            int(id_cliente),
            marca.strip(),
            modelo.strip(),
            anio_guardado,
            placas.strip(),
            color.strip(),
        ),
    )

    conexion.commit()
    id_vehiculo = cursor.lastrowid
    conexion.close()

    return True, f"Vehiculo registrado correctamente. ID asignado: {id_vehiculo}"


def consultar_vehiculos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT id_vehiculo, id_cliente, marca, modelo, anio, placas, color
        FROM vehiculos
        ORDER BY id_vehiculo
        """
    )
    vehiculos = cursor.fetchall()

    conexion.close()
    return vehiculos


def consultar_vehiculos_por_cliente(id_cliente):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT id_vehiculo, id_cliente, marca, modelo, anio, placas, color
        FROM vehiculos
        WHERE id_cliente = ?
        ORDER BY id_vehiculo
        """,
        (id_cliente,),
    )
    vehiculos = cursor.fetchall()

    conexion.close()
    return vehiculos


def buscar_vehiculo_por_id(id_vehiculo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT id_vehiculo, id_cliente, marca, modelo, anio, placas, color
        FROM vehiculos
        WHERE id_vehiculo = ?
        """,
        (id_vehiculo,),
    )
    vehiculo = cursor.fetchone()

    conexion.close()
    return vehiculo


def editar_vehiculo(id_vehiculo, id_cliente, marca, modelo, anio=None, placas="", color=""):
    es_valido, mensaje = validar_vehiculo(id_cliente, marca, modelo, placas, anio)
    if not es_valido:
        return False, mensaje

    vehiculo = buscar_vehiculo_por_id(id_vehiculo)
    if vehiculo is None:
        return False, "No existe un vehiculo con ese ID."

    anio_guardado = None if anio in (None, "") else int(anio)

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        UPDATE vehiculos
        SET id_cliente = ?, marca = ?, modelo = ?, anio = ?, placas = ?, color = ?
        WHERE id_vehiculo = ?
        """,
        (
            int(id_cliente),
            marca.strip(),
            modelo.strip(),
            anio_guardado,
            placas.strip(),
            color.strip(),
            id_vehiculo,
        ),
    )

    conexion.commit()
    conexion.close()

    return True, "Vehiculo actualizado correctamente."
