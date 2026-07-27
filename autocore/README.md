# AutoCore

AutoCore es un sistema de gestion para talleres mecanicos desarrollado para la
materia Desarrollo de Utilerias y Manejadores.

## Tecnologias

- Python
- SQLite
- Visual Studio Code
- unittest

## Modulos implementados

### Clientes

Requerimientos atendidos:

- RF-01 Registrar clientes.
- RF-02 Consultar clientes.
- RF-03 Editar informacion de clientes.

Historia relacionada:

- HU-01 Como recepcionista quiero registrar clientes para mantener organizada
  la informacion de las personas que utilizan los servicios del taller.

Funciones principales:

- Crear tabla `clientes`.
- Registrar cliente.
- Consultar clientes.
- Buscar cliente por ID.
- Editar cliente.
- Validar campos obligatorios.

### Vehiculos

El modulo de Vehiculos se relaciona directamente con Clientes. Un cliente puede
tener varios vehiculos, pero cada vehiculo debe pertenecer a un cliente
registrado.

Funciones principales:

- Crear tabla `vehiculos`.
- Registrar vehiculo.
- Consultar vehiculos.
- Consultar vehiculos por cliente.
- Buscar vehiculo por ID.
- Editar vehiculo.
- Validar que el cliente exista.
- Validar marca, modelo, placas y anio.

### Ordenes de Servicio

El modulo de Ordenes de Servicio se relaciona directamente con Vehiculos. Una
orden debe pertenecer a un vehiculo registrado y permite consultar o actualizar
el estado del trabajo.

Requerimientos atendidos:

- RF-06 Crear ordenes de servicio.
- RF-07 Consultar ordenes de servicio.
- RF-08 Actualizar el estado de una orden.
- RF-09 Actualizar observaciones de una orden de servicio.

Historias relacionadas:

- HU-03 Como recepcionista quiero crear ordenes de servicio para documentar el
  ingreso de un vehiculo al taller.
- HU-06 Como administrador quiero consultar el estado de las ordenes.
- HU-07 Como mecanico o asesor de servicio quiero actualizar las observaciones
  tecnicas de una orden para conservar evidencia de los hallazgos y trabajos
  realizados durante el servicio.

Funciones principales:

- Crear tabla `ordenes_servicio`.
- Registrar orden de servicio.
- Consultar ordenes de servicio.
- Consultar ordenes por vehiculo.
- Buscar orden por ID.
- Actualizar estado de orden.
- Actualizar observaciones de una orden.
- Validar que el vehiculo exista.
- Validar descripcion, fecha y estado.
- Rechazar observaciones vacias y validar que la orden exista antes de
  actualizarlas.

Trazabilidad de RF-09:

- RF-09 -> HU-07 -> CA-09.1 -> `test_ca_09_1_actualizar_observaciones_y_consultarlas`
  -> `modules/ordenes_servicio.py`.
- RF-09 -> HU-07 -> CA-09.2 ->
  `test_ca_09_2_actualizar_observaciones_elimina_espacios_exteriores`
  -> `modules/ordenes_servicio.py`.
- RF-09 -> HU-07 -> CA-09.3 ->
  `test_ca_09_3_rechazar_id_inexistente_sin_modificar_otras_ordenes` y
  `test_ca_09_3_rechazar_observaciones_vacias_y_conservar_informacion`
  -> `modules/ordenes_servicio.py`.

## Estructura del proyecto

```text
autocorp/
  database/
    connection.py
  modules/
    clientes.py
    vehiculos.py
    ordenes_servicio.py
  tests/
    test_clientes.py
    test_vehiculos.py
    test_ordenes_servicio.py
  main.py
  README.md
```

## Base de datos

El proyecto usa SQLite. Al ejecutar el sistema se genera automaticamente el
archivo:

```text
autocore.db
```

Tablas utilizadas:

- `clientes`
- `vehiculos`
- `ordenes_servicio`

## Como ejecutar el sistema

Desde la carpeta `autocorp`:

```powershell
python main.py
```

El menu de consola permite:

- Registrar clientes.
- Consultar clientes.
- Editar clientes.
- Registrar vehiculos.
- Consultar vehiculos.
- Consultar vehiculos por cliente.
- Editar vehiculos.
- Registrar ordenes de servicio.
- Consultar ordenes de servicio.
- Consultar ordenes por vehiculo.
- Actualizar estado de orden.
- Actualizar observaciones de una orden.

## Como ejecutar las pruebas

Desde la carpeta `autocorp`, ejecutar todas las pruebas:

```powershell
python -B -m unittest discover tests
```

Ejecutar solo pruebas de Clientes:

```powershell
python -B -m unittest tests.test_clientes
```

Ejecutar solo pruebas de Vehiculos:

```powershell
python -B -m unittest tests.test_vehiculos
```

Ejecutar solo pruebas de Ordenes de Servicio:

```powershell
python -B -m unittest tests.test_ordenes_servicio
```

## Alcance actual

Este avance incluye los modulos de Clientes, Vehiculos y Ordenes de Servicio.
No se incluye interfaz grafica.
