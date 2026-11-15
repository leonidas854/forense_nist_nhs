#!/usr/bin/env python3
"""
Script pericial de inspección estática de binarios PE para el caso WannaCry.
Analiza cabeceras PE, secciones, calcula hashes y extrae cadenas forenses
sin requerir dependencias externas (utiliza únicamente la librería estándar de Python).

Uso:
    python3 scripts/analisis-ghidra-pe.py --help
    python3 scripts/analisis-ghidra-pe.py <ruta-al-ejecutable>
"""

import sys
import os
import struct
import hashlib
import re
import argparse

def calcular_hashes(datos: bytes) -> dict:
    return {
        "md5": hashlib.md5(datos).hexdigest(),
        "sha1": hashlib.sha1(datos).hexdigest(),
        "sha256": hashlib.sha256(datos).hexdigest()
    }

def analizar_cabecera_pe(datos: bytes) -> dict:
    if len(datos) < 64 or datos[:2] != b'MZ':
        raise ValueError("El archivo no posee cabecera MZ válida.")
    
    e_lfanew = struct.unpack('<I', datos[60:64])[0]
    if len(datos) < e_lfanew + 24 or datos[e_lfanew:e_lfanew+4] != b'PE\x00\x00':
        raise ValueError("No se encontró la firma PE válida.")
    
    file_header_offset = e_lfanew + 4
    machine, num_sections, timedatestamp, _, _, opt_hdr_size, characteristics = struct.unpack(
        '<HHIIIHH', datos[file_header_offset:file_header_offset+20]
    )
    
    opt_header_offset = file_header_offset + 20
    magic = struct.unpack('<H', datos[opt_header_offset:opt_header_offset+2])[0]
    is_pe32_plus = (magic == 0x20b)
    
    if is_pe32_plus:
        entry_point = struct.unpack('<I', datos[opt_header_offset+16:opt_header_offset+20])[0]
        image_base = struct.unpack('<Q', datos[opt_header_offset+24:opt_header_offset+32])[0]
    else:
        entry_point = struct.unpack('<I', datos[opt_header_offset+16:opt_header_offset+20])[0]
        image_base = struct.unpack('<I', datos[opt_header_offset+28:opt_header_offset+32])[0]
        
    sections_offset = opt_header_offset + opt_hdr_size
    secciones = []
    
    for i in range(num_sections):
        sec_hdr = sections_offset + (i * 40)
        sec_data = datos[sec_hdr:sec_hdr+40]
        if len(sec_data) < 40:
            break
        name = sec_data[:8].rstrip(b'\x00').decode('latin1', errors='replace')
        vsize, vaddr, raw_size, raw_offset = struct.unpack('<IIII', sec_data[8:24])
        secciones.append({
            "nombre": name,
            "vsize": vsize,
            "vaddr": hex(vaddr),
            "raw_size": raw_size,
            "raw_offset": hex(raw_offset)
        })
        
    return {
        "machine": "x86 (32-bit)" if machine == 0x14c else ("x64 (64-bit)" if machine == 0x8664 else hex(machine)),
        "num_secciones": num_sections,
        "timestamp_unix": timedatestamp,
        "entry_point": hex(entry_point),
        "image_base": hex(image_base),
        "secciones": secciones
    }

def buscar_cadenas_forenses(datos: bytes) -> dict:
    patrones = {
        "kill_switch_url": rb"http://www\.iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea\.com",
        "servicio_worm": rb"mssecsvc2\.0",
        "servicio_display": rb"Microsoft Security Center \(2\.0\) Service",
        "clave_zip_interna": rb"WNcry@2ol7",
        "antiforense_vssadmin": rb"vssadmin delete shadows",
        "antiforense_wbadmin": rb"wbadmin delete catalog",
        "cabecera_cifrado": rb"WANACRY!",
        "nota_rescate": rb"@Please_Read_Me@\.txt",
        "decryptor_gui": rb"@WanaDecryptor@\.exe"
    }
    
    hallazgos = {}
    for nombre, regex in patrones.items():
        matches = [m.start() for m in re.finditer(regex, datos, re.IGNORECASE)]
        hallazgos[nombre] = [hex(idx) for idx in matches]
    return hallazgos

def main():
    parser = argparse.ArgumentParser(
        description="Analizador estático de binarios PE para peritaje forense de WannaCry."
    )
    parser.add_argument("archivo", nargs="?", help="Ruta al binario PE a inspeccionar.")
    parser.add_argument("--json", action="store_true", help="Salida estructurada en JSON.")
    args = parser.parse_args()

    if not args.archivo:
        print("Uso: python3 scripts/analisis-ghidra-pe.py <archivo.exe>")
        print("Ejemplo: python3 scripts/analisis-ghidra-pe.py evidencias/originales/CASO-001/muestra.exe")
        sys.exit(1)

    if not os.path.isfile(args.archivo):
        print(f"Error: El archivo '{args.archivo}' no existe o no es accesible.")
        sys.exit(1)

    with open(args.archivo, "rb") as f:
        datos = f.read()

    hashes = calcular_hashes(datos)
    try:
        pe_info = analizar_cabecera_pe(datos)
    except Exception as e:
        pe_info = {"error": str(e)}

    cadenas = buscar_cadenas_forenses(datos)

    if args.json:
        import json
        resultado = {
            "archivo": os.path.basename(args.archivo),
            "tamano_bytes": len(datos),
            "hashes": hashes,
            "pe_header": pe_info,
            "cadenas_forenses": cadenas
        }
        print(json.dumps(resultado, indent=2))
    else:
        print("=" * 70)
        print("DICTAMEN PERICIAL: INSPECCIÓN ESTÁTICA PE (CASO WANNACRY)")
        print("=" * 70)
        print(f"Archivo:      {os.path.basename(args.archivo)}")
        print(f"Tamaño:       {len(datos):,} bytes")
        print(f"SHA-256:      {hashes['sha256']}")
        print(f"MD5:          {hashes['md5']}")
        print("-" * 70)
        print("CABECERA PORTABLE EXECUTABLE (PE):")
        if "error" in pe_info:
            print(f"  Aviso: {pe_info['error']}")
        else:
            print(f"  Arquitectura: {pe_info['machine']}")
            print(f"  ImageBase:    {pe_info['image_base']}")
            print(f"  EntryPoint:   {pe_info['entry_point']}")
            print(f"  Secciones:    {pe_info['num_secciones']}")
            for sec in pe_info['secciones']:
                print(f"    - {sec['nombre']:<8} VSize: {sec['vsize']:<8} RawSize: {sec['raw_size']:<8} Offset: {sec['raw_offset']}")
        print("-" * 70)
        print("DETECCIÓN DE PATRONES FORENSES CRÍTICOS:")
        for nombre, offsets in cadenas.items():
            estado = f"DETECTADO en {len(offsets)} offset(s): {', '.join(offsets)}" if offsets else "NO DETECTADO"
            print(f"  {nombre:<24}: {estado}")
        print("=" * 70)

if __name__ == "__main__":
    main()

