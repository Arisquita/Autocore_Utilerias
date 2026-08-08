import sys
import sqlite3
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import database.connection as connection
from database.connection import crear_tabla_clientes
from modules.clientes import registrar_cliente
from modules.vehiculos import (
    buscar_vehiculo_por_id,
    consultar_vehiculos,
    consultar_vehiculos_por_cliente,
    crear_tabla_vehiculos,
    editar_vehiculo,
    registrar_vehiculo,
    validar_vehiculo,
)


class TestVehiculos(unittest.TestCase):
    def setUp(self):
        # Cada prueba usa una base temporal para no modificar autocore.db.
        self.temp_dir = tempfile.TemporaryDirectory(dir=PROJECT_ROOT)
        self.db_path = Path(self.temp_dir.name) / "autocore_test.db"
        connection.DB_PATH = self.db_path
        crear_tabla_clientes()
        crear_tabla_vehiculos()
        registrar_cliente("Juan Perez", "5551234567", "juan@email.com", "Calle 1")
        registrar_cliente("Ana Ruiz", "5557654321", "ana@email.com", "Calle 2")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_crear_tabla_vehiculos_genera_base_de_datos(self):
        self.assertTrue(self.db_path.exists())

    def test_consultar_vehiculos_sin_registros_devuelve_lista_vacia(self):
        self.assertEqual([], consultar_vehiculos())

    def test_sqlite_rechaza_vehiculo_con_cliente_inexistente(self):
        conexion = connection.obtener_conexion()

        try:
            with self.assertRaises(sqlite3.IntegrityError):
                conexion.execute(
                    """
                    INSERT INTO vehiculos (
                        id_cliente, marca, modelo, anio, placas, color
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (999, "Nissan", "Versa", 2022, "XYZ999", "Azul"),
                )
        finally:
            conexion.close()

    def test_registrar_vehiculo_con_datos_validos(self):
        exito, mensaje = registrar_vehiculo(1, "Nissan", "Versa", 2020, "ABC123", "Rojo")

        vehiculo = consultar_vehiculos()[0]

        self.assertTrue(exito)
        self.assertIn("Vehiculo registrado correctamente", mensaje)
        self.assertEqual(1, vehiculo[1])
        self.assertEqual("Nissan", vehiculo[2])
        self.assertEqual("Versa", vehiculo[3])
        self.assertEqual(2020, vehiculo[4])
        self.assertEqual("ABC123", vehiculo[5])
        self.assertEqual("Rojo", vehiculo[6])

    def test_registrar_vehiculo_con_datos_minimos(self):
        registrar_vehiculo(1, "Ford", "Fiesta", placas="XYZ987")

        vehiculo = consultar_vehiculos()[0]

        self.assertEqual("Ford", vehiculo[2])
        self.assertEqual("Fiesta", vehiculo[3])
        self.assertIsNone(vehiculo[4])
        self.assertEqual("XYZ987", vehiculo[5])
        self.assertEqual("", vehiculo[6])

    def test_error_al_registrar_sin_id_cliente(self):
        exito, mensaje = registrar_vehiculo(None, "Nissan", "Versa", 2020, "ABC123")

        self.assertFalse(exito)
        self.assertEqual("El ID del cliente es obligatorio.", mensaje)
        self.assertEqual([], consultar_vehiculos())

    def test_error_al_registrar_con_cliente_inexistente(self):
        exito, mensaje = registrar_vehiculo(99, "Nissan", "Versa", 2020, "ABC123")

        self.assertFalse(exito)
        self.assertEqual("No existe un cliente con ese ID.", mensaje)

    def test_error_al_registrar_sin_marca(self):
        exito, mensaje = registrar_vehiculo(1, "", "Versa", 2020, "ABC123")

        self.assertFalse(exito)
        self.assertEqual("La marca es obligatoria.", mensaje)

    def test_error_al_registrar_sin_modelo(self):
        exito, mensaje = registrar_vehiculo(1, "Nissan", "", 2020, "ABC123")

        self.assertFalse(exito)
        self.assertEqual("El modelo es obligatorio.", mensaje)

    def test_error_al_registrar_sin_placas(self):
        exito, mensaje = registrar_vehiculo(1, "Nissan", "Versa", 2020, "")

        self.assertFalse(exito)
        self.assertEqual("Las placas son obligatorias.", mensaje)

    def test_error_al_registrar_anio_no_numerico(self):
        exito, mensaje = registrar_vehiculo(1, "Nissan", "Versa", "dos mil", "ABC123")

        self.assertFalse(exito)
        self.assertEqual("El anio debe ser un numero entero.", mensaje)

    def test_registrar_vehiculo_elimina_espacios(self):
        registrar_vehiculo(1, "  Toyota  ", "  Corolla  ", "2021", "  DEF456  ", "  Azul  ")

        vehiculo = consultar_vehiculos()[0]

        self.assertEqual("Toyota", vehiculo[2])
        self.assertEqual("Corolla", vehiculo[3])
        self.assertEqual("DEF456", vehiculo[5])
        self.assertEqual("Azul", vehiculo[6])

    def test_consultar_vehiculos_por_cliente(self):
        registrar_vehiculo(1, "Nissan", "Versa", 2020, "ABC123")
        registrar_vehiculo(2, "Mazda", "3", 2022, "XYZ987")

        vehiculos_cliente_1 = consultar_vehiculos_por_cliente(1)

        self.assertEqual(1, len(vehiculos_cliente_1))
        self.assertEqual("Nissan", vehiculos_cliente_1[0][2])

    def test_cliente_puede_tener_varios_vehiculos(self):
        registrar_vehiculo(1, "Nissan", "Versa", 2020, "ABC123")
        registrar_vehiculo(1, "Toyota", "Corolla", 2021, "DEF456")

        self.assertEqual(2, len(consultar_vehiculos_por_cliente(1)))

    def test_buscar_vehiculo_por_id_existente(self):
        registrar_vehiculo(1, "Nissan", "Versa", 2020, "ABC123")

        vehiculo = buscar_vehiculo_por_id(1)

        self.assertIsNotNone(vehiculo)
        self.assertEqual("Nissan", vehiculo[2])

    def test_buscar_vehiculo_por_id_inexistente_devuelve_none(self):
        self.assertIsNone(buscar_vehiculo_por_id(99))

    def test_editar_vehiculo_existente(self):
        registrar_vehiculo(1, "Nissan", "Versa", 2020, "ABC123", "Rojo")

        exito, mensaje = editar_vehiculo(1, 1, "Toyota", "Corolla", 2021, "DEF456", "Azul")
        vehiculo = buscar_vehiculo_por_id(1)

        self.assertTrue(exito)
        self.assertEqual("Vehiculo actualizado correctamente.", mensaje)
        self.assertEqual("Toyota", vehiculo[2])
        self.assertEqual("Corolla", vehiculo[3])
        self.assertEqual(2021, vehiculo[4])
        self.assertEqual("DEF456", vehiculo[5])
        self.assertEqual("Azul", vehiculo[6])

    def test_error_al_editar_vehiculo_inexistente(self):
        exito, mensaje = editar_vehiculo(99, 1, "Toyota", "Corolla", 2021, "DEF456")

        self.assertFalse(exito)
        self.assertEqual("No existe un vehiculo con ese ID.", mensaje)

    def test_error_al_editar_con_cliente_inexistente(self):
        registrar_vehiculo(1, "Nissan", "Versa", 2020, "ABC123")

        exito, mensaje = editar_vehiculo(1, 99, "Toyota", "Corolla", 2021, "DEF456")

        self.assertFalse(exito)
        self.assertEqual("No existe un cliente con ese ID.", mensaje)

    def test_validar_vehiculo_con_datos_correctos(self):
        es_valido, mensaje = validar_vehiculo(1, "Nissan", "Versa", "ABC123", 2020)

        self.assertTrue(es_valido)
        self.assertEqual("", mensaje)

    def test_validar_vehiculo_con_id_cliente_no_entero(self):
        es_valido, mensaje = validar_vehiculo("abc", "Nissan", "Versa", "ABC123", 2020)

        self.assertFalse(es_valido)
        self.assertEqual("El ID del cliente debe ser un numero entero.", mensaje)


if __name__ == "__main__":
    unittest.main()
