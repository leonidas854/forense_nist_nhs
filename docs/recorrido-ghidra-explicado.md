# Estudiar el código actual de WannaCry en Ghidra

Para profundizar en la relación entre capas y comparar las dos vistas, continúa
con [Capas: decompilado y desensamblado](guia-capas-decompilado-desensamblado.md).
Incluye nuevas comprobaciones del depósito de R/1831 y la lectura de t.wnry.

Revisión del **15/11/2026** mediante MCP. Proyecto:
`local/ghidra/proyectos/WannaCry_NHS.gpr`. Respuestas conservadas en
`local/recorrido-ghidra/`. Se examinaron archivos y código sin ejecutar las
muestras ni contactar el dominio embebido.

## 1. Qué tienes realmente

Tienes binarios compilados y un proyecto de ingeniería inversa. **Decompiler**
reconstruye pseudocódigo parecido a C; no recupera necesariamente el código fuente
original. **Listing** muestra instrucciones desensambladas. Las conclusiones
deben contrastarse con bytes, referencias y documentación de las APIs.

| Programa, abreviado | Observación local | Punto para empezar |
|---|---|---|
| `24d004…exe-e88954` | Comprobación de dominio, servicio y recurso R/1831 | `00408140` |
| `ed01eb…exe-5ff465` | Contenido de R/1831; contiene ZIP XIA/2058 | `00401dab` |
| `ec1383…exe-a0366d` | DLL de 64 bits, aunque se llama .exe; recurso W/101 | `180001014` |
| `W_101_contenido.exe-32b201` | PE delimitado extraído de W/101 | Comparación detallada pendiente |
| `u.wnry-45356a` | PE extraído del ZIP; cadena contra mecanismos de recuperación | `00420fd8` |
| `taskdl.exe-47a9ad`, `taskse.exe-be5d62` | Auxiliares importados y autoanalizados | Interpretación detallada pendiente |

Las relaciones comprobadas por extracción y hashes son:

```text
24d004…
└── R / 1831 = ed01eb…
    └── XIA / 2058 = ZIP
        ├── u.wnry
        ├── taskdl.exe y taskse.exe
        └── t.wnry y otros archivos

ec1383…
└── W / 101
    ├── primeros 4 bytes: longitud del PE
    └── PE de 3.756.032 bytes: SHA-256 93db4b26…
```

**El texto adjunto intercambia ed01 y 24d004.** El PE de W/101 tampoco es
idéntico a 24d004: su hash es distinto. La estructura de ec1383 no prueba que
proceda de un honeypot. Los hashes completos, tamaños y offsets están en
[el análisis comprobado](analisis-ghidra-codigo.md) y en
`local/ghidra/extraidos/manifiesto.json`.

Los campos de fabricante o nombre original de un PE pueden falsificarse. Ver
«Microsoft Corporation» o «DiskPart» en los recursos no acredita esa autoría.

## 2. Abrir y aprender a leer la pantalla

Desde `/home/leonidas/deveploment/forense_nist_nhs`, comprueba los archivos:

```bash
python3 scripts/verificar_caso_nist.py
```

Esta revisión devolvió **49 archivos verificados y 20 filas de matriz**. Comprueba
integridad y referencias de códigos CSF, no la verdad automática del informe ni
cumplimiento NIST. La comprobación quedó en
`local/revision-nist/comprobacion-20261115T165313361319Z.json`.

Si Ghidra está abierto, usa esa ventana. Si está cerrado:

```bash
./scripts/ghidra-mcp.sh
```

No abrir otra instancia sobre el mismo proyecto. Para comprobar el puerto:
`ss -ltn '( sport = :8765 )'`. La instalación ya preparada se documenta en
[ghidra-mcp.md](ghidra-mcp.md); no necesitas reinstalar para este recorrido.

1. Abre con doble clic **dentro de Ghidra** el programa `24d004…`.
2. Activa **Window → Decompiler**, **Window → Symbol Tree** y
   **Window → Defined Strings** si no están visibles.
3. Haz clic en Listing, pulsa **G**, escribe `00408140` y acepta.
4. Comprueba siempre la pestaña del programa: una dirección sola es ambigua.
5. Haz doble clic en una función del Decompiler para seguir una llamada.
6. Para los usos de una cadena, abre en Listing el menú contextual
   **References → Show References To**.

| Elemento | Significado |
|---|---|
| `0x727` | Hexadecimal: 1831 decimal |
| `00408140` | Dirección virtual de este programa; no offset dentro del archivo |
| `FUN_…` | Nombre automático cuando falta un nombre original útil |
| `DAT_…` / `local_…` | Dato o variable local identificados por Ghidra |
| `undefined4` | Valor de cuatro bytes con tipo preciso todavía desconocido |
| `NULL` / `(void *)0x0` | Puntero nulo; significado según la API |
| `handle` | Referencia que Windows entrega para trabajar con un objeto |
| `XREF` | Referencia desde código/datos, no registro de ejecución |
| `Comprobar_KillSwitch` | Nombre descriptivo añadido por el analista |

Los nombres españoles no son nombres originales recuperados. Registra el motivo
de cada anotación. Los prototipos de WinINet ya se corrigieron; otras zonas
todavía tienen tipos y argumentos imperfectos. **Autoanálisis terminado no
equivale a ingeniería inversa exhaustiva.**

## 3. Primera práctica: entender la decisión del kill switch

**Pregunta:** ¿qué condición permite entrar en la rutina posterior?

Programa `24d004…`, dirección `00408140`. Busca `InternetOpenA` y
`InternetOpenUrlA`. Esta es una simplificación didáctica del flujo, que omite
la copia de la cadena y el cierre de handles:

```c
handle = InternetOpenUrlA(session, url, NULL, 0, 0x84000000, 0);
if (handle == NULL) {
    Preparar_Servicio_Y_Carga();
}
return 0;
```

`url` procede de `004313d0` y se copia a una variable local. Ese bucle copia
texto; no demuestra cifrado. `InternetOpenA` prepara la sesión y la llamada
siguiente intenta abrir el recurso. Microsoft documenta handle válido o `NULL`
si falla; este código no comprueba explícitamente HTTP 200.
[Microsoft, InternetOpenUrlA](https://learn.microsoft.com/en-us/windows/win32/api/wininet/nf-wininet-internetopenurla).

| Resultado | Rama observada |
|---|---|
| `NULL` | Cierra handles, llama a `00408090` y retorna |
| No nulo | Cierra handles y retorna sin esa llamada |

Comprueba en Listing:

```text
00408194  CALL [0040a138]   ; InternetOpenUrlA
0040819a  MOV EDI,EAX      ; conserva el resultado
004081a3  TEST EDI,EDI     ; comprueba si es cero
004081a5  JNZ 004081bc     ; si no es cero, evita la llamada posterior
...
004081ad  CALL 00408090    ; rama del resultado cero
```

`TEST` establece los indicadores del procesador; `JNZ` salta si no es cero.
Ambas ramas retornan cero: ese `return 0` no significa «ataque exitoso». La
decompilación incluye un cierre con handle nulo; conservarlo al transcribir
literalmente, aunque el ejemplo explicativo lo omita.

**Conclusión:** esa comprobación gobierna el acceso a una rutina en el camino
examinado. **No demuestra:** qué respuesta recibió un equipo NHS, una causa
concreta de firewall/proxy, ausencia global de daño o reversión de cifrado previo.
No hace falta visitar el dominio para analizar la condición.

## 4. Segunda práctica: seguir la rama y el servicio

Ve a `00408090`. `__p___argc` permite consultar el número de argumentos del
proceso. Si es menor que dos, llama a `00407f20`, cuyo cuerpo observado contiene:

```c
Crear_Servicio_mssecsvc();
Extraer_Recurso_R_1831();
return 0;
```

Con más argumentos aparece otro camino relacionado con el gestor de servicios.
La secuencia anterior no describe necesariamente todos los caminos del programa.

Ve a `00407c40` y lee estas operaciones:

| Llamada | Interpretación |
|---|---|
| `OpenSCManagerA` | Solicita acceso al gestor de servicios |
| `CreateServiceA` | Solicita crear `mssecsvc2.0`, con argumento `-m security` |
| `StartServiceA` | Solicita iniciarlo si se obtuvo un handle de servicio |

El **2 en dwStartType** corresponde a inicio automático. No aplicar ese
significado a cualquier 2 de cualquier función.
[Microsoft, CreateServiceA](https://learn.microsoft.com/en-us/windows/win32/api/winsvc/nf-winsvc-createservicea).

**Puedes afirmar:** existe código para solicitar creación e inicio del servicio.
**No puedes afirmar:** que Windows aceptó las solicitudes. Harían falta registros
del sistema adquirido, como configuración del servicio y eventos disponibles
de instalación. Aquí no se adquirió un evento 7045.

Ejercicio: identifica el `if` que impide llamar a `StartServiceA` cuando no hay
handle. Explica por qué ese control no demuestra que `StartServiceA` tuvo éxito.

## 5. Tercera práctica: seguir los recursos hasta el paquete

En `24d004…`, ve a `00407ce0`:

| API | Función en la secuencia |
|---|---|
| `FindResourceA` | Localiza R, ID `0x727` = 1831 |
| `LoadResource` | Obtiene un handle de sus datos |
| `LockResource` | Obtiene un puntero a los bytes |
| `SizeofResource` | Obtiene el tamaño |
| `WriteFile` | Se usa después para escribir bytes |

`FindResourceA` sola no extrae al disco. Varias APIs se resuelven mediante
`GetProcAddress`: para entender una llamada indirecta a `DAT_…`, sigue qué
dirección se le asignó. Aquí todavía hay argumentos mal reconstruidos: no
transcribirlos como si fueran código fuente original exacto.

El manifiesto muestra que R/1831 mide **3.514.368 bytes** y coincide con ed01.
Puedes verificar igualdad sin ejecutar los archivos:

```bash
cmp local/ghidra/extraidos/24d004a1/R_1831_1033.bin \
  wannacry/ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa.exe
```

Sin diferencias, `cmp` no imprime contenido y termina con código cero. La
igualdad de bytes demuestra esta relación; no demuestra procedencia hospitalaria.

Abre **ed01…** y ve a `00401dab`: localiza **XIA/2058**, ID `0x80a`.
La extracción estática identificó un ZIP y validó sus miembros. En `00401fe7`
verás la llamada de extracción, la referencia a la contraseña interna en
`0040f52c`, a `icacls` en `0040f4fc`, y referencias posteriores a `t.wnry` y
`TaskStart`. La secuencia está condicionada por varios resultados.

La contraseña sirve para el paquete: **no descifra por sí misma documentos de
víctimas**. `t.wnry` sigue como contenedor cifrado; no se ha reconstruido toda
su criptografía. Una referencia a `TaskStart` no demuestra una llamada exitosa.

## 6. Cuarta práctica: entender W/101 y los punteros

Abre **ec1383…**, dirección `180001014`. Fragmento observado:

```c
DVar1 = *pDVar2;
/* ... apertura del archivo ... */
WriteFile(hFile, pDVar2 + 1, DVar1, local_res8, NULL);
```

`pDVar2` es un `DWORD *`: sumarle uno avanza **cuatro bytes**, no uno. El primer
DWORD contiene la longitud; la escritura empieza después. El extractor comprobó
límites y obtuvo un PE de 3.756.032 bytes. No hay descifrado de W/101 en esta rutina.

Observa además que retorna 1 incluso por una ruta donde `CreateFileA` falló,
y aquí no comprueba el retorno de `WriteFile`. Por eso no basta interpretar
«retornó 1» como «escribió correctamente todo el archivo».

En `1800010f8` aparece `CreateProcessA` usando la ruta global. Esto sustenta una
capacidad de lanzar la carga; no acredita captura en honeypot, inyección por un
exploit concreto ni ejecución en un hospital.

Ejercicio resuelto: ¿por qué cortar desde la primera firma MZ hasta el final
del recurso puede producir un hash distinto? Porque puede incluir bytes posteriores
al PE delimitado. Aquí la longitud declarada permite definir el contenido preciso.

## 7. Quinta práctica: distinguir conexión y explotación

Vuelve a **24d004…**, `00407480`. En `004074a2`, Listing muestra
`PUSH 0x1bd`: **445 decimal**. Mira también
**Symbol Tree → Imports → WS2_32.DLL**. Varias funciones están importadas por
ordinal, de ahí `Ordinal_9`, `Ordinal_4`, etc., con firmas todavía incompletas.

La constante y el contexto de sockets sustentan una rutina para comprobar
conexión al puerto 445. Recuperar todos los nombres requiere contrastar las
exportaciones y las firmas, no adivinar por el número del ordinal.

MCP encontró referencias de llamada en `004076b6`, `0040794c` y `00407999`.
Son puntos para continuar el estudio del flujo. No se ha reconstruido aquí el
exploit completo ni todos los llamadores. Un resultado vacío de búsqueda semántica
tampoco demostraría ausencia: algunos programas aún no tienen ese índice listo.

445 se utiliza para SMB sobre TCP y **no identifica exclusivamente SMBv1**.
[Microsoft, transporte SMB](https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/direct-hosting-of-smb-over-tcpip),
[Microsoft, SMB2/3](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-smb2/4287490c-602c-41c0-a23e-140a1f137832).

Puerta abierta, versión vulnerable, parche ausente y explotación exitosa son
afirmaciones distintas. El puerto por sí solo no prueba las otras. Tampoco
demuestra que todos los hospitales estuvieran en una N3 sin segmentación.

## 8. Sexta práctica: del texto de sabotaje a su uso potencial

Abre **u.wnry**, `00420fd8`. La cadena contiene `vssadmin`, `wmic`, `bcdedit`
y `wbadmin`, con operaciones contra copias sombra, catálogo y opciones de
recuperación. Léela dentro de Ghidra; no es una orden para pegar en una consola.

1. Localiza la cadena con la dirección o Defined Strings.
2. Abre las referencias `004066fe` y `0040670c`: cargan su dirección y copian bytes.
3. En `0040672f`, observa la llamada a `00401bb0` y la decisión posterior.
4. Abre `00401bb0`: construye un SID con autoridad 5 y subautoridades 32 y 544
   (`0x20`, `0x220`), y usa `CheckTokenMembership`.
5. Si esa rutina devuelve cero, el bloque llama a `00401b50`: esta usa
   `ShellExecuteExA` con verbo `runas`.
6. En la otra rama se prepara una cadena y se llama a `00401a90` desde
   `0040677c`: esta rutina usa `CreateProcessA`.

El SID construido corresponde al grupo integrado Administradores. La API
comprueba si el SID está habilitado en el token efectivo. No concede privilegios.
Su resultado de pertenencia se escribe en un parámetro de salida; su retorno
indica si la consulta funcionó. La rutina de la muestra retorna cero también
cuando la consulta falla, así que cero no demuestra siempre «usuario no administrador».
[Microsoft, CheckTokenMembership](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-checktokenmembership).

Esquema didáctico del bloque, no transcripción completa:

```text
Preparar la cadena
        |
Consultar SID de Administradores
        |
        +-- resultado cero --> rutina con ShellExecuteExA / runas
        |
        +-- resultado no cero --> rutina con CreateProcessA
```

`runas` es una solicitud, no prueba de elevación conseguida. En `00401a90`
el código comprueba si `CreateProcessA` falló; si tuvo éxito puede retornar 1
sin esperar al proceso cuando su parámetro de espera es cero. El llamador
examinado pasa ese cero. **Crear un proceso no demuestra que todas las órdenes
de la cadena concluyan correctamente.**

MCP no encontró una función decompilable que contuviera `004066fe` en el estado
actual. Listing sí muestra instrucciones. No crear una función arbitrariamente
ahí para ocultar el problema: antes habría que recuperar sus límites.

Conclusión sustentada: cadena referenciada desde código con caminos hacia
rutinas que solicitan ejecución. No se demostró borrado efectivo, privilegios
suficientes ni el momento respecto al cifrado. Las copias sombra no equivalen
a todos los respaldos y su existencia no está garantizada en cada Windows.

## 9. Qué es incorrecto o todavía no está demostrado

| Afirmación del texto adjunto | Evaluación |
|---|---|
| ed01 contiene a 24d004 | Incorrecta: relación comprobada inversa |
| Responde el dominio y ya no puede haber daño | Excesiva: esta rama evita una llamada, no revierte daños |
| Los proxies NHS explican las infecciones posteriores | Hipótesis que requiere evidencia de los equipos/redes |
| 445 abierto demuestra SMBv1 vulnerable y explotación | Inferencia insuficiente |
| Toda N3 era plana y todos se infectaron entre sí | Generalización no acreditada |
| FindResourceA extrae por sí sola al disco | Incorrecta: localiza; siguen otras operaciones |
| Creación de tasksche marca el inicio exacto del cifrado | Incorrecta: creación, ejecución y cifrado son eventos distintos |
| W/101 se descifra en la rutina estudiada | No corresponde al código observado: longitud y PE en claro |
| Contraseña ZIP equivale a clave de los documentos | Incorrecta |
| La cadena de sabotaje está en ed01 | Para esta cadena, está en el miembro u.wnry |
| Se borraron todas las copias de rayos X, resonancia y servidores NHS | No demostrado con nuestras muestras ni artefactos de esos equipos |
| Ver sabotaje demuestra RC.RP-01 | Incorrecta: hace falta evidencia de ejecución de recuperación |

NHS §2.3 considera **probable** la entrada por SMB vulnerable expuesto. NAO,
resumen 12, documenta propagación por internet, incluida N3, y no por NHSmail.
No identifica así el primer equipo ni cada salto. Véanse fuente, páginas y
límites del hallazgo H-04 del [informe corregido](informe-forense.md).

## 10. Trabajar el caso con NIST y registrar hallazgos

SP 800-86 estructura recopilación, examen, análisis y presentación de resultados.
En esta práctica: identificar/preservar muestras, examinar código, contrastar
hipótesis y comunicar conclusiones con límites. CSF 2.0 es un mapeo retrospectivo
del caso de 2017, no una certificación del trabajo.
[NIST SP 800-86](https://doi.org/10.6028/NIST.SP.800-86),
[NIST CSF 2.0](https://doi.org/10.6028/NIST.CSWP.29).

| Resultado CSF | Qué aportar |
|---|---|
| RS.AN-03 | Explicación de mecanismos, causas y alternativas |
| RS.AN-06 | Registro de actuaciones, fechas, herramientas y anotaciones |
| RS.AN-07 | Datos y metadatos, integridad, procedencia y relación original/derivado |
| PR.IR-01 | Relacionar exposición con controles; para evaluarlos hacen falta reglas/topología reales |
| PR.DS-11 | Protección y pruebas de respaldos; el código solo muestra el riesgo |
| RC.RP-01 | Evidencia de ejecución del plan de recuperación; pendiente localmente |
| RC.RP-03 / RC.RP-05 | Verificar respaldos antes de usarlos y activos después de restaurarlos |

Registra en `local/`, fuera de Git, para cada hallazgo:

1. Pregunta e identificador.
2. Hash completo, programa, dirección y herramienta/versión.
3. Acción real, fecha de análisis y archivo de respuesta o captura conservado.
4. Observación literal e interpretación justificada.
5. Alternativas y evidencia faltante.
6. Fuente histórica separada con página/sección, si relacionas con NHS.
7. Resultado NIST y límite del mapeo.

Ejemplo de conclusión:

> En la muestra local 24d004… se observó en 00408140 una comparación del handle
> de InternetOpenUrlA con cero. El ensamblado confirma que la rama cero llama
> 00408090. Esto explica una condición del flujo y contribuye a RS.AN-03.
> No demuestra qué respuesta recibió un equipo NHS ni la causa individual de
> su infección.

No conviertas la fecha de la consulta MCP en fecha de infección. Un hash
coincidente acredita integridad respecto de una referencia; no reconstruye la
procedencia ni la cadena de custodia previa.

## 11. Repetir una consulta y estudiar por tu cuenta

Con Ghidra/MCP abierto, desde la raíz del repositorio:

```bash
PYTHON=local/ghidra/herramientas/pyghidra-mcp/.venv/bin/python
"$PYTHON" scripts/ghidra_mcp_consulta.py list_project_binaries
"$PYTHON" scripts/ghidra_mcp_consulta.py decompile_function \
  '{"binary_name":"/24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c.exe-e88954","name_or_address":"00408140"}' \
  --output local/recorrido-ghidra/mi-consulta-killswitch.json
```

Elige una salida nueva para cada actuación. Revisa `isError` y también el
campo `error` individual de cada función: una respuesta MCP general correcta
puede contener un fallo de decompilación. Los resultados de este recorrido
se guardaron bajo `local/recorrido-ghidra/`, excluido de Git.

Orden de estudio recomendado:

| Sesión | Trabajo | Resultado que debes poder explicar |
|---|---|---|
| 1 | Secciones 1–3: interfaz, tipos y kill switch | Dibujar las dos ramas y explicar NULL |
| 2 | Secciones 4–6: servicio y recursos | Relacionar archivos por hashes y explicar DWORD + 1 |
| 3 | Secciones 7–8: conexiones y sabotaje | Distinguir capacidad, llamada y éxito |
| 4 | Secciones 9–10: contrastar NHS y NIST | Escribir un hallazgo con fuente y limitación |

Preguntas resueltas para autoevaluarte:

- **¿Una cadena prueba ejecución?** No; las referencias muestran uso potencial.
  Para ejecución hacen falta observaciones o artefactos del sistema.
- **¿Una llamada CreateProcessA prueba borrado?** No; hay que comprobar creación,
  ejecución de órdenes y resultado sobre los objetos afectados.
- **¿Un timestamp de creación prueba cuándo empezó el cifrado?** No; correlacionar
  varios artefactos y sus relojes. Los timestamps pueden alterarse.
- **¿No aparece una función en Decompiler, entonces no hay código?** No; revisar
  Listing, referencias y límites de funciones. Aquí ocurrió en 004066fe.
- **¿El servicio tiene nombre de Microsoft, entonces es legítimo?** No; el nombre
  es un dato controlable, no una firma de confianza.
- **¿Tenemos el incidente NHS reconstruido host por host?** No; tenemos documentación
  histórica y muestras locales, sin imágenes de disco/RAM de esos hospitales.
- **¿Tenemos todo WannaCry explicado?** No; quedan la criptografía de t.wnry,
  auxiliares, caminos no revisados y la procedencia previa de las muestras.

La VM no está registrada en este anfitrión: no se presenta una detonación,
captura RAM ni recuperación como ejecutadas. El próximo trabajo estático útil
es completar los límites de funciones y tipos pendientes, siguiendo siempre
la evidencia y documentando cada cambio; no hace falta habilitar redes.
