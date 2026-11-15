# Análisis estático comprobado en Ghidra

Revisión del **15 de noviembre de 2026**, Ghidra **12.2 DEV** en Linux,
mediante PyGhidra-MCP. Este documento sustituye el relato anterior, que
intercambiaba los papeles de dos hashes y presentaba pseudocódigo ilustrativo
como decompilación observada. Se conservó una copia local del texto anterior
en `local/ghidra/resultados/analisis-ghidra-anterior-no-validado.md`.

Las observaciones pertenecen a muestras locales. No acreditan ejecución,
adquisición de RAM ni hechos de un hospital del NHS. El marco NIST CSF 2.0
se aplica retrospectivamente; no describe el marco vigente en 2017.

## Identificación y relación entre capas

| SHA-256 | Bytes | Observación local |
|---|---:|---|
| `24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c` | 3.723.264 | PE32 x86; comprobación de URL, servicio y recurso R/1831 |
| `ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa` | 3.514.368 | PE32 x86; componente extraído del anterior, ZIP XIA/2058 y preparación de la carga |
| `ec138352c4726fa3b6706b30bf4692252f818108c8066e8518920dd9823a34bb` | 5.298.176 | PE32+ DLL x64; extracción de W/101 y llamada a CreateProcessA |

Los tres hashes se recalcularon sobre los originales. **R/1831 de 24d004…
es exactamente ed01…**: offset de archivo 204.964, longitud 3.514.368 y el
mismo SHA-256. Es un PE, no el ZIP cifrado. El ZIP está en **XIA/2058 de
ed01…**, offset 65.776, longitud 3.446.325.

El recurso **W/101 de ec1383…** ocupa 5.242.880 bytes desde el offset 51.364.
Su primer DWORD little-endian declara 3.756.032 bytes de contenido que
empiezan cuatro bytes después. La decompilación confirma esa longitud de
`WriteFile` y el comienzo en recurso+4. El PE delimitado tiene SHA-256
`93db4b26be3a4e6b724bf85830746f458cde613ad88501bcb23d2ae1ab9976c9`;
no es idéntico a 24d004…. La rutina examinada no descifra W/101.

Se conservaron 40 derivados con hashes y relaciones padre/hijo en
`local/ghidra/extraidos/manifiesto.json`, incluidos los 36 miembros del ZIP.
Los cortes antiguos `wannacry/pe_extraido_*` se preservan pero no se usaron
como fuente del proyecto nuevo: sus longitudes incluían bytes posteriores.

## Direcciones para revisar

Son direcciones virtuales de cada programa, no offsets de archivo.

| Programa | Dirección | Nombre del analista / hallazgo | Relación retrospectiva |
|---|---|---|---|
| 24d004… | `00408140` | `Comprobar_KillSwitch`: resultado de InternetOpenUrlA determina la rama | RS.AN |
| 24d004… | `00407c40` | `Crear_Servicio_mssecsvc`: mssecsvc2.0, argumento `-m security` | DE.CM |
| 24d004… | `00407ce0` | `Extraer_Recurso_R_1831`: ID `0x727`, tipo R | RS.AN |
| 24d004… | `00408090` | `Preparar_Servicio_Y_Carga`: ramas según argumentos | RS.AN |
| 24d004… | `00407480` | `Comprobar_Conexion_445`: constante `0x1bd` y sockets por ordinal | PR.IR / DE.CM |
| ed01… | `00401dab` | `Extraer_Paquete_XIA_2058`: ID `0x80a` | RS.AN |
| ed01… | `00401fe7` | `Preparar_Paquete_Y_Permisos`: contraseña interna e icacls | RS.AN |
| ec1383… | `180001014` | `Extraer_Recurso_W_101`: ID `0x65`, longitud y escritura del PE | RS.AN |
| ec1383… | `1800010f8` | `Crear_Proceso_Carga`: llamada a CreateProcessA | DE.CM |
| u.wnry | `004066fe`, `0040670c` | Referencias al comando de sabotaje desde `00420fd8` | RC.RP |

Los nueve nombres de funciones son anotaciones del analista guardadas en el
proyecto, no nombres de código fuente recuperados. Los identificadores NIST
son categorías: esta relación no constituye una evaluación de cumplimiento.

## Qué demuestra el kill switch

En 24d004…, el ensamblado de `00408140` copia la URL desde `004313d0`,
prepara cinco argumentos de `InternetOpenA` con tipo de acceso **1**, llama
a `InternetOpenUrlA` y compara su handle con cero. Si es cero, llama a
`00408090`; si es distinto de cero, retorna sin esa llamada.

No se observa una comprobación explícita de HTTP 200 ni la llamada a
`ExitProcess` del texto anterior. Tampoco debe representarse esta llamada
como `INTERNET_OPEN_TYPE_PRECONFIG`. Microsoft distingue el acceso directo
de la lectura de configuración del registro.
[Microsoft, InternetOpenA](https://learn.microsoft.com/en-us/windows/win32/api/wininet/nf-wininet-internetopena).

Una restricción HTTP podría afectar a esa rama: es una inferencia del código.
Atribuirla a proxys concretos del NHS requiere evidencia histórica independiente.
Esta revisión no contactó el dominio embebido.

## Paquete interno y sabotaje de recuperación

La contraseña interna se localizó en ed01… y permitió extraer XIA/2058
estáticamente, validando los CRC del ZIP. Los archivos y la contraseña se
conservan localmente. `t.wnry` sigue siendo un contenedor cifrado, no una DLL
decompilada en esta sesión.

La cadena con `vssadmin`, `wmic`, `bcdedit` y `wbadmin` está en **u.wnry**, no
en la dirección atribuida a ed01… en el texto anterior. Se comprobaron sus
referencias y el ensamblado posterior. En ed01… se confirmó `icacls` y su
referencia en `00401fe7`. Esto demuestra presencia y uso potencial del código,
no que se hayan borrado copias o cambiado permisos.

Los eventos 7045, 4688 o Sysmon 1 serían fuentes a consultar en un análisis
dinámico con la auditoría correspondiente. No se generaron ni adquirieron
esos eventos aquí. Un timestamp PE es modificable: no demuestra la fecha
de compilación original ni la fecha de infección.

## Lectura y límites técnicos

Se importaron y autoanalizaron siete programas: los tres originales,
W_101_contenido.exe, u.wnry, taskdl.exe y taskse.exe. Las respuestas MCP,
decompilaciones, desensamblados y manifiestos están en `local/ghidra/`,
excluido de Git. Consultar [ghidra-mcp.md](ghidra-mcp.md) para continuar.

El pseudocódigo es una reconstrucción. El primer resultado de WinINet
mostró firmas incompletas y variables de pila confusas; se cotejó con el
ensamblado y se aplicaron prototipos explícitos a sus tres APIs externas.
La versión revisada muestra los cinco parámetros de InternetOpenA y la URL
local en InternetOpenUrlA. No tratar parámetros inferidos automáticamente como código
fuente original. Los avisos de datos solapados y cadenas no definidas
permanecen en el log del analizador.

Quedan pendientes la reconstrucción completa de la capa criptográfica
t.wnry, la interpretación detallada de ambos auxiliares y la revisión de
todos los caminos. **Autoanálisis terminado no significa ingeniería inversa
exhaustiva.** Tampoco atribuye ec1383… a Dionaea, DoublePulsar o una fecha
de adquisición: falta procedencia independiente para esas afirmaciones.
