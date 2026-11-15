> **Pendiente de actualización (15/11/2026):** este material anterior contiene afirmaciones aún no reconciliadas. Para la defensa usar [el informe corregido](informe-forense.md) y [la guía de comprobación NIST](guia-comprobacion-nist.md).

# Guion de Exposición y Defensa Oral (2 Expositores)
## Caso de Estudio: WannaCry en el NHS · Mapeo a NIST CSF 2.0
**Materia:** Informática Forense  
**Equipo:** 8 Estudiantes (2 Expositores Principales + 6 Especialistas de Soporte)  
**Tiempo Estimado:** 24 minutos de ponencia (12 min por expositor) + 6 minutos de preguntas y respuestas del tribunal docente.

---

## Pautas Generales para los Expositores

1. **Postura y Tono Pericial:** Mantener un lenguaje formal, técnico y objetivo. No usar términos coloquiales como "virus malo" o "hackeo"; utilizar "amenaza de tipo criptogusano (ransomware + worm)", "vector de propagación SMBv1", "análisis estático de binarios PE", "artefactos en memoria volátil y registros EVTX".
2. **Defensa de la Cadena de Custodia:** Enfatizar siempre la distinción entre **documentación histórica certificada** (informes oficiales NAO y DHSC 2018), **observaciones de ingeniería inversa estática** (Ghidra 12.2) y **evidencias de laboratorio controlado** (sin afirmar jamás haber infectado la red real del NHS).
3. **Manejo del Tiempo:** El Expositor 1 debe entregar la palabra exactamente en el minuto 12:00. El Expositor 2 debe cerrar las conclusiones en el minuto 24:00.

---

## BLOQUE 1: EXPOSITOR 1 (Minutos 0:00 a 12:00)
### Rol: Perito Coordinador · Contexto Histórico, Gobernanza, Identificación y Protección

---

### Minuto 0:00 - 2:00 | Diapositivas 1 y 2
**[Objetivo: Carátula, presentación formal del equipo de 8 y delimitación pericial]**

> **[EXPOSITOR 1]:**  
> *"Muy buenos días estimado docente y miembros del tribunal evaluador. En representación del equipo pericial conformado por ocho integrantes, daremos inicio a la defensa del trabajo de investigación forense titulado: **'WannaCry en el NHS: laboratorio forense y mapeo retrospectivo al marco NIST Cybersecurity Framework versión 2.0 y su perfil de ransomware NIST IR 8374 Revisión 1'**.*  
>
> *Este proyecto fue estructurado bajo una estricta división de trabajo pericial: mientras mis compañeros han liderado áreas clave como la auditoría de infraestructura, ingeniería inversa de malware, forense de memoria volátil y registros del sistema operativo, hoy dos de nosotros sintetizaremos la investigación, respaldados por la matriz de responsabilidades que figura en el documento oficial.*  
>
> *Nuestro objetivo principal es doble: primero, reconstruir con rigor documental el mayor incidente de ciberseguridad en el sector sanitario mundial —el ataque de WannaCry al National Health Service el 12 de mayo de 2017—; y segundo, correlacionar la causa del código malicioso mediante ingeniería inversa con los efectos dejados en el sistema operativo, auditando el incidente bajo las seis funciones del estándar NIST CSF 2.0 publicado en 2024."*

---

### Minuto 2:00 - 5:00 | Diapositivas 3, 4 y 5
**[Objetivo: El incidente del NHS con cifras oficiales certificadas de la NAO y DHSC 2018]**

> **[EXPOSITOR 1]:**  
> *"Para iniciar el análisis, debemos remitirnos a la verdad histórica comprobada en fuentes primarias. En el peritaje informático no nos basamos en artículos de prensa ni en blogs, sino en los informes oficiales de auditoría gubernamental: el informe de la **National Audit Office (NAO)** de abril de 2018 y la revisión de lecciones aprendidas del **Department of Health and Social Care (DHSC)**.*  
>
> *El 12 de mayo de 2017, el NHS colapsó. La NAO certifica formalmente que **80 de los 236 trusts hospitalarios** de Inglaterra resultaron directamente afectados, junto con 603 centros de atención primaria. Es fundamental aclarar una precisión metodológica: la web de la NAO menciona inicialmente 81 trusts, pero la revisión ministerial formalizó la cifra en 80 al constatar que uno de los centros no sufrió infección interna, sino desconexión preventiva.*  
>
> *El impacto operativo fue devastador para los pacientes: se identificaron **6.912 citas médicas canceladas**, aunque la propia NAO estima que la cifra real superó las **19.000 citas**, obligando a desviar ambulancias de cinco servicios de urgencias y dejando inoperativos equipos biomédicos críticos como resonadores magnéticos y refrigeradores de sangre. El impacto financiero total se cuantificó en **92 millones de libras esterlinas**: 72 millones en sustitución urgente de infraestructura y 20 millones en pérdida de productividad médica.*  
>
> *Desmentimos además un mito común en la literatura no especializada: WannaCry **no ingresó al NHS por un correo de phishing masivo**. Las pericias del NCSC británico confirmaron que el vector inicial fue la exposición directa del puerto TCP 445 en equipos conectados a internet, propagándose luego de forma lateral y descontrolada por la red privada hospitalaria N3."*

---

### Minuto 5:00 - 8:30 | Diapositivas 6, 7 y 8
**[Objetivo: Funciones NIST: Govern (GV) e Identify (ID) · Anatomía del Fallo Hospitalario]**

> **[EXPOSITOR 1]:**  
> *"Al aplicar retrospectivamente el NIST CSF 2.0, el primer gran quiebre se evidencia en la función **GOVERN (Gobernanza)**. La subcategoría **GV.OV-01** exige vigilar que las decisiones de gestión de riesgos se comuniquen y se cumpla su ejecución. ¿Qué ocurrió en el NHS? El centro de ciberseguridad sanitaria, NHS Digital (a través de CareCERT), había emitido alertas críticas en marzo y abril de 2017 advirtiendo que Microsoft había liberado el parche MS17-010 para subsanar la vulnerabilidad de SMBv1. Sin embargo, no existía un mecanismo formal de auditoría nacional para verificar qué hospitales habían instalado el parche. Asimismo, bajo **GV.RR-02**, durante las primeras horas de la crisis nadie en el Ministerio de Salud tenía formalmente la autoridad jurídica y operativa para ordenar la desconexión total de la red nacional sanitaria.*  
>
> *Esto nos lleva directamente a la función **IDENTIFY (Identificación)**, en su subcategoría **ID.AM-01** (inventario de activos). El NHS desconocía cuántos dispositivos ejecutaban sistemas operativos obsoletos o desatendidos. Miles de equipos de diagnóstico clínico —como escáneres de rayos X y analizadores de laboratorio— operaban con versiones embebidas de Windows XP y Windows 7 sin soporte de parches automáticos. Los administradores locales no tenían mapeada la superficie de ataque (**ID.RA-01**), asumiendo erróneamente que por estar dentro de la red privada N3, los dispositivos no requerían actualización ni protección perimetral."*

---

### Minuto 8:30 - 11:30 | Diapositivas 9 y 10
**[Objetivo: Función NIST Protect (PR) · El Vector EternalBlue y la Red N3]**

> **[EXPOSITOR 1]:**  
> *"El colapso de las barreras preventivas se materializa en la función **PROTECT (Protección)**. La subcategoría **PR.PS-02** estipula el mantenimiento y actualización oportuna del software según el perfil de riesgo. El parche crítico de Microsoft **MS17-010** estuvo disponible dos meses antes del ataque, pero en los trusts no se aplicó debido a la falta de ventanas de mantenimiento y temor a desestabilizar el software médico.*  
>
> *Pero el fallo determinante de protección ocurrió en la arquitectura de red: subcategoría **PR.IR-01** (resiliencia de infraestructura y segmentación). La red N3 era una WAN privada que interconectaba a todos los hospitales del Reino Unido. Era una red completamente **plana**, sin filtrado interno ni listas de control de acceso en el puerto **TCP 445 (SMB)**. En consecuencia, en cuanto un solo equipo en un trust fue infectado, la red N3 funcionó como una autopista de propagación automática sin barreras, permitiendo que el módulo de gusano infectara decenas de hospitales a cientos de kilómetros de distancia en cuestión de minutos.*  
>
> *Habiendo demostrado las causas de gobernanza, visibilidad y protección que permitieron el ingreso de la amenaza, cedo la palabra a mi compañero, quien expondrá el análisis forense técnico del artefacto, la ingeniería inversa en Ghidra y la correlación en memoria, logs y disco bajo las funciones de Detección, Respuesta y Recuperación."*

---

### Minuto 11:30 - 12:00 | Transición
> **[EXPOSITOR 1]:**  
> *"Adelante, colega."*

---

## BLOQUE 2: EXPOSITOR 2 (Minutos 12:00 a 24:00)
### Rol: Ingeniero Inverso & Perito Técnico · Laboratorio, Ghidra, Evidencias, Detección, Respuesta y Cierre

---

### Minuto 12:00 - 14:00 | Diapositivas 11 y 12
**[Objetivo: Arquitectura de Laboratorio Forense Aislado]**

> **[EXPOSITOR 2]:**  
> *"Muchas gracias. Continuando con la fundamentación pericial, pasamos a la dimensión técnica y experimental del caso. Todo peritaje de código malicioso exige garantizar dos premisas innegociables: **integridad de las evidencias** y **seguridad de contención**.*  
>
> *Para este trabajo, implementamos una estación forense sobre anfitrión Linux gestionada mediante **Vagrant 2.4.9** y **VirtualBox 7.2**. La máquina virtual, denominada `forense-nhs-win10`, fue configurada bajo una política de aislamiento absoluto: sus **ocho adaptadores de red están físicamente deshabilitados**, el comunicador interno está fijado en modo experimental `none` (sin SSH ni WinRM), y se desactivaron de raíz las carpetas compartidas, portapapeles bidireccional y arrastrar/soltar.  
>
> *Esta rigurosidad se audita automáticamente en nuestro repositorio mediante el script `scripts/check_isolation.py` y una suite de cinco pruebas unitarias en Python, garantizando que ninguna traza maliciosa pueda escapar ni que la estación altere los sistemas circundantes. Las herramientas de análisis —incluyendo Ghidra 12.2, OpenJDK 25, Volatility 3 fijado en el commit `881e970` y la suite Sysinternals— fueron empaquetadas en una imagen ISO de solo lectura montada como unidad óptica virtual."*

---

### Minuto 14:00 - 17:30 | Diapositivas 13, 14 y 15
**[Objetivo: Análisis Estático en Ghidra (RS.AN-03) · Kill Switch, Dropper y Paradoja del Proxy]**

> **[EXPOSITOR 2]:**  
> *"Ingresando al análisis de ingeniería inversa estática bajo la subcategoría **RS.AN-03** (Análisis de Incidente y Causa Raíz), analizamos la muestra canónica original de WanaCrypt0r 2.0 (hash SHA-256 `ed01ebfbc...`, tamaño de 3.51 MB) en Ghidra 12.2.*  
>
> *Al inspeccionar el árbol de símbolos e imports en `WININET.DLL`, localizamos la API `InternetOpenUrlA` referenciada directamente en la función `WinMain`. Aquí reside el célebre **Kill Switch**. El binario intenta conectarse al dominio sin sentido `www.iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com`.  
>
> *La lógica condicional decompilada es de suma relevancia pericial:*  
> - *Si la función `InternetOpenUrlA` tiene éxito y recibe una respuesta HTTP (código 200 OK), el programa llama a `InternetCloseHandle` y finaliza su ejecución de inmediato sin cifrar absolutamente nada.*  
> - *Si la llamada devuelve NULL o falla —que es lo que ocurría antes de que el dominio fuera registrado— el flujo continúa hacia la función maliciosa, invocando a `CreateServiceA` en `ADVAPI32.DLL` para registrar el servicio del gusano denominado `mssecsvc2.0` con la descripción engañosa 'Microsoft Security Center (2.0) Service'.*  
>
> *Aquí aportamos el **hallazgo forense clave para el caso NHS**: El investigador Marcus Hutchins registró el dominio el 12 de mayo, deteniendo el ataque globalmente. Sin embargo, en el Reino Unido varios hospitales se infectaron **después** de ese registro. ¿Por qué? Porque la arquitectura de red hospitalaria obligaba a todo el tráfico web a pasar por **servidores proxy corporativos** con autenticación o listas blancas. Como la API `InternetOpenUrlA` de WannaCry no implementaba autenticación proxy, la consulta HTTP al Kill Switch devolvía un error de conexión (falla). En consecuencia, el malware interpretaba erróneamente que el Kill Switch seguía inactivo y procedía a detonar el cifrado.*  
>
> *Asimismo, al analizar los recursos del ejecutable mediante `FindResourceA` y `LockResource`, descubrimos que el binario principal funciona como un **dropper**: extrae un archivo PE oculto en la sección `.rsrc/R` y lo escribe en `C:\Windows\tasksche.exe`. Al decompilar este segundo ejecutable (el cifrador puro), localizamos en la tabla de cadenas la contraseña embebida `WNcry@2ol7` utilizada para descomprimir su configuración interna (`c.wnry`, `t.wnry`), junto con el comando antiforense `vssadmin delete shadows /all /quiet`."*

---

### Minuto 17:30 - 20:30 | Diapositivas 16, 17 y 18
**[Objetivo: Correlación Forense de Artefactos: Eventos, Memoria y Disco]**

> **[EXPOSITOR 2]:**  
> *"La gran ventaja del enfoque forense es la **correlación causa-efecto**: lo que identificamos en el código decompilado en Ghidra deja una huella digital indeleble en el sistema operativo:*  
>
> 1. *Bajo **DETECT (DE.AE-03 y DE.CM-01)**, la creación del servicio del gusano genera en el registro `System.evtx` el **Evento ID 7045**, registrando el nombre del servicio `mssecsvc2.0` y la ruta a la imagen ejecutable. Asimismo, en `Security.evtx` (Evento ID 4688) y Sysmon (Evento ID 1), se captura la invocación oculta de `cmd.exe /c vssadmin delete shadows /all /quiet`, demostrando la intención deliberada de destruir los puntos de restauración del sistema.*  
> 2. *En **Memoria Volátil (RS.AN)**, utilizando Volatility 3 sobre volcados de RAM adquiridos con WinPmem, el plugin `windows.pslist` y `windows.malfind` permite rastrear el proceso padre e hijo `tasksche.exe`, identificando la inyección en memoria de la biblioteca criptográfica `t.wnry` y la manipulación de claves temporales de la CryptoAPI de Windows.*  
> 3. *En el **Sistema de Archivos (RS.AN-06)**, la tabla `$MFT` de NTFS evidencia la creación masiva de archivos temporales con cabecera `WANACRY!` y la sustitución de extensiones originales de historias clínicas y documentos por `.WNCRY`, junto con la persistencia de las notas de rescate `@Please_Read_Me@.txt`."*

---

### Minuto 20:30 - 24:00 | Diapositivas 19, 20 y 21
**[Objetivo: Función Recover (RC), Lecciones Aprendidas del Informe Smart y Conclusiones]**

> **[EXPOSITOR 2]:**  
> *"Llegamos a la última función del NIST CSF 2.0: **RECOVER (Recuperación)**.  
> La subcategoría **RC.RP-01** exige la ejecución de planes de recuperación basados en copias de respaldo. En el NHS, como el malware ejecutó con éxito el borrado de copias sombra mediante `vssadmin` y `wbadmin`, la recuperación local fue imposible. Los hospitales no pagaron el rescate de 300 dólares en Bitcoin —cumpliendo con la recomendación formal de la función **Govern**—, debiendo aislar físicamente los equipos, formatear unidades desde cero y restaurar desde copias externas offline o frías (**PR.DS-11**).*  
>
> *Las lecciones aprendidas oficiales, consolidadas en el informe del CIO Will Smart (2018), dejaron directrices que hoy están plenamente consagradas en el perfil NIST IR 8374 Rev. 1:*  
> 1. *La necesidad imperiosa de deshabilitar SMBv1 en toda la red corporativa.*  
> 2. *La migración obligatoria de la red plana N3 hacia la nueva red segura **HSCN (Health and Social Care Network)** con segmentación estricta y monitoreo continuo.*  
> 3. *La designación de roles con autoridad expresa para ordenar desconexiones perimetrales de emergencia (subcategoría **GV.RR-02**).*  
>
> *Como conclusión general del equipo pericial: WannaCry no triunfó en el NHS por la sofisticación técnica de su criptografía, sino por la convergencia de fallos sistémicos en las funciones de Gobernanza, Identificación y Protección de NIST CSF 2.0. Un incidente que pudo mitigarse con un parche emitido dos meses antes terminó costando 92 millones de libras y miles de horas médicas.*  
>
> *Con esto damos por concluida nuestra presentación formal y quedamos a disposición del docente y del tribunal para responder a sus preguntas. Muchas gracias."*

---

## BLOQUE 3: RONDA DE PREGUNTAS (Minutos 24:00 a 30:00)
### Protocolo de Distribución de Preguntas para los 8 Integrantes

Durante la sesión de preguntas, los Expositores 1 y 2 reciben la consulta y pueden delegar la profundización técnica al especialista del equipo:

| Tópico de la Pregunta | Especialista que Responde | Documento de Apoyo |
|---|---|---|
| **Gobernanza, Roles y Cadena de Custodia** | Integrante 1 (Coordinador) | `docs/informe-forense.md` (Sección 2) |
| **Infraestructura del NHS y Equipos Médicos** | Integrante 2 (Infraestructura) | `docs/informe-forense.md` (Sección 1) |
| **Protocolo SMBv1, MS17-010 y Red N3** | Integrante 3 (Redes/Protección) | `docs/informe-forense.md` (Sección 4) |
| **Eventos .evtx, Sysmon y Reglas Sigma** | Integrante 4 (Logs/Detección) | `docs/informe-forense.md` (Sección 5) |
| **Decompilación en Ghidra y Kill Switch** | Integrante 5 (Ingeniería Inversa) | `docs/informe-forense.md` (Sección 5.1) |
| **Volcados de RAM, WinPmem y Volatility** | Integrante 6 (Memoria Volátil) | `docs/informe-forense.md` (Sección 5.3) |
| **Tabla $MFT, vssadmin y Antiforense** | Integrante 7 (Sistema de Archivos) | `docs/informe-forense.md` (Sección 5.4) |
| **Copias de Seguridad, Costos y Lecciones** | Integrante 8 (Recuperación) | `docs/informe-forense.md` (Sección 6) |

