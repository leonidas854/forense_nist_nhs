### 13.1 Secuencia de exposición y reparto de revisión

La autoría continúa siendo colectiva de los ocho autores. Para ensayar, cuatro parejas pueden revisar los cuatro componentes y luego intercambiar revisiones; no se atribuye una función a una persona sin constancia. Quienes expongan deben poder seguir el recorrido completo. El siguiente guion propone 20 minutos y puede repartirse entre dos voces sin cambiar la autoría.

| Tiempo | Qué mostrar | Qué debe comprender el público |
|---|---|---|
| 0–2 min | Pregunta, caso NHS y fuentes | El incidente histórico y nuestras observaciones de laboratorio son conjuntos distintos |
| 2–6 min | Matriz de las siete capas y figura 8 | HTTP/SMB, TCP/IP y soporte de enlace; operaciones locales fuera de esa clasificación |
| 6–9 min | 24d004…, 00408140 y R/1831 | Condición NULL, continuación y extracción; API llamada no equivale a efecto completado |
| 9–12 min | ed01…, XIA/2058 y TaskStart | Paquete, procesos externos y frontera de la carga no reconstruida |
| 12–14 min | u.wnry, token y Listing | Consulta de pertenencia, selección de auxiliar y efecto contra recuperación aún no observado |
| 14–16 min | ec1383…, W/101 | Longitud, +4, escritura y llamada siguiente aunque el retorno no se valide |
| 16–18 min | Cadena de impacto y mapeo NIST | Cómo los mecanismos ayudan a explicar indisponibilidad, contención y recuperación histórica |
| 18–20 min | Práctica benigna y conclusiones | Qué se comprobó realmente, qué sigue pendiente y cómo se preservó la evidencia |

Cada explicación de código debe contener una entrada, una condición, un recurso y un siguiente paso. Es preferible mostrar dos decisiones bien justificadas y dejar el catálogo completo para las preguntas que leer 16 cuerpos de C en voz alta.

### 13.2 Respuestas razonadas a preguntas del ingeniero

**¿Qué hace WannaCry en cada capa OSI?** En las funciones seleccionadas se observa una solicitud HTTP mediante WinINet y una rutina con indicios de conexión a 445; la propagación mediante SMBv1 se sustenta además en fuentes técnicas. TCP/IP y enlace proporcionan el transporte subyacente. Para presentación y sesión no se ha aislado aquí un mecanismo específico. El archivo no contiene necesariamente una función por capa.

**¿Dónde está la vulnerabilidad: en la capa 4 o en el puerto?** El puerto identifica un extremo de transporte. MS17-010 corrige el tratamiento de solicitudes en el servidor SMBv1. Una conexión a 445 no prueba explotación; hay que estudiar el protocolo y el efecto en el receptor. El servicio puede implementarse en componentes del sistema sin que cambie el papel conceptual del protocolo de aplicación.

**¿El cifrado corresponde a presentación?** El cifrado de documentos en disco es una operación local. Para asignar un mecanismo a presentación habría que justificar su papel en el intercambio de datos entre entidades; transformar bytes por sí solo no basta. Aquí tampoco se reconstruyó el cifrador entero, así que distinguimos la descripción técnica publicada del cuerpo local disponible.

**¿Qué función hace el cifrado exactamente?** Nuestra selección muestra lectura y procesamiento de t.wnry, auxiliares y una llamada indirecta asociada a TaskStart. Falta recuperar y analizar toda esa carga para asignar cada operación criptográfica a instrucciones concretas. No es correcto llamar «cifrador completo» a 004014a6 ni al CALL EAX sin estudiar su destino.

**¿Qué es W/101 y por qué se suma 1?** W es el tipo del recurso PE y 101 es su ID. El primer DWORD contiene la longitud. Como el puntero es DWORD*, sumar 1 avanza cuatro bytes, no uno; la instrucción LEA confirma +4. Así se omite la longitud y se apunta al PE. Esa rutina copia datos; no muestra descifrado.

**¿Qué sucede si falla la escritura en ec1383…?** La auxiliar puede devolver 1 tras superar los controles iniciales aunque no logre abrir el destino; tampoco comprueba el resultado de WriteFile para decidir ese retorno. PlayGame llama después a la auxiliar de proceso sin validar la extracción. Que exista esa llamada no garantiza un hijo válido: pueden faltar datos, permisos o un archivo utilizable.

**¿Qué es un handle y por qué lo cierra?** Es una referencia gestionada por una API a un objeto o contexto. Se usa para operaciones posteriores y se cierra con la API correspondiente. Cerrar el handle del proceso no equivale a terminarlo. El significado se obtiene del tipo de objeto y del contrato de la API.

**¿Cero siempre significa error?** No. InternetOpenUrlA devuelve NULL si falla; memcmp devuelve cero cuando los bytes comparados coinciden. Algunas auxiliares de las muestras devuelven cero en todos sus caminos. Hay que leer el contrato de la API y las ramas del llamador, no memorizar un significado universal.

**¿Cuánta memoria o CPU utiliza?** Conocemos tamaños de archivos y recursos, y vemos reservas y operaciones. No medimos consumo dinámico del malware. El tamaño del PE, la reserva de una auxiliar y la memoria total del proceso son magnitudes diferentes. La VM configurada con 4 GB no demuestra que el malware consuma 4 GB ni que necesite esa cantidad.

**¿Qué sigue después de CreateProcessA?** Primero se distingue si informó éxito. Luego se mira si el llamador espera, consulta salida o solo cierra handles. En 1800010f8 no hay espera. En 00401064 y 00401a90 la espera depende de un parámetro. Para demostrar el trabajo del hijo se necesitan datos de ese hijo y del objeto afectado. [API3]

**¿Sin red ya no puede hacer nada?** Deshabilitar la red impide ese canal de comunicación; no equivale a impedir operaciones locales. En 00408140, un resultado NULL permite continuar hacia preparación. El aislamiento del laboratorio no es una prueba de inocuidad ni se utilizó para ejecutar WannaCry. Se estudiaron las decisiones estáticamente y se realizó un ejercicio benigno separado.

**¿El error 500 de ANY.RUN demuestra que se detuvo?** El dato comunicado corresponde a la página del servicio. Sin informe de tarea no tenemos resultado de la API del malware, traza del proceso ni efecto sobre archivos. No se traslada ese 500 a la condición del kill switch.

**¿Podemos afirmar que estos cuatro archivos recorrieron juntos el NHS?** No. La contención 24d004… → ed01… → paquete con u.wnry se acredita localmente. ec1383… contiene otro PE. La cadena hospitalaria concreta requeriría evidencias con procedencia, tiempos y contexto del hospital, no solo parecido funcional.

**¿En qué parte se aplica NIST?** SP 800-86 ordena preservación, examen, análisis e informe. CSF 2.0 permite discutir resultados de gestión retrospectivamente. OSI ayuda a explicar comunicaciones. Los tres aportan perspectivas distintas; ninguno transforma una hipótesis en observación. La matriz se sustenta en los hallazgos y declara sus límites.

### 13.3 Ensayo de una respuesta completa

«En ec1383…, la exportación PlayGame construye una ruta global y llama a 180001014. Esta busca W/101, comprueba referencias iniciales, lee una longitud de cuatro bytes y solicita escribir el tramo siguiente. El recurso utiliza memoria del módulo y la escritura utiliza un archivo del sistema. Su retorno no garantiza que se haya escrito. PlayGame llama después a 1800010f8 sin validar ese resultado; esta solicita un proceso y no espera a que termine. Son operaciones locales, no siete pasos OSI. Para demostrar ejecución necesitaríamos correlacionar archivo, contenido, proceso y tiempo. El código local no acredita por sí solo que esto sucediera en el NHS».

Para evaluar el ensayo, el compañero debe poder señalar la dirección de cada afirmación y distinguir llamada, retorno y efecto. Una respuesta correcta puede concluir «no está demostrado con esta selección» y explicar qué evidencia lo resolvería.
