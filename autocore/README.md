# AutoCore

AutoCore es un sistema de gestión para talleres mecánicos desarrollado para la
materia Desarrollo de Utilerías y Manejadores.

## Tecnologías

- Python
- SQLite
- Visual Studio Code
- `unittest`

## Módulos implementados

### Clientes

El módulo `modules/clientes.py` permite registrar, consultar, buscar y editar
clientes, además de validar sus campos obligatorios.

### Vehículos

El módulo `modules/vehiculos.py` permite registrar, consultar, buscar y editar
vehículos. Cada vehículo debe asociarse con un cliente registrado y un cliente
puede tener varios vehículos.

### Órdenes de servicio

El módulo `modules/ordenes_servicio.py` permite crear y consultar órdenes,
consultarlas por vehículo y actualizar su estado y sus observaciones. Cada orden
debe pertenecer a un vehículo registrado.

## Requerimientos funcionales

- RF-01 Registrar clientes.
- RF-02 Consultar clientes.
- RF-03 Editar información de clientes.
- RF-04 Registrar vehículos.
- RF-05 Asociar vehículos con clientes.
- RF-06 Crear órdenes de servicio.
- RF-07 Consultar órdenes de servicio.
- RF-08 Actualizar el estado de una orden.
- RF-09 Actualizar observaciones de una orden de servicio.

### Trazabilidad

| Requerimiento | Historia de usuario | Criterio de aceptación principal | Prueba relacionada | Módulo responsable | Estado |
| --- | --- | --- | --- | --- | --- |
| RF-01 | HU-01: Como recepcionista quiero registrar clientes para mantener organizada la información de quienes utilizan el taller. | Un cliente con nombre y teléfono válidos se almacena y recibe un ID. | `test_03_registrar_cliente_con_datos_validos` y `test_flujo_principal_persiste_relaciones_y_actualizaciones` | `modules/clientes.py` | Implementado y probado |
| RF-02 | Como recepcionista quiero consultar clientes para recuperar sus datos. | La consulta devuelve los clientes almacenados, ordenados por ID. | `test_15_consultar_clientes_respeta_orden_por_id` y `test_flujo_principal_persiste_relaciones_y_actualizaciones` | `modules/clientes.py` | Implementado y probado |
| RF-03 | Como recepcionista quiero editar la información de un cliente para mantenerla actualizada. | Los cambios válidos se guardan para un cliente existente sin modificar otros registros. | `test_18_editar_cliente_existente` y `test_28_editar_un_cliente_no_modifica_otros_clientes` | `modules/clientes.py` | Implementado y probado individualmente |
| RF-04 | Como recepcionista quiero registrar vehículos para conservar sus datos en el sistema. | Un vehículo con datos válidos se almacena y recibe un ID. | `test_registrar_vehiculo_con_datos_validos` y `test_flujo_principal_persiste_relaciones_y_actualizaciones` | `modules/vehiculos.py` | Implementado y probado |
| RF-05 | Como recepcionista quiero asociar vehículos con clientes para identificar a su propietario. | El vehículo solo se registra con un cliente existente y puede recuperarse mediante la consulta por cliente. | `test_consultar_vehiculos_por_cliente`, `test_error_al_registrar_con_cliente_inexistente` y `test_flujo_principal_persiste_relaciones_y_actualizaciones` | `modules/vehiculos.py` | Implementado y probado |
| RF-06 | HU-03: Como recepcionista quiero crear órdenes de servicio para documentar el ingreso de un vehículo al taller. | Una orden válida se registra únicamente para un vehículo existente. | `test_registrar_orden_con_datos_validos`, `test_error_al_registrar_orden_con_vehiculo_inexistente` y `test_flujo_principal_persiste_relaciones_y_actualizaciones` | `modules/ordenes_servicio.py` | Implementado y probado |
| RF-07 | HU-06: Como administrador quiero consultar las órdenes de servicio para conocer la información y el avance del trabajo. | La consulta recupera la orden registrada y conserva su asociación con el vehículo. | `test_consultar_ordenes_por_vehiculo` y `test_flujo_principal_persiste_relaciones_y_actualizaciones` | `modules/ordenes_servicio.py` | Implementado y probado |
| RF-08 | Como mecánico o asesor de servicio quiero actualizar el estado de una orden para reflejar su avance. | Una orden existente acepta un estado válido y la consulta posterior devuelve el cambio. | `test_actualizar_estado_orden_existente` y `test_flujo_principal_persiste_relaciones_y_actualizaciones` | `modules/ordenes_servicio.py` | Implementado y probado |
| RF-09 | HU-07: Como mecánico o asesor de servicio quiero actualizar las observaciones técnicas para conservar evidencia de hallazgos y trabajos. | CA-09.1: Las observaciones válidas se guardan en una orden existente y pueden consultarse posteriormente. | `test_ca_09_1_actualizar_observaciones_y_consultarlas` y `test_flujo_principal_persiste_relaciones_y_actualizaciones` | `modules/ordenes_servicio.py` | Implementado y probado |

RF-09 también cuenta con cobertura para eliminar espacios exteriores, rechazar
IDs inexistentes y rechazar observaciones vacías mediante los casos CA-09.2 y
CA-09.3 de `tests/test_ordenes_servicio.py`.

## Requerimientos no funcionales

| Requerimiento | Categoría | Cumplimiento actual |
| --- | --- | --- |
| RNF-01 | Usabilidad | El sistema ofrece un menú de consola con opciones identificables para las operaciones disponibles. |
| RNF-02 | Persistencia | Los datos se almacenan en SQLite y permanecen disponibles para consultas posteriores. |
| RNF-03 | Integridad de datos | Las validaciones de campos y existencia de clientes, vehículos y órdenes protegen las relaciones entre registros. |
| RNF-04 | Mantenibilidad | La solución separa conexión, clientes, vehículos, órdenes de servicio y pruebas en módulos específicos. |
| RNF-05 | Pruebas | Las funciones cuentan con pruebas unitarias y con una prueba del flujo principal usando una base de datos temporal. |

## Flujo principal

El flujo integrado representa el recorrido operativo principal del sistema:

```text
Cliente → Vehículo → Orden → Estado → Observaciones → Consulta final
```

1. Se registra y consulta un cliente.
2. Se registra un vehículo asociado con ese cliente.
3. Se crea una orden asociada con el vehículo.
4. Se actualiza el estado de la orden.
5. Se actualizan sus observaciones.
6. Se realiza una consulta final que recupera las relaciones y los cambios
   persistidos.

RF-03 está implementado y probado individualmente en
`tests/test_clientes.py`, pero la edición de clientes no forma parte del flujo
principal de integración.

## Prueba de integración

`tests/test_flujo_integracion.py` contiene
`test_flujo_principal_persiste_relaciones_y_actualizaciones`, que ejecuta en un
solo escenario RF-01, RF-02 y RF-04 a RF-09. Durante la preparación de la prueba
se cambia temporalmente la ruta de conexión a una base SQLite creada para el
caso de prueba; al finalizar se restaura la ruta original y se elimina el
directorio temporal. De esta manera, la prueba no utiliza ni altera
`autocore.db`.

## Estructura del proyecto

```text
autocore/
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
    test_flujo_integracion.py
  main.py
  README.md
```

## Base de datos

El proyecto usa SQLite. Al ejecutar el sistema se genera automáticamente el
archivo `autocore.db`.

Tablas utilizadas:

- `clientes`
- `vehiculos`
- `ordenes_servicio`

## Cómo ejecutar el sistema

Desde la carpeta `autocore`:

```powershell
python main.py
```

## Cómo ejecutar las pruebas

Desde la carpeta `autocore`, ejecutar la suite completa:

```powershell
python -B -m unittest discover tests
```

Resultado registrado al cierre de la Semana 12:

```text
Ran 73 tests

OK
```

## Alcance actual

El cierre de la Semana 12 incluye RF-01 a RF-09 en los módulos de Clientes,
Vehículos y Órdenes de Servicio. No se incluye interfaz gráfica.

## Mejoras futuras

- Incorporar una interfaz gráfica conservando la separación actual por módulos.
- Ampliar los escenarios de integración y los casos de datos límite.
- Mejorar los mensajes y la navegación del menú de consola.
- Preparar documentación de instalación y distribución para otros entornos.
