# Parte práctica: análisis estático de WannaCry con Ghidra y revisión offline de tráfico

## 1. Propósito y resultados disponibles

Esta parte permite estudiar cómo se pasa de un archivo a una conclusión forense defendible. Integra cuatro capítulos por componente, diagramas, fragmentos de desensamblado y las 16 transcripciones de pseudocódigo preservadas. La autoría corresponde a los ocho autores de la portada; no se atribuyen actuaciones individuales que no estén registradas.

El resultado técnico disponible combina **análisis estático seleccionado**, revisión offline de una captura de red externa y un intento de apertura en un clon aislado que la protección antimalware de Windows rechazó antes de que se observara la creación de un proceso. No se recuperó un evento del antivirus ni un identificador de detección que permita atribuir con más precisión el bloqueo a un motor o firma concreta. No hubo detonación efectiva ni impacto local atribuible a WannaCry. El PCAP externo no es del NHS; las actividades no realizadas se identifican sin presentarlas como resultados.

La secuencia de estudio es: método → identidad de los objetos → recursos y capas → lectura de cada componente → correlación de hallazgos → NIST → práctica benigna y revisión. El informe general contiene la reconstrucción histórica; esta parte explica cómo sostener las afirmaciones técnicas. Ambos documentos distinguen el NHS de Inglaterra de los archivos del laboratorio.

### Qué es WannaCry: familia, ransomware y gusano

**WannaCry** (también llamado WannaCrypt, WanaCrypt0r o WCry) es un nombre de familia/linaje para malware de Windows asociado al brote de mayo de 2017. Una familia agrupa muestras relacionadas; no es un solo archivo. El SHA-256 identifica el ejemplar exacto que se examinó. MITRE ATT&CK cataloga esos nombres relacionados como S0366. [T1; T3]

| Concepto | Explicación sencilla | Evidencia que lo respalda en este estudio |
|---|---|---|
| Ransomware | Intenta dejar los archivos inaccesibles, cifrarlos y exigir dinero para recuperarlos | Microsoft describe archivos cifrados, nota y demanda de rescate. Nuestro análisis estático no reconstruye el cifrador completo |
| Gusano (worm) | Puede buscar y propagarse a otros equipos por red sin que alguien tenga que volver a abrir cada copia | Microsoft y CISA describen la propagación usando vulnerabilidades de SMBv1. El PCAP externo muestra comunicaciones SMB del mismo hash de muestra |
| Familia | Conjunto de variantes o componentes relacionados; sus nombres no garantizan contenido idéntico | El ejemplar 24d004… se identifica por SHA-256 completo. El sitio que publicó el PCAP informa ese mismo hash para el binario lanzado en su laboratorio |

La forma breve es **ransomware con capacidad de gusano** (a veces «ransomworm»). El ransomware explica el impacto sobre archivos y la extorsión; la capacidad de gusano explica el alcance automático en red. Sus componentes pueden separar comprobación del kill switch, propagación y cifrado. No todas las fases se demuestran con el mismo artefacto, y una conversación SMB no prueba por sí sola que la explotación tuvo éxito. [T1; T3; T4]

La revisión de Wireshark descrita en 5.3 es un PCAP real de un laboratorio externo que usó el mismo hash; no es tráfico del NHS ni una detonación realizada por el equipo. Los archivos de la captura se mantienen fuera de Git.

## 2. Método forense aplicado a la práctica

### 2.1 Recolección: registrar lo que realmente se tiene

Según SP 800-86, §3.1, el trabajo comienza identificando fuentes y preservando datos relevantes. En este caso se recibieron archivos ya presentes; no se adquirieron discos de hospitales. Deben registrarse identidad, ubicación, fecha de comprobación, responsable real, herramienta y relación con el caso. Si la procedencia previa es desconocida, se escribe «no acreditada».

Los originales se conservan sin edición. La extracción de un recurso produce un derivado con identidad propia y vínculo al padre. Una transcripción de Ghidra es otro derivado analítico: su hash no es el hash del ejecutable. La evidencia local se mantiene fuera del repositorio; la publicación académica contiene explicaciones y código seleccionado para lectura.

### 2.2 Examen: separar estructura de significado

Se comprueban cabeceras y recursos antes de confiar en el nombre del archivo. Después se localizan cadenas e importaciones, se siguen referencias y se contrastan las condiciones del desensamblado con el decompilado. El examinador conserva el resultado original y anota las correcciones de tipos o nombres. No modifica bytes del binario para obtener un pseudocódigo más cómodo.

### 2.3 Análisis: demostrar una afirmación por vez

Una ficha útil contiene pregunta, observación, dirección, condición, llamadas, retorno, soporte y limitación. Por ejemplo: «la rutina lee una longitud de cuatro bytes y pasa un puntero desplazado cuatro bytes a WriteFile» es una afirmación estática comprobable. «El archivo fue escrito y cifró un hospital» añade hechos que esa observación no demuestra.

### 2.4 Informe: permitir que otra persona compruebe el razonamiento

Cada capítulo incluye un procedimiento de lectura y preguntas resueltas. La revisión colectiva debe volver al hash y a la dirección, seguir ambas ramas y contrastar la fuente. Una firma de revisión solo se agrega cuando una persona real realizó esa revisión. No se completa una cadena de custodia ficticia para mejorar la apariencia de la entrega. [NIST SP 800-86, §§3.1–3.4]

## 3. Inventario, identidad y alcance

### 3.1 Identificadores completos

| Componente | SHA-256 |
|---|---|
| 24d004… | 24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c |
| ed01… | ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa |
| u.wnry | b9c5d4339809e0ad9a00d4d3dd26fdf44a32819a54abf846bb9b560d81391c25 |
| ec1383… | ec138352c4726fa3b6706b30bf4692252f818108c8066e8518920dd9823a34bb |
| PE delimitado dentro de W/101 | 93db4b26be3a4e6b724bf85830746f458cde613ad88501bcb23d2ae1ab9976c9 |

Los prefijos abreviados son etiquetas de lectura, no sustitutos de los identificadores completos. Coincidir por SHA-256 es una comprobación de identidad de contenido con alta confianza práctica; una comparación directa byte a byte es un procedimiento distinto. El comentario heredado de una transcripción que mezcla ambos términos se conserva como antecedente y se precisa aquí.

### 3.2 Cobertura real

| Objeto | Formato | Funciones reconocidas | Transcripciones seleccionadas |
|---|---|---|---|
| 24d004… | PE32 x86 | 176 | 6 |
| ed01… | PE32 x86 | 244 | 4 |
| u.wnry | PE32 x86 | 1.070 | 3 |
| ec1383… | PE32+ x64, DLL | 265 | 3 |
| Total de estos cuatro objetos | Distintos programas | 1.755 | 16 |

El proyecto también reconoció funciones en el PE de W/101, taskdl.exe y taskse.exe. No se suman a la tabla porque no son los cuatro objetos principales de esta entrega. Una función reconocida puede corresponder a lógica propia, bibliotecas, inicialización, manejo de errores, interfaz o auxiliares; esas clases requieren validación, no se asignan solo por el nombre.

La selección prioriza decisiones relevantes y relaciones verificables. Las demás funciones siguen existiendo. «No transcrita» no significa «inútil», «no ejecutada» o «no maliciosa». Tampoco se convierte la relación 16/1.755 en porcentaje de comportamiento cubierto: las funciones tienen complejidades y caminos diferentes.

### 3.3 Relaciones de contención

| Padre y recurso | Desplazamiento en archivo | Tamaño / contenido examinado |
|---|---|---|
| 24d004…, R/1831 | 204.964 bytes | 3.514.368 bytes; coincide con ed01… |
| ed01…, XIA/2058 | 65.776 bytes | 3.446.325 bytes; paquete ZIP de 36 miembros |
| ec1383…, W/101 | 51.364 bytes | Recurso de 5.242.880 bytes; longitud inicial de 3.756.032 |
| Tramo PE de W/101 | Recurso +4 | 3.756.032 bytes; SHA-256 93db4b26… |

Los desplazamientos anteriores son offsets de archivo documentados en la extracción. Las direcciones de funciones de Ghidra son direcciones virtuales del programa importado. No se intercambian ambos valores. El resto del recurso W/101, fuera de los cuatro bytes iniciales y la longitud declarada, no integra el PE delimitado.

## 4. Capas OSI, componentes y operaciones de Windows

### 4.1 Bytes, formato PE y recursos

Un byte representa ocho bits. Hexadecimal permite escribir un byte con dos dígitos. PE es un formato de ejecutable de Windows que organiza cabeceras, secciones y directorios. La extensión del nombre no decide si es una DLL: hay que consultar la estructura. Un recurso PE es contenido incorporado que el programa puede localizar por tipo e identificador.

**W/101** significa «tipo W, identificador 101». La barra es notación del informe, no una carpeta, un puerto ni una división. 0x65 equivale a 101; 0x727 a 1831; 0x80a a 2058; 0x100 a 256; 0x1bd a 445. W y XIA son nombres de tipo elegidos en el archivo; no prueban por sí solos el formato de los datos.

Un DWORD ocupa cuatro bytes. En little-endian, el byte menos significativo aparece primero: `00 01 00 00` representa 256. Si un puntero tiene tipo DWORD*, sumarle uno avanza cuatro bytes. Si fuera un puntero a byte, sumarle uno avanzaría un byte. Por eso la aritmética del tipo debe contrastarse con el desplazamiento del desensamblado.

### 4.2 Cadenas, importaciones y referencias

Una cadena es un dato textual, no una acción. Una importación indica que el binario puede recurrir a una API; algunas APIs se resuelven dinámicamente con GetProcAddress y aparecen como llamadas indirectas. Una referencia cruzada enlaza una instrucción o dato con otro elemento. Seguirla permite mostrar cómo se utiliza una cadena y cuáles son las condiciones para alcanzar su uso.

Una ruta `C:\WINDOWS\mssecsvc.exe` explica un destino previsto. No demuestra que el archivo exista. Una referencia al nombre TaskStart indica búsqueda de un símbolo o destino; la instrucción `CALL EAX` indica una llamada indirecta al valor del registro. Ninguna revela, por sí sola, el cuerpo completo de la carga siguiente.

### 4.3 Desensamblado: instrucciones y saltos

El Listing muestra instrucciones recuperadas a partir de bytes. `MOV` mueve datos; `CALL` transfiere control a una rutina; `TEST` afecta indicadores de la CPU según una operación lógica; `JZ` y `JNZ` seleccionan caminos según el resultado. En `TEST EDI,EDI`, un valor cero activa la condición de cero. `JNZ` toma la salida cuando el resultado no es cero.

En x86 pueden verse argumentos colocados en la pila; en Windows x64 los primeros argumentos enteros o punteros se suelen observar en RCX, RDX, R8 y R9. Esto orienta la lectura, pero debe contrastarse con el convenio concreto y el prototipo. Un fragmento de Listing aislado no equivale al análisis completo de todos sus predecesores.

### 4.4 Decompilado: representación interpretativa

El Decompiler propone una representación semejante a C. `undefined4` indica cuatro bytes cuyo tipo semántico no se recuperó de manera más precisa; no significa «virus desconocido». `FUN_`, `DAT_` y `LAB_` son etiquetas automáticas comunes de función, dato y ubicación. Variables como `iVar1` son nombres generados, no los nombres del código fuente original.

Los errores de tipo afectan la lectura: un entero mal interpretado como puntero puede deformar parámetros. En 00407ce0 y 004014a6 hay limitaciones documentadas. Se conservan las transcripciones y se contrasta el Listing, sin reescribirlas para compilarlas. El propósito es comprender los caminos y su soporte, no reconstruir un ejecutable funcional.

### 4.5 Retorno, parámetro de salida y efecto

Un retorno de cero no tiene un significado universal. `memcmp == 0` expresa igualdad; un handle NULL puede indicar fallo; una rutina propia puede devolver cero tanto tras éxito como tras fallo. Una API puede devolver éxito y escribir otro resultado en un parámetro de salida. Finalmente, solicitar un proceso no acredita que terminara ni que alcanzara su objetivo. [API1–API4]

Estas distinciones explican buena parte del análisis: seguir solo el nombre de una función o su último return lleva a conclusiones incorrectas. Los cuatro capítulos muestran casos concretos.

{{INCLUIR:enfoque_osi.md}}

## 5. Entorno de laboratorio y herramientas

<!-- ESTADO_LAB: el generador incorpora el estado comprobado desde estado_laboratorio.md. -->

{{INCLUIR:estado_laboratorio.md}}

### 5.1 Herramientas y función en el estudio

| Herramienta | Para qué se utiliza | Estado y límite |
|---|---|---|
| Ghidra 12.2 DEV, anfitrión | Proyecto y exportaciones del 15/11 | Resultados preservados; sin nueva sesión MCP en esta edición |
| Ghidra 12.2 PUBLIC y JDK 25, paquetes Windows | Estación futura de lectura | Descargas fijadas; instalación en invitado requiere evidencia |
| Sysinternals | Observación de actividad benigna | No equivale a captura realizada |
| FLOSS | Examen de cadenas | No confundir texto extraído con ejecución |
| Wireshark/TShark 4.7.4, anfitrión | Revisión offline de una captura externa publicada | Uso de TShark comprobado; la copia Windows sigue apagada, sin NICs y sin instalación de Wireshark declarada dentro del invitado |
| WinPmem y Volatility 3 | Adquisición y análisis de RAM, si se autorizan y prueban | Ninguna captura o análisis de RAM declarado aquí |

Las versiones y SHA-256 de descargas están en `config/descargas.lock.json`; SP 800-86 tiene manifiesto complementario. No se sustituyen silenciosamente paquetes. Una descarga correcta no demuestra que una herramienta funcione dentro de Windows. La compatibilidad y la prueba benigna deben documentarse por separado.

### 5.2 Preparación de una sesión estática

1. Leer alcance, identificar el objeto por hash y registrar la fecha real.
2. Comprobar aislamiento antes de usar la estación; guardar el resultado fuera de Git.
3. Trabajar sobre una copia autorizada, preservando originales y manifiestos.
4. Abrir el proyecto local conservado en Ghidra o consultar las transcripciones si no se dispone del proyecto.
5. Seleccionar el programa por hash, no solo por nombre. Abrir Listing y Decompiler.
6. Usar navegación a dirección y llegar a la función indicada en cada capítulo. Revisar sus referencias.
7. Anotar observación, camino alternativo y efecto que permanece pendiente.
8. Guardar exportaciones y registro real de la sesión, con versión de herramienta y hashes; publicar únicamente síntesis académica revisada.

El proyecto local está en `local/ghidra/proyectos/WannaCry_NHS.gpr`. Las exportaciones conservadas corresponden a `local/exportaciones-ghidra/20261115T175358527847Z/`. El lanzador y la consulta MCP están documentados en `docs/ghidra-mcp.md`. Que exista ese procedimiento no significa que el puente esté activo; en la comprobación de esta edición no escuchaba en 127.0.0.1:8765.

### 5.3 Revisión offline de una captura real de laboratorio con TShark

Para observar tráfico sin conectar la VM a ninguna red, se analizó un PCAP publicado por Malware-Traffic-Analysis.net. El editor indica que la captura fue enviada por David Szili desde un entorno de prueba; la página identifica `192.168.116.149` como equipo donde se lanzó WannaCry y declara el SHA-256 del binario. Ese hash coincide exactamente con el objeto local 24d004…. La coincidencia vincula el ejemplar descrito con la captura del laboratorio externo; no vincula ese entorno con el NHS. [T5]

La evidencia se preservó en `local/analisis-wireshark-20261121/`: PCAP SHA-256 `feb8befd8d6891511bd00471d153a2bf8d57d022e1d81e00755941b872fdc355`; ZIP de origen SHA-256 `03b2fb0ef820ffc258fa114822058ec129e0badd903f1e3835580f665ed1ecff`. El ZIP se comprobó con 7-Zip. Capinfos registra 46.654 paquetes Ethernet y una duración de 695,472382 segundos. TShark 4.7.4 es la versión de Wireshark utilizada en el anfitrión; el PCAP y el ejecutable de malware nunca se ejecutaron.

**Observaciones reproducibles en la captura:**

1. El filtro `ip.addr==192.168.116.149 && tcp.port==445` muestra conversaciones del host identificado por la fuente hacia otros equipos por TCP/445.
2. El filtro `ip.src==192.168.116.149 && tcp.dstport==445 && smb.cmd==0x32` devuelve solicitudes SMB1 TRANS2 a varios destinos, incluidos `.138`, `.143` y `.172`. Esto demuestra intercambios en el PCAP; el comando aislado no demuestra que el exploit terminara con infección.
3. El PCAP completo incluye 16.389 tramas TCP decodificadas como NBSS/SMB. Ese total contiene tráfico de varios equipos, no se atribuye todo a WannaCry.
4. No hay coincidencias en esta captura para las consultas DNS al dominio kill switch ni para tráfico TCP/80 del host `.149`. No se concluye que el proceso omitiera esa consulta: el PCAP puede empezar después o no contener ese tramo.

La página del autor afirma que la muestra se propagó a otros hosts de su laboratorio. La captura respalda la actividad de red descrita, pero no acredita por sí sola qué archivos cifró cada víctima, quién inició la infección ni el resultado clínico de un equipo. Tampoco se exportaron archivos desde SMB. Para reproducir la revisión en Wireshark, abrir el PCAP local en modo lectura y aplicar los filtros anteriores; la VM debe continuar desconectada. [N1, §§3.1–3.4; T5]

**Relación NIST.** Se registraron procedencia publicada, identidad/hash del archivo, herramienta, observación e interpretación por separado, siguiendo el flujo de recolección, examen, análisis e informe de SP 800-86. La captura sirve como ejemplo para discutir monitoreo y análisis de red dentro del CSF 2.0; no demuestra que el NHS tuviera o no tuviera una capacidad concreta. El informe de la NAO y la revisión Smart siguen siendo las fuentes históricas del NHS. [N1; N2; H1; T5]

## 6. Análisis de 24d004…: decisión, servicio y carga

{{INCLUIR:analisis/24d004.md}}

## 7. Análisis de ed01…: paquete y frontera de carga

{{INCLUIR:analisis/ed01.md}}

## 8. Análisis de u.wnry: referencias, privilegios y recuperación

{{INCLUIR:analisis/u_wnry.md}}

## 9. Análisis de ec1383…: W/101 y solicitud de lanzamiento

{{INCLUIR:analisis/ec1383.md}}

## 10. Correlación de hallazgos con artefactos de un sistema

Los artefactos de la tabla son **fuentes que se necesitarían**, no objetos adquiridos del NHS ni resultados generados en esta práctica. Su presencia depende de configuración, versión, retención y acciones previas. Una coincidencia nominal es una pista; la correlación debe sostener identidad y secuencia.

| Capacidad observada | Fuente que podría corroborarla | Qué habría que comprobar |
|---|---|---|
| Solicitud de servicio | Registro System, evento 7045; clave de servicio | Host, hora, ruta, ejecutable y proceso asociado |
| Solicitud de proceso | Auditoría de creación de procesos; telemetría existente | Relación padre-hijo, comando, token y tiempos |
| Escritura de componente | Archivo, metadatos y registro de actividad | Hash, ubicación y relación con el proceso |
| Acceso de red | Captura o registros DNS/firewall/proxy disponibles | Destino, tiempo y host; no solo puerto |
| Acción contra recuperación | Procesos y estado de copias antes/después | Operación realmente terminada y efecto comprobado |
| Cifrado | Archivos afectados y comparación con referencia | Contenido, extensión, proceso y secuencia; no solo nombre |

No se equipara un evento de autenticación de red con RDP sin más datos. Un timestamp de compilación tampoco determina la fecha de infección; puede no ser fiable. Una línea temporal debe conservar zona horaria, precisión, desfase conocido y fuente de cada hora. [NIST SP 800-86, §§4–6]

### 10.1 Ficha modelo ya completada con un hallazgo estático

| Campo | Contenido |
|---|---|
| Pregunta | ¿La rutina W/101 descifra el recurso? |
| Objeto | ec1383…, SHA-256 completo en sección 3 |
| Localizador | 180001014; instrucciones 18000108b y 1800010c4–1800010d3 |
| Observación | Lectura de DWORD inicial y WriteFile desde recurso+4 |
| Procedimiento | Cotejo de transcripción con Listing preservado y límites del recurso |
| Resultado | El tramo delimitado corresponde al PE 93db4b26… |
| Interpretación | La rutina seleccionada copia un tramo; no se observa descifrado en ella |
| Límite | No establece cómo se invocó PlayGame ni que la escritura ocurriera |
| NIST | RS.AN-03 y RS.AN-07; método SP 800-86 |

Una nueva ficha debe identificar a quien hizo realmente la comprobación. Este ejemplo expone un razonamiento documentado; no acredita una revisión individual nueva por cada autor.

{{INCLUIR:catalogo_funciones.md}}

## 11. Prácticas benignas: procedimiento y resultados

### 11.1 Ejercicio de decisiones, sin ejecución del malware

Construir una tabla en papel con entradas hipotéticas: handle nulo/no nulo, recurso disponible/ausente, creación de archivo válida/inválida y creación de proceso válida/inválida. Recorrer los diagramas y anotar únicamente la salida del código. Etiquetar todas las entradas como S. El ejercicio se aprueba si se distinguen el retorno de la función, el resultado de la API y el efecto externo desconocido.

Respuestas de control: un handle no nulo evita la llamada 00408090; en W/101, después de pasar los controles iniciales, un fallo de CreateFileA puede llegar al retorno 1; en 1800010f8 tanto la ruta de éxito de CreateProcessA como la de fallo llegan a retorno 0. Ninguna respuesta implica que el malware se ejecutó.

### 11.2 Ejercicio de integridad y restauración de documentos ficticios

En una sesión de Windows verificada, crear una carpeta nueva de práctica con un texto que diga «dato ficticio de clase». Registrar su SHA-256 con Get-FileHash, conservar una copia separada y modificar manualmente solo el documento de trabajo. Comparar hashes, restaurar desde la copia y comprobar tanto la igualdad como la lectura del contenido. No utilizar documentos personales, muestras ni órdenes del malware.

El registro debe incluir fecha, acción, objeto, hash anterior/posterior, copia utilizada y resultado real. Restaurar un texto verifica esa operación limitada. No demuestra recuperación frente a WannaCry, limpieza de un respaldo ni restablecimiento de un servicio hospitalario. Relación NIST: PR.DS-11, RC.RP-03 y RC.RP-05.

### 11.3 Ejercicio de observación de proceso benigno

En la estación verificada, observar una aplicación inocua como el editor de texto con una herramienta disponible y validada. Anotar proceso, apertura y cierre reales. Si la auditoría o la herramienta no conserva un dato, registrar esa ausencia y su causa conocida; no inventar un evento. El objetivo es aprender la diferencia entre presencia de archivo, creación de proceso y operación terminada.

Los ejercicios de integridad, restauración y proceso se ejecutaron con datos ficticios en la sesión documentada a continuación. No se generaron conexiones de red ni se ejecutó malware. El ejercicio de mesa sigue siendo una propuesta distinta de esa ejecución.

{{INCLUIR:practica_windows_realizada.md}}

### 11.5 Intento controlado de apertura de la muestra: bloqueado

El 21 de noviembre de 2026 se descargó el ZIP de la muestra 24d004… desde la entrada de Malware-Traffic-Analysis.net y se comprobó que el ejecutable extraído coincide con el SHA-256 `24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c`. Se preparó como ISO óptico y se conectó a un **clon enlazado desechable** de la copia autorizada de Windows 10. La VM original y la copia base no se arrancaron ni modificaron.

El clon tuvo un único adaptador conectado a una red interna VirtualBox de nombre único, sin NAT, puente, host-only, puerta de enlace o DNS; los otros siete adaptadores quedaron desactivados. Dentro de Windows se observó IPv4 automática `169.254.106.134`, sin gateway ni DNS. Carpetas compartidas, USB, portapapeles, transferencia por portapapeles, drag-and-drop y VRDE estuvieron desactivados. La interfaz capturó tráfico mediante `nictrace` de VirtualBox. No se desactivó Defender, no se creó una exclusión y no se elevó el proceso.

Al solicitar la apertura del único `.EXE` del ISO, PowerShell devolvió que la operación no podía completarse porque el archivo contenía un virus o software potencialmente no deseado. El mensaje es compatible con un bloqueo antimalware de Windows, pero no se consultó el registro de Defender para identificar motor, firma o evento. **Resultado:** intento bloqueado por protección del invitado; no se obtuvo evidencia de ejecución efectiva de WannaCry, cifrado, servicio creado ni propagación. No debe describirse como detonación. La identidad del archivo se verificó en el anfitrión antes de construir el ISO; la lectura/hash desde Windows recibió un error equivalente de protección.

La captura de VirtualBox contiene 100 paquetes durante 449,225006 s. TShark 4.7.4 contó 0 tramas TCP, 0 TCP/445 y 0 DNS; encontró anuncios de red del propio Windows, incluidos cuatro paquetes UDP/138. No se atribuyen esos paquetes a WannaCry: el bloqueo observado y la ausencia de evidencia de proceso impiden esa atribución. Los tiempos absolutos del PCAP aparecen en 1969; son inválidos y no se usan como cronología. No había un segundo equipo conectado al segmento interno, por lo que esta práctica tampoco podía probar propagación ni recibir una respuesta de explotación.

En términos de SP 800-86, se registraron fuente, hash, configuración, acción, salida de error, captura y limitaciones para examen, análisis e informe. Como contraste retrospectivo de CSF 2.0, el ejercicio muestra una configuración de aislamiento relacionada con PR.IR-01 y una actividad de análisis de evento relacionada con RS.AN-03; **no certifica controles ni demuestra hechos del NHS**. El PCAP, las imágenes, la muestra y el clon permanecen fuera de Git; el clon enlazado se apagó y eliminó tras preservar los registros. El suplemento ampliado está en `entrega_nist/ejecucion_controlada_bloqueada.md`; el resumen del laboratorio, en `entrega_nist/estado_laboratorio.md`.

## 12. Cómo ampliar el análisis de las demás funciones

### 12.1 Inventario antes de conclusiones

Exportar un listado de funciones del programa autorizado, conservando nombre, dirección, tamaño, llamadas y referencias. Clasificar cada entrada solo después de examinarla: inicialización, biblioteca, datos, recursos, interfaz, red, procesos, criptografía o sin resolver. Registrar el criterio y su confianza. La plantilla anterior de inventario está vacía y no se presenta como trabajo ya completado.

### 12.2 Prioridades concretas

| Componente | Próxima pregunta estática | Condición para cerrarla |
|---|---|---|
| 24d004… | ¿Qué caminos siguen al dispatcher y a las rutinas de red? | Grafo de llamadas contrastado y condiciones documentadas |
| ed01… | ¿Qué hacen los auxiliares previos a TaskStart? | Tipos revisados, entradas/salidas y fronteras de carga comprobadas |
| u.wnry | ¿Cuál es el límite correcto del bloque llamador? | Referencias y flujo de instrucciones revisados sin inventar C |
| ec1383… | ¿Cómo se inicializa el módulo y quién llama a la exportación? | Callers e inicialización sustentados; procedencia externa separada |

Una función grande puede contener bibliotecas o interfaz y no ser el mecanismo principal. Una función pequeña puede tomar una decisión decisiva. La prioridad se justifica por la pregunta del caso, no por el número de líneas. No debe renombrarse una función como «cifrador» antes de demostrar qué transforma y cómo se relaciona con la carga.

## 13. Revisión colectiva y defensa

Los ocho autores pueden revisar por pares de manera rotativa, eligiendo un componente y una fuente histórica. Esta es una propuesta de trabajo, no una asignación nominal ni constancia de tareas realizadas. La revisión debe producir comentarios verificables y correcciones, sin reconstruir retrospectivamente firmas.

| Pregunta de defensa | Respuesta sustentada |
|---|---|
| ¿Los cuatro archivos son iguales? | No. Hay relaciones de contención y componentes distintos; ec1383… contiene otro PE |
| ¿Qué es W/101? | Tipo e identificador de recurso; el PE delimitado empieza cuatro bytes después |
| ¿HTTP 500 detuvo la muestra? | El 500 fue comunicado sobre la página ANY.RUN; no hay informe para concluirlo |
| ¿Ghidra muestra el código original? | Produce desensamblado y una aproximación de alto nivel, con tipos y nombres inferidos |
| ¿Se analizó todo WannaCry? | Se examinaron mecanismos seleccionados; 16 transcripciones no cubren 1.755 funciones |
| ¿Qué aporta NIST? | Método y resultados verificables de gestión; no añade evidencia ni certificación |
| ¿La VM demuestra lo ocurrido en 2017? | No; sirve para lectura y ejercicios benignos con resultados propios |

La exposición puede seguir este orden: identidad de los objetos, mapa de contenido, una decisión de cada componente, relación documental con el NHS, resultados NIST y límites. El detalle de código debe explicar una afirmación concreta; no es necesario leer en voz alta cada inicialización automática.

{{INCLUIR:guion_exposicion_osi.md}}

## 14. Conclusión práctica

La práctica permite justificar relaciones entre contenedores y cargas, interpretar decisiones de funciones y distinguir solicitudes de operaciones de efectos observados. El análisis más importante no es afirmar que una muestra «hace todo», sino indicar qué condición conduce a cada acción prevista y qué prueba sería necesaria para demostrarla en un equipo.

La documentación queda preparada para nuevas sesiones con el mismo criterio de trazabilidad. Cada ampliación deberá conservar versión, hash, dirección, resultado y límite. Los capítulos siguientes incluyen las transcripciones para estudiar sin abrir muestras; no constituyen una reconstrucción compilable ni instrucciones para lanzar ransomware.

## Referencias de la parte práctica

[NIST SP 800-86] Kent, K., Chevalier, S., Grance, T., y Dang, H. (2006). *Guide to integrating forensic techniques into incident response*. [DOI](https://doi.org/10.6028/NIST.SP.800-86). Capítulo 3 para el método; capítulos 4–6 para fuentes y examen.

[NIST CSF 2.0] National Institute of Standards and Technology. (2024). *The NIST Cybersecurity Framework (CSF) 2.0*. [DOI](https://doi.org/10.6028/NIST.CSWP.29). Códigos del apéndice A. Contexto histórico y restantes referencias en el informe general.

[T1] Microsoft Defender Security Research Team. (2017, 12 de mayo). *WannaCrypt ransomware worm targets out-of-date systems*. [Análisis técnico](https://www.microsoft.com/en-us/security/blog/2017/05/12/wannacrypt-ransomware-worm-targets-out-of-date-systems/). Componentes, kill switch y propagación; no es resultado de ejecución local.

[T3] National Cybersecurity and Communications Integration Center (NCCIC), U.S. Department of Homeland Security. (2017). *WannaCry ransomware* [fact sheet]. [CISA, PDF](https://www.cisa.gov/sites/default/files/FactSheets/NCCIC%20ICS_FactSheet_WannaCry_Ransomware_S508C.pdf). Describe el ransomware y su componente de gusano que explota SMBv1.

[T4] MITRE ATT&CK. (s. f.). *WannaCry, S0366*. [Registro de software relacionado y alias](https://attack.mitre.org/software/S0366/). Consulta: 21/11/2026.

[T5] Szili, D. (2017, 18 de mayo). *PCAP of WannaCry spreading using EternalBlue* [captura enviada desde entorno de prueba]. En B. Duncan, Malware-Traffic-Analysis.net. [Entrada y metadatos](https://www.malware-traffic-analysis.net/2017/05/18/index2.html). No representa tráfico del NHS.

[H1] National Audit Office. (2018, 25 de abril). *Investigation: WannaCry cyber attack and the NHS* (HC 414; revisión del informe de 2017). [PDF](https://www.nao.org.uk/wp-content/uploads/2017/10/Investigation-WannaCry-cyber-attack-and-the-NHS.pdf). Fuente histórica del NHS; no incluye la PCAP externa.

[API1] Microsoft. (s. f.). *InternetOpenUrlA*. [Documentación oficial](https://learn.microsoft.com/en-us/windows/win32/api/wininet/nf-wininet-internetopenurla). Consulta: 20/11/2026.

[API2] Microsoft. (s. f.). *FindResourceA*. [Documentación oficial](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-findresourcea). Tipo, identificador y retorno; consulta: 20/11/2026.

[API3] Microsoft. (s. f.). *CreateProcessA*. [Documentación oficial](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa). Creación y límites de finalización; consulta: 20/11/2026.

[API4] Microsoft. (s. f.). *CheckTokenMembership*. [Documentación oficial](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-checktokenmembership). Retorno y parámetro de salida; consulta: 20/11/2026.

[REGISTROS LOCALES] Proyecto académico. (2026, 15 de noviembre). *Exportaciones Ghidra, Listing y manifiestos de extracción*. Referencias y SHA-256 en `trazabilidad.json`. Edición de transcripciones original cotejada por `scripts/verificar_material_equipo.py`. No se atribuyen estos archivos a un hospital.

## Anexo: transcripciones seleccionadas del Decompiler

Los 16 cuerpos siguientes se incorporan desde la edición conservada y se cotejan por SHA-256. Se preservan instrucciones, nombres y comentarios; solo la presentación impresa puede envolver líneas. Los nombres en español y comentarios del analista no son símbolos originales. Los prototipos imperfectos se conservan deliberadamente; las precisiones se explican en cada capítulo.

{{TRANSCRIPCIONES}}
