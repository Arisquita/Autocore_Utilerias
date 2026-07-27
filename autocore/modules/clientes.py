from database.connection import obtener_conexion


# Este modulo administra el registro, consulta y edicion de clientes.
def validar_cliente(nombre, telefono):
    if not nombre or not nombre.strip():
        return False, "El nombre es obligatorio."

    if not telefono or not telefono.strip():
        return False, "El telefono es obligatorio."

    return True, ""


def registrar_cliente(nombre, telefono, correo="", direccion=""):
    es_valido, mensaje = validar_cliente(nombre, telefono)
    if not es_valido:
        return False, mensaje

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO clientes (nombre, telefono, correo, direccion)
        VALUES (?, ?, ?, ?)
        """,
        (nombre.strip(), telefono.strip(), correo.strip(), direccion.strip()),
    )

    conexion.commit()
    id_cliente = cursor.lastrowid
    conexion.close()

    return True, f"Cliente registrado correctamente. ID asignado: {id_cliente}"


def consultar_clientes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT id_cliente, nombre, telefono, correo, direccion
        FROM clientes
        ORDER BY id_cliente
        """
    )
    clientes = cursor.fetchall()

    conexion.close()
    return clientes


def buscar_cliente_por_id(id_cliente):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT id_cliente, nombre, telefono, correo, direccion
        FROM clientes
        WHERE id_cliente = ?
        """,
        (id_cliente,),
    )
    cliente = cursor.fetchone()

    conexion.close()
    return cliente


def editar_cliente(id_cliente, nombre, telefono, correo="", direccion=""):
    es_valido, mensaje = validar_cliente(nombre, telefono)
    if not es_valido:
        return False, mensaje

    cliente = buscar_cliente_por_id(id_cliente)
    if cliente is None:
        return False, "No existe un cliente con ese ID."

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        UPDATE clientes
        SET nombre = ?, telefono = ?, correo = ?, direccion = ?
        WHERE id_cliente = ?
        """,
        (
            nombre.strip(),
            telefono.strip(),
            correo.strip(),
            direccion.strip(),
            id_cliente,
        ),
    )

    conexion.commit()
    conexion.close()

    return True, "Cliente actualizado correctamente."
