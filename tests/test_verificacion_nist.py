"""Rechaza integridad falsa, material ausente y atribuciones automáticas de cumplimiento."""
import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('verificar', Path(__file__).resolve().parents[1] / 'scripts/verificar_caso_nist.py')
verificar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verificar)


class TestComprobacionNIST(unittest.TestCase):
    def test_cambio_de_bytes_y_tamano_no_pasa(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'copia').write_bytes(b'original')
            expected = hashlib.sha256(b'original').hexdigest()
            self.assertEqual(verificar.check_file(root, 'copia', expected, 8)['estado'], 'VERIFICADO')
            self.assertEqual(verificar.check_file(root, 'copia', expected, 9)['estado'], 'ERROR')
            (root / 'copia').write_bytes(b'alterado')
            self.assertEqual(verificar.check_file(root, 'copia', expected, 8)['estado'], 'ERROR')

    def test_ausencia_no_se_interpreta_como_verificacion(self):
        with tempfile.TemporaryDirectory() as folder:
            result = verificar.check_file(Path(folder), 'ausente', '0' * 64)
            self.assertEqual(result['estado'], 'PENDIENTE')

    def test_no_lee_fuera_del_expediente(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(verificar.check_file(Path(folder), '../ajeno', '0' * 64)['estado'], 'ERROR')

    def test_rechaza_codigos_inventados_y_cumplimiento_no_sustentado(self):
        row = dict(id='N-X', subcategoria='RS.AN-99', fuente_localizador='Fuente §1',
                   criterio_comprobacion='Revisar material', estado_historico='NO_EVALUADO',
                   estado_local='CUMPLE', limitacion='Sin evidencia')
        errors = verificar.validate_matrix([row], {'RS.AN-07'})
        self.assertTrue(any('Subcategoría' in e for e in errors))
        self.assertTrue(any('Estado local' in e for e in errors))

    def test_rechaza_filas_duplicadas_y_sin_limites(self):
        row = dict(id='N-X', subcategoria='RS.AN-07', fuente_localizador='CSF §A',
                   criterio_comprobacion='Hash y procedencia', estado_historico='NO_EVALUADO',
                   estado_local='PARCIAL', limitacion='')
        errors = verificar.validate_matrix([row, row], {'RS.AN-07'})
        self.assertTrue(any('duplicado' in e for e in errors))
        self.assertTrue(any('incompleta' in e for e in errors))
