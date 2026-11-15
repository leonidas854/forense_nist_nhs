> **Pendiente de actualización (15/11/2026):** este material anterior contiene afirmaciones aún no reconciliadas. Para la defensa usar [el informe corregido](informe-forense.md) y [la guía de comprobación NIST](guia-comprobacion-nist.md).

# Banco de Preguntas y Respuestas para la Defensa Oral (Tribunal Docente)
## Caso WannaCry en el NHS con NIST CSF 2.0 · 20 Preguntas Críticas

Este documento entrena a los **dos expositores** y a los **seis especialistas técnicos** del equipo para afrontar la ronda de preguntas del tribunal de Informática Forense con solvencia técnica, rigor normativo y respaldo documental.

---

## BLOQUE I: CADENA DE CUSTODIA, INTEGRIDAD Y METODOLOGÍA (Preguntas 1 a 5)

### Pregunta 1: "¿Por qué en su laboratorio no ejecutaron el malware con salida a internet para capturar el tráfico real hacia el Kill Switch o los paneles de control de los atacantes?"
* **Intención del tribunal:** Evaluar si el estudiante comprende la ética pericial, la ley contra delitos informáticos y las normas de bioseguridad informática.
* **Respuesta Pericial:**
  > *"Como peritos informáticos, nuestra prioridad metodológica innegociable es la **no proliferación y la contención**. Permitir que una muestra de WannaCry —que contiene un módulo de gusano SMB automatizado— acceda a internet viola el estándar ISO/IEC 27037 y la legislación sobre delitos informáticos, ya que la máquina virtual comenzaría a escanear indiscriminadamente direcciones IP públicas y locales en el puerto 445 intentando infectar terceros. El análisis de la conexión al Kill Switch se resolvió con máxima precisión mediante **ingeniería inversa estática en Ghidra 12.2**: desensamblamos la función `WinMain` y examinamos la llamada a `InternetOpenUrlA`, comprobando la lógica de decisión sin poner en riesgo ningún sistema circundante."*
* **Especialista de apoyo:** Integrante 1 (Coordinador) e Integrante 5 (Ingeniería Inversa).

---

### Pregunta 2: "¿Cómo prueban que la muestra descargada corresponde a WannaCry y no a un archivo corrupto o un señuelo?"
* **Intención del tribunal:** Verificar si el equipo sabe validar procedencia e integridad criptográfica.
* **Respuesta Pericial:**
  > *"La autenticación de la muestra se sustenta en tres niveles de verificación pericial:  
  > 1. **Cotejo de Hash SHA-256:** El hash de la muestra canónica analizada (`ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa`) coincide exactamente con el boletín oficial de IOCs publicado globalmente por el CISA, el FBI y el NCSC en mayo de 2017.  
  > 2. **Cabecera PE y Secciones:** En Ghidra se comprobó la estructura Portable Executable de 32 bits, identificando la sección de recursos `.rsrc` con el identificador `R` que contiene el archivo ZIP con contraseña interna `WNcry@2ol7`.  
  > 3. **Trazabilidad en Manifest:** Los hashes y procedencias se encuentran congelados en nuestro archivo `config/descargas.lock.json` bajo control de versiones."*
* **Especialista de apoyo:** Integrante 1 (Custodio) e Integrante 5 (Ghidra).

---

### Pregunta 3: "¿Cuál es la diferencia legal y técnica entre los datos del NHS que presentan y los resultados de su máquina virtual?"
* **Intención del tribunal:** Cazar al grupo en una confusión entre evidencia histórica real y simulación de laboratorio.
* **Respuesta Pericial:**
  > *"Mantenemos una separación estricta:  
  > - Los datos del NHS (como los 80 trusts afectados, las 6.912 citas canceladas y el costo de 92 millones de libras) son **evidencias documentales históricas certificadas** obtenidas de los reportes oficiales de la National Audit Office (NAO) y del Department of Health and Social Care (DHSC 2018).  
  > - Por el contrario, los eventos de Windows (ID 7045, ID 4688) y los comandos de decompilación en Ghidra son **observaciones técnicas de laboratorio** obtenidas en nuestra estación de trabajo para modelar y corroborar las hipótesis de cómo operó el artefacto. Jamás afirmamos haber tenido acceso a discos físicos confiscados de los hospitales británicos."*
* **Especialista de apoyo:** Integrante 1 (Coordinador).

---

### Pregunta 4: "Si una herramienta como Volatility 3 o Ghidra se actualiza a una versión más reciente mañana, ¿afecta eso su peritaje?"
* **Intención del tribunal:** Evaluar repetibilidad y reproducibilidad pericial.
* **Respuesta Pericial:**
  > *"No afecta nuestro peritaje porque aplicamos el principio de **fijación de versiones (pinning)**. En nuestro repositorio, el código fuente de Volatility 3 está anclado al commit específico `881e970121c16f0932fb9d16fbd5fb258cbcbf75` (versión 2.28.2) y Ghidra a la versión 12.2 pública con hash SHA-256 auditado. Si un nuevo perito descarga nuestro repositorio, el script `scripts/download.sh` verifica contra `config/SHA256SUMS`. Cualquier cambio de versión requeriría un nuevo proceso de validación para garantizar que no existan discrepancias en los resultados."*
* **Especialista de apoyo:** Integrante 6 (Memoria) e Integrante 1.

---

### Pregunta 5: "¿Por qué no utilizaron un clon en vivo de la máquina virtual o una snapshot como única evidencia?"
* **Intención del tribunal:** Comprobar si el alumno confunde una snapshot de virtualización con una imagen forense.
* **Respuesta Pericial:**
  > *"Una snapshot de VirtualBox (`.sav`) es un volcado de estado de la máquina virtual optimizado para hipervisores; **no es una imagen forense ni garantiza cadena de custodia**. Un archivo `.sav` no equivale a un volcado `.raw` de memoria RAM ni a una imagen de disco `E01` o `DD`. Las snapshots las utilizamos únicamente como mecanismo operativo para regresar el laboratorio a un estado limpio (`limpio-herramientas`), pero cualquier extracción de evidencias exige el cálculo de hashes SHA-256 independientes antes y después de la adquisición, tal como se documenta en `docs/metodologia.md`."*
* **Especialista de apoyo:** Integrante 7 (Disco) e Integrante 6 (Memoria).

---

## BLOQUE II: LABORATORIO Y ARQUITECTURA TÉCNICA (Preguntas 6 a 10)

### Pregunta 6: "¿Qué garantiza que el malware no escape de VirtualBox hacia el sistema anfitrión Linux?"
* **Intención del tribunal:** Probar conocimientos sobre escapes de hipervisor (VM escape) y defensas en profundidad.
* **Respuesta Pericial:**
  > *"Aplicamos una arquitectura de defensa en profundidad con cuatro barreras:  
  > 1. **Diferencia de arquitectura binaria:** El binario de WannaCry es un ejecutable PE de Windows x86; en el anfitrión Linux no existe intérprete Wine ni compatibilidad nativa.  
  > 2. **Desconexión física de interfaces de red:** Las 8 tarjetas de red virtuales están explícitamente deshabilitadas (`nic: none`), impidiendo cualquier tráfico TCP/IP o SMB hacia el host.  
  > 3. **Anulación de canales de canalización:** Se deshabilitaron carpetas compartidas, portapapeles compartido y arrastrar/soltar.  
  > 4. **Aislamiento verificado por script:** El script `scripts/check_isolation.py` inspecciona la API de VirtualBox antes de cada sesión, confirmando que ninguna integración esté encendida."*
* **Especialista de apoyo:** Integrante 3 (Redes) e Integrante 1.

---

### Pregunta 7: "¿Por qué configuraron el comunicador de Vagrant en modo experimental 'none' en vez de usar SSH o WinRM?"
* **Intención del tribunal:** Evaluar el entendimiento de la herramienta Vagrant y la no interferencia pericial.
* **Respuesta Pericial:**
  > *"Por defecto, Vagrant intenta inyectar un par de claves SSH o habilitar el servicio WinRM a través de un adaptador de red NAT para aprovisionar la máquina. En informática forense, **habilitar un canal de red o un servicio remoto en el invitado altera el estado del sistema operativo y crea un vector de fuga**. Al forzar la bandera experimental `none_communicator`, Vagrant controla el ciclo de vida del hardware (encendido, apagado, guardado) sin interactuar por red con el sistema operativo invitado, preservando la pureza de la estación."*
* **Especialista de apoyo:** Integrante 3 (Redes/Laboratorio).

---

### Pregunta 8: "¿Cómo introdujeron las herramientas forenses a Windows si la máquina no tiene red ni carpetas compartidas?"
* **Intención del tribunal:** Comprobar si realmente montaron el laboratorio o están inventando la metodología.
* **Respuesta Pericial:**
  > *"Utilizamos una imagen ISO montada como unidad óptica virtual de solo lectura (`local/herramientas.iso`), construida con el script `scripts/build-tools-iso.sh`. Esta ISO contiene Ghidra, el JDK, Sysinternals, Volatility y WinPmem, junto con sus respectivos manifiestos de hashes. Al ser un medio CD/DVD virtual de solo lectura (`read-only`), Windows puede leer e instalar las herramientas sin capacidad de escribir, alterar ni infectar el medio de instalación."*
* **Especialista de apoyo:** Integrante 4 (Herramientas/Logs).

---

### Pregunta 9: "¿Por qué utilizaron Windows 10 en su laboratorio si el NHS fue atacado principalmente en Windows 7 y Windows XP?"
* **Intención del tribunal:** Cuestionar la representatividad del sistema operativo de prueba.
* **Respuesta Pericial:**
  > *"Es una excelente observación. El informe oficial de la NAO documenta que en 2017 el NHS tenía terminales con Windows XP y 7. Sin embargo, nuestro objetivo pedagógico y de laboratorio es **analizar la compatibilidad de herramientas forenses modernas (Ghidra 12.2, JDK 25, Volatility 3) y estudiar la correlación de artefactos en el registro de eventos y la memoria**. Windows 10 implementa de forma nativa la infraestructura moderna de Event Tracing for Windows (ETW), Microsoft Defender y canalizaciones Sysmon avanzadas que permiten ilustrar con mayor riqueza los controles de NIST CSF 2.0. Asimismo, en nuestro informe aclaramos explícitamente que la VM es una estación de práctica y no una réplica idéntica de la infraestructura británica."*
* **Especialista de apoyo:** Integrante 2 (Infraestructura).

---

### Pregunta 10: "¿Qué problemas de estabilidad presenta WinPmem en versiones recientes de Windows?"
* **Intención del tribunal:** Comprobar si el estudiante realmente probó la herramienta o solo la menciona de memoria.
* **Respuesta Pericial:**
  > *"WinPmem opera mediante un controlador en modo kernel para mapear la memoria física. En versiones modernas de Windows con aislamiento de núcleo (Core Isolation) y Device Guard habilitados, el controlador de WinPmem puede ser bloqueado si no cuenta con una firma digital WHQL válida o si se activa la protección de integridad de código en hipervisor (HVCI). Por ello, en `docs/laboratorio.md` registramos explícitamente que la versión descargada es una candidata (RC2) y que su controlador debe validarse previamente en una sesión limpia antes de intentar una adquisición forense formal."*
* **Especialista de apoyo:** Integrante 6 (Memoria).

---

## BLOQUE III: INGENIERÍA INVERSA Y ARTEFACTOS FORENSES (Preguntas 11 a 15)

### Pregunta 11: "Expliquen la paradoja del Kill Switch: ¿Por qué falló en proteger a los hospitales que tenían salida a internet mediante Proxy?"
* **Intención del tribunal:** Evaluar la comprensión profunda del código malicioso y la arquitectura de red hospitalaria.
* **Respuesta Pericial:**
  > *"La rutina de comprobación en `WinMain` utiliza la API nativa de Windows `InternetOpenUrlA` pasándole directamente la URL `http://www.iuqerfsodp9...com`.  
  > En muchas redes hospitalarias, el acceso a la web no es directo, sino que está intermediado por un **servidor proxy corporativo** que exige autenticación de usuario (NTLM/Kerberos) o que bloquea peticiones a dominios nuevos sin categorizar. Como el código de WannaCry no implementó cabeceras de autenticación proxy, la petición HTTP era rechazada por el proxy del hospital con un código de error (como HTTP 407 o 502), haciendo que la API devolviera NULL. Para la lógica del malware, un fallo en la llamada HTTP significa que el Kill Switch 'no existe', por lo que procedió a detonar el cifrado en los equipos internos."*
* **Especialista de apoyo:** Integrante 5 (Ingeniería Inversa) e Integrante 3 (Redes).

---

### Pregunta 12: "¿Cómo logra WannaCry persistencia en el sistema tras reiniciar el equipo?"
* **Intención del tribunal:** Evaluar el análisis del módulo de servicio.
* **Respuesta Pericial:**
  > *"A través de dos mecanismos complementarios:  
  > 1. **Servicio del Sistema:** Invoca a `CreateServiceA` para crear el servicio `mssecsvc2.0` configurado con tipo de inicio automático (`SERVICE_AUTO_START`). Esto garantiza que el módulo de gusano SMB se ejecute cada vez que Windows arranque, bajo privilegios de `SYSTEM`.  
  > 2. **Claves de Registro Run:** El cifrador extraído (`tasksche.exe`) añade entradas en la clave de registro `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run` apuntando a `@WanaDecryptor@.exe` para forzar que la pantalla de rescate se abra en la sesión del usuario."*
* **Especialista de apoyo:** Integrante 5 (Ghidra) e Integrante 4 (Logs).

---

### Pregunta 13: "¿Por qué WannaCry ejecutó el comando 'vssadmin delete shadows /all /quiet' y qué artefacto deja en el sistema?"
* **Intención del tribunal:** Evaluar técnicas antiforense y detección en logs.
* **Respuesta Pericial:**
  > *"El propósito es **sabotear la recuperación local**. Las Volume Shadow Copies (VSS) permiten a Windows restaurar versiones previas de archivos. Al eliminarlas silenciosamente con `vssadmin` y deshabilitar el catálogo de respaldos con `wbadmin`, los atacantes obligan a la víctima a recurrir a sus copias de seguridad externas o a la extorsión.  
  > En Windows, esto deja dos huellas forenses críticas:  
  > 1. **Sysmon Event ID 1 / Security Event ID 4688:** Registra la línea de comandos completa ejecutada por `cmd.exe`.  
  > 2. **Metadatos NTFS:** El servicio VSS registra eventos de detención y purga en el log `Application.evtx`."*
* **Especialista de apoyo:** Integrante 7 (Disco/MFT) e Integrante 4 (Logs).

---

### Pregunta 14: "¿Qué es la cabecera mágica WANACRY! y dónde se localiza?"
* **Intención del tribunal:** Identificar artefactos de bajo nivel en el sistema de archivos.
* **Respuesta Pericial:**
  > *"Cada archivo cifrado por WannaCry es sobrescrito comenzando con una cabecera fija de 8 bytes: los caracteres ASCII `WANACRY!` (en hexadecimal: `57 41 4E 41 43 52 59 21`). A continuación de esta firma, el malware almacena el tamaño de la clave AES cifrada con la clave pública RSA-2048 embebida de los atacantes, seguido por los datos cifrados con algoritmo AES-128 en modo CBC. Esta cabecera permite a la herramienta `@WanaDecryptor@.exe` reconocer qué archivos han sido procesados y verificar si la clave privada proporcionada puede descifrarlos."*
* **Especialista de apoyo:** Integrante 7 (Sistema de Archivos).

---

### Pregunta 15: "¿Cómo se analiza en Volatility 3 la presencia de WannaCry si el malware inyecta su DLL directamente en memoria?"
* **Intención del tribunal:** Evaluar el uso de plugins avanzados de Volatility 3.
* **Respuesta Pericial:**
  > *"Se utiliza el plugin `windows.malfind`. WannaCry extrae la biblioteca criptográfica `t.wnry` en memoria y la ejecuta reflectivamente. `windows.malfind` rastrea las secciones de memoria virtual asignadas con permisos `PAGE_EXECUTE_READWRITE` (lectura, escritura y ejecución simultáneas) que no están respaldadas por un archivo en disco (`unmapped memory`), identificando la cabecera MZ de la DLL inyectada dentro del espacio de memoria del proceso `tasksche.exe`."*
* **Especialista de apoyo:** Integrante 6 (Memoria Volátil).

---

## BLOQUE IV: NIST CSF 2.0, IR 8374r1 Y CASO NHS (Preguntas 16 a 20)

### Pregunta 16: "Si WannaCry ocurrió en mayo de 2017 y NIST CSF 2.0 se publicó en febrero de 2024, ¿no es un anacronismo metodológico aplicar este estándar?"
* **Intención del tribunal:** Cuestionar la validez del marco metodológico del proyecto.
* **Respuesta Pericial:**
  > *"No es un anacronismo; es un **análisis retrospectivo (Post-Mortem Framework Mapping)** plenamente avalado por la comunidad científica y por el propio NIST. El NIST publicó en junio de 2026 la versión final de **NIST IR 8374 Rev. 1** (*Ransomware Risk Management: A CSF 2.0 Community Profile*) precisamente para auditar y prevenir incidentes de ransomware modernos a la luz de los grandes fallos del pasado. Aplicar CSF 2.0 al NHS nos permite demostrar cómo las fallas organizativas de 2017 encajan de forma milimétrica en las categorías que el estándar formalizó en 2024, especialmente la nueva función **GOVERN (Gobernanza)**."*
* **Especialista de apoyo:** Integrante 1 (Coordinador) e Integrante 8 (Lecciones).

---

### Pregunta 17: "¿Por qué la función GOVERN (Gobernanza) fue la que más falló en el NHS si el problema era un puerto abierto?"
* **Intención del tribunal:** Probar si el estudiante distingue entre la causa técnica inmediata y la causa raíz organizativa.
* **Respuesta Pericial:**
  > *"El puerto 445 abierto fue solo el síntoma técnico. La causa raíz fue de **Gobernanza (GV.OV-01 y GV.RR-02)**:  
  > 1. NHS Digital había emitido alertas formales (CareCERT) dos meses antes ordenando aplicar el parche MS17-010, pero nadie a nivel ministerial tenía la potestad ni el proceso para auditar si los directores de los 236 trusts habían cumplido la orden.  
  > 2. Durante la emergencia, ningún líder tenía la autoridad jurídica clara para ordenar a los proveedores de telecomunicaciones desconectar la red WAN N3.  
  > Si la gobernanza hubiera funcionado, el parche habría estado instalado y la red segmentada antes del 12 de mayo."*
* **Especialista de apoyo:** Integrante 1 (Gobernanza).

---

### Pregunta 18: "¿Por qué el informe de lecciones aprendidas del NHS (2018) cambió la cifra de trusts afectados de 81 a 80?"
* **Intención del tribunal:** Comprobar si el estudiante leyó las fuentes primarias en detalle (la nota al pie de página).
* **Respuesta Pericial:**
  > *"El informe de lecciones aprendidas publicado por el CIO Will Smart en febrero de 2018 explica en su **Nota 3 (página 5)** que la cifra inicial publicada por la NAO en octubre de 2017 reportaba 81 trusts. Sin embargo, tras la auditoría forense posterior y las revisiones post-incidente, se determinó que uno de los 81 trusts nunca sufrió una infección activa de malware en sus servidores, sino que sus administradores desconectaron preventivamente sus sistemas de la red N3 para evitar el contagio. Por tanto, la cifra oficial definitiva de trusts infectados se ajustó formalmente a **80 de 236**."*
* **Especialista de apoyo:** Integrante 2 (Infraestructura) e Integrante 8 (Lecciones).

---

### Pregunta 19: "¿Qué recomienda NIST IR 8374 Rev. 1 frente al pago de rescates en extorsiones de ransomware?"
* **Intención del tribunal:** Evaluar el conocimiento de las recomendaciones del estándar sobre extorsión.
* **Respuesta Pericial:**
  > *"Bajo las subcategorías **GV.RM-03** (definición del apetito de riesgo frente a extorsiones) y **RS.CO** (comunicación durante la respuesta), NIST IR 8374 Rev. 1 y el FBI desaconsejan enérgicamente el pago de rescates por tres razones periciales:  
  > 1. No existe garantía técnica de que los atacantes entreguen una clave válida o que el software de descifrado no corrompa los archivos.  
  > 2. Financia directamente operaciones de crimen organizado o actores estado-nación.  
  > 3. En el caso del NHS, ningún hospital pagó el rescate y el servicio fue restaurado mediante reinstalación e imágenes limpias, demostrando que la resiliencia organizativa (**RC.RP**) debe basarse en copias de seguridad inmutables y no en la sumisión al extorsionador."*
* **Especialista de apoyo:** Integrante 8 (Recuperación).

---

### Pregunta 20: "¿Cuáles fueron las tres transformaciones estructurales del NHS tras WannaCry consagradas hoy en día?"
* **Intención del tribunal:** Evaluar la capacidad de sintetizar el impacto real del caso y las lecciones aprendidas.
* **Respuesta Pericial:**
  > *"Las tres reformas críticas implementadas por el gobierno británico fueron:  
  > 1. **Reemplazo de la red N3 por HSCN:** Se desmanteló la red plana N3 y se migró a la **Health and Social Care Network**, que exige segmentación estricta, encriptación en tránsito y monitoreo continuo de tráfico perimetral.  
  > 2. **Creación del CSOC de NHS Digital:** Un Centro de Operaciones de Ciberseguridad centralizado con facultades explícitas para intervenir y aislar trusts hospitalarios ante ciberataques activos (**GV.RR-02**).  
  > 3. **Erradicación total de SMBv1 y fondos de actualización:** Se prohibió el uso del protocolo SMBv1 en todo el sector salud y se asignó un presupuesto de emergencia de cientos de millones de libras para sustituir el hardware médico legado que operaba con Windows obsoletos."*
* **Especialista de apoyo:** Integrante 8 (Lecciones) e Integrante 3 (Redes).

