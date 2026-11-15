# Guía de comprobación para la tarea de forense

El objetivo es responder **qué ocurrió, cómo lo sabemos y qué no podemos
concluir**. Lee primero el [informe corregido](informe-forense.md). Esta práctica
usa SP 800-86 para el método y CSF 2.0 para relacionar resultados de riesgo.
No exige ejecutar ransomware para demostrar lo que ya se observa estáticamente.

## 1. Fijar el alcance y las reglas

Escribe en la carátula: «Estudio documental del NHS de Inglaterra y análisis
estático de muestras locales, con mapeo retrospectivo a NIST CSF 2.0».
Identifica a los ocho integrantes, fecha de trabajo y responsable de cada paso.
Usa H para historia, L para observación local, I para inferencia y P para pendiente.
No feches un evento como medianoche UTC si solo se conoce el día.

**Criterio de aceptación:** cada conclusión del informe tiene clase, fuente,
localizador y límite. NIST SP 800-86 §3; CSF RS.AN-03.

## 2. Preservar y comprobar los materiales — recolección

Desde la raíz del repositorio:

```bash
python3 scripts/verificar_caso_nist.py
```

Guarda el JSON que genera bajo `local/revision-nist/`. El comando recalcula hashes
de PDF, muestras y derivados, coteja los códigos de la matriz con el PDF de CSF
2.0 y revisa la exclusión de evidencias de Git. Necesita `pdftotext`.
Salida 0: esas comprobaciones técnicas pasaron; 1: error; 2: material faltante.
**Ninguna salida certifica cumplimiento NIST ni prueba procedencia del malware.**

Copia las plantillas a una carpeta dentro de `local/` para registrar trabajo real.
Anota origen acreditable, quién recibió, cuándo, qué operaciones se hicieron y
qué resultados quedaron. Si no se conoce la adquisición original, escribe
«desconocida» y registra separadamente la hora de la comprobación actual.
No inventes responsables ni traspasos para completar filas.

**Criterio:** hashes/tamaños coinciden y las lagunas de procedencia son explícitas.
SP 800-86 §§3.1 y 4.2.2; RS.AN-06 para actuaciones y RS.AN-07 para datos.

## 3. Comprobar qué pasó en el NHS — examen documental

Abre los PDF conservados y anota estos localizadores (página PDF contada desde 1):

| Pregunta | Qué revisar | Respuesta admisible |
|---|---|---|
| ¿Todos los afectados estaban infectados? | NAO PDF p.8, resumen 5 | No: 34 infectados y 46 con interrupciones, total 80 |
| ¿Por qué unas fuentes dicen 81? | NHS PDF p.5, nota 3 | Edición y reclasificación; indicar qué edición se usa |
| ¿Fue phishing? | NHS PDF p.10, §2.3; NAO PDF p.12, resumen 12 | Entrada probable por SMB; NAO no registra propagación por NHSmail |
| ¿Fue solo Windows XP? | NAO §2.5 y resumen 12 | Mayoría de dispositivos infectados identificados con Windows 7 sin parchear |
| ¿Se verificaron los avisos? | NAO PDF p.21, §2.10 | No había mecanismo formal previo para comprobar su aplicación |
| ¿Cuántas citas? | NAO PDF p.10, resumen 6 | 6.912 identificadas; más de 19.000 estimadas |
| ¿Cómo se recuperó? | NHS PDF p.12, §2.14 | Reinstalación/parcheo de prácticas infectadas; respetar ese alcance |

**Criterio:** otra persona encuentra el mismo pasaje y tu frase conserva sus
matices. No sustituir «probable» por «demostrado». No atribuir a Ghidra los números
históricos. SP 800-86 §§3.2–3.3; RS.AN-03 y RS.AN-08.

## 4. Examinar el código en Ghidra

El proyecto preparado está en `local/ghidra/proyectos/WannaCry_NHS.gpr`.
Si la instancia anterior sigue abierta, úsala. Si está cerrada:

```bash
./scripts/ghidra-mcp.sh
```

Lista el estado con el cliente MCP local:

```bash
PYTHON=local/ghidra/herramientas/pyghidra-mcp/.venv/bin/python
"$PYTHON" scripts/ghidra_mcp_consulta.py list_project_binaries \
  --output local/revision-nist/programas-comprobados.json
```

**Prueba A — kill switch.** En 24d004… usa G → `00408140`. Compara Listing y
Decompiler. Localiza `InternetOpenUrlA`, el resultado cero y la llamada a
`Preparar_Servicio_Y_Carga`. Revisa el acceso directo 1 de InternetOpenA.

```bash
"$PYTHON" scripts/ghidra_mcp_consulta.py decompile_function \
  '{"binary_name":"/24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c.exe-e88954","name_or_address":"00408140"}' \
  --output local/revision-nist/prueba-A-killswitch.json
```

**Aceptación:** código y ensamblado sustentan la misma bifurcación. Describe el
resultado como estático; no abras el dominio ni concluyas por él que hubo HTTP 200.

**Prueba B — capas.** En 24d004… ve a `00407ce0`; localiza recurso R e ID
`0x727`. Comprueba en `local/ghidra/extraidos/manifiesto.json` su hash ed01….
En ed01… ve a `00401dab` para XIA e ID `0x80a`. Para repetir la extracción:

```bash
"$PYTHON" scripts/extraer_recursos_wannacry.py
python3 scripts/verificar_caso_nist.py
```

**Aceptación:** bytes y tamaño del recurso coinciden; no se identifica el
componente solo por el nombre. No usar una búsqueda indiscriminada de `MZ`.

**Prueba C — DLL contenedora.** En ec1383… ve a `180001014`. El primer DWORD
del recurso W/101 determina el tamaño; `WriteFile` recibe recurso+4.
**Aceptación:** la decompilación coincide con los límites de extracción. No afirmar
que aquí se descifra el recurso ni que es una captura de un equipo del NHS.

**Prueba D — servicio y sabotaje.** Revisa 24d004… `00407c40`; después u.wnry
`004066fe` y la cadena desde `00420fd8`. Guarda referencias y ensamblado.
**Aceptación:** identifica las llamadas/referencias, pero deja como pendiente la
creación efectiva del servicio y el borrado de copias. t.wnry sigue sin análisis
criptográfico completo.

SP 800-86 §3.2; interpretación en §3.3 y CSF RS.AN-03. Las direcciones son
virtuales dentro de cada programa. Las anotaciones españolas son del analista.

## 5. Correlacionar con artefactos — análisis

Completa esta tabla sin rellenar lo que falta con resultados supuestos:

| Hipótesis | Evidencia necesaria de un mismo host | Estado actual |
|---|---|---|
| Se instaló mssecsvc2.0 | System.evtx/registro Services, ruta del binario y hash | Pendiente |
| Se ejecutó un proceso de sabotaje | Auditoría de procesos disponible, línea de comando, padre y tiempo | Pendiente |
| Hubo comunicación SMB | PCAP o registros de red con origen, destino y tiempos | Pendiente |
| Se cifraron archivos | Archivos originales/afectados y metadatos comparables | Pendiente |
| Se recuperó el servicio | Respaldo verificado y prueba funcional posterior | Pendiente |

Una práctica benigna puede validar recolección y correlación en un Windows
instalado, con datos ficticios y claramente rotulada como ejercicio. No demuestra
comportamiento de WannaCry. La VM está creada, apagada y aislada, pero Windows
no está instalado. No se habilitarán redes ni comparticiones para completar esta tabla. No hay autorización
implícita para detonar malware al seguir esta guía.

## 6. Aplicar las seis funciones de CSF 2.0

Abre [matriz-nist.csv](matriz-nist.csv). Por cada fila responde:

1. ¿Cuál es el resultado de la subcategoría en el Core, en tus palabras?
2. ¿Qué fuente histórica o hallazgo local lo hace relevante?
3. ¿Qué comprobación permitiría evaluar el resultado?
4. ¿Qué material falta y qué conclusión no se puede sostener?

Ejemplo: **PR.PS-02** trata mantenimiento de software. La NAO documenta equipos
sin parchear. Ver un gusano en Ghidra no comprueba la configuración de Windows:
se necesitaría inventario y prueba del estado de actualizaciones del equipo.

Ejemplo: **RS.AN-07** se apoya en nuestros hashes y relaciones padre/hijo, pero
queda parcial porque no está acreditada la procedencia previa. El resultado no
se convierte en «cumple» solo porque el hash sea correcto.

Ejemplo: **RC.RP-03** necesita comprobar respaldos antes de restaurar; **RC.RP-05**
necesita verificar los activos y su operación después. No usar el mismo hash de
malware como prueba de ambos resultados.

## 7. Presentar el informe y defenderlo

Expositor 1: pregunta, alcance, H-01 a H-09 y funciones GV/ID/PR. Expositor 2:
pruebas A–D, diferencia entre código y ejecución, DE/RS/RC y pendientes.
Los demás integrantes revisan fuentes, integridad, artefactos ausentes y límites.

Una respuesta defendible: «La fuente oficial considera probable la entrada por
SMB; nosotros comprobamos estáticamente mecanismos compatibles. No tenemos los
logs del primer equipo, por lo que no afirmamos una reconstrucción completa».

Antes de entregar, revisar nombres, fecha, rúbrica del docente, enlaces y matriz.
Los guiones, diapositivas y dashboard antiguos no deben usarse como fuente técnica
hasta reconciliarlos con este informe. Las pruebas automáticas no sustituyen la
revisión por otro integrante. SP 800-86 §3.4; RS.AN-06 y RS.AN-07.
