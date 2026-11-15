"""Las plantillas versionadas no deben contener adquisiciones ni resultados reales."""
import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestPlantillasForenses(unittest.TestCase):
    def test_esquemas_sin_evidencias_versionadas(self):
        required = {
            'inventario-evidencias.csv': {'id', 'archivo', 'origen', 'sha256', 'fecha_adquisicion_utc'},
            'cadena-custodia.csv': {'id_evidencia', 'fecha_utc', 'accion', 'sha256_verificado'},
            'bitacora.csv': {'fecha_utc', 'analista', 'accion_comando', 'resultado'},
            'hallazgos.csv': {'id', 'observacion', 'interpretacion', 'limitacion', 'categoria_csf'},
            'timeline.csv': {'timestamp_original', 'zona_original', 'timestamp_utc', 'confianza'},
        }
        for filename, fields in required.items():
            with self.subTest(archivo=filename):
                with (ROOT / 'plantillas' / filename).open(newline='') as stream:
                    reader = csv.DictReader(stream)
                    self.assertTrue(fields.issubset(reader.fieldnames))
                    self.assertEqual(list(reader), [], 'Guardar registros en local/, no en plantillas versionadas')

    def test_matriz_distingue_evaluaciones_y_limites(self):
        with (ROOT / 'docs/matriz-nist.csv').open(newline='') as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual({r['subcategoria'].split('.')[0] for r in rows}, {'GV', 'ID', 'PR', 'DE', 'RS', 'RC'})
        self.assertEqual(len({r['id'] for r in rows}), len(rows))
        for row in rows:
            for field in ['fuente_localizador', 'criterio_comprobacion', 'estado_historico', 'estado_local', 'limitacion']:
                self.assertTrue(row[field].strip(), f'Falta {field} en {row["id"]}')
