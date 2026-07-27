from database.connection import crear_tabla_clientes
from modules.clientes import consultar_clientes, editar_cliente, registrar_cliente
from modules.ordenes_servicio import (
    actualizar_observaciones_orden,
    actualizar_estado_orden,
    consultar_ordenes_por_vehiculo,
    consultar_ordenes_servicio,
    crear_tabla_ordenes_servicio,
    registrar_orden_servicio,
)
from modules.vehiculos import (
    consultar_vehiculos,
    consultar_vehiculos_por_cliente,
    crear_tabla_vehiculos,
    editar_vehiculo,
    registrar_vehiculo,
)


def mostrar_menu():
    print("\n=== AutoCore ===")
    print("1. Registrar cliente")
    print("2. Consultar clientes")
    print("3. Editar cliente")
    print("\n4. Registrar vehiculo")
    print("5. Consultar vehiculos")
    print("6. Consultar vehiculos por cliente")
    print("7. Editar vehiculo")
    print("\n8. Registrar orden de servicio")
    print("9. Consultar ordenes de servicio")
    print("10. Consultar ordenes por vehiculo")
    print("11. Actualizar estado de orden")
    print("12. Actualizar observaciones de orden")
    print("13. Salir")


def pedir_datos_cliente():
    nombre = input("Nombre completo: ")
    telefono = input("Telefono: ")
    correo = input("Correo: ")
    direccion = input("Direccion: ")

    return nombre, telefono, correo, direccion


def pedir_datos_vehiculo():
    id_cliente = input("ID del cliente: ")
    marca = input("Marca: ")
    modelo = input("Modelo: ")
    anio = input("Anio: ")
    placas = input("Placas: ")
    color = input("Color: ")

    return id_cliente, marca, modelo, anio, placas, color


def pedir_datos_orden_servicio():
    id_vehiculo = input("ID del vehiculo: ")
    descripcion = input("Descripcion del servicio: ")
    fecha = input("Fecha: ")
    estado = input("Estado (pendiente, en_proceso, finalizada, cancelada): ")
    observaciones = input("Observaciones: ")

    return id_vehiculo, descripcion, fecha, estado, observaciones


def opcion_registrar_cliente():
    print("\n--- Registrar cliente ---")
    nombre, telefono, correo, direccion = pedir_datos_cliente()
    exito, mensaje = registrar_cliente(nombre, telefono, correo, direccion)
    print(mensaje)


def opcion_consultar_clientes():
    print("\n--- Clientes registrados ---")
    clientes = consultar_clientes()

    if not clientes:
        print("No hay clientes registrados.")
        return

    for cliente in clientes:
        id_cliente, nombre, telefono, correo, direccion = cliente
        print(
            f"ID: {id_cliente} | Nombre: {nombre} | Telefono: {telefono} | "
            f"Correo: {correo} | Direccion: {direccion}"
        )


def opcion_editar_cliente():
    print("\n--- Editar cliente ---")

    try:
        id_cliente = int(input("ID del cliente a editar: "))
    except ValueError:
        print("El ID debe ser un numero entero.")
        return

    nombre, telefono, correo, direccion = pedir_datos_cliente()
    exito, mensaje = editar_cliente(id_cliente, nombre, telefono, correo, direccion)
    print(mensaje)


def opcion_registrar_vehiculo():
    print("\n--- Registrar vehiculo ---")
    id_cliente, marca, modelo, anio, placas, color = pedir_datos_vehiculo()
    exito, mensaje = registrar_vehiculo(id_cliente, marca, modelo, anio, placas, color)
    print(mensaje)


def mostrar_vehiculos(vehiculos):
    if not vehiculos:
        print("No hay vehiculos registrados.")
        return

    for vehiculo in vehiculos:
        id_vehiculo, id_cliente, marca, modelo, anio, placas, color = vehiculo
        print(
            f"ID Vehiculo: {id_vehiculo} | ID Cliente: {id_cliente} | "
            f"Marca: {marca} | Modelo: {modelo} | Anio: {anio} | "
            f"Placas: {placas} | Color: {color}"
        )


def opcion_consultar_vehiculos():
    print("\n--- Vehiculos registrados ---")
    mostrar_vehiculos(consultar_vehiculos())


def opcion_consultar_vehiculos_por_cliente():
    print("\n--- Vehiculos por cliente ---")

    try:
        id_cliente = int(input("ID del cliente: "))
    except ValueError:
        print("El ID debe ser un numero entero.")
        return

    mostrar_vehiculos(consultar_vehiculos_por_cliente(id_cliente))


def opcion_editar_vehiculo():
    print("\n--- Editar vehiculo ---")

    try:
        id_vehiculo = int(input("ID del vehiculo a editar: "))
    except ValueError:
        print("El ID debe ser un numero entero.")
        return

    id_cliente, marca, modelo, anio, placas, color = pedir_datos_vehiculo()
    exito, mensaje = editar_vehiculo(
        id_vehiculo, id_cliente, marca, modelo, anio, placas, color
    )
    print(mensaje)


def opcion_registrar_orden_servicio():
    print("\n--- Registrar orden de servicio ---")
    id_vehiculo, descripcion, fecha, estado, observaciones = pedir_datos_orden_servicio()
    exito, mensaje = registrar_orden_servicio(
        id_vehiculo, descripcion, fecha, estado, observaciones
    )
    print(mensaje)


def mostrar_ordenes(ordenes):
    if not ordenes:
        print("No hay ordenes de servicio registradas.")
        return

    for orden in ordenes:
        id_orden, id_vehiculo, descripcion, fecha, estado, observaciones = orden
        print(
            f"ID Orden: {id_orden} | ID Vehiculo: {id_vehiculo} | "
            f"Descripcion: {descripcion} | Fecha: {fecha} | "
            f"Estado: {estado} | Observaciones: {observaciones}"
        )


def opcion_consultar_ordenes_servicio():
    print("\n--- Ordenes de servicio registradas ---")
    mostrar_ordenes(consultar_ordenes_servicio())


def opcion_consultar_ordenes_por_vehiculo():
    print("\n--- Ordenes por vehiculo ---")

    try:
        id_vehiculo = int(input("ID del vehiculo: "))
    except ValueError:
        print("El ID debe ser un numero entero.")
        return

    mostrar_ordenes(consultar_ordenes_por_vehiculo(id_vehiculo))


def opcion_actualizar_estado_orden():
    print("\n--- Actualizar estado de orden ---")

    try:
        id_orden = int(input("ID de la orden: "))
    except ValueError:
        print("El ID debe ser un numero entero.")
        return

    estado = input("Nuevo estado (pendiente, en_proceso, finalizada, cancelada): ")
    exito, mensaje = actualizar_estado_orden(id_orden, estado)
    print(mensaje)


def opcion_actualizar_observaciones_orden():
    print("\n--- Actualizar observaciones de orden ---")

    try:
        id_orden = int(input("ID de la orden: "))
    except ValueError:
        print("El ID debe ser un numero entero.")
        return

    observaciones = input("Nuevas observaciones: ")
    exito, mensaje = actualizar_observaciones_orden(id_orden, observaciones)
    print(mensaje)


def main():
    crear_tabla_clientes()
    crear_tabla_vehiculos()
    crear_tabla_ordenes_servicio()

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opcion: ")

        if opcion == "1":
            opcion_registrar_cliente()
        elif opcion == "2":
            opcion_consultar_clientes()
        elif opcion == "3":
            opcion_editar_cliente()
        elif opcion == "4":
            opcion_registrar_vehiculo()
        elif opcion == "5":
            opcion_consultar_vehiculos()
        elif opcion == "6":
            opcion_consultar_vehiculos_por_cliente()
        elif opcion == "7":
            opcion_editar_vehiculo()
        elif opcion == "8":
            opcion_registrar_orden_servicio()
        elif opcion == "9":
            opcion_consultar_ordenes_servicio()
        elif opcion == "10":
            opcion_consultar_ordenes_por_vehiculo()
        elif opcion == "11":
            opcion_actualizar_estado_orden()
        elif opcion == "12":
            opcion_actualizar_observaciones_orden()
        elif opcion == "13":
            print("Saliendo de AutoCore.")
            break
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    main()
