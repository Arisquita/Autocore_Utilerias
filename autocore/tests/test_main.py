import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import database.connection as connection
import main as main_app
from modules.clientes import buscar_cliente_por_id
from modules.ordenes_servicio import buscar_orden_por_id
from modules.vehiculos import buscar_vehiculo_por_id


class TestMain(unittest.TestCase):
    def setUp(self):
        self.db_path_original = connection.DB_PATH
        self.temp_dir = tempfile.TemporaryDirectory(dir=PROJECT_ROOT)
        connection.DB_PATH = Path(self.temp_dir.name) / "autocore_menu.db"

    def tearDown(self):
        connection.DB_PATH = self.db_path_original
        self.temp_dir.cleanup()

    def test_menu_ejecuta_rf_01_a_rf_09_con_base_temporal(self):
        entradas = [
            "1", "Ana Lopez", "5551112233", "ana@email.com", "Calle 1",
            "2",
            "3", "1", "Ana Lopez Ruiz", "5559998877", "ana.ruiz@email.com", "Calle 2",
            "4", "1", "Nissan", "Versa", "2022", "ABC123", "Azul",
            "8", "1", "Revision general", "2026-08-08", "pendiente", "Revision inicial",
            "9",
            "11", "1", "en_proceso",
            "12", "1", "Trabajo iniciado",
            "9",
            "13",
        ]

        salida = io.StringIO()
        with patch("builtins.input", side_effect=entradas), redirect_stdout(salida):
            main_app.main()

        cliente = buscar_cliente_por_id(1)
        vehiculo = buscar_vehiculo_por_id(1)
        orden = buscar_orden_por_id(1)

        self.assertEqual("Ana Lopez Ruiz", cliente[1])
        self.assertEqual(1, vehiculo[1])
        self.assertEqual(1, orden[1])
        self.assertEqual("en_proceso", orden[4])
        self.assertEqual("Trabajo iniciado", orden[5])
        self.assertIn("Saliendo de AutoCore.", salida.getvalue())


if __name__ == "__main__":
    unittest.main()
