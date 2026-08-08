import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


PROCESO_REGISTRO = """
import sys
from pathlib import Path
import database.connection as connection
from database.connection import crear_tabla_clientes
from modules.clientes import registrar_cliente
from modules.ordenes_servicio import crear_tabla_ordenes_servicio, registrar_orden_servicio
from modules.vehiculos import crear_tabla_vehiculos, registrar_vehiculo

connection.DB_PATH = Path(sys.argv[1])
crear_tabla_clientes()
crear_tabla_vehiculos()
crear_tabla_ordenes_servicio()
assert registrar_cliente("Mario Soto", "5551234567")[0]
assert registrar_vehiculo(1, "Ford", "Focus", 2020, "PER123", "Gris")[0]
assert registrar_orden_servicio(1, "Afinacion", "2026-08-08")[0]
"""


PROCESO_CONSULTA = """
import sys
from pathlib import Path
import database.connection as connection
from modules.clientes import buscar_cliente_por_id
from modules.ordenes_servicio import buscar_orden_por_id
from modules.vehiculos import buscar_vehiculo_por_id

connection.DB_PATH = Path(sys.argv[1])
assert buscar_cliente_por_id(1)[1] == "Mario Soto"
assert buscar_vehiculo_por_id(1)[1] == 1
assert buscar_orden_por_id(1)[1] == 1
"""


class TestPersistencia(unittest.TestCase):
    def test_datos_persisten_entre_dos_procesos(self):
        with tempfile.TemporaryDirectory(dir=PROJECT_ROOT) as temp_dir:
            db_path = Path(temp_dir) / "autocore_persistencia.db"

            registro = subprocess.run(
                [sys.executable, "-B", "-c", PROCESO_REGISTRO, str(db_path)],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, registro.returncode, registro.stderr)

            consulta = subprocess.run(
                [sys.executable, "-B", "-c", PROCESO_CONSULTA, str(db_path)],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, consulta.returncode, consulta.stderr)


if __name__ == "__main__":
    unittest.main()
