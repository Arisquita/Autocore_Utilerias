from database.connection import obtener_conexion
from modules.vehiculos import buscar_vehiculo_por_id


ESTADOS_PERMITIDOS = ("pendiente", "en_proceso", "finalizada", "cancelada")


# Este modulo administra ordenes de servicio asociadas a vehiculos registrados.
def crear_tabla_ordenes_servicio():
    """Crea la tabla ordenes_servicio si todavia no existe."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ordenes_servicio (
            id_orden INTEGER PRIMARY KEY AUTOINCREMENT,
            id_vehiculo INTEGER NOT NULL,
            descripcion TEXT NOT NULL,
            fecha TEXT NOT NULL,
            estado TEXT NOT NULL,
            observaciones TEXT,
            FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id_vehiculo)
        )
        """
    )

    conexion.commit()
    conexion.close()


def validar_vehiculo_existente(id_vehiculo):
    """Verifica que la orden pertenezca a un vehiculo existente."""
    if id_vehiculo is None:
        return False, "El ID del vehiculo es obligatorio."

    try:
        id_vehiculo = int(id_vehiculo)
    except (TypeError, ValueError):
        return False, "El ID del vehiculo debe ser un numero entero."

    if buscar_vehiculo_por_id(id_vehiculo) is None:
        return False, "No existe un vehiculo con ese ID."

    return True, ""


def validar_estado(estado):
    if not estado or not estado.strip():
        return False, "El estado es obligatorio."

    if estado.strip() not in ESTADOS_PERMITIDOS:
        return False, "El estado de la orden no es valido."

    return True, ""


def validar_orden_servicio(id_vehiculo, descripcion, fecha, estado="pendiente"):
    es_vehiculo_valido, mensaje = validar_vehiculo_existente(id_vehiculo)
    if not es_vehiculo_valido:
        return False, mensaje

    if not descripcion or not descripcion.strip():
        return False, "La descripcion es obligatoria."

    if not fecha or not fecha.strip():
        return False, "La fecha es obligatoria."

    return validar_estado(estado)


def registrar_orden_servicio(
    id_vehiculo, descripcion, fecha, estado="pendiente", observaciones=""
):
    es_valida, mensaje = validar_orden_servicio(
        id_vehiculo, descripcion, fecha, estado
    )
    if not es_valida:
        return False, mensaje

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO ordenes_servicio (
            id_vehiculo, descripcion, fecha, estado, observaciones
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            int(id_vehiculo),
            descripcion.strip(),
            fecha.strip(),
            estado.strip(),
            observaciones.strip(),
        ),
    )

    conexion.commit()
    id_orden = cursor.lastrowid
    conexion.close()

    return True, f"Orden de servicio registrada correctamente. ID asignado: {id_orden}"


def consultar_ordenes_servicio():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT id_orden, id_vehiculo, descripcion, fecha, estado, observaciones
        FROM ordenes_servicio
        ORDER BY id_orden
        """
    )
    ordenes = cursor.fetchall()

    conexion.close()
    return ordenes


def consultar_ordenes_por_vehiculo(id_vehiculo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT id_orden, id_vehiculo, descripcion, fecha, estado, observaciones
        FROM ordenes_servicio
        WHERE id_vehiculo = ?
        ORDER BY id_orden
        """,
        (id_vehiculo,),
    )
    ordenes = cursor.fetchall()

    conexion.close()
    return ordenes


def buscar_orden_por_id(id_orden):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT id_orden, id_vehiculo, descripcion, fecha, estado, observaciones
        FROM ordenes_servicio
        WHERE id_orden = ?
        """,
        (id_orden,),
    )
    orden = cursor.fetchone()

    conexion.close()
    return orden


def actualizar_estado_orden(id_orden, estado):
    es_estado_valido, mensaje = validar_estado(estado)
    if not es_estado_valido:
        return False, mensaje

    orden = buscar_orden_por_id(id_orden)
    if orden is None:
        return False, "No existe una orden con ese ID."

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        UPDATE ordenes_servicio
        SET estado = ?
        WHERE id_orden = ?
        """,
        (estado.strip(), id_orden),
    )

    conexion.commit()
    conexion.close()

    return True, "Estado de la orden actualizado correctamente."


def actualizar_observaciones_orden(id_orden, observaciones):
    """Actualiza las observaciones de una orden de servicio existente."""
    if not observaciones or not observaciones.strip():
        return False, "Las observaciones no pueden estar vacias."

    orden = buscar_orden_por_id(id_orden)
    if orden is None:
        return False, "No existe una orden con ese ID."

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        UPDATE ordenes_servicio
        SET observaciones = ?
        WHERE id_orden = ?
        """,
        (observaciones.strip(), id_orden),
    )

    conexion.commit()
    conexion.close()

    return True, "Observaciones de la orden actualizadas correctamente."
