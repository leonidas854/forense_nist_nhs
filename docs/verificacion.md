# Estado comprobado · 11 de noviembre de 2026

## Preparación realizada

- Cuenta de GitHub: `leonidas854`; repositorio `forense_nist_nhs`, privado.
- Vagrant 2.4.9 y VirtualBox 7.2.22 disponibles en el anfitrión.
- Box local `nhs/windows10-installer` creada y registrada; contiene hardware vacío.
- VM `forense-nhs-win10`, con archivos en `local/vms/`, importada mediante Vagrant.
- Arranque real del instalador de Windows 10 x64 en español comprobado.
  [Captura de la consola](capturas/windows-installer.png).
- Red e integraciones con el anfitrión desactivadas, comprobadas con
  `VBoxManage showvminfo` y `scripts/check_isolation.py`.
- Cinco PDF oficiales descargados, legibles con `pdfinfo`/`pdftotext`.
  Portadas de NAO e IR 8374r1 inspeccionadas visualmente.
- Seis paquetes de herramientas descargados y código de Volatility 3 fijado a
  `v2.28.2`, commit `881e970121c16f0932fb9d16fbd5fb258cbcbf75`.
- Volatility 3 instalado en `local/analysis-env`; ayuda de CLI ejecutada con éxito.
- ISO `local/herramientas.iso` creada con los seis paquetes, XML Sysmon, hashes y
  guía. Contenido binario cotejado con los hashes de los archivos descargados.
- ISO Windows propia localizada y hasheada; ruta y hash conservados solo en `local/`.

## Comprobaciones

| Comprobación | Resultado |
|---|---|
| `python3 -m unittest discover -s tests -v` | 5 pruebas correctas; incluyen escenarios de escape de red e integraciones |
| `./lab validate` y `ruby -c Vagrantfile` | Correctos |
| Scripts shell | Sintaxis comprobada |
| `LAB_GUI=false ./lab up --provider=virtualbox` | Arranque real correcto |
| `python3 scripts/check_isolation.py` | Correcto sobre VM encendida y apagada |
| `sha256sum -c config/SHA256SUMS` | 11 archivos coincidentes |
| Descarga repetida | Archivos existentes reconocidos por hash; commit de Volatility comprobado |
| SISIFO | 0 fallos automáticos; 10 afirmaciones con fragmentos localizados |

Los hashes del manifiesto registran integridad de la descarga, no atribución
histórica ni una auditoría de los binarios. El JDK se cotejó además con el checksum
publicado por la API de Adoptium. Los enlaces finales de GitHub omiten parámetros
firmados efímeros; las URL iniciales permiten volver a descargar.

## Incidencias resueltas o delimitadas

- Vagrant no activaba el comunicador `none` por defecto. Se comprobó la bandera
  experimental en su código instalado y se añadió `./lab` para activarla antes
  de cargar plugins. El arranque se repitió con éxito.
- VirtualBox identifica esta ISO, pero su detección automática devuelve
  `NS_ERROR_NOT_IMPLEMENTED`. Se comprobó el arranque normal y se dejó instalación
  interactiva; no se afirma haber completado una instalación desatendida.
- La primera comprobación de la ISO con `hashlib.file_digest` no funcionó sobre
  el objeto virtual de pycdlib. La lectura explícita por bloques confirmó los
  tamaños y hashes de todos los paquetes: el contenido no estaba corrupto.
- Se corrigieron citas y catálogo bibliográfico que faltaban en la primera
  revisión documental. La segunda revisión no presentó fallos automáticos.

## Lo que falta para realizar la práctica

1. Instalar y activar Windows con la edición/licencia del usuario.
2. Instalar/probar herramientas en el invitado, validar Sysmon y captura de RAM,
   y guardar la snapshot limpia. No se ha probado Npcap ni el controlador WinPmem.
3. Adquirir una muestra o dataset con procedencia. No se descargó ni ejecutó
   WannaCry; la API de MalwareBazaar requiere Auth-Key no proporcionada.
4. Definir adquisición de disco, salida de evidencias y símbolos de Volatility
   para la build concreta. No se ha adquirido RAM, MFT, EVTX ni PCAP del caso.
5. Incorporar enunciado/rúbrica del docente y producir el informe con resultados.

## Revisión del usuario pendiente

SISIFO deja 9 comprobaciones manuales: las dos líneas rojas del BRIEF; las dos
referencias institucionales sin DOI como un grupo; y los seis criterios de
terminado. Las fuentes sin DOI son los informes NAO/NHS, comprobados aquí en sus
sitios institucionales, no artículos que deban tener DOI. Los resultados técnicos
anteriores son evidencia para esa revisión; no se marcan como aprobación del usuario.

Esta entrega corresponde a la **preparación del repositorio y del laboratorio**.
No es un informe forense terminado ni un laboratorio de infección ya ejecutado.
