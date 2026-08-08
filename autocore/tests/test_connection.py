import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import database.connection as connection


class TestConnection(unittest.TestCase):
    def setUp(self):
        self.db_path_original = connection.DB_PATH
        self.temp_dir = tempfile.TemporaryDirectory(dir=PROJECT_ROOT)
        connection.DB_PATH = Path(self.temp_dir.name) / "autocore_test.db"

    def tearDown(self):
        connection.DB_PATH = self.db_path_original
        self.temp_dir.cleanup()

    def test_obtener_conexion_activa_claves_foraneas(self):
        conexion = connection.obtener_conexion()

        try:
            foreign_keys = conexion.execute("PRAGMA foreign_keys").fetchone()[0]
        finally:
            conexion.close()

        self.assertEqual(1, foreign_keys)


if __name__ == "__main__":
    unittest.main()
