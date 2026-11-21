### 10.2 Catálogo de las 16 funciones: entradas, recursos y continuación

Este catálogo se lee junto con los capítulos 6–9 y las transcripciones del anexo. Resume las funciones seleccionadas; no incorpora nuevas exportaciones ni cubre las 1.755 funciones reconocidas. Las direcciones corresponden al programa indicado, no a una captura de memoria en ejecución. «Siguiente» describe el control previsto cuando se alcanza ese camino.

### 24d004…: seis funciones

| Dirección y entrada | Cómo opera y qué recursos utiliza | Condición, continuación y prueba del efecto |
|---|---|---|
| 00408140. URL incorporada al programa | Copia texto a un buffer local. InternetOpenA crea contexto WinINet; InternetOpenUrlA solicita la apertura. Usa memoria y servicios de comunicación | NULL conduce a 00408090; no nulo evita esa llamada. Ambos caminos retornan 0. Para acreditar una consulta real hacen falta resultado de API y contexto de red/proceso |
| 00408090. Ruta del módulo y argc | GetModuleFileNameA alimenta una variable global. Examina argumentos; usa handles del administrador de servicios y del servicio existente | argc < 2 llama a 00407f20. El otro camino prepara el dispatcher con LAB_00408000, tras consultas condicionadas. Falta seguir todas las auxiliares y acreditar estado real del servicio |
| 00407f20. Contexto preparado por el llamador | Llama a 00407c40 y luego a 00407ce0. Coordina dos operaciones; no realiza por sí misma una transferencia de red | No comprueba un resultado entre ambas llamadas. Retorna 0. El fallo de la primera no demuestra que se omita la segunda |
| 00407c40. Ruta global del módulo | Forma la línea del servicio; OpenSCManagerA, CreateServiceA y StartServiceA solicitan administración, creación e inicio. Usa buffer y handles de servicio | El handle del administrador y luego el del servicio condicionan las llamadas. Cierra handles; retorna 0. Para probar instalación e inicio hay que comprobar configuración y estado, no solo el nombre mssecsvc2.0 |
| 00407ce0. Módulo, APIs resueltas y R/1831 | GetProcAddress obtiene direcciones de funciones. FindResource/LoadResource/LockResource/SizeofResource acceden a datos; prepara rutas y solicita archivo, escritura y proceso. Usa memoria, disco y handles | Hay controles sobre APIs y recurso, y sobre el handle del archivo. El resultado de escritura no valida toda la secuencia. El hijo contenido coincide con ed01…; su ejecución requeriría artefactos de proceso. Los prototipos indirectos requieren Listing |
| 00407480. param_1 y constante 0x1bd | Usa WS2_32 por ordinal, variables y estructuras parcialmente recuperadas. Se observa llamada inicial, control de -1, otras llamadas y devolución de un resultado | Es consistente con trabajo de conexión, sujeto a confirmar símbolos y prototipos. No se ha reconstruido su llamador completo ni el exploit. Una traza sería necesaria para afirmar destino, conexión o tráfico |

**Relación con OSI y NIST.** En 24d004…, 00408140 se relaciona directamente con aplicación (HTTP/WinINet); 00407480 aporta un indicio de socket/transporte y posible destino 445, pendiente de reconstruir. Las otras cuatro funciones de ese módulo solicitan operaciones locales de servicio, archivo y proceso. Las cuatro funciones de ed01… trabajan con el ZIP, archivos, permisos y procesos; las tres de u.wnry consultan token y solicitan procesos; las tres de ec1383… localizan/escriben un recurso y solicitan un proceso. Estas catorce funciones son operaciones del host, fuera de la clasificación OSI. La investigación sigue SP 800-86 para preservar, examinar, analizar e informar evidencia. La relación con CSF 2.0 se presenta retrospectivamente en el capítulo 10.3, a nivel de resultado/capacidad y con sus límites; no se asigna un control CSF a cada función. La API de servicios podría tener otras capacidades en otros programas, pero aquí los parámetros locales deben guiar la interpretación; no se le atribuye administración remota por el nombre de la API.

### ed01…: cuatro funciones

| Dirección y entrada | Cómo opera y qué recursos utiliza | Condición, continuación y prueba del efecto |
|---|---|---|
| 00401dab. Módulo y datos auxiliares para XIA/2058 | Accede al recurso y entrega sus datos a 004075ad. Con un contexto válido, 004075c4 obtiene información de entradas y 0040763d solicita extracción. Usa memoria del paquete y rutas de archivos | Si el nombre es c.wnry y ya tiene atributos válidos, omite esa extracción. Cierra contexto con 00407656. Retorno 1 no prueba cada escritura; habría que cotejar los miembros producidos |
| 00401fe7. Argumentos, ruta propia y directorio | Puede copiar tasksche.exe en la rama especial. En la principal establece directorio, solicita extracción y procesos de atributos/permisos. Después usa lectura y auxiliares hacia TaskStart | Puede salir antes por la rama de argumentos. Las llamadas externas con espera 0 no garantizan finalización. Solo alcanza la llamada indirecta si las condiciones sucesivas y el destino lo permiten. Falta el cuerpo completo de la carga |
| 00401064. Línea de proceso, parámetro de espera y posible salida | Inicializa STARTUPINFO y PROCESS_INFORMATION. CreateProcessA solicita un hijo. Si corresponde, WaitForSingleObject espera y GetExitCodeProcess consulta; cierra handles | Fallo de creación devuelve 0. Con espera no cero, un resultado de espera no cero conduce a TerminateProcess. Devuelve 1 tras creación informada; no demuestra el efecto de atributos o permisos del hijo |
| 004014a6. Archivo t.wnry y contexto de llamada | Abre y lee archivo, comprueba tamaño y WANACRY!, interpreta campos y reserva memoria con GlobalAlloc. Recurre a 004019e1, 00402a76 y 00403a77 | Comprobaciones fallidas impiden obtener el buffer útil. El llamador exige resultados posteriores antes de TaskStart. Hay que revisar el convenio __thiscall y las auxiliares para explicar la transformación completa |

En estas cuatro funciones, paquete, permisos, memoria y procesos son recursos del equipo. Una contraseña interna de paquete no es necesariamente la clave de cifrado de documentos. La cabecera WANACRY! y el campo 256 se observan; atribuirles una función criptográfica exacta exige seguir sus consumidores. Ninguna de estas cuatro funciones demuestra por sí sola una nueva conversación de red.

### u.wnry: tres auxiliares y un bloque de Listing

| Dirección y entrada | Cómo opera y qué recursos utiliza | Condición, continuación y prueba del efecto |
|---|---|---|
| 00401bb0. Contexto de seguridad consultado con handle NULL | AllocateAndInitializeSid construye el SID de administradores. CheckTokenMembership escribe la pertenencia habilitada en una variable; FreeSid libera el SID | Retorna el resultado consultado, o 0 si hubo determinados fallos. El bloque llamador utiliza ese valor para elegir auxiliar. No cambia por sí misma permisos ni eleva privilegios |
| 00401b50. Archivo, parámetros y opción de visualización | Prepara SHELLEXECUTEINFOA; coloca runas en lpVerb, el archivo en lpFile y argumentos en lpParameters; solicita ShellExecuteExA | La solicitud no prueba elevación concedida ni efecto sobre recuperación. La expresión booleana del decompilado debe leerse como está conservada; no se sustituye por un éxito de objetivo inventado |
| 00401a90. Línea de proceso, espera y posible puntero de salida | CreateProcessA obtiene, si tiene éxito, handles de proceso/hilo. Puede esperar, solicitar terminación o consultar salida, según parámetros y resultados; cierra referencias | Retorna 0 si falla la creación y 1 al completar su camino posterior. Ese 1 no demuestra que se borraran copias ni que finalizara correctamente el hijo. Se necesitan evidencias del proceso y del objeto afectado |

El Listing relaciona la cadena 00420fd8 con el bloque que consulta 00401bb0. Después selecciona 00401b50 en el camino cero o 00401a90 en el camino no cero, sujeto a las condiciones previas. El bloque principal no dispone de función contenedora correctamente decompilada en este proyecto. No se inventa un cuarto cuerpo para cubrir ese hueco. La finalidad contra recuperación se infiere del contenido y sus referencias; la eliminación efectiva no se observó.

### ec1383…: tres funciones

| Dirección y entrada | Cómo opera y qué recursos utiliza | Condición, continuación y prueba del efecto |
|---|---|---|
| 1800011a4, PlayGame. Invocación externa aún no identificada | sprintf construye C:\\WINDOWS\\mssecsvc.exe en una variable global. Llama al extractor y después a la auxiliar de proceso | No prueba el retorno del extractor entre llamadas. Retorna 0. La exportación existe, pero falta demostrar quién la invocó y con qué contexto |
| 180001014. Handle global de módulo y ruta global | Busca W/101, obtiene datos y tamaño; lee el DWORD inicial como longitud. CreateFileA solicita el destino; WriteFile usa recurso+4 y esa longitud; cierra archivo | Fallos iniciales devuelven 0. Superados esos controles, puede retornar 1 aun si no abre el archivo. No valida el resultado de escritura ni todos los límites de longitud. El cotejo externo del PE no es una comprobación realizada por esta función |
| 1800010f8. Ruta preparada por PlayGame | Inicializa estructuras y solicita CreateProcessA. Con resultado no cero, cierra los handles devueltos | No espera al proceso y retorna 0 en ambos caminos. Para afirmar ejecución y resultado se requieren registros correlacionados del hijo y sus cambios; cerrar handles no lo termina |

W/101 es un recurso local del módulo. El PE delimitado tiene SHA-256 93db4b26… y es distinto de 24d004…. El nombre de archivo de destino o su parecido con un servicio no sustituye el hash. El comportamiento posterior del hijo requiere su propio análisis; no se heredan automáticamente todas las conclusiones de otro componente.

### 10.3 De la función a la evidencia y al resultado NIST

| Pregunta técnica | Evidencia adecuada para resolverla | Relación retrospectiva y límite |
|---|---|---|
| ¿Se abrió una conexión y qué transportó? | Tráfico o registros de red correlacionados con proceso, dirección y tiempo | DE.CM-01 orienta el monitoreo de redes; una constante estática no acredita ese monitoreo |
| ¿Se creó un servicio o un proceso? | Configuración, registros y contexto de ejecución preservados | DE.CM-09 orienta el monitoreo del entorno de ejecución; las APIs son pistas para buscar artefactos |
| ¿Se escribió el hijo esperado? | Contenido adquirido, tamaño, hash y procedencia; correlación temporal | RS.AN-03 apoya el análisis causal y RS.AN-07 la integridad/procedencia; nombre idéntico no prueba identidad |
| ¿Se impidió la recuperación? | Estado anterior y posterior de mecanismos de recuperación y registros de operaciones | El código motiva investigar; no acredita por sí solo pérdida de respaldo ni éxito del ataque |
| ¿Se recuperaron datos confiables? | Validación del respaldo y de los datos restaurados, con alcance declarado | RC.RP-03 orienta la verificación de los activos de restauración. La copia benigna en el mismo disco solo aporta una demostración limitada |

OSI organiza dónde buscar comunicaciones; el método de SP 800-86 organiza cómo preservar y razonar sobre lo adquirido. Los códigos CSF no se asignan mecánicamente uno por capa. Un mismo hallazgo puede orientar detección, análisis y recuperación, sin demostrar que esos resultados de gestión estén plenamente implantados.
