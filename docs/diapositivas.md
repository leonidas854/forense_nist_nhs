---
marp: true
theme: default
paginate: true
header: "Informática Forense · WannaCry en el NHS · NIST CSF 2.0"
footer: "Equipo de Peritaje Forense (8 Integrantes) · leonidas854"
style: |
  section {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 24px;
    padding: 40px;
  }
  h1 {
    color: #0b3954;
    font-size: 38px;
  }
  h2 {
    color: #087e8b;
    font-size: 30px;
  }
  .highlight {
    background-color: #ff5a5f;
    color: white;
    padding: 2px 8px;
    border-radius: 4px;
  }
  .badge {
    background-color: #c81d25;
    color: white;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 18px;
    font-weight: bold;
  }
  table {
    font-size: 18px;
  }
---

# WannaCry en el NHS: Laboratorio Forense y Mapeo Retrospectivo a NIST CSF 2.0
### Caso de Estudio Pericial · Sector Sanitario del Reino Unido (2017)

**Materia:** Informática Forense  
**Marco de Trabajo:** NIST CSF 2.0 (2024) & NIST IR 8374 Rev. 1 (Final 2026)  
**Equipo de Investigación:** 8 Peritos  
**Expositores Principales:**  
- **Expositor 1:** Perito Coordinador (Gobernanza, Contexto NHS, ID y Protección)  
- **Expositor 2:** Perito Técnico (Laboratorio, Ghidra, Evidencias, DE, RS y Recuperación)  

---

## Agenda de la Defensa Oral

1. **Parte I: Contexto y Prevención (Expositor 1 · 12 min)**
   - Cronología y fuentes oficiales certificadas (NAO y DHSC 2018).
   - El vector de intrusión: Desmitificación del phishing vs SMBv1.
   - Auditoría de Gobernanza (**GV**), Identificación (**ID**) y Protección (**PR**).
2. **Parte II: Análisis Técnico y Respuesta (Expositor 2 · 12 min)**
   - Estación forense aislada en Linux / Vagrant / VirtualBox.
   - Ingeniería inversa en Ghidra 12.2: Decompilación del Kill Switch y Dropper PE.
   - Correlación de artefactos: Logs `.evtx`, Memoria RAM y Sistema de Archivos `$MFT`.
   - Detección (**DE**), Respuesta (**RS**), Recuperación (**RC**) y Lecciones del NHS.
3. **Parte III: Preguntas del Tribunal (Equipo de 8 · 6 min)**

---

## El Día Cero: 12 de Mayo de 2017 en el NHS

- **08:30 UTC:** Inicio de anomalías en hospitales de Inglaterra.
- **12:30 UTC:** Colapso simultáneo de terminales clínicas; aparición masiva del cartel `@WanaDecryptor@.exe` exigiendo **300 USD en Bitcoin**.
- **14:00 UTC:** Desvío de ambulancias en 5 departamentos de urgencias hospitalarias.
- **15:30 UTC:** Marcus Hutchins (MalwareTech) registra el dominio del Kill Switch.
- **16:00 UTC:** Varios hospitales siguen infectándose pese al registro del dominio.

> **Pregunta Pericial Central:**  
> *¿Por qué un exploit parchado por Microsoft dos meses antes paralizó al sistema de salud británico y por qué el Kill Switch no detuvo el ataque en ciertos hospitales?*

---

## Cifras Oficiales Auditadas: NAO 2018 vs DHSC

| Parámetro Pericial | Cifra Oficial Certificada | Fuente Primaria |
|---|---|---|
| **Trusts hospitalarios afectados** | **80 de 236** (34% del total) | NAO (2018, p. 8) / DHSC (2018, p. 5) |
| **Centros de atención primaria (GP)** | **603 centros** afectados | DHSC / Lessons Learned Review |
| **Citas médicas canceladas (reales)** | **6.912 citas** identificadas | NAO (2018, p. 10) |
| **Citas médicas estimadas** | **> 19.000 citas** perdidas | NAO (2018, p. 10) |
| **Costo financiero total** | **£92.000.000** (£72M TI + £20M productividad) | Department of Health (DHSC, 2018) |
| **Rescates pagados en Bitcoin** | **£0** (Ningún trust pagó extorsión) | NAO (2018, p. 11) |

*Nota metodológica:* La reclasificación de 81 a 80 trusts se formalizó en el informe ministerial tras verificar que un trust no sufrió infección interna sino desconexión preventiva.

---

## Desmitificación Forense: ¿Por qué NO fue Phishing?

```text
Mito Popular:
[Usuario desprevenido] ──> Abre correo malicioso ──> Ejecuta adjunto ──> Infección

Evidencia Forense Certificada (NCSC / NAO 2018):
[Internet WAN]
      │ (Puerto TCP 445 abierto sin filtro)
      ▼
[Host Perimetral Vulnerable] (MS17-010 EternalBlue)
      │
      ▼ (Infección y ejecución automática de mssecsvc.exe)
[Red WAN N3 plana interhospitalaria] ──> Infección masiva lateral a 80 Trusts
```

- **Cero interacción de usuario requerida.**
- Intrusión directa por desbordamiento de búfer en el controlador `srv.sys` de Windows.
- La red WAN privada N3 actuó como canal acelerador sin fronteras de seguridad.

---

## Mapeo Retrospectivo a NIST CSF 2.0

> **NIST CSF 2.0 (Publicado en Feb 2024)** & **NIST IR 8374 Rev. 1 (Final Jun 2026)**  
> Se aplica de forma retrospectiva como herramienta de autopsia organizativa.

```mermaid
graph LR
    GV[1. GOVERN] --> ID[2. IDENTIFY]
    ID --> PR[3. PROTECT]
    PR --> DE[4. DETECT]
    DE --> RS[5. RESPOND]
    RS --> RC[6. RECOVER]
    RC -.->|Retroalimentación| GV
```

- **CSF 1.1:** 5 funciones (Carecía de Gobernanza explícita).
- **CSF 2.0:** Incorpora **GOVERN (GV)** como eje rector, enfatizando la toma de decisiones, autoridad de desconexión y gestión de riesgos en la cadena de suministro.

---

## Función GOVERN (GV): El Vacío de Supervisión y Mando

* **GV.OV-01 (Supervisión de Decisiones de Riesgo):**
  - NHS Digital emitió alertas **CareCERT** en marzo y abril de 2017 sobre el riesgo crítico de SMBv1.
  - **Fallo pericial:** No existían mecanismos formales para auditar ni exigir el cumplimiento del parche en los 236 trusts independientes.
* **GV.RR-02 (Roles y Autoridad de Emergencia):**
  - Durante el ataque, ningún funcionario del Ministerio de Salud tenía autoridad legal explícita para desconectar la red nacional N3.
  - Los directores locales tomaron decisiones fragmentadas (desconectar cables a ciegas).
* **GV.SC (Gestión de Riesgos de Terceros):**
  - Proveedores de software médico exigían no modificar el sistema operativo base, impidiendo actualizaciones de seguridad.

---

## Función IDENTIFY (ID): La Ceguera de Activos Críticos

* **ID.AM-01 (Inventario de Activos Físicos y Software):**
  - El NHS desconocía cuántos equipos ejecutaban versiones sin soporte de Windows.
  - Equipos de diagnóstico por imágenes (resonadores, tomógrafos, analizadores de sangre) funcionaban con **Windows XP embebido** y **Windows 7 sin Service Pack**.
* **ID.RA-01 (Evaluación de Vulnerabilidades):**
  - No se realizaban escaneos periódicos del puerto TCP 445 en interfaces internas ni en enlaces hacia la red N3.
  - Falsa sensación de seguridad: *"Si está en la red interna N3, estamos protegidos"*.

---

## Función PROTECT (PR): El Parche MS17-010 y la Red N3

* **PR.PS-02 (Mantenimiento y Parches de Software):**
  - Microsoft publicó el boletín **MS17-010** el 14 de marzo de 2017 (dos meses antes del ataque).
  - La mayoría de los hospitales no aplicaron el parche por falta de ventanas de mantenimiento programadas.
* **PR.IR-01 (Resiliencia de Red y Segmentación):**
  - La red **N3** era una WAN compartida totalmente plana.
  - **Cero segmentación:** No existían firewalls internos ni filtrado de paquetes SMB entre hospitales.
  - Un solo dispositivo infectado en Londres propagó paquetes `SYN 445` a centros en Manchester y Yorkshire en segundos.

---

## Transición Técnica: De la Estrategia al Código

```text
========================================================================
EXPOSITOR 1 (Gobernanza / Contexto)  ───►  EXPOSITOR 2 (Forense / Código)
========================================================================
- ¿Qué falló en la organización?          - ¿Cómo opera el malware en Ghidra?
- ¿Por qué estaba vulnerable la red?     - ¿Qué artefactos deja en Windows?
- Mapeo a GV, ID y PR                    - Mapeo a DE, RS y RC
```

---

## Estación Forense Aislada (Vagrant + VirtualBox)

* **Anfitrión:** Linux x86_64.
* **Hipervisor:** VirtualBox 7.2.22 controlado mediante Vagrant 2.4.9.
* **VM de Análisis:** `forense-nhs-win10` (Windows 10 x64, 4 GiB RAM, 64 GiB disco).
* **Política de Aislamiento Innegociable:**
  - **8 adaptadores de red físicamente desconectados** (`nic1: "none" ... nic8: "none"`).
  - Comunicador Vagrant configurado en modo experimental `none` (sin WinRM ni SSH).
  - Carpetas compartidas, portapapeles y Drag & Drop **deshabilitados**.
  - Script verificador: `python3 scripts/check_isolation.py` (ejecutado y validado).
* **DVD de Herramientas (Solo Lectura):** Ghidra 12.2, OpenJDK 25, Volatility 3, Sysinternals, Wireshark 4.6.9.

---

## Muestra Canónica de WannaCry (Mayo 2017)

* **Identificador Canónico:** WanaCrypt0r 2.0 (Muestra Original de Referencia).
* **Hash SHA-256:** `ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa`
* **Tamaño:** 3.514.368 bytes (~3.51 MB).

```text
[ed01eb... Muestra Completa (~3.5 MB)]
  ├── FASE 1: El Gusano y Dropper (mssecsvc.exe)
  │     ├── Comprobación del Kill Switch (InternetOpenUrlA)
  │     ├── Creación del servicio persistente mssecsvc2.0
  │     └── Explotación SMBv1 (EternalBlue / DoublePulsar)
  │
  └── FASE 2: El Cifrador Puro (Oculto en .rsrc/R -> tasksche.exe ~1.8 MB)
        ├── Descompresión con contraseña interna: WNcry@2ol7
        ├── Sabotaje antiforense: vssadmin delete shadows /all /quiet
        └── Cifrado híbrido AES-128-CBC + RSA-2048 (Extensión .WNCRY)
```

---

## Ghidra 12.2: Decompilación del Kill Switch (RS.AN-03)

```c
// Decompilación en Ghidra de WinMain (Muestra ed01eb...)
hInternet = InternetOpenA("Microsoft Internet Explorer", 0, NULL, NULL, 0);
hUrl = InternetOpenUrlA(hInternet, 
       "http://www.iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com", 
       NULL, 0, 0x84000000, 0);

if (hUrl != NULL) {
    // KILL SWITCH ACTIVO: El dominio responde (HTTP 200)
    InternetCloseHandle(hUrl);
    InternetCloseHandle(hInternet);
    ExitProcess(0); // SE DETIENE SIN CIFRAR
}

// SI FALLA LA CONEXIÓN: CONTINÚA LA INFECCIÓN
InternetCloseHandle(hInternet);
Payload_ExecuteServiceInstall();
```

---

## El Gran Hallazgo Forense: La Paradoja del Proxy en el NHS

> **¿Por qué algunos hospitales se infectaron después de que Marcus Hutchins registró el dominio el 12 de mayo a las 15:30 UTC?**

```text
[Equipo Hospitalario del NHS]
       │
       │ (Petición HTTP a iuqerfsodp9...com)
       ▼
[Servidor Proxy Corporativo del NHS]
       │ ──► Exige Autenticación NTLM/Kerberos O bloquea dominio desconocido
       ▼
[Error HTTP: 407 Proxy Auth Required / Conexión Rechazada]
       │
       ▼
[API InternetOpenUrlA devuelve NULL (Fallo)]
       │
       ▼
[MALWARE CREE QUE EL KILL SWITCH NO EXISTE -> PROCEDE A CIFRAR]
```

---

## Ghidra 12.2: Persistencia del Servicio y Dropper

* **Persistencia en el Sistema:**
  - API `CreateServiceA` en `ADVAPI32.DLL`.
  - Nombre de servicio: `mssecsvc2.0`.
  - Display Name: `"Microsoft Security Center (2.0) Service"`.
  - Binario asociado: `C:\Windows\mssecsvc.exe -k DcomLaunch`.

* **Extracción del Recurso Cifrador (Dropper):**
  - APIs de `KERNEL32.DLL`: `FindResourceA(hModule, "R", 0x802)` y `LockResource`.
  - Extrae el archivo ZIP cifrado y escribe el ejecutable en:
    `C:\Windows\tasksche.exe`
  - Contraseña interna hardcodeada: **`WNcry@2ol7`**

---

## Función DETECT (DE): Detección en Windows Event Logs

* **System.evtx · Creación de Servicio (Evento ID 7045):**
  ```xml
  <EventID>7045</EventID>
  <ServiceName>mssecsvc2.0</ServiceName>
  <ImagePath>C:\Windows\mssecsvc.exe -k DcomLaunch</ImagePath>
  <ServiceType>user mode service</ServiceType>
  <StartType>auto start</StartType>
  ```
* **Security.evtx / Sysmon · Ejecución Antiforense (ID 4688 / Sysmon 1):**
  - Línea de comando detectada:
    `cmd.exe /c vssadmin delete shadows /all /quiet`
    `cmd.exe /c wbadmin delete catalog -quiet`
    `cmd.exe /c bcdedit /set {default} recoveryenabled No`

---

## Función RESPOND (RS): Forense de Memoria Volátil

* **Adquisición en Vivo:** Controlador WinPmem RC2 (`winpmem_mini_x64_rc2.exe`).
* **Análisis con Volatility 3 (`windows.pslist`, `windows.malfind`):**
  - Identificación del proceso `tasksche.exe` desvinculado de procesos legítimos de tareas programadas (`taskhostw.exe`).
  - Detección de memoria inyectada con permisos `PAGE_EXECUTE_READWRITE` (DLL `t.wnry` cargada reflectivamente).
  - Triage criptográfico: Búsqueda de claves AES-128 efímeras en RAM generadas por `CryptGenRandom` antes del reinicio del equipo.

```bash
# Comando ejecutado en el entorno local de Volatility 3:
local/analysis-env/bin/python descargas/volatility3/vol.py \
  -f local/copia-memoria.raw windows.pslist
```

---

## Función RESPOND (RS): Artefactos en Sistema de Archivos

* **Tabla `$MFT` (Master File Table):**
  - Creación de registros masivos de archivos temporales finalizados en `.wnry`.
  - Reemplazo y renombrado masivo de extensiones (`.docx`, `.pdf`, `.dcm` a `.WNCRY`).
  - Modificación de atributos `$STANDARD_INFORMATION` y `$FILE_NAME` (análisis de timestomping).
* **Entropía Criptográfica:**
  - Archivos afectados presentan entropía cercana a **7.99 / 8.0** (cifrado AES indistinguible de ruido blanco).
  - Cabecera fija de 8 bytes añadida a cada archivo cifrado:
    **`WANACRY!` (Hex: `57 41 4E 41 43 52 59 21`)**

---

## Función RECOVER (RC): El Colapso de la Recuperación Local

* **RC.RP-01 (Ejecución del Plan de Recuperación):**
  - La recuperación local mediante *Restaurar Sistema* fue saboteada por el borrado de Volume Shadow Copies (`vssadmin`).
  - Imposibilidad de revertir el estado del sistema sin respaldos offline.
* **RC.RP-05 (Integridad de Activos Restaurados):**
  - Cero pagos de rescate: Cumplimiento de la directriz de no alimentar el cibercrimen.
  - Reinstalación completa de imágenes base limpias desde discos físicos.
  - Validación de respaldos fríos desvinculados de la red (**PR.DS-11**).

---

## Lecciones del Informe Smart (DHSC 2018)

1. **Fin de la Red N3:** Migración obligatoria y acelerada hacia **HSCN (Health and Social Care Network)** con segmentación por defecto y telemetría centralizada.
2. **Erradicación de SMBv1:** Bloqueo perimetral e interno del puerto TCP 445 en todos los enrutadores del sector salud.
3. **Mando Centralizado (GV.RR-02):** Creación del Centro de Operaciones de Ciberseguridad (CSOC) de NHS Digital con autoridad expresa para aislar trusts de la red nacional ante ataques activos.
4. **Subsidio de Actualización:** Fondos gubernamentales para reemplazar sistemas operativos heredados en equipos biomédicos.

---

## Conclusiones del Peritaje

1. **WannaCry no triunfó por su criptografía:** El malware utilizó primitivas criptográficas estándar (CryptoAPI). El vector de devastación fue el componente de gusano SMBv1 y la ausencia de segmentación interna.
2. **La causa raíz radicó en Gobernanza e Identificación:** El parche existía desde marzo de 2017; fallaron la supervisión (GV.OV-01) y la visibilidad de activos clínicos legados (ID.AM-01).
3. **El Kill Switch demostró la interdependencia entre código y red:** La configuración de los proxys corporativos hospitalarios invalidó la efectividad del dominio de interrupción en ciertos centros.
4. **CSF 2.0 e IR 8374r1 validan su pertinencia:** La inclusión de la función *Govern* responde precisamente a los vacíos institucionales evidenciados en el caso NHS.

---

## Bibliografía y Fuentes Primarias Oficiales (APA 7)

* **Department of Health and Social Care [DHSC].** (2018). *Lessons learned review of the WannaCry ransomware cyber attack*. Her Majesty's Stationery Office.
* **National Audit Office [NAO].** (2018). *Investigation: WannaCry cyber attack and the NHS* (Report by the Comptroller and Auditor General HC 414). National Audit Office.
* **National Institute of Standards and Technology [NIST].** (2024). *The NIST Cybersecurity Framework (CSF) 2.0* (NIST CSWP 29). https://doi.org/10.6028/NIST.CSWP.29
* **National Institute of Standards and Technology [NIST].** (2025). *Incident Response Recommendations and Considerations for Cybersecurity Risk Management* (NIST SP 800-61 Rev. 3).
* **Souppaya, M., Barker, W. C., Fisher, W., & Scarfone, K.** (2026). *Ransomware Risk Management: A Cybersecurity Framework 2.0 Community Profile* (NIST IR 8374 Rev. 1). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.IR.8374r1

