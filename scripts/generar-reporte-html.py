#!/usr/bin/env python3
"""
Inspector de datos CSV heredado. No genera ni sincroniza el dashboard HTML.

Uso:
    python3 scripts/generar-reporte-html.py
"""

import os
import csv
import sys

def cargar_csv(ruta):
    if not os.path.exists(ruta):
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    plantillas_dir = os.path.join(base_dir, "plantillas")
    docs_dir = os.path.join(base_dir, "docs")
    
    inventario = cargar_csv(os.path.join(plantillas_dir, "inventario-evidencias.csv"))
    hallazgos = cargar_csv(os.path.join(plantillas_dir, "hallazgos.csv"))
    timeline = cargar_csv(os.path.join(plantillas_dir, "timeline.csv"))
    matriz = cargar_csv(os.path.join(docs_dir, "matriz-nist.csv"))

    print(f"[+] Datos cargados: {len(inventario)} evidencias, {len(hallazgos)} hallazgos, {len(timeline)} eventos de timeline, {len(matriz)} categorías NIST.")
    
    destino_html = os.path.join(docs_dir, "dashboard-forense-nist.html")
    if os.path.exists(destino_html):
        print(f"[!] El archivo '{destino_html}' es una versión anterior pendiente de reconciliación.")
    else:
        print(f"[!] Aviso: No se encontró '{destino_html}'.")

    print("[!] Inspección terminada. No se ha generado ni sincronizado el HTML.")

if __name__ == "__main__":
    main()

