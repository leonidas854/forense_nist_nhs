### 11.4 Ejecución benigna comprobada en Windows

El 20 de noviembre de 2026, hora del anfitrión en Bolivia, se ejecutó una práctica
en `forense-nhs-win10-copia`. Se utilizó el Windows existente clonado, con un
snapshot previo y los ocho adaptadores de VirtualBox desactivados. Se mantuvieron
inhabilitados comparticiones, portapapeles, transferencia por portapapeles,
arrastrar/soltar, USB y VRDE. Los puertos serie y paralelo también se observaron
desactivados. El original del usuario no se utilizó para ejecutar la prueba.

La entrada fue un DVD virtual de solo lectura con `prueba_benigna.ps1`. El script
está publicado en `scripts/windows/` y su SHA-256 se cotejó con el mostrado dentro
del invitado: **97c2861a384dcc49194fde88ff0b5c5ce11c5e649c329c32cac7cd4e1cf4eaa1**.
No contiene WannaCry ni ejecuta sus comandos. La opción de política de ejecución
se limitó al proceso de PowerShell de la práctica; no se cambió la política
persistente de Windows.

### Procedimiento ejecutado y resultado

| Paso real | Comprobación | Resultado observado |
|---|---|---|
| Consultar adaptadores en el invitado | Win32_NetworkAdapter, propiedad NetEnabled | Cero adaptadores habilitados |
| Crear referencia y copia | Texto ficticio en una carpeta nueva; SHA-256 | Copia igual a referencia |
| Modificar solo el archivo de trabajo | Recalcular SHA-256 | Cambio detectado |
| Restaurar desde la copia | Comparar hash y contenido leído | Coincidencia con la referencia |
| Abrir Bloc de notas sobre ese texto | Get-Process sobre el PID devuelto e interfaz lista | Proceso notepad observado |
| Solicitar cierre normal | Esperar salida y consultar resultado | Proceso terminado, código de salida cero |

La herramienta efectivamente usada fue Windows PowerShell 5.1.18362.145, con
Get-FileHash, consultas locales del sistema y Bloc de notas. La consola mostró
el estado COMPLETADO. El uso de estas herramientas no acredita la validación
de los paquetes descargados de Ghidra, Sysinternals, WinPmem o Volatility dentro
de Windows; esa validación permanece pendiente.

| Objeto ficticio | SHA-256 observado |
|---|---|
| Referencia | 273891F95D948B6F3BF4A103AF64672960E971332E17946182CDA8FBD7F4CC15 |
| Archivo modificado | 5FE5FBE5029A405C9302BECAFA00346971F0CD374603E866665BE63BC880D6F6 |
| Archivo restaurado | 273891F95D948B6F3BF4A103AF64672960E971332E17946182CDA8FBD7F4CC15 |

Los hashes de referencia y modificación se calcularon también en el anfitrión
sobre los mismos textos y codificación, y coincidieron. Este cotejo comprueba
la consistencia del ejercicio; no convierte el texto ficticio en evidencia del
NHS. La copia de prueba estaba en el mismo disco virtual: no se presenta como
un respaldo independiente protegido frente a ransomware.

### Registro, horas y preservación

El script guardó `resultado.json` y `resultado.sha256` dentro de la carpeta nueva
`%LOCALAPPDATA%\NHS_Forense_Practica\`, con identificador propio. Se volvió a leer
el JSON y se mostró su hash en la consola del invitado. No se exportó ese archivo
al anfitrión mediante redes o carpetas compartidas.

En el anfitrión se conservaron las capturas de pantalla, el script, comprobaciones
de aislamiento y una transcripción manual identificada expresamente como tal en
`local/practica-windows/20261121T0350Z/`. Las capturas y registros originales
permanecen fuera de Git. La edición anterior de los informes también se preservó
localmente antes de incorporar los resultados.

Se detectó que el UTC informado por el invitado estaba **aproximadamente cinco
horas atrasado respecto del anfitrión**. Se consultó el reloj entre dos marcas
temporales del anfitrión y se observó la zona Romance Standard Time en Windows.
No se corrigieron los tiempos originales ni se atribuyó precisión absoluta al
reloj del anfitrión. Una cronología conjunta debe conservar esa diferencia e
incertidumbre; no se deben ordenar directamente ambos registros como si sus
relojes estuvieran sincronizados.

### Alcance metodológico

Los datos son ficticios (S), mientras que su procesamiento y los resultados de
esta sesión son observaciones locales reales (L). SP 800-86 organiza la
identificación, examen, interpretación y reporte. RS.AN-06 y RS.AN-07 ayudan a
explicar registro, integridad y procedencia. PR.DS-11 y RC.RP-03 se relacionan
parcialmente con la copia y restauración; RC.RP-05 requiere además validación
funcional del servicio, que aquí no se realizó.

La prueba demuestra detección de un cambio, restauración de un archivo ficticio
y observación de un proceso benigno. **No es una detonación de WannaCry, un ensayo
de cifrado ni una recuperación hospitalaria.** Se cerró Windows y se comprobó
de nuevo el aislamiento. La ausencia de interfaces habilitadas es una
comprobación concreta de configuración, no una garantía absoluta sobre el
hipervisor o la limpieza previa del sistema clonado.
