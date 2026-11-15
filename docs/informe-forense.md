# Informe Pericial de Informática Forense
## Caso de Estudio: WannaCry en el NHS · Laboratorio Forense y Mapeo Retrospectivo a NIST CSF 2.0 & NIST IR 8374 Rev. 1

**Materia:** Informática Forense  
**Caso:** Incidente de Criptogusano en el National Health Service (Reino Unido, 12 de mayo de 2017)  
**Normativa y Estándares Aplicados:** NIST CSF 2.0 (NIST CSWP 29, 2024), NIST IR 8374 Rev. 1 (Final, junio 2026), NIST SP 800-61 Rev. 3 (2025), ISO/IEC 27037.  
**Equipo Pericial (8 Integrantes):**  
- **Perito 1 (Coordinador General & Custodio Líder):** Gobernanza (GV), Marco Metodológico y Cadena de Custodia. *(Expositor 1)*  
- **Perito 2 (Auditor de Infraestructura & Activos):** Identificación (ID), Inventario de Activos y Dispositivos Clínicos Legados.  
- **Perito 3 (Especialista en Protección & Redes):** Protección (PR), Autopsia de SMBv1/MS17-010 y Arquitectura de Red N3.  
- **Perito 4 (Analista de Monitorización & Logs):** Detección (DE), Auditoría de Windows Event Logs (`.evtx`) y Reglas Sysmon.  
- **Perito 5 (Ingeniero Inverso de Malware):** Respuesta (RS.AN-03), Decompilación en Ghidra 12.2 y Análisis del Dropper/Kill Switch. *(Expositor 2)*  
- **Perito 6 (Analista Forense de Memoria Volátil):** Respuesta (RS.AN), Triage de Memoria RAM con Volatility 3 y WinPmem RC2.  
- **Perito 7 (Analista de Sistema de Archivos & Disco):** Respuesta (RS.AN-06/07), Tabla `$MFT`, Antiforense (`vssadmin`) y Cifrado `.WNCRY`.  
- **Perito 8 (Auditor de Recuperación & Lecciones):** Recuperación (RC), Planes de Continuidad, Impacto Financiero y Recomendaciones.  

---

## 1. Resumen Ejecutivo (Executive Summary)

El presente informe constituye el dictamen pericial y académico sobre el incidente de seguridad informática ocurrido el 12 de mayo de 2017 que paralizó al **National Health Service (NHS)** de Inglaterra mediante la propagación del criptogusano **WanaCrypt0r 2.0** (conocido comúnmente como WannaCry).

A través de un enfoque pericial riguroso, este trabajo correlaciona la **evidencia documental histórica certificada** por los órganos fiscalizadores del Reino Unido (National Audit Office y Department of Health and Social Care) con la **observación técnica y experimental** desarrollada en una estación de laboratorio aislada (anfitrión Linux, hipervisor VirtualBox 7.2 y Vagrant 2.4.9 con aislamiento estricto de red).

El análisis de ingeniería inversa estática ejecutado en **Ghidra 12.2** sobre la muestra canónica original (`ed01eb...`) permitió descomponer la anatomía del artefacto en dos fases: el módulo de gusano/dropper (`mssecsvc.exe`) y el módulo de cifrado (`tasksche.exe`). Se demostró la mecánica del dominio de interrupción (*Kill Switch*) y se explicó pericialmente la llamada *paradoja del proxy hospitalario*, la cual provocó que múltiples centros hospitalarios se infectaran incluso después de que el dominio fuera registrado a nivel global.

Finalmente, el incidente fue sometido a una auditoría retrospectiva bajo las seis funciones del nuevo **NIST Cybersecurity Framework versión 2.0 (CSF 2.0)** y las directrices del perfil comunitario **NIST IR 8374 Rev. 1 (versión final de junio de 2026)**. Se concluye que el impacto devastador del ataque no se debió a una sofisticación criptográfica sin precedentes, sino a fallas estructurales y sistémicas en las funciones de **Gobernanza (GV)**, **Identificación (ID)** y **Protección (PR)**, las cuales permitieron que una vulnerabilidad parchada dos meses antes por Microsoft (boletín MS17-010) causara pérdidas estimadas en **92 millones de libras esterlinas** y la suspensión de miles de atenciones médicas.

---

## 2. Marco Legal, Ético y Cadena de Custodia

### 2.1. Principios Periciales e Integridad de la Evidencia (ISO/IEC 27037)
El equipo de investigación rigió todas sus actuaciones bajo las directrices internacionales para el manejo de evidencia digital (ISO/IEC 27037:2012):
1. **Admisibilidad y Confiabilidad:** Toda afirmación histórica se respalda en reportes de auditoría gubernamental con número de informe y página contrastables.
2. **Preservación Criptográfica:** Ningún archivo original ha sido modificado. Toda muestra o binario de herramienta cuenta con su correspondiente hash **SHA-256** documentado en `config/descargas.lock.json` y cotejado con `config/SHA256SUMS`.
3. **No Proliferación y Bioseguridad Informática:** El análisis de muestras de malware se ejecutó exclusivamente mediante métodos estáticos de ingeniería inversa y en entornos con desconexión física de interfaces de red, acatando las normativas nacionales e internacionales que prohíben la puesta en riesgo de redes informáticas ajenas.

### 2.2. Delimitación Metodológica
Para garantizar la honestidad académica y pericial, este informe distingue explícitamente tres niveles de información:
- **Hechos Históricos Documentados:** Datos procedentes de las auditorías oficiales del NHS, NAO y NCSC.
- **Observaciones de Laboratorio:** Datos derivados del desensamblado estático en Ghidra y la inspección de artefactos en el laboratorio virtual propio.
- **Hipótesis Periciales:** Deducciones técnicas formuladas a partir de la correlación de ambas fuentes, debidamente etiquetadas.

---

## 3. Contexto Histórico y Hechos Certificados del Caso NHS

```text
CRONOLOGÍA PERICIAL DEL 12 DE MAYO DE 2017
────────────────────────────────────────────────────────────────────────
08:30 UTC  Primeras detecciones de lentitud y fallos en enlaces hospitalarios.
12:30 UTC  Bloqueo simultáneo de pantallas con la nota @WanaDecryptor@.exe.
14:00 UTC  Desvío masivo de ambulancias de urgencias a hospitales no afectados.
15:30 UTC  Marcus Hutchins registra el dominio iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com.
16:00 UTC  Hospitales con salida filtrada por Proxy continúan cifrándose.
18:00 UTC  Desconexión física manual de cables de red en decenas de centros de salud.
```

### 3.1. Auditoría Oficial de la National Audit Office (NAO 2018)
De acuerdo al informe oficial emitido por la Oficina Nacional de Auditoría del Reino Unido (NAO, 2018):
- **Alcance de la Afección:** Un total de **80 de los 236 trusts hospitalarios** de Inglaterra (el 34% de la red hospitalaria nacional) resultaron afectados de forma directa, además de 603 centros de atención médica primaria (General Practices).
- **Aclaración sobre la Cifra de Trusts (81 vs 80):** Si bien los primeros despachos informativos mencionaban 81 trusts, el informe de lecciones aprendidas del Ministerio de Salud (DHSC, 2018, nota 3, p. 5) certificó que un trust fue reclasificado al comprobarse que sus administradores desconectaron la infraestructura preventivamente sin haber sufrido infección interna activa.
- **Impacto Asistencial:** La NAO registró formalmente **6.912 citas médicas canceladas**, aunque su estimación pericial concluye que el número real superó las **19.000 citas**. Cinco departamentos de urgencias hospitalarias (Accident & Emergency) se vieron forzados a desviar ambulancias hacia otros centros de salud.
- **Impacto Financiero:** El Department of Health and Social Care calculó un costo total para el erario público de **92 millones de libras esterlinas**: £72 millones en sustitución y restauración urgente de sistemas de tecnología, y £20 millones en pérdidas directas de productividad del personal médico durante la contingencia.
- **Extorsión:** Ninguna institución del NHS pagó el rescate exigido de 300 dólares en Bitcoin.

### 3.2. Desmitificación Forense: El Vector de Entrada Real
Durante los primeros días posteriores al ataque, se difundió la hipótesis infundada de que el incidente se originó por empleados hospitalarios abriendo correos electrónicos con enlaces maliciosos (*phishing*).

Las investigaciones forenses del **National Cyber Security Centre (NCSC)** y la NAO refutaron categóricamente esta afirmación:
1. No se halló evidencia alguna de campañas de correo previas distribuyendo la muestra en las bandejas del NHS.
2. El vector inicial fue la exposición directa del puerto **TCP 445 (SMBv1)** a internet en determinados hosts perimetrales del NHS.
3. Tras la intrusión en el primer equipo, el módulo de gusano automatizado explotó la vulnerabilidad **EternalBlue (CVE-2017-0144 / MS17-010)**, inyectando el backdoor **DoublePulsar** en la memoria del kernel de Windows y propagándose lateralmente a través de la red privada **N3** sin requerir credenciales ni acción humana.

---

## 4. Estación de Laboratorio Forense y Protocolo de Aislamiento

Para analizar la muestra y correlacionar artefactos, se diseñó una estación pericial segura:

```text
+--------------------------------------------------------------------------+
|                       ESTACIÓN ANFITRIONA (LINUX)                        |
|                                                                          |
|  +--------------------------------------------------------------------+  |
|  |                 VIRTUALBOX 7.2 + VAGRANT 2.4.9                     |  |
|  |                                                                    |  |
|  |  VM: forense-nhs-win10 (Windows 10 x64, 4 GiB RAM, 64 GiB Disco)   |  |
|  |                                                                    |  |
|  |  [x] NIC 1: none  [x] NIC 2: none  ...  [x] NIC 8: none            |  |
|  |  [x] Shared Folders: DISABLED     [x] Clipboard: DISABLED          |  |
|  |  [x] Drag & Drop: DISABLED        [x] VRDE Remote: DISABLED        |  |
|  |  [x] Communicator: 'none' (Sin SSH ni WinRM)                       |  |
|  |                                                                    |  |
|  |  Unidad Óptica D: [local/herramientas.iso (Solo Lectura)]          |  |
|  |    ├── Ghidra 12.2 + OpenJDK 25                                    |  |
|  |    ├── Volatility 3 (Commit 881e970)                               |  |
|  |    ├── WinPmem RC2 (Adquisición RAM)                               |  |
|  |    ├── Sysinternals Suite (Procmon, Procexp, Sysmon64)             |  |
|  |    └── Wireshark 4.6.9 x64                                         |  |
|  +--------------------------------------------------------------------+  |
+--------------------------------------------------------------------------+
```

### 4.1. Verificación Automatizada del Aislamiento
El estado de la máquina virtual es auditado rigurosamente mediante el script `scripts/check_isolation.py`, el cual consulta las propiedades del hipervisor mediante `VBoxManage showvminfo`:
- Las 8 tarjetas de red virtuales (`nic1` a `nic8`) se encuentran configuradas en `none` (desactivadas).
- Se prohíbe cualquier canal de comunicación que permita fugas de datos hacia el host (portapapeles, carpetas compartidas, arrastrar y soltar).
- Se ejecutan cinco pruebas unitarias (`python3 -m unittest discover -s tests -v`) que validan que el sistema rechace de inmediato cualquier intento de aprovisionamiento con red activa.

---

## 5. Análisis Técnico de la Muestra Canónica (Ghidra 12.2 y Artefactos)

Se tomó como referencia formal la muestra canónica original de **WanaCrypt0r 2.0**:
- **Hash SHA-256:** `ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa`
- **Formato:** Portable Executable (PE32) x86 para Windows, tamaño 3.514.368 bytes.

### 5.1. Ingeniería Inversa en Ghidra: La Lógica del Kill Switch
Al abrir el binario en Ghidra 12.2 e inspeccionar el árbol de símbolos (`Symbol Tree -> Imports -> WININET.DLL`), se localiza la llamada a la función `InternetOpenUrlA` dentro del flujo principal de `WinMain`:

```c
// Decompilación en Ghidra 12.2 (WinMain - Muestra ed01eb...)
hSession = InternetOpenA("Microsoft Internet Explorer", 0, NULL, NULL, 0);
if (hSession != NULL) {
    hUrl = InternetOpenUrlA(hSession, 
           "http://www.iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com", 
           NULL, 0, 0x84000000, 0);
    if (hUrl != NULL) {
        // RAMA 1: CONEXIÓN EXITOSA -> KILL SWITCH ACTIVADO
        InternetCloseHandle(hUrl);
        InternetCloseHandle(hSession);
        ExitProcess(0); // El proceso finaliza limpiamente sin infectar
    }
    InternetCloseHandle(hSession);
}

// RAMA 2: CONEXIÓN FALLIDA -> EJECUCIÓN DEL ATAQUE
ExecutePayloadAndPropagate();
```

### 5.2. El Hallazgo Forense: La Paradoja del Proxy en el NHS
Esta estructura lógica explica el fenómeno observado en diversos trusts hospitalarios que sufrieron cifrado a pesar de que el investigador Marcus Hutchins ya había registrado el dominio a las 15:30 UTC del 12 de mayo:
1. En las estaciones clínicas hospitalarias, el tráfico web saliente estaba forzado a atravesar **servidores proxy corporativos** que exigían autenticación de usuario (NTLM/Kerberos) o que bloqueaban el acceso a dominios de reciente registro o categorizados como sospechosos.
2. La API `InternetOpenUrlA` utilizada por los autores de WannaCry **no implementó parámetros ni cabeceras para autenticarse ante un proxy**.
3. Al intentar conectar al dominio del Kill Switch, el proxy hospitalario denegó la conexión devolviendo un error HTTP (código 407 Proxy Authentication Required o 502 Bad Gateway).
4. La función `InternetOpenUrlA` interpretó este error retornando un puntero nulo (`NULL`), indicando falla en la conexión.
5. El malware concluyó que el dominio seguía inactivo y procedió con la rutina de instalación del servicio y cifrado de discos.

### 5.3. El Dropper Oculto y Persistencia del Servicio
- **Persistencia:** Mediante la API `CreateServiceA` de `ADVAPI32.DLL`, el gusano registra un servicio en el Administrador de Control de Servicios (SCM):
  - Nombre: `mssecsvc2.0`
  - Display Name: `Microsoft Security Center (2.0) Service`
  - Ruta de imagen: `C:\Windows\mssecsvc.exe -k DcomLaunch`
  - Tipo de inicio: `SERVICE_AUTO_START` (garantizando persistencia tras reinicio).
- **Extracción de la Fase 2 (El Cifrador):** Mediante `FindResourceA` y `LockResource`, localiza en su sección `.rsrc` el recurso con identificador `R` (tipo `0x802`), el cual contiene un archivo ZIP protegido por contraseña. Lo descomprime utilizando la clave hardcodeada **`WNcry@2ol7`** y escribe en disco el ejecutable **`C:\Windows\tasksche.exe`** (~1.8 MB), el cual es el motor de cifrado definitivo.

### 5.4. Sabotaje Antiforense en el Código
Al inspeccionar las cadenas del binario secundario (`tasksche.exe`), se evidencian las instrucciones destinadas a impedir la recuperación del sistema operativo:
```powershell
cmd.exe /c vssadmin delete shadows /all /quiet
cmd.exe /c wbadmin delete catalog -quiet
cmd.exe /c bcdedit /set {default} recoveryenabled No
cmd.exe /c bcdedit /set {default} bootstatuspolicy ignoreallfailures
cmd.exe /c icacls . /grant Everyone:F /T /C /Q
```

---

## 6. Correlación de Artefactos Forenses en el Sistema Operativo

| Vector Forense | Artefacto Generado en Windows | Herramienta de Extracción | Subcategoría NIST CSF 2.0 |
|---|---|---|---|
| **Servicios del Sistema** | **System.evtx (Evento ID 7045):** Instalación del servicio `mssecsvc2.0`. | Event Viewer / Hayabusa | **DE.AE-03 / DE.CM-01** |
| **Creación de Procesos** | **Security.evtx (ID 4688) / Sysmon (ID 1):** Invocación de `vssadmin delete shadows`. | Sysinternals Procmon / Sysmon | **RS.AN-03 / DE.CM-09** |
| **Memoria Volátil (RAM)** | Proceso `tasksche.exe` inyectando biblioteca reflectiva `t.wnry` en memoria no mapeada (`PAGE_EXECUTE_READWRITE`). | Volatility 3 (`windows.malfind`) | **RS.AN / RS.MI-01** |
| **Sistema de Archivos NTFS** | Modificación en tabla `$MFT`, sustitución de extensiones por `.WNCRY`, entropía 7.99 y cabecera mágica `WANACRY!`. | MFTECmd / FTK Imager | **RS.AN-06 / RS.AN-07** |
| **Red y Enlaces** | Ráfagas de paquetes `TCP SYN 445` hacia subredes locales y WAN N3. | Wireshark / Zeek | **DE.CM-01 / PR.IR-01** |

---

## 7. Mapeo Retrospectivo Exhaustivo a NIST CSF 2.0 y NIST IR 8374 Rev. 1

A continuación se detalla la matriz de evaluación pericial que audita retrospectivamente las fallas organizativas y técnicas del NHS frente a las 6 funciones del estándar:

### 7.1. Función GOVERN (Gobernanza)
* **GV.OV-01 (Supervisión de Decisiones de Gestión de Riesgo):**  
  *Fallo en el NHS:* NHS Digital emitió boletines críticos de advertencia (CareCERT) en marzo y abril de 2017 sobre la vulnerabilidad SMBv1. Sin embargo, no existía un proceso formal de supervisión para verificar si los directores de los 236 trusts cumplían las órdenes de actualización.  
  *Lección pericial:* La ciberseguridad en redes interconectadas requiere auditorías centralizadas con métricas vinculantes de cumplimiento.
* **GV.RR-02 (Roles, Responsabilidades y Autoridades):**  
  *Fallo en el NHS:* Durante las primeras 6 horas del ataque, ninguna autoridad nacional tenía el mandato legal expreso para ordenar el aislamiento o la desconexión total de la red N3, dejando las decisiones críticas en manos de administradores locales desbordados.
* **GV.SC (Gestión de Riesgo de Terceros y Proveedores):**  
  *Fallo en el NHS:* Los contratos con proveedores de equipamiento médico impedían expresamente que el personal del hospital aplicara parches de Windows en los terminales clínicos sin invalidar las garantías.

### 7.2. Función IDENTIFY (Identificación)
* **ID.AM-01 (Inventario de Activos y Dispositivos Críticos):**  
  *Fallo en el NHS:* Los trusts carecían de un catálogo actualizado de activos. Se desconocía el número exacto de terminales con sistemas obsoletos (**Windows XP** y **Windows 7** sin Service Pack) integrados en escáneres de tomografía y resonancia magnética.
* **ID.RA-01 (Evaluación de Riesgos y Vulnerabilidades):**  
  *Fallo en el NHS:* Ausencia de escaneos periódicos para detectar puertos TCP 445 expuestos internamente hacia la red compartida N3.

### 7.3. Función PROTECT (Protección)
* **PR.PS-02 (Mantenimiento y Actualización de Software):**  
  *Fallo en el NHS:* El parche oficial de Microsoft **MS17-010** estuvo disponible durante dos meses antes del ataque, pero no fue desplegado en los servidores y clientes del NHS debido al temor a incompatibilidades y falta de políticas de cambio.
* **PR.IR-01 (Resiliencia de Red y Segmentación):**  
  *Fallo en el NHS:* La red privada WAN **N3** funcionaba como una red plana y sin fronteras. La ausencia de firewalls internos y de bloqueo del protocolo SMB permitió que el gusano saltara de un hospital en Londres a trusts en Norfolk y Hertfordshire en minutos.
* **PR.DS-11 (Integridad y Aislamiento de Respaldos):**  
  *Fallo en el NHS:* Varios centros mantenían sus copias de seguridad en discos compartidos de red mapeados, los cuales fueron cifrados por el malware al tener permisos de escritura.

### 7.4. Función DETECT (Detección)
* **DE.CM-01 / DE.CM-09 (Monitorización Continua de Red y Sistemas):**  
  *Fallo en el NHS:* Ausencia de sistemas de detección de intrusos (IDS) con capacidad de alertar sobre ráfagas inusuales de tráfico SMBv1 (puerto 445).  
  *Artefacto de laboratorio:* La presencia de eventos `System.evtx` ID 7045 debió haber disparado alertas automatizadas en los primeros 60 segundos de infección.
* **DE.AE-03 (Correlación de Eventos y Análisis de Anomalías):**  
  *Fallo en el NHS:* Inexistencia de un SIEM centralizado a nivel nacional capaz de correlacionar las alertas locales de múltiples hospitales.

### 7.5. Función RESPOND (Respuesta)
* **RS.AN-03 (Análisis de Incidente y Causa Raíz):**  
  *Aplicación pericial:* Decompilación estática de la lógica de decisión en Ghidra 12.2 y extracción de indicadores de compromiso (IoCs).
* **RS.AN-06 / RS.AN-07 (Registro de Actuaciones e Integridad de Evidencias):**  
  *Aplicación pericial:* Levantamiento de bitácoras de adquisición, generación de hashes SHA-256 de volcados de memoria y registro de marcas temporales normalizadas a UTC.
* **RS.MI-01 (Contención del Incidente):**  
  *Fallo en el NHS:* La contención inicial se realizó mediante desconexión física caótica de cables de red, interrumpiendo servicios en áreas no infectadas.

### 7.6. Función RECOVER (Recuperación)
* **RC.RP-01 (Ejecución del Plan de Recuperación):**  
  *Fallo en el NHS:* La recuperación local falló debido a la destrucción de las copias de sombra del volumen (`vssadmin`). Los hospitales debieron reinstalar estaciones desde medios físicos externos.
* **RC.RP-03 (Verificación de Integridad antes de Restaurar):**  
  *Directriz pericial:* Validación de que los sistemas restaurados no contuvieran la persistencia en el registro (`HKLM Run`) ni el servicio malicioso antes de conectarlos nuevamente a la red.
* **RC.RP-05 (Pruebas Funcionales e Integridad Post-Recuperación):**  
  *Resultado en el NHS:* Se restablecieron los servicios clínicos tras días de trabajo continuo, sin haber financiado a los extorsionadores.

---

## 8. Lecciones Aprendidas y Evaluación de Resiliencia Sanitaria

El informe ministerial de lecciones aprendidas elaborado por el CIO Will Smart (DHSC, 2018) sentó las bases de la transformación tecnológica de la salud en el Reino Unido, muchas de cuyas directrices fueron posteriormente adoptadas por el NIST:

1. **Desmantelamiento de la Red N3:** Se reemplazó la red N3 por la **Health and Social Care Network (HSCN)**, una infraestructura moderna basada en el principio de confianza cero (*Zero Trust*), con segmentación estricta entre hospitales y cifrado perimétrico obligatorio.
2. **Erradicación del Protocolo SMBv1:** Se prohibió de forma terminante el uso del protocolo SMBv1 en todo el sector público británico, forzando la deshabilitación del puerto 445 en enlaces interinstitucionales.
3. **Mando Unificado y Creación del CSOC de NHS Digital:** Se otorgó autoridad centralizada a un Centro de Operaciones de Ciberseguridad (CSOC) nacional con capacidad jurídica y técnica para intervenir y desconectar trusts de la red sanitaria ante ciberataques activos.
4. **Programa Nacional de Actualización de Dispositivos Clínicos:** Se crearon fondos de subvención específicos para reemplazar terminales obsoletos con Windows XP y Windows 7 en equipos de radiología y análisis clínico.

---

## 9. Conclusiones Periciales

1. **La vulnerabilidad de WannaCry fue sistémica, no criptográfica:** El ataque no prevaleció por la complejidad de su cifrado (el cual utilizó algoritmos estándar AES y RSA), sino por el vector automatizado de gusano SMBv1 propagándose sobre una red WAN nacional carente de segmentación.
2. **Validación del Marco NIST CSF 2.0:** El análisis retrospectivo confirma la necesidad imperiosa de haber incorporado la función **GOVERN (Gobernanza)** en el estándar. Si el NHS hubiera contado con mecanismos de verificación del cumplimiento de parches (GV.OV-01) y roles de mando claros (GV.RR-02), el ataque habría sido mitigado antes de su detonación.
3. **El Kill Switch como lección de arquitectura:** La efectividad del dominio de interrupción registrado por Marcus Hutchins demostró la estrecha dependencia entre el código malicioso y la infraestructura de telecomunicaciones: la presencia de proxys hospitalarios impidió la activación del freno de emergencia en múltiples centros asistenciales.
4. **Metodología Forense Probada:** Se demostró la viabilidad de realizar un peritaje integral combinando fuentes oficiales certificadas, ingeniería inversa estática en Ghidra y verificación de artefactos en un laboratorio virtualizado y aislado, preservando en todo momento la cadena de custodia y los principios éticos de la informática forense.

---

## 10. Referencias Bibliográficas (Formato APA 7)

* Department of Health and Social Care [DHSC]. (2018). *Lessons learned review of the WannaCry ransomware cyber attack* (Report by Will Smart, Chief Information Officer). Her Majesty's Stationery Office.
* National Audit Office [NAO]. (2018). *Investigation: WannaCry cyber attack and the NHS* (Report by the Comptroller and Auditor General, HC 414). National Audit Office.
* National Institute of Standards and Technology [NIST]. (2024). *The NIST Cybersecurity Framework (CSF) 2.0* (NIST CSWP 29). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.CSWP.29
* National Institute of Standards and Technology [NIST]. (2025). *Incident Response Recommendations and Considerations for Cybersecurity Risk Management* (NIST Special Publication 800-61 Revision 3). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.SP.800-61r3
* Souppaya, M., Barker, W. C., Fisher, W., & Scarfone, K. (2026). *Ransomware Risk Management: A Cybersecurity Framework 2.0 Community Profile* (NIST Interagency Report 8374 Revision 1, Final). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.IR.8374r1

