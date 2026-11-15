# P2 — ed01…: paquete XIA/2058 y frontera de t.wnry

**Alcance inicial:** 4 funciones transcritas de 244 reconocidas por Ghidra.
Consulta [qué falta y cómo ampliar P2](../ALCANCE-Y-AMPLIACION.md#p2);
la selección no equivale al análisis completo del componente.

[Equipo](../README.md) · [Código de tus cuatro funciones](codigo.md) · [Cómo estudiar](../COMO-ESTUDIAR.md)

Tu pregunta central: **¿qué contiene este componente, cómo prepara sus datos y
hasta dónde llega lo que podemos afirmar sobre la carga siguiente?**
Coordinarás inventario e integridad. P3 revisará tu trabajo.

## Qué estudiar y en qué orden

| Paso | Función / dirección | Busca | Qué debes explicar |
|---|---|---|---|
| 1 | [00401dab](codigo.md#f-00401dab) | 0x80a, FindResourceA, bucle | XIA/2058 como paquete ZIP y tratamiento particular de c.wnry |
| 2 | [00401fe7](codigo.md#f-00401fe7) | Directorio, extracción, llamadas y condiciones | Preparación y secuencia de decisiones |
| 3 | [00401064](codigo.md#f-00401064) | CreateProcessA y espera condicionada | Creación de proceso, espera y resultado son hechos diferentes |
| 4 | [004014a6](codigo.md#f-004014a6) | WANACRY!, 0x100, lecturas, memoria | Cabecera y procesamiento de t.wnry; límites de la interpretación |

Usa transcripciones, Ghidra y los [manifiestos y fuentes](../../docs/materiales-preparados.md).
Para repetir extracción/hashes hace falta el material local autorizado. Leer
el ZIP como datos no requiere ejecutar los archivos que contiene.

## Contraste con Listing y datos

Extractos de la [guía de capas](../../docs/guia-capas-decompilado-desensamblado.md):

```text
00401db6 PUSH 0x40f43c      ; referencia al tipo "XIA"
00401dbb PUSH 0x80a         ; ID 2058
00401dc0 PUSH [EBP+0x8]     ; módulo
00401dc3 CALL [00408100]    ; FindResourceA
00401dcb TEST ESI,ESI
00401dcd JZ 00401e07       ; camino de fallo

00402125 PUSH 0x40f4f4     ; referencia a t.wnry
0040212d CALL 004014a6     ; lectura/procesamiento
...
00402154 JZ 0040215a       ; evita llamada si destino es cero
00402158 CALL EAX          ; llamada indirecta, no cuerpo del cifrador
```

En `t.wnry`, la cabecera observada empieza por `WANACRY!` y después el campo
little-endian `00 01 00 00`, equivalente a 256. `0x100` y 256 son el mismo
número. No demuestran por sí solos un algoritmo criptográfico. No confundir
un contenedor con una DLL en claro, ni la contraseña interna de ZIP con una
clave para recuperar documentos.

El prototipo de `004014a6` y su llamada muestran imperfecciones de recuperación
de tipos/convenio. Conserva el texto y contrasta argumentos en Listing: no lo
«repares» para compilarlo. Explica por qué `memcmp == 0` significa igualdad,
mientras una API que devuelve NULL puede indicar fallo.

La documentación de [FindResourceA](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-findresourcea)
distingue tipo e identificador. El acceso a los datos y su interpretación como
ZIP requieren pasos y comprobaciones adicionales.

## Historia y NIST

Usa la sección de método del [informe](../../docs/informe-forense.md) y
[SP 800-86](../../fuentes/NIST.SP.800-86.pdf), §3.1, para justificar preservación
y examen. En la [matriz](../../docs/matriz-nist.csv) trabaja N-12 (RS.AN-06)
y N-13 (RS.AN-07): registro, integridad y procedencia. Un hash coincidente no
reconstruye cuándo, de quién o de qué hospital se obtuvo el archivo.

## Entrega y revisión

- Árbol A → B → ZIP → miembros, separando formato y función supuesta.
- Dos fichas: extracción del paquete y lectura de la cabecera de t.wnry.
- Tabla «comprobado / inferido / pendiente» para la llamada indirecta final.
- P3 revisa una condición de salida y la interpretación de la cabecera;
  identifica si repitió el cotejo de bytes o solo revisó su documentación.

Preguntas: ¿por qué no basta buscar MZ? ¿Cada entrada del ZIP sigue el mismo
camino? ¿Se espera a que termine cada orden? ¿CALL EAX revela el algoritmo de
cifrado? La criptografía completa de t.wnry permanece fuera de lo comprobado.
