# P1 — 24d004…: decisión, servicio y recurso R/1831

**Alcance inicial:** 6 funciones transcritas de 176 reconocidas por Ghidra.
Consulta [qué falta y cómo ampliar P1](../ALCANCE-Y-AMPLIACION.md#p1);
la selección no equivale al análisis completo del componente.

[Equipo](../README.md) · [Código de tus seis funciones](codigo.md) · [Cómo estudiar](../COMO-ESTUDIAR.md)

Tu pregunta central: **¿qué condiciones y operaciones conectan este componente
con ed01, y qué parte de esa explicación puede relacionarse con el caso NHS?**
Coordinarás la síntesis histórica y el informe. P2 revisará tu trabajo.

## Qué estudiar y en qué orden

| Paso | Función / dirección | Busca en el código | Qué debes poder explicar |
|---|---|---|---|
| 1 | [00408140](codigo.md#f-00408140) | InternetOpenUrlA, `handle == NULL` | Qué resultado lleva a la rutina siguiente y qué rama la evita |
| 2 | [00408090](codigo.md#f-00408090) | Cantidad de argumentos, dispatcher | Por qué existen caminos diferentes |
| 3 | [00407f20](codigo.md#f-00407f20) | Dos llamadas consecutivas | Orden previsto y falta de control de retorno entre ellas |
| 4 | [00407c40](codigo.md#f-00407c40) | OpenSCManagerA, CreateServiceA, StartServiceA | Solicitud de servicio frente a servicio realmente instalado |
| 5 | [00407ce0](codigo.md#f-00407ce0) | FindResourceA, 0x727, tamaño y escritura | Relación de contención R/1831 → ed01 |
| 6 | [00407480](codigo.md#f-00407480) | 0x1bd y funciones por ordinal | Puerto 445 frente a explotación de SMB demostrada |

Usa Ghidra, las transcripciones y un lector PDF. No necesitas Wireshark ni una
captura de RAM para completar esta lectura. Para repetir la comparación de
bytes necesitas las muestras y el manifiesto de extracción de la estación local.

## Contraste con Listing

Estos son extractos didácticos del [recorrido comprobado](../../docs/recorrido-ghidra-explicado.md)
y la [guía de capas](../../docs/guia-capas-decompilado-desensamblado.md), no una ejecución:

```text
0040819a MOV EDI,EAX       ; resultado de InternetOpenUrlA
004081a3 TEST EDI,EDI      ; compara implícitamente con cero
004081a5 JNZ 004081bc      ; no cero: evita la llamada siguiente
...
004081ad CALL 00408090     ; camino del resultado cero

00407d69 PUSH 0x43137c     ; referencia al tipo "R"
00407d6e PUSH 0x727        ; identificador 1831
00407d73 PUSH EBX          ; módulo cero en este camino
00407d74 CALL [0040a05c]   ; FindResourceA
```

Completa una tabla para `handle == NULL` y `handle != NULL`, sin contactar el
dominio. Microsoft distingue handle válido y NULL en
[InternetOpenUrlA](https://learn.microsoft.com/en-us/windows/win32/api/wininet/nf-wininet-internetopenurla).
No sustituyas esa condición por «HTTP 200» ni por «hay Internet».

En R/1831 contrasta también los argumentos de escritura en `00407e54–00407e61`.
El pseudocódigo tiene tipos/argumentos imperfectos; no se interpreta `uVar12`
como puntero confirmado únicamente por su posición en la decompilación.

## Historia y NIST

Lee [caso NHS](../../docs/caso-nhs.md), el [PDF NAO](../../fuentes/NAO-WannaCry-NHS.pdf)
y el [informe NHS](../../fuentes/NHS-lessons-learned-2018.pdf). Copia la edición,
página y denominador de cualquier cifra; diferencia infectados e interrumpidos.
El código local no demuestra el punto de entrada de un hospital concreto.

En la [matriz](../../docs/matriz-nist.csv), trabaja N-01 (GV.OV-01), N-09
(DE.CM-09), N-11 (RS.AN-03) y N-14 (RS.AN-08). Son preguntas de supervisión,
detección, análisis e impacto, no propiedades que «implementa» el malware.

## Entrega y revisión

- Dos fichas: decisión del handle y relación R/1831 → ed01, con C y Listing.
- Un diagrama A → B y una ficha del servicio con evidencia de ejecución faltante.
- Una página de historia con fuentes y límites, para integrar el informe común.
- P2 coteja la rama en Listing y, si tiene acceso al laboratorio, la igualdad
  del recurso y ed01. Si solo revisa el texto, debe decirlo expresamente.

Preguntas de defensa: ¿por qué ambos caminos pueden retornar 0? ¿Crear el servicio
implica que arrancó? ¿Un puerto 445 prueba EternalBlue? ¿Un hash identifica al
hospital de procedencia? Cierra cada respuesta señalando qué observación la sustenta.
