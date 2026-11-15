"""
Pruebas automatizadas de integridad para las plantillas forenses del caso NHS WannaCry.
Valida encabezados, tipos de datos, formato de hashes SHA-256 y marcas de tiempo UTC.
"""

import unittest
import csv
import os
import glob
import re

class TestPlantillasForenses(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.plantillas_dir = os.path.join(self.base_dir, "plantillas")

    def test_plantillas_existen(self):
        archivos_requeridos = [
            "inventario-evidencias.csv",
            "cadena-custodia.csv",
            "bitacora.csv",
            "hallazgos.csv",
            "timeline.csv"
        ]
        for archivo in archivos_requeridos:
            ruta = os.path.join(self.plantillas_dir, archivo)
            self.assertTrue(os.path.isfile(ruta), f"Falta la plantilla requerida: {archivo}")

    def test_inventario_evidencias_datos(self):
        ruta = os.path.join(self.plantillas_dir, "inventario-evidencias.csv")
        with open(ruta, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            self.assertGreaterEqual(len(reader), 10, "El inventario debe contener al menos 10 evidencias")
            sha256_regex = re.compile(r"^[a-f0-9]{64}$")
            for fila in reader:
                self.assertTrue(fila["id"].startswith("EVI-"), f"ID inválido: {fila['id']}")
                self.assertTrue(sha256_regex.match(fila["sha256"]), f"SHA-256 inválido en {fila['id']}: {fila['sha256']}")
                self.assertTrue(int(fila["tamano_bytes"]) > 0, f"Tamaño inválido en {fila['id']}")

    def test_cadena_custodia_datos(self):
        ruta = os.path.join(self.plantillas_dir, "cadena-custodia.csv")
        with open(ruta, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            self.assertGreaterEqual(len(reader), 10, "La cadena de custodia debe contener registros de trazabilidad")
            for fila in reader:
                self.assertTrue(fila["id_evidencia"].startswith("EVI-"))
                self.assertTrue(len(fila["sha256_verificado"]) == 64)
                self.assertTrue(len(fila["accion"]) > 0)

    def test_bitacora_datos(self):
        ruta = os.path.join(self.plantillas_dir, "bitacora.csv")
        with open(ruta, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            self.assertGreaterEqual(len(reader), 10, "La bitácora debe contener al menos 10 registros de comandos")
            for fila in reader:
                self.assertTrue("T" in fila["fecha_utc"] and fila["fecha_utc"].endswith("Z"))
                self.assertTrue(len(fila["accion_comando"]) > 0)
                self.assertTrue(len(fila["analista"]) > 0)

    def test_hallazgos_csf_categorias(self):
        ruta = os.path.join(self.plantillas_dir, "hallazgos.csv")
        categorias_validas = {"GV", "ID", "PR", "DE", "RS", "RC"}
        with open(ruta, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            self.assertGreaterEqual(len(reader), 10, "Deben existir al menos 10 hallazgos técnicos")
            for fila in reader:
                self.assertTrue(fila["id"].startswith("HAL-"))
                codigo_csf = fila["categoria_csf"].split(".")[0].split("-")[0]
                self.assertIn(codigo_csf, categorias_validas, f"Categoría CSF inválida: {fila['categoria_csf']}")

    def test_timeline_fechas_utc(self):
        ruta = os.path.join(self.plantillas_dir, "timeline.csv")
        with open(ruta, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            self.assertGreaterEqual(len(reader), 15, "La línea de tiempo debe contener al menos 15 hitos")
            for fila in reader:
                self.assertTrue("T" in fila["timestamp_utc"] and fila["timestamp_utc"].endswith("Z"))
                self.assertIn(fila["confianza"], {"alta", "media", "baja"})

if __name__ == "__main__":
    unittest.main()

