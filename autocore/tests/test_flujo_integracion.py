import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import database.connection as connection
from database.connection import crear_tabla_clientes
from modules.clientes import (
    buscar_cliente_por_id,
    consultar_clientes,
    registrar_cliente,
)
from modules.ordenes_servicio import (
    actualizar_observaciones_orden,
    actualizar_estado_orden,
    buscar_orden_por_id,
    consultar_ordenes_servicio,
    crear_tabla_ordenes_servicio,
    registrar_orden_servicio,
)
from modules.vehiculos import (
    consultar_vehiculos_por_cliente,
    crear_tabla_vehiculos,
    registrar_vehiculo,
)


class TestFlujoIntegracion(unittest.TestCase):
    """Integra RF-01, RF-02 y RF-04 a RF-09 en un solo flujo.

    RF-03 no se ejecuta porque la edicion de clientes no forma parte del flujo
    principal aprobado para esta prueba de integracion.
    """

    def setUp(self):
        self.db_path_original = connection.DB_PATH
        self.temp_dir = tempfile.TemporaryDirectory(dir=PROJECT_ROOT)
        connection.DB_PATH = Path(self.temp_dir.name) / "autocore_integracion.db"

        crear_tabla_clientes()
        crear_tabla_vehiculos()
        crear_tabla_ordenes_servicio()

    def tearDown(self):
        connection.DB_PATH = self.db_path_original
        self.temp_dir.cleanup()

    def test_flujo_principal_persiste_relaciones_y_actualizaciones(self):
        # RF-01: registrar un cliente valido.
        cliente_creado, _ = registrar_cliente(
            "Laura Martinez",
            "5551234567",
            "laura@email.com",
            "Avenida Central 100",
        )
        self.assertTrue(cliente_creado)

        # RF-02: consultar clientes y obtener el ID generado.
        clientes = consultar_clientes()
        self.assertEqual(1, len(clientes))
        id_cliente = clientes[0][0]
        self.assertIsNotNone(buscar_cliente_por_id(id_cliente))

        # RF-04 y RF-05: registrar el vehiculo asociado al cliente.
        vehiculo_creado, _ = registrar_vehiculo(
            id_cliente, "Nissan", "Versa", 2022, "ABC123", "Azul"
        )
        self.assertTrue(vehiculo_creado)

        vehiculos_cliente = consultar_vehiculos_por_cliente(id_cliente)
        self.assertEqual(1, len(vehiculos_cliente))
        id_vehiculo = vehiculos_cliente[0][0]
        self.assertEqual(id_cliente, vehiculos_cliente[0][1])

        # RF-06: crear una orden asociada al vehiculo.
        orden_creada, _ = registrar_orden_servicio(
            id_vehiculo,
            "Revision del sistema de frenos",
            "2026-08-01",
            "pendiente",
            "Pendiente de revision",
        )
        self.assertTrue(orden_creada)

        # RF-07: consultar la orden creada y comprobar su asociacion.
        ordenes = consultar_ordenes_servicio()
        self.assertEqual(1, len(ordenes))
        orden = ordenes[0]
        id_orden = orden[0]
        self.assertEqual(id_vehiculo, orden[1])

        # RF-08: actualizar el estado de la orden.
        estado_actualizado, _ = actualizar_estado_orden(id_orden, "en_proceso")
        self.assertTrue(estado_actualizado)

        # RF-09: actualizar las observaciones de la orden.
        observaciones_actualizadas, _ = actualizar_observaciones_orden(
            id_orden, "Se detecto desgaste en las balatas"
        )
        self.assertTrue(observaciones_actualizadas)

        # RF-07: una nueva consulta debe recuperar ambos cambios desde SQLite.
        orden_actualizada = buscar_orden_por_id(id_orden)
        self.assertEqual(id_vehiculo, orden_actualizada[1])
        self.assertEqual("en_proceso", orden_actualizada[4])
        self.assertEqual(
            "Se detecto desgaste en las balatas", orden_actualizada[5]
        )
        self.assertTrue(connection.DB_PATH.exists())


if __name__ == "__main__":
    unittest.main()
