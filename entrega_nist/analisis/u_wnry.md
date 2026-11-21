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
