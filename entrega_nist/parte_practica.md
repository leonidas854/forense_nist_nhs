# Parte práctica: examen estático de cuatro componentes de WannaCry con Ghidra

## 1. Propósito y resultados disponibles

Esta parte permite estudiar cómo se pasa de un archivo a una conclusión forense defendible. Integra cuatro capítulos por componente, diagramas, fragmentos de desensamblado y las 16 transcripciones de pseudocódigo preservadas. La autoría corresponde a los ocho autores de la portada; no se atribuyen actuaciones individuales que no estén registradas.

El resultado técnico disponible es **análisis estático seleccionado**. Se comprobaron identidades y relaciones de contenido y se revisaron ramas de funciones. No se ejecutó WannaCry ni se observó su impacto en un sistema. Las actividades que aún no se han realizado se presentan como procedimientos futuros, con criterios de aceptación, y no como resultados.

La secuencia de estudio es: método → identidad de los objetos → recursos y capas → lectura de cada componente → correlación de hallazgos → NIST → práctica benigna y revisión. El informe general contiene la reconstrucción histórica; esta parte explica cómo sostener las afirmaciones técnicas. Ambos documentos distinguen el NHS de Inglaterra de los archivos del laboratorio.

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

## 4. Cómo leer las capas sin confundirlas

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
| Wireshark | Lectura de capturas autorizadas | No se habilitan NICs para esta práctica |
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

## 11. Prácticas benignas para ampliar el estudio

### 11.1 Ejercicio de decisiones, sin ejecución del malware

Construir una tabla en papel con entradas hipotéticas: handle nulo/no nulo, recurso disponible/ausente, creación de archivo válida/inválida y creación de proceso válida/inválida. Recorrer los diagramas y anotar únicamente la salida del código. Etiquetar todas las entradas como S. El ejercicio se aprueba si se distinguen el retorno de la función, el resultado de la API y el efecto externo desconocido.

Respuestas de control: un handle no nulo evita la llamada 00408090; en W/101, después de pasar los controles iniciales, un fallo de CreateFileA puede llegar al retorno 1; en 1800010f8 tanto la ruta de éxito de CreateProcessA como la de fallo llegan a retorno 0. Ninguna respuesta implica que el malware se ejecutó.

### 11.2 Ejercicio de integridad y restauración de documentos ficticios

En una sesión futura de Windows verificada, crear una carpeta nueva de práctica con un texto que diga «dato ficticio de clase». Registrar su SHA-256 con Get-FileHash, conservar una copia separada y modificar manualmente solo el documento de trabajo. Comparar hashes, restaurar desde la copia y comprobar tanto la igualdad como la lectura del contenido. No utilizar documentos personales, muestras ni órdenes del malware.

El registro debe incluir fecha, acción, objeto, hash anterior/posterior, copia utilizada y resultado real. Restaurar un texto verifica esa operación limitada. No demuestra recuperación frente a WannaCry, limpieza de un respaldo ni restablecimiento de un servicio hospitalario. Relación NIST: PR.DS-11, RC.RP-03 y RC.RP-05.

### 11.3 Ejercicio de observación de proceso benigno

En la estación verificada, observar una aplicación inocua como el editor de texto con una herramienta disponible y validada. Anotar proceso, apertura y cierre reales. Si la auditoría o la herramienta no conserva un dato, registrar esa ausencia y su causa conocida; no inventar un evento. El objetivo es aprender la diferencia entre presencia de archivo, creación de proceso y operación terminada.

No se afirma que estos ejercicios ya se realizaron. Tampoco se generan conexiones de red o muestras artificialmente dañinas para rellenar una tabla. El ejercicio de mesa puede realizarse sin Windows; las observaciones del invitado requieren una sesión real y documentada.

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

## 14. Conclusión práctica

La práctica permite justificar relaciones entre contenedores y cargas, interpretar decisiones de funciones y distinguir solicitudes de operaciones de efectos observados. El análisis más importante no es afirmar que una muestra «hace todo», sino indicar qué condición conduce a cada acción prevista y qué prueba sería necesaria para demostrarla en un equipo.

La documentación queda preparada para nuevas sesiones con el mismo criterio de trazabilidad. Cada ampliación deberá conservar versión, hash, dirección, resultado y límite. Los capítulos siguientes incluyen las transcripciones para estudiar sin abrir muestras; no constituyen una reconstrucción compilable ni instrucciones para lanzar ransomware.

## Referencias de la parte práctica

[NIST SP 800-86] Kent, K., Chevalier, S., Grance, T., y Dang, H. (2006). *Guide to integrating forensic techniques into incident response*. [DOI](https://doi.org/10.6028/NIST.SP.800-86). Capítulo 3 para el método; capítulos 4–6 para fuentes y examen.

[NIST CSF 2.0] National Institute of Standards and Technology. (2024). *The NIST Cybersecurity Framework (CSF) 2.0*. [DOI](https://doi.org/10.6028/NIST.CSWP.29). Códigos del apéndice A. Contexto histórico y restantes referencias en el informe general.

[API1] Microsoft. (s. f.). *InternetOpenUrlA*. [Documentación oficial](https://learn.microsoft.com/en-us/windows/win32/api/wininet/nf-wininet-internetopenurla). Consulta: 20/11/2026.

[API2] Microsoft. (s. f.). *FindResourceA*. [Documentación oficial](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-findresourcea). Tipo, identificador y retorno; consulta: 20/11/2026.

[API3] Microsoft. (s. f.). *CreateProcessA*. [Documentación oficial](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa). Creación y límites de finalización; consulta: 20/11/2026.

[API4] Microsoft. (s. f.). *CheckTokenMembership*. [Documentación oficial](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-checktokenmembership). Retorno y parámetro de salida; consulta: 20/11/2026.

[REGISTROS LOCALES] Proyecto académico. (2026, 15 de noviembre). *Exportaciones Ghidra, Listing y manifiestos de extracción*. Referencias y SHA-256 en `trazabilidad.json`. Edición de transcripciones original cotejada por `scripts/verificar_material_equipo.py`. No se atribuyen estos archivos a un hospital.

## Anexo: transcripciones seleccionadas del Decompiler

Los 16 cuerpos siguientes se incorporan desde la edición conservada y se cotejan por SHA-256. Se preservan instrucciones, nombres y comentarios; solo la presentación impresa puede envolver líneas. Los nombres en español y comentarios del analista no son símbolos originales. Los prototipos imperfectos se conservan deliberadamente; las precisiones se explican en cada capítulo.

{{TRANSCRIPCIONES}}
