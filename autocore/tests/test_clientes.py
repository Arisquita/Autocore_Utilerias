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
    editar_cliente,
    registrar_cliente,
    validar_cliente,
)


class TestClientes(unittest.TestCase):
    def setUp(self):
        # Cada prueba usa una base temporal para no modificar autocore.db.
        self.temp_dir = tempfile.TemporaryDirectory(dir=PROJECT_ROOT)
        self.db_path = Path(self.temp_dir.name) / "autocore_test.db"
        connection.DB_PATH = self.db_path
        crear_tabla_clientes()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_01_crear_tabla_clientes_genera_base_de_datos(self):
        self.assertTrue(self.db_path.exists())

    def test_02_consultar_clientes_sin_registros_devuelve_lista_vacia(self):
        self.assertEqual([], consultar_clientes())

    def test_03_registrar_cliente_con_datos_validos(self):
        exito, mensaje = registrar_cliente(
            "Juan Perez", "5551234567", "juan@email.com", "Calle Centro 123"
        )

        clientes = consultar_clientes()

        self.assertTrue(exito)
        self.assertIn("Cliente registrado correctamente", mensaje)
        self.assertEqual(1, len(clientes))
        self.assertEqual("Juan Perez", clientes[0][1])
        self.assertEqual("5551234567", clientes[0][2])
        self.assertEqual("juan@email.com", clientes[0][3])
        self.assertEqual("Calle Centro 123", clientes[0][4])

    def test_04_registrar_cliente_con_datos_limite_minimos(self):
        exito, mensaje = registrar_cliente("A", "1")

        clientes = consultar_clientes()

        self.assertTrue(exito)
        self.assertIn("Cliente registrado correctamente", mensaje)
        self.assertEqual("A", clientes[0][1])
        self.assertEqual("1", clientes[0][2])
        self.assertEqual("", clientes[0][3])
        self.assertEqual("", clientes[0][4])

    def test_05_registrar_cliente_sin_correo_ni_direccion(self):
        registrar_cliente("Laura Gomez", "5550001111")

        cliente = consultar_clientes()[0]

        self.assertEqual("", cliente[3])
        self.assertEqual("", cliente[4])

    def test_06_registrar_cliente_elimina_espacios_en_nombre_y_telefono(self):
        registrar_cliente("  Mario Lopez  ", "  5552223333  ")

        cliente = consultar_clientes()[0]

        self.assertEqual("Mario Lopez", cliente[1])
        self.assertEqual("5552223333", cliente[2])

    def test_07_registrar_cliente_elimina_espacios_en_correo_y_direccion(self):
        registrar_cliente(
            "Sofia Diaz", "5554445555", "  sofia@email.com  ", "  Avenida 45  "
        )

        cliente = consultar_clientes()[0]

        self.assertEqual("sofia@email.com", cliente[3])
        self.assertEqual("Avenida 45", cliente[4])

    def test_08_error_cuando_falta_el_nombre(self):
        exito, mensaje = registrar_cliente("", "5551234567")

        self.assertFalse(exito)
        self.assertEqual("El nombre es obligatorio.", mensaje)
        self.assertEqual([], consultar_clientes())

    def test_09_error_cuando_nombre_solo_tiene_espacios(self):
        exito, mensaje = registrar_cliente("   ", "5551234567")

        self.assertFalse(exito)
        self.assertEqual("El nombre es obligatorio.", mensaje)

    def test_10_error_cuando_falta_el_telefono(self):
        exito, mensaje = registrar_cliente("Juan Perez", "")

        self.assertFalse(exito)
        self.assertEqual("El telefono es obligatorio.", mensaje)
        self.assertEqual([], consultar_clientes())

    def test_11_error_cuando_telefono_solo_tiene_espacios(self):
        exito, mensaje = registrar_cliente("Juan Perez", "   ")

        self.assertFalse(exito)
        self.assertEqual("El telefono es obligatorio.", mensaje)

    def test_12_error_cuando_nombre_es_none(self):
        exito, mensaje = registrar_cliente(None, "5551234567")

        self.assertFalse(exito)
        self.assertEqual("El nombre es obligatorio.", mensaje)

    def test_13_error_cuando_telefono_es_none(self):
        exito, mensaje = registrar_cliente("Juan Perez", None)

        self.assertFalse(exito)
        self.assertEqual("El telefono es obligatorio.", mensaje)

    def test_14_registrar_dos_clientes_asigna_ids_diferentes(self):
        registrar_cliente("Cliente Uno", "111")
        registrar_cliente("Cliente Dos", "222")

        clientes = consultar_clientes()

        self.assertEqual(1, clientes[0][0])
        self.assertEqual(2, clientes[1][0])

    def test_15_consultar_clientes_respeta_orden_por_id(self):
        registrar_cliente("Cliente B", "222")
        registrar_cliente("Cliente A", "111")

        clientes = consultar_clientes()

        self.assertEqual("Cliente B", clientes[0][1])
        self.assertEqual("Cliente A", clientes[1][1])

    def test_16_buscar_cliente_por_id_existente(self):
        registrar_cliente("Andrea Ruiz", "5559998888")

        cliente = buscar_cliente_por_id(1)

        self.assertIsNotNone(cliente)
        self.assertEqual("Andrea Ruiz", cliente[1])

    def test_17_buscar_cliente_por_id_inexistente_devuelve_none(self):
        self.assertIsNone(buscar_cliente_por_id(99))

    def test_18_editar_cliente_existente(self):
        registrar_cliente("Nombre Original", "5551112222", "a@email.com", "Dir 1")

        exito, mensaje = editar_cliente(1, "Nombre Editado", "5553334444", "b@email.com", "Dir 2")
        cliente = buscar_cliente_por_id(1)

        self.assertTrue(exito)
        self.assertEqual("Cliente actualizado correctamente.", mensaje)
        self.assertEqual("Nombre Editado", cliente[1])
        self.assertEqual("5553334444", cliente[2])
        self.assertEqual("b@email.com", cliente[3])
        self.assertEqual("Dir 2", cliente[4])

    def test_19_editar_cliente_inexistente_devuelve_error(self):
        exito, mensaje = editar_cliente(99, "Cliente", "5551234567")

        self.assertFalse(exito)
        self.assertEqual("No existe un cliente con ese ID.", mensaje)

    def test_20_editar_cliente_sin_nombre_devuelve_error(self):
        registrar_cliente("Cliente", "5551234567")

        exito, mensaje = editar_cliente(1, "", "5551234567")

        self.assertFalse(exito)
        self.assertEqual("El nombre es obligatorio.", mensaje)
        self.assertEqual("Cliente", buscar_cliente_por_id(1)[1])

    def test_21_editar_cliente_sin_telefono_devuelve_error(self):
        registrar_cliente("Cliente", "5551234567")

        exito, mensaje = editar_cliente(1, "Cliente Editado", "")

        self.assertFalse(exito)
        self.assertEqual("El telefono es obligatorio.", mensaje)
        self.assertEqual("5551234567", buscar_cliente_por_id(1)[2])

    def test_22_editar_cliente_elimina_espacios_en_campos(self):
        registrar_cliente("Cliente", "5551234567")

        editar_cliente(1, "  Cliente Editado  ", "  123  ", "  c@email.com  ", "  Calle 9  ")
        cliente = buscar_cliente_por_id(1)

        self.assertEqual("Cliente Editado", cliente[1])
        self.assertEqual("123", cliente[2])
        self.assertEqual("c@email.com", cliente[3])
        self.assertEqual("Calle 9", cliente[4])

    def test_23_validar_cliente_con_datos_correctos(self):
        es_valido, mensaje = validar_cliente("Cliente", "5551234567")

        self.assertTrue(es_valido)
        self.assertEqual("", mensaje)

    def test_24_validar_cliente_sin_nombre(self):
        es_valido, mensaje = validar_cliente("", "5551234567")

        self.assertFalse(es_valido)
        self.assertEqual("El nombre es obligatorio.", mensaje)

    def test_25_validar_cliente_sin_telefono(self):
        es_valido, mensaje = validar_cliente("Cliente", "")

        self.assertFalse(es_valido)
        self.assertEqual("El telefono es obligatorio.", mensaje)

    def test_26_registrar_cliente_con_caracteres_especiales(self):
        registrar_cliente("Jose Nunez", "+52-555-123-4567")

        cliente = consultar_clientes()[0]

        self.assertEqual("Jose Nunez", cliente[1])
        self.assertEqual("+52-555-123-4567", cliente[2])

    def test_27_registrar_cliente_con_nombre_largo(self):
        nombre_largo = "Cliente " + "Muy Largo " * 20

        registrar_cliente(nombre_largo, "5551234567")

        self.assertEqual(nombre_largo.strip(), consultar_clientes()[0][1])

    def test_28_editar_un_cliente_no_modifica_otros_clientes(self):
        registrar_cliente("Cliente Uno", "111")
        registrar_cliente("Cliente Dos", "222")

        editar_cliente(1, "Cliente Uno Editado", "333")
        cliente_dos = buscar_cliente_por_id(2)

        self.assertEqual("Cliente Dos", cliente_dos[1])
        self.assertEqual("222", cliente_dos[2])


if __name__ == "__main__":
    unittest.main()
