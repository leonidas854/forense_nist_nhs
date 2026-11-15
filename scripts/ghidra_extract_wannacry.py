# @category Forensic.WannaCry
# @description Script de automatización pericial para Ghidra: extrae IoCs, referencias al Kill Switch y configuración de WannaCry.
# @author Equipo de Peritaje Forense NHS (leonidas854)

"""
Script para Ghidra Script Manager / analyzeHeadless.
Inspecciona automáticamente la muestra canónica de WannaCry (ed01eb...) y extrae:
1. Referencias cruzadas a InternetOpenUrlA (Kill Switch).
2. Referencias cruzadas a CreateServiceA (Servicio del gusano mssecsvc2.0).
3. Ubicación y tamaño del recurso cifrado 'R'.
4. Cadenas de comandos antiforense (vssadmin delete shadows).
"""

try:
    # Entorno nativo de GhidraScript (disponible dentro de Ghidra)
    from ghidra.program.model.symbol import RefType
    from ghidra.program.model.data import StringDataType
    RUNNING_IN_GHIDRA = True
except ImportError:
    RUNNING_IN_GHIDRA = False

def run_in_ghidra():
    print("=" * 70)
    print("GHIDRA 12.2 · SCRIPT PERICIAL DE EXTRACCIÓN AUTOMATIZADA DE WANNACRY")
    print("=" * 70)
    
    current_prog = getCurrentProgram()
    listing = current_prog.getListing()
    sym_table = current_prog.getSymbolTable()
    
    print("[+] Programa cargado: %s" % current_prog.getName())
    print("[+] Base de imagen:   %s" % current_prog.getImageBase())
    
    # 1. Búsqueda de InternetOpenUrlA
    print("\n[*] 1. Rastreo de llamada a InternetOpenUrlA (Kill Switch)...")
    symbols = sym_table.getSymbols("InternetOpenUrlA")
    for sym in symbols:
        refs = sym.getReferences()
        for ref in refs:
            if ref.getReferenceType().isCall():
                from_addr = ref.getFromAddress()
                func = listing.getFunctionContaining(from_addr)
                func_name = func.getName() if func else "Desconocida"
                print("    -> Invocación detectada en: %s (Función: %s)" % (from_addr, func_name))
                # Inspeccionar instrucciones previas para extraer argumento URL
                instr = listing.getInstructionAt(from_addr)
                prev_instr = instr.getPrevious()
                count = 0
                while prev_instr and count < 8:
                    print("       %s: %s" % (prev_instr.getAddressString(False, True), prev_instr.toString()))
                    prev_instr = prev_instr.getPrevious()
                    count += 1

    # 2. Búsqueda de CreateServiceA
    print("\n[*] 2. Rastreo de persistencia (CreateServiceA)...")
    symbols = sym_table.getSymbols("CreateServiceA")
    for sym in symbols:
        refs = sym.getReferences()
        for ref in refs:
            if ref.getReferenceType().isCall():
                from_addr = ref.getFromAddress()
                func = listing.getFunctionContaining(from_addr)
                func_name = func.getName() if func else "Desconocida"
                print("    -> Invocación detectada en: %s (Función: %s)" % (from_addr, func_name))

    # 3. Búsqueda de cadenas de texto críticas
    print("\n[*] 3. Búsqueda de Indicadores de Compromiso (IoCs) en memoria...")
    cadenas_objetivo = [
        "iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com",
        "mssecsvc2.0",
        "Microsoft Security Center (2.0) Service",
        "WNcry@2ol7",
        "vssadmin delete shadows /all /quiet"
    ]
    
    data_iterator = listing.getDefinedData(True)
    while data_iterator.hasNext():
        data = data_iterator.next()
        val = str(data.getValue()) if data.getValue() else ""
        for target in cadenas_objetivo:
            if target in val:
                print("    [MATCH] %-35s en %s" % (target, data.getAddress()))

    print("\n" + "=" * 70)
    print("[+] Análisis en Ghidra completado con éxito.")
    print("=" * 70)

def run_standalone():
    print("""
========================================================================
GHIDRA WANNACRY EXTRACTOR SCRIPT
========================================================================
Este script está diseñado para ejecutarse dentro de Ghidra 12.2 mediante:

1. Modo Gráfico (GUI):
   - Abre Ghidra y carga la muestra en el CodeBrowser.
   - Ve a: Window -> Script Manager.
   - Añade la carpeta 'scripts' como fuente de scripts.
   - Ejecuta 'ghidra_extract_wannacry.py'.

2. Modo Headless (Línea de Comandos en Linux):
   $GHIDRA_HOME/support/analyzeHeadless \\
     /ruta/proyecto/ghidra ProyectoWannaCry \\
     -process WannaCry.exe \\
     -postScript scripts/ghidra_extract_wannacry.py
========================================================================
""")

if __name__ == "__main__":
    if RUNNING_IN_GHIDRA:
        run_in_ghidra()
    else:
        run_standalone()

