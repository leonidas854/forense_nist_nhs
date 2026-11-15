# Cómo estudiar el material y usar las herramientas

[Volver al reparto](README.md).

## 1. Empezar desde GitHub o un clon

En GitHub abre `equipo/README.md`, elige P1–P4 y sigue sus enlaces. No necesitas
ejecutar ningún archivo para leer el código. `codigo.md` se muestra con resaltado
de C y con explicaciones en español.

Para trabajar en tu equipo, con acceso al repositorio privado y Git instalado:

```bash
git clone https://github.com/leonidas854/forense_nist_nhs.git
cd forense_nist_nhs
python3 scripts/verificar_material_equipo.py
```

El verificador requiere Python 3.10 o posterior. En Windows con Python instalado
puedes usar `py -3` en lugar de `python3`.
Si ya tienes un clon, revisa `git status` y actualiza con `git pull --ff-only`
cuando no tengas cambios locales que lo impidan. No borres trabajo para actualizar.

Abre la carpeta en VS Code: Archivo → Abrir carpeta. Abre `equipo/README.md`
y utiliza la vista previa de Markdown; el PDF de cada fuente también puede abrirse
con un lector de PDF. No hacen falta extensiones, servidor web ni una VM para esta etapa.

## 2. Qué necesita cada persona

| Herramienta o material | Quién lo usa | Para qué | Necesario ahora |
|---|---|---|---|
| GitHub o editor Markdown y lector PDF | Todos | Leer código, documentar argumentos y cotejar fuentes | Sí |
| Python 3.10 o posterior | Todos, si verifican el clon | Comprobar hashes del paquete | Para esa comprobación |
| Ghidra + Java compatibles | Todos durante la revisión de binarios | Comparar Listing, Decompiler, recursos y referencias | Solo para repetir el análisis del binario |
| Ghidra MCP preparado en el anfitrión | Coordinación de la revisión | Consultas/exportaciones sobre el proyecto local | Opcional para lectura individual |
| Vagrant y VirtualBox | P4, con apoyo del equipo | Preparar y comprobar la estación Windows | La VM actual está preparada y apagada |
| Sysinternals | P3/P4 en una práctica futura | Examinar actividad benigna del invitado | Pendiente de Windows |
| FLOSS | Apoyo a la revisión estática | Revisar cadenas cuando sea pertinente | No es requisito para leer las 16 funciones |
| Wireshark | Si se incorpora un PCAP autorizado | Analizar tráfico ya capturado | No hay PCAP de este laboratorio |
| WinPmem / Volatility 3 | Solo si se amplía a RAM | Adquirir/analizar memoria con procedimiento documentado | Fuera del trabajo estático actual |

Los paquetes Windows fijados se obtienen con `bash scripts/download.sh` desde
Linux y se comprueban con `sha256sum -c config/SHA256SUMS`. No modificar el lock
para hacer pasar un archivo diferente. Un clon incluye los PDFs y los scripts,
pero **no** las descargas grandes, las muestras ni el proyecto local Ghidra.
Para Windows, P4 prepara el DVD siguiendo [materiales preparados](../docs/materiales-preparados.md).
La configuración de Java del Ghidra DEV del anfitrión y la del paquete PUBLIC
para Windows están documentadas por separado en [Ghidra MCP](../docs/ghidra-mcp.md).

## 3. Leer una función sin perderse

Antes de empezar, consulta [alcance y ampliación](ALCANCE-Y-AMPLIACION.md):
explica por qué hay 16 transcripciones, qué otras funciones reconoce Ghidra
y cómo priorizar el inventario, la clasificación y el análisis profundo.

1. Anota componente, SHA-256 y dirección de entrada. `00401a90` sin identificar
   el programa no basta: distintas muestras pueden tener esa misma dirección.
2. Lee la pregunta de la función. Identifica entradas (`param_*`), variables
   locales (`local_*`) y datos globales (`DAT_*`, `s_*`).
3. Marca las llamadas a APIs, después los `if`, los saltos y los retornos.
4. Distingue el retorno de una API del retorno de la función que la contiene.
   Ejemplo: una rutina puede devolver 1 sin comprobar el resultado de `WriteFile`.
5. Sigue una sola ruta y después la alternativa. Escribe qué condición cambia.
6. Contrasta con el fragmento de Listing y con la documentación enlazada.
7. Registra qué se observa, qué se interpreta y qué requiere otra evidencia.

`undefined4` significa que Ghidra conserva un valor de cuatro bytes con tipo
imperfecto; no significa que el programa use una biblioteca llamada undefined4.
`FUN_*` es un nombre automático. Los nombres españoles son etiquetas analíticas.
`&variable` indica su dirección; `*puntero` lee el valor apuntado. En un `DWORD *`,
`puntero + 1` avanza cuatro bytes. `0x65` es 101 decimal; W/101 es tipo e ID de
un recurso, no una carpeta ni un puerto. Para términos restantes, usa el glosario.

Las declaraciones del Decompiler pueden ser incompletas: una llamada que parece
tener argumentos ausentes se contrasta en Listing; no se corrige inventándolos.
El código de lectura conserva estas limitaciones y no se compila ni se ejecuta.

## 4. Repetir la lectura en Ghidra

Esta parte requiere el **proyecto local y los binarios autorizados**, que Git no
distribuye. El clon por sí solo no permite volver a generar el desensamblado.
Si no tienes esos materiales, registra «revisión documental» y coordina una
sesión en la estación preparada; no presentes la lectura de Markdown como una
repetición del análisis del binario.

En el anfitrión ya preparado:

1. Usa el Ghidra abierto. Si está cerrado, inicia `./scripts/ghidra-mcp.sh`.
   No abras dos instancias sobre el mismo proyecto.
2. Abre el programa de tu carpeta **dentro del proyecto Ghidra**, contrastando
   nombre y SHA-256 con `equipo/indice.json`.
3. Activa Window → Decompiler y la vista Listing. En Listing pulsa **G** e
   introduce la dirección de la tabla de tu participante.
4. Lee el pseudocódigo a la derecha y las instrucciones de ese programa a la
   izquierda. Sigue referencias con References → Show References To.
5. Documenta una condición y los argumentos decisivos de una llamada. Si el
   Decompiler falla, registra el fallo y usa Listing; no inventes su salida.
6. Guarda las notas/capturas originales en `local/equipo/Pn/`, con fecha,
   versión y responsable. Los cambios de nombre deben explicarse por separado.

Para una nueva exportación seleccionada, con MCP abierto:

```bash
local/ghidra/herramientas/pyghidra-mcp/.venv/bin/python scripts/exportar-decompilados.py
```

Ese comando conserva resultados fechados en `local/exportaciones-ghidra/`;
no reemplaza automáticamente la edición didáctica publicada.

## 5. Documentar y entregar

Copia `equipo/FICHA-ANALISIS.md` a `local/equipo/Pn/` y completa una ficha por
afirmación relevante. Las [plantillas CSV](../plantillas/README.md) se reservan
para registros reales de actuaciones y evidencias; no se rellenan con sucesos
imaginados. El original y las capturas permanecen locales según `AGENTS.md`.

La entrega académica para integrar al repositorio es una síntesis en Markdown:
pregunta, fragmento comentado, interpretación, fuente y limitación. Antes de
publicarla, el revisor comprueba que no incluya muestras, claves, registros
originales ni capturas de evidencia. No atribuyas observaciones locales a un
hospital: separa **H** (historia), **L** (observación local), **I** (inferencia),
**S** (simulación) y **P** (pendiente).

En la matriz NIST identifica una pregunta de control y su criterio de comprobación.
Encontrar una API no demuestra que se cumpla una subcategoría. SP 800-86 orienta
el procedimiento forense; CSF 2.0 se aplica retrospectivamente al caso de 2017.

## 6. Verificar según el material disponible

| Comprobación | Dónde | Qué acredita |
|---|---|---|
| `python3 scripts/verificar_material_equipo.py` | Cualquier clon con Python 3 | Integridad de la edición didáctica publicada |
| `python3 scripts/verificar_caso_nist.py` | Estación con evidencias y pdftotext | Integridad local y referencias de matriz; un clon incompleto dará PARCIAL |
| `python3 scripts/check_isolation.py` | Anfitrión del laboratorio | Configuración real de la VM del proyecto |

No declares fallido tu trabajo de lectura porque tu clon no contiene evidencias
locales; tampoco declares verificado el laboratorio por pasar el control de Markdown.
