# Método de trabajo forense

Este procedimiento sigue las cuatro fases de **NIST SP 800-86, sección 3**:
recolección, examen, análisis e informe. La preservación acompaña todas las
fases. CSF 2.0 se usa para relacionar resultados de riesgo, no para sustituir
el procedimiento. La secuencia ejecutable y los criterios de aceptación están
en [guia-comprobacion-nist.md](guia-comprobacion-nist.md); el resultado actual,
en [informe-forense.md](informe-forense.md).

| Fase SP 800-86 | Aplicación aquí | Estado |
|---|---|---|
| Recolección (§3.1) | Identificar y comprobar archivos presentes y fuentes oficiales | Procedencia previa de muestras pendiente; no adquisición de equipos NHS |
| Examen (§3.2) | Recursos PE, referencias, ensamblado y decompilación | Realizado con alcance estático |
| Análisis (§3.3) | Contrastar hipótesis y fuentes; separar historia y observación | Documentado con límites |
| Informe (§3.4) | Conclusiones, método, fuentes y lo no demostrado | Informe académico actualizado |

## 1. Preparación y alcance

Lee el BRIEF y registra objetivo, responsable, fecha UTC, zona horaria de Windows,
versión/build del SO, herramientas y snapshot inicial. Utiliza exclusivamente
datos ficticios. Conserva por separado el contexto de Gemini y las fuentes oficiales.

El árbol local sugerido es `evidencias/originales/CASO-001/` para originales y
`evidencias/trabajo/CASO-001/` para copias. Ambas rutas están excluidas de Git.
Las plantillas versionadas están vacías de resultados.

## 2. Recepción e integridad

Asigna identificador a cada archivo recibido. Anota origen/URL, fecha de adquisición,
formato, tamaño, SHA-256, persona que lo recibió y permisos. Calcula el hash de
un contenedor y también del contenido si se extrae, conservando la relación.

```bash
sha256sum evidencias/originales/CASO-001/archivo
```

No modifiques los originales. Usa copias para importar en herramientas y comprueba
hashes antes/después de transferirlas. Un hash acredita coincidencia de bytes;
por sí solo no demuestra quién creó el archivo ni su vínculo con el NHS.

## 3. Análisis estático en Ghidra

1. La sesión comprobada usa Ghidra en el anfitrión Linux y un proyecto bajo
   `local/ghidra/`; no en una VM Windows instalada. Para futuras adquisiciones,
   preserva originales y trabaja con copias identificadas. Registra SHA-256,
   formato, arquitectura y versión de Ghidra; no ejecutes las muestras.
2. Ejecuta el análisis automático. Revisa imports, strings, secciones y recursos.
3. Sigue referencias cruzadas a las APIs relevantes. Documenta dirección de
   función, llamadas, condiciones y limitaciones del decompilador.
4. Para cada hipótesis (archivo creado, servicio, comunicación o modificación de
   configuración), registra qué artefacto permitiría corroborarla y cómo buscarlo.
5. Guarda capturas y exportaciones identificadas. Distingue función observada de
   nombre asignado por el analista. No presupongas imports ni rutas idénticas en variantes.

FLOSS y Strings ayudan a recuperar cadenas; encontrar una cadena no acredita
que esa ruta del programa se haya ejecutado. No se incluyen modificaciones del
binario, evasión ni instrucciones para forzar su ejecución.

## 4. Captura de una línea base limpia

Antes de cualquier experimento, practica la recolección en Windows recién
instalado. Los siguientes comandos se ejecutan **dentro de la VM**, en PowerShell
elevado. No equivalen a una imagen forense completa:

```powershell
New-Item -ItemType Directory -Force C:\Forense\Captura
Get-Date -Format o | Out-File C:\Forense\Captura\hora.txt
Get-TimeZone | Format-List * | Out-File C:\Forense\Captura\zona.txt
Get-ComputerInfo | Out-File C:\Forense\Captura\equipo.txt
Get-Process | Select-Object Id,ProcessName,Path | Export-Csv C:\Forense\Captura\procesos.csv -NoTypeInformation
wevtutil epl System C:\Forense\Captura\System.evtx
wevtutil epl Security C:\Forense\Captura\Security.evtx
# Solo si Sysmon se instaló y el canal existe:
wevtutil epl Microsoft-Windows-Sysmon/Operational C:\Forense\Captura\Sysmon.evtx
Get-ChildItem C:\Forense\Captura -File | Get-FileHash -Algorithm SHA256 |
  Export-Csv C:\Forense\hashes-captura.csv -NoTypeInformation
```

La captura en vivo altera el sistema: registra los comandos y sus tiempos en
la bitácora. Los comandos anteriores están documentados pero todavía no se han
ejecutado en el Windows de este laboratorio.

## 5. RAM, disco y timeline

Para RAM, WinPmem ofrece adquisición desde Windows; valida primero su controlador
en la VM limpia. Su [proyecto oficial](https://github.com/Velocidex/WinPmem)
documenta uso y limitaciones. Registra la versión exacta, permisos y hash del volcado.
Un `.sav` de VirtualBox no debe renombrarse como `.raw`: no son formatos equivalentes.

Volatility 3 se instala localmente en `local/analysis-env`, aislado del Python del
sistema. Con un volcado compatible y una copia de trabajo:

```bash
local/analysis-env/bin/python descargas/volatility3/vol.py -f /ruta/copia-memoria.raw windows.info
local/analysis-env/bin/python descargas/volatility3/vol.py -f /ruta/copia-memoria.raw windows.pslist
```

Los símbolos de Windows dependen de la build capturada. No se descargó un juego
de símbolos específico porque aún no existe un volcado. Documenta si Volatility
necesita recuperarlos antes de exigir análisis totalmente offline. No subas el
volcado a servicios externos para resolver dependencias.

Para disco, preserva una copia con la VM apagada y registra los hashes. La
adquisición lógica, el VDI y una imagen física no se presentan como equivalentes.
El procedimiento definitivo depende del formato y herramienta que acepte el docente.

Normaliza timestamps a UTC, conserva el valor y zona originales y registra
desfases del reloj. Correlaciona logs, archivos, memoria y observaciones estáticas
en `plantillas/timeline.csv`; las ausencias no demuestran que no ocurrió un evento.

## 6. Informe

Cada hallazgo debe enlazar: pregunta → fuente o evidencia → método → observación
→ interpretación → limitación → resultado CSF propuesto. Identifica explícitamente
qué proviene del NHS, qué de la VM y qué continúa siendo hipótesis.

Estructura sugerida: objetivo y alcance; fuentes del caso; laboratorio y custodia;
análisis estático; adquisición y correlación; matriz CSF; recuperación y lecciones;
conclusiones sustentadas; anexos de hashes, bitácoras y capturas.
