"""
Pruebas automatizadas para el analizador estático PE y generador HTML forense.
"""

import unittest
import os
import sys
import subprocess
import struct

# Agregar scripts al path para importación
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))

# Importamos directamente las funciones del analizador PE
analizador_pe = __import__("analisis-ghidra-pe")

class TestAnalisisPE(unittest.TestCase):

    def test_calcular_hashes(self):
        data = b"WannaCry Forensic Test Data"
        hashes = analizador_pe.calcular_hashes(data)
        self.assertIn("md5", hashes)
        self.assertIn("sha1", hashes)
        self.assertIn("sha256", hashes)
        self.assertEqual(len(hashes["sha256"]), 64)

    def test_analizar_cabecera_no_mz(self):
        with self.assertRaises(ValueError):
            analizador_pe.analizar_cabecera_pe(b"NOT_A_PE_FILE")

    def test_analizar_cabecera_pe_sintetica(self):
        # Construir una cabecera PE mínima sintética válida
        # MZ header (64 bytes)
        mz = bytearray(64)
        mz[0:2] = b'MZ'
        # e_lfanew en offset 60 -> apunta a offset 64
        struct.pack_into('<I', mz, 60, 64)

        # PE signature (4 bytes)
        pe_sig = b'PE\x00\x00'

        # File header (20 bytes): machine(x86=0x14c), num_sections(1), timedatestamp(0), opt_hdr_size(224), chars(0x102)
        file_hdr = struct.pack('<HHIIIHH', 0x14c, 1, 1494587039, 0, 0, 224, 0x102)

        # Optional header standard fields (magic=0x10b, entrypoint=0x1000, imagebase=0x400000)
        opt_hdr = bytearray(224)
        struct.pack_into('<H', opt_hdr, 0, 0x10b) # PE32
        struct.pack_into('<I', opt_hdr, 16, 0x1000) # Entry point
        struct.pack_into('<I', opt_hdr, 28, 0x400000) # Image base

        # Section header (40 bytes): name b'.text\x00\x00\x00', vsize, vaddr, raw_size, raw_offset
        sec_hdr = bytearray(40)
        sec_hdr[0:8] = b'.text\x00\x00\x00'
        struct.pack_into('<IIII', sec_hdr, 8, 0x1000, 0x1000, 0x1000, 0x200)

        raw_binary = bytes(mz) + pe_sig + file_hdr + bytes(opt_hdr) + bytes(sec_hdr)

        res = analizador_pe.analizar_cabecera_pe(raw_binary)
        self.assertEqual(res["machine"], "x86 (32-bit)")
        self.assertEqual(res["num_secciones"], 1)
        self.assertEqual(res["entry_point"], "0x1000")
        self.assertEqual(res["image_base"], "0x400000")
        self.assertEqual(len(res["secciones"]), 1)
        self.assertEqual(res["secciones"][0]["nombre"], ".text")

    def test_generador_reporte_html_ejecucion(self):
        script_path = os.path.join(BASE_DIR, "scripts", "generar-reporte-html.py")
        res = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Error ejecutando generar-reporte-html.py: {res.stderr}")
        self.assertIn("Datos cargados", res.stdout)
        self.assertIn("No se ha generado ni sincronizado el HTML", res.stdout)

if __name__ == "__main__":
    unittest.main()
