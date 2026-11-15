# P4 — ec1383…: W/101, PlayGame y laboratorio

**Lectura visual:** [diagramas de flujo de este componente](diagramas.md).

**Alcance inicial:** 3 funciones transcritas de 265 reconocidas por Ghidra.
Consulta [qué falta y cómo ampliar P4](../ALCANCE-Y-AMPLIACION.md#p4);
la selección no equivale al análisis completo del componente.

[Equipo](../README.md) · [Código de tus tres funciones](codigo.md) · [Cómo estudiar](../COMO-ESTUDIAR.md)

Tu pregunta central: **¿cómo deposita y solicita lanzar una carga este componente,
y qué relación está realmente comprobada con los demás?**
Coordinarás preparación y comprobaciones de la VM con apoyo del equipo. P1 revisará tu trabajo.

## Qué estudiar y en qué orden

| Paso | Función / dirección | Busca | Qué debes explicar |
|---|---|---|---|
| 1 | [PlayGame, 1800011a4](codigo.md#f-1800011a4) | sprintf y dos llamadas | Ruta formada y orden previsto sin comprobar el retorno intermedio |
| 2 | [180001014](codigo.md#f-180001014) | FindResourceA, DWORD*, WriteFile | Tipo W, ID 101, longitud y datos desde recurso+4 |
| 3 | [1800010f8](codigo.md#f-1800010f8) | CreateProcessA y cierre de handles | Solicitud de proceso frente a impacto confirmado |

El archivo es una DLL x64 aunque termine en `.exe`. `PlayGame` es una exportación;
su existencia no demuestra que se haya llamado. No se usa un ejecutor de DLL
para realizar esta práctica. Herramientas: Ghidra, editor y lector PDF; para la
tarea transversal, los comandos de preparación indicados más abajo.

## W/101, explicado con los datos

W es el **tipo del recurso** y 101 su **identificador** (`0x65`). La barra es
notación de análisis. No es una carpeta, un puerto ni el nombre de una función.

```text
Recurso W/101
  +0: DWORD (4 bytes), longitud del contenido que se pretende escribir
  +4: comienzo del PE interno
      ... longitud declarada de bytes ...
      bytes posteriores del recurso, fuera de ese tramo
```

En el pseudocódigo `pDVar2` es `DWORD *`: `*pDVar2` lee la longitud y `pDVar2 + 1`
avanza cuatro bytes. La [guía de capas](../../docs/guia-capas-decompilado-desensamblado.md)
contrasta ese cálculo con Listing:

```text
18000102a LEA R8,[1800092b0]   ; tipo "W", tercer argumento
180001031 MOV EDX,0x65        ; ID 101, segundo argumento
180001036 CALL [180009030]    ; FindResourceA
...
18000108b MOV ESI,[RDI]       ; longitud declarada
1800010c4 LEA RDX,[RDI+4]     ; dirección inicial de datos
1800010cd MOV R8D,ESI         ; longitud para WriteFile
1800010d3 CALL [180009008]    ; escritura solicitada
```

Contrasta el significado de los argumentos con
[FindResourceA](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-findresourcea).
En `PlayGame`, revisa `1800011c9 CALL 180001014` y `1800011ce CALL 1800010f8`:
no hay una comprobación del resultado de extracción entre ambas llamadas.
La lectura de [CreateProcessA](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa)
ayuda a interpretar la solicitud posterior, sin equipararla con ejecución terminada.

Busca dos límites adicionales: no se comprueba el resultado de `WriteFile` en
esta rutina y su retorno final puede ser 1 aunque falle la apertura del destino.
El extractor estático del repositorio valida límites para preservar el análisis;
eso no significa que el malware haga esas mismas validaciones.

El PE delimitado tiene SHA-256 **93db4b26…**, diferente de 24d004…. No hay una
arista demostrada ec1383 → 24d004 ni evidencia de que esta DLL concreta se usara
en un hospital. Evita atribuirle procedencia de honeypot por su estructura.

## Laboratorio: lo que corresponde hacer ahora

En el anfitrión preparado, consulta sin arrancar ni instalar Windows:

```bash
./lab status
./lab validate
python3 scripts/check_isolation.py
./scripts/vbox-lab.sh list vms
```

Para ver la GUI del registro del proyecto: `./scripts/vbox-lab.sh --gui`.
El estado documentado es VM apagada, disco vacío y DVD de herramientas conectado;
Windows está pendiente por indicación del usuario. Estas comprobaciones no
acreditan herramientas instaladas en el invitado. Sigue
[materiales preparados](../../docs/materiales-preparados.md) y
[laboratorio](../../docs/laboratorio.md) cuando se retome esa fase.
En otro equipo, no presentes el resultado del anfitrión actual como una comprobación propia.

## NIST, entrega y revisión

Trabaja N-06 (PR.IR-01), N-11 (RS.AN-03) y N-12 (RS.AN-06) de la
[matriz](../../docs/matriz-nist.csv): aislamiento, explicación del mecanismo y registro.

- Diagrama W/101 con longitud, inicio y límites de extracción.
- Dos fichas: argumentos/aritmética de punteros y control de resultados.
- Comparación de identidades: DLL, PE interno y 24d004, con límites de procedencia.
- Registro local del estado real de VM; síntesis académica separada para Git.
- P1 comprueba el avance de cuatro bytes y la ausencia de control entre llamadas.

Preguntas: ¿W significa necesariamente Windows? ¿Un `.exe` puede ser DLL?
¿PlayGame se ejecutó por aparecer exportada? ¿Retornar 1 demuestra escritura?
¿Compartir una ruta de destino demuestra compartir los mismos bytes?
