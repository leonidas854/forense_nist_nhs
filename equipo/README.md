# Material de trabajo para los cuatro participantes

Este es el punto de entrada del equipo. Puedes leer **el pseudocódigo de las
16 funciones seleccionadas** directamente en GitHub, sin descargar muestras ni
instalar Windows. Cada carpeta reúne el código, las direcciones, las preguntas,
las fuentes y los entregables de una persona.

**No son todas las funciones:** Ghidra reconoce 1.755 en estos cuatro componentes.
Lee [alcance, otras rutinas y ampliación del análisis](ALCANCE-Y-AMPLIACION.md)
para conocer la selección inicial, las limitaciones y el siguiente trabajo de P1–P4.

| Participante | Componente y tarea | Guía individual | Código para leer | Revisor |
|---|---|---|---|---|
| P1 | 24d004…: condición de salida, servicio y recurso R/1831 | [Empezar P1](p1-24d004/README.md) | [6 funciones](p1-24d004/codigo.md) | P2 |
| P2 | ed01…: paquete XIA/2058 y frontera de t.wnry | [Empezar P2](p2-ed01/README.md) | [4 funciones](p2-ed01/codigo.md) | P3 |
| P3 | u.wnry: referencias y auxiliares relacionados con recuperación | [Empezar P3](p3-u-wnry/README.md) | [3 funciones](p3-u-wnry/codigo.md) | P4 |
| P4 | ec1383…: W/101, PlayGame y preparación del laboratorio | [Empezar P4](p4-ec1383/README.md) | [3 funciones](p4-ec1383/codigo.md) | P1 |

P1–P4 son puestos; los nombres todavía no se han asignado. El [plan de trabajo](../docs/plan-trabajo-equipo-4.md)
define las diez sesiones propuestas. Nadie queda encargado únicamente de instalar programas.

## Cómo verlo todo

Empieza por [diagramas y análisis general](DIAGRAMAS-Y-ANALISIS.md): mapa de
contenido, contexto NHS, método forense y flujos de P1–P4 con condiciones y límites.

1. Lee [cómo estudiar y usar las herramientas](COMO-ESTUDIAR.md).
2. Abre tu guía individual y después su `codigo.md`. En GitHub usa la vista
   **Preview**; en VS Code abre la vista previa de Markdown con `Ctrl+Shift+V`.
3. Recorre las funciones en el orden indicado. Los enlaces llevan al bloque
   concreto, con notas antes y después del pseudocódigo.
4. Completa una copia local de la [ficha de análisis](FICHA-ANALISIS.md).
5. Contrasta al menos una afirmación con el revisor. Distingue revisar una
   transcripción de repetir la comprobación sobre el binario en Ghidra.

Los cuatro deben poder explicar este mapa de **contención**, que por sí mismo
no acredita el orden de infección de un hospital:

```text
P1: 24d004…
    └─ R/1831 = P2: ed01…
                    └─ XIA/2058 = ZIP
                                  ├─ P3: u.wnry
                                  ├─ t.wnry (análisis parcial de P2)
                                  └─ otros auxiliares

P4: ec1383…
    └─ W/101 = longitud + PE interno 93db4b26… + datos posteriores
       Este PE tiene un hash diferente de 24d004…
```

## Qué código se publica

`codigo.md` contiene una **edición didáctica de pseudocódigo seleccionado**, con
los cuerpos transcritos desde la exportación MCP del 15/11/2026 y explicaciones
separadas. No es el código fuente original, no es el programa completo y no se
preparó para compilar. Conserva tipos imperfectos y nombres añadidos por el analista.
Los comentarios españoles que ya aparecen dentro del código son anotaciones del
proyecto Ghidra. Se normalizan únicamente espacios finales y líneas vacías exteriores.

[indice.json](indice.json) identifica cada componente por SHA-256 y cada función
por dirección; registra también hashes del texto de origen y de su transcripción.
No es un manifiesto de adquisición ni acredita procedencia histórica. Las respuestas
MCP originales, los proyectos Ghidra, las muestras y las evidencias permanecen
fuera de Git conforme al [AGENTS.md](../AGENTS.md). El repositorio publica material
de estudio y explicaciones, como el informe, no el expediente original de evidencia.

Comprueba la integridad del material publicado desde la raíz del repositorio:

```bash
python3 scripts/verificar_material_equipo.py
```

Funciona en un clon sin muestras, Ghidra ni paquetes externos. Comprueba archivos
y hashes del material; no certifica sus conclusiones ni cumplimiento NIST.

## Lecturas compartidas

- [Glosario, incluido W/101](../docs/plan-trabajo-equipo-4.md#3-glosario-que-los-cuatro-deben-dominar-antes-de-dividirse).
- [Capas, decompilado y desensamblado](../docs/guia-capas-decompilado-desensamblado.md).
- [Informe y límites del caso](../docs/informe-forense.md).
- [Procedimiento forense y comprobación NIST](../docs/guia-comprobacion-nist.md).
- [Matriz de resultados NIST](../docs/matriz-nist.csv) y [fuentes públicas](../fuentes/README.md).
- [Herramientas y estado real de la VM](../docs/materiales-preparados.md).

Windows sigue sin instalarse. La lectura del repositorio y la revisión estática
en el anfitrión ya pueden desarrollarse; las prácticas dentro de Windows están pendientes.
