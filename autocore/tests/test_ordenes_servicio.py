import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import database.connection as connection
from database.connection import crear_tabla_clientes
from modules.clientes import registrar_cliente
from modules.ordenes_servicio import (
    actualizar_observaciones_orden,
    actualizar_estado_orden,
    buscar_orden_por_id,
    consultar_ordenes_por_vehiculo,
    consultar_ordenes_servicio,
    crear_tabla_ordenes_servicio,
    registrar_orden_servicio,
    validar_estado,
    validar_orden_servicio,
)
from modules.vehiculos import crear_tabla_vehiculos, registrar_vehiculo


class TestOrdenesServicio(unittest.TestCase):
    def setUp(self):
        # Cada prueba usa una base temporal para no modificar autocore.db.
        self.temp_dir = tempfile.TemporaryDirectory(dir=PROJECT_ROOT)
        self.db_path = Path(self.temp_dir.name) / "autocore_test.db"
        connection.DB_PATH = self.db_path

        crear_tabla_clientes()
        crear_tabla_vehiculos()
        crear_tabla_ordenes_servicio()

        registrar_cliente("Juan Perez", "5551234567", "juan@email.com", "Calle 1")
        registrar_vehiculo(1, "Nissan", "Versa", 2020, "ABC123", "Rojo")
        registrar_vehiculo(1, "Toyota", "Corolla", 2021, "DEF456", "Azul")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_crear_tabla_ordenes_genera_base_de_datos(self):
        self.assertTrue(self.db_path.exists())

    def test_consultar_ordenes_sin_registros_devuelve_lista_vacia(self):
        self.assertEqual([], consultar_ordenes_servicio())

    def test_registrar_orden_con_datos_validos(self):
        exito, mensaje = registrar_orden_servicio(
            1, "Cambio de aceite", "2026-07-13", "pendiente", "Sin observaciones"
        )

        orden = consultar_ordenes_servicio()[0]

        self.assertTrue(exito)
        self.assertIn("Orden de servicio registrada correctamente", mensaje)
        self.assertEqual(1, orden[1])
        self.assertEqual("Cambio de aceite", orden[2])
        self.assertEqual("2026-07-13", orden[3])
        self.assertEqual("pendiente", orden[4])
        self.assertEqual("Sin observaciones", orden[5])

    def test_registrar_orden_con_estado_por_defecto(self):
        registrar_orden_servicio(1, "Revision general", "2026-07-13")

        orden = consultar_ordenes_servicio()[0]

        self.assertEqual("pendiente", orden[4])
        self.assertEqual("", orden[5])

    def test_error_al_registrar_orden_sin_id_vehiculo(self):
        exito, mensaje = registrar_orden_servicio(
            None, "Cambio de aceite", "2026-07-13"
        )

        self.assertFalse(exito)
        self.assertEqual("El ID del vehiculo es obligatorio.", mensaje)
        self.assertEqual([], consultar_ordenes_servicio())

    def test_error_al_registrar_orden_con_id_vehiculo_no_entero(self):
        exito, mensaje = registrar_orden_servicio(
            "abc", "Cambio de aceite", "2026-07-13"
        )

        self.assertFalse(exito)
        self.assertEqual("El ID del vehiculo debe ser un numero entero.", mensaje)

    def test_error_al_registrar_orden_con_vehiculo_inexistente(self):
        exito, mensaje = registrar_orden_servicio(
            99, "Cambio de aceite", "2026-07-13"
        )

        self.assertFalse(exito)
        self.assertEqual("No existe un vehiculo con ese ID.", mensaje)

    def test_error_al_registrar_orden_sin_descripcion(self):
        exito, mensaje = registrar_orden_servicio(1, "", "2026-07-13")

        self.assertFalse(exito)
        self.assertEqual("La descripcion es obligatoria.", mensaje)

    def test_error_al_registrar_orden_sin_fecha(self):
        exito, mensaje = registrar_orden_servicio(1, "Cambio de aceite", "")

        self.assertFalse(exito)
        self.assertEqual("La fecha es obligatoria.", mensaje)

    def test_error_al_registrar_orden_con_estado_invalido(self):
        exito, mensaje = registrar_orden_servicio(
            1, "Cambio de aceite", "2026-07-13", "cerrada"
        )

        self.assertFalse(exito)
        self.assertEqual("El estado de la orden no es valido.", mensaje)

    def test_registrar_orden_elimina_espacios(self):
        registrar_orden_servicio(
            1,
            "  Afinacion  ",
            "  2026-07-13  ",
            "pendiente",
            "  Cliente espera llamada  ",
        )

        orden = consultar_ordenes_servicio()[0]

        self.assertEqual("Afinacion", orden[2])
        self.assertEqual("2026-07-13", orden[3])
        self.assertEqual("Cliente espera llamada", orden[5])

    def test_consultar_ordenes_por_vehiculo(self):
        registrar_orden_servicio(1, "Cambio de aceite", "2026-07-13")
        registrar_orden_servicio(2, "Revision de frenos", "2026-07-14")

        ordenes_vehiculo_1 = consultar_ordenes_por_vehiculo(1)

        self.assertEqual(1, len(ordenes_vehiculo_1))
        self.assertEqual("Cambio de aceite", ordenes_vehiculo_1[0][2])

    def test_vehiculo_puede_tener_varias_ordenes(self):
        registrar_orden_servicio(1, "Cambio de aceite", "2026-07-13")
        registrar_orden_servicio(1, "Revision electrica", "2026-07-14")

        self.assertEqual(2, len(consultar_ordenes_por_vehiculo(1)))

    def test_buscar_orden_por_id_existente(self):
        registrar_orden_servicio(1, "Cambio de aceite", "2026-07-13")

        orden = buscar_orden_por_id(1)

        self.assertIsNotNone(orden)
        self.assertEqual("Cambio de aceite", orden[2])

    def test_buscar_orden_por_id_inexistente_devuelve_none(self):
        self.assertIsNone(buscar_orden_por_id(99))

    def test_actualizar_estado_orden_existente(self):
        registrar_orden_servicio(1, "Cambio de aceite", "2026-07-13")

        exito, mensaje = actualizar_estado_orden(1, "en_proceso")
        orden = buscar_orden_por_id(1)

        self.assertTrue(exito)
        self.assertEqual("Estado de la orden actualizado correctamente.", mensaje)
        self.assertEqual("en_proceso", orden[4])

    def test_error_al_actualizar_estado_de_orden_inexistente(self):
        exito, mensaje = actualizar_estado_orden(99, "finalizada")

        self.assertFalse(exito)
        self.assertEqual("No existe una orden con ese ID.", mensaje)

    def test_error_al_actualizar_estado_invalido(self):
        registrar_orden_servicio(1, "Cambio de aceite", "2026-07-13")

        exito, mensaje = actualizar_estado_orden(1, "cerrada")

        self.assertFalse(exito)
        self.assertEqual("El estado de la orden no es valido.", mensaje)
        self.assertEqual("pendiente", buscar_orden_por_id(1)[4])

    def test_validar_estado_correcto(self):
        es_valido, mensaje = validar_estado("finalizada")

        self.assertTrue(es_valido)
        self.assertEqual("", mensaje)

    def test_validar_orden_con_datos_correctos(self):
        es_valida, mensaje = validar_orden_servicio(
            1, "Cambio de aceite", "2026-07-13", "pendiente"
        )

        self.assertTrue(es_valida)
        self.assertEqual("", mensaje)

    def test_ca_09_1_actualizar_observaciones_y_consultarlas(self):
        registrar_orden_servicio(
            1, "Cambio de aceite", "2026-07-13", "pendiente", "Sin revisar"
        )

        exito, mensaje = actualizar_observaciones_orden(
            1, "Se reemplazo el filtro de aceite"
        )
        orden = buscar_orden_por_id(1)

        self.assertTrue(exito)
        self.assertEqual(
            "Observaciones de la orden actualizadas correctamente.", mensaje
        )
        self.assertEqual("Se reemplazo el filtro de aceite", orden[5])
        self.assertEqual("pendiente", orden[4])

    def test_ca_09_2_actualizar_observaciones_elimina_espacios_exteriores(self):
        registrar_orden_servicio(
            1, "Revision general", "2026-07-13", "en_proceso", "Pendiente"
        )

        exito, _ = actualizar_observaciones_orden(
            1, "  Se detecto desgaste en las balatas  "
        )

        self.assertTrue(exito)
        self.assertEqual(
            "Se detecto desgaste en las balatas", buscar_orden_por_id(1)[5]
        )
        self.assertEqual("en_proceso", buscar_orden_por_id(1)[4])

    def test_ca_09_3_rechazar_id_inexistente_sin_modificar_otras_ordenes(self):
        registrar_orden_servicio(
            1, "Cambio de aceite", "2026-07-13", "pendiente", "Original"
        )

        exito, mensaje = actualizar_observaciones_orden(99, "Nueva observacion")

        self.assertFalse(exito)
        self.assertEqual("No existe una orden con ese ID.", mensaje)
        self.assertEqual("Original", buscar_orden_por_id(1)[5])

    def test_ca_09_3_rechazar_observaciones_vacias_y_conservar_informacion(self):
        registrar_orden_servicio(
            1, "Cambio de aceite", "2026-07-13", "pendiente", "Original"
        )

        for observaciones in ("", "   "):
            with self.subTest(observaciones=repr(observaciones)):
                exito, mensaje = actualizar_observaciones_orden(1, observaciones)

                self.assertFalse(exito)
                self.assertEqual(
                    "Las observaciones no pueden estar vacias.", mensaje
                )
                self.assertEqual("Original", buscar_orden_por_id(1)[5])


if __name__ == "__main__":
    unittest.main()
