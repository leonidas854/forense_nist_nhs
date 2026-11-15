# P3 — Código seleccionado para lectura

**Lectura visual:** [diagramas de flujo de este componente](diagramas.md).

**Alcance inicial:** 3 funciones transcritas de 1.070 reconocidas por Ghidra.
Consulta [qué falta y cómo ampliar P3](../ALCANCE-Y-AMPLIACION.md#p3);
la selección no equivale al análisis completo del componente.

[Guía de esta persona](README.md) · [Índice del equipo](../README.md)

Componente SHA-256: `b9c5d4339809e0ad9a00d4d3dd26fdf44a32819a54abf846bb9b560d81391c25`. Arquitectura: **x86, PE32**.

Consulta de origen (UTC): `2026-11-15T17:54:00.965095+00:00`. Ghidra **12.2 DEV**.

Cuerpos transcritos del Decompiler, con normalización de espacios; las explicaciones exteriores son editoriales. No es código fuente original ni preparado para compilar. Los comentarios y nombres españoles dentro del código pertenecen al analista.

El JSON original y las muestras se conservan localmente, fuera de Git. La identidad y los hashes de texto están en [indice.json](../indice.json).

## Navegación

- [00401bb0 — Consulta de SID y token](#f-00401bb0)
- [00401b50 — Solicitud mediante ShellExecuteExA](#f-00401b50)
- [00401a90 — Creación y espera de proceso](#f-00401a90)

<a id="f-00401bb0"></a>

## 00401bb0 — Consulta de SID y token

Nombre en la exportación: `FUN_00401bb0-00401bb0`.

**Qué mirar:** Distingue el éxito de la llamada (BVar1) del resultado por parámetro de salida (local_10). Observa la salida cuando falla una consulta.

```c
undefined4 FUN_00401bb0(void)

{
  BOOL BVar1;
  BOOL local_10;
  PSID local_c;
  _SID_IDENTIFIER_AUTHORITY local_8;

  local_8.Value[0] = '\0';
  local_8.Value[1] = '\0';
  local_8.Value[2] = '\0';
  local_8.Value[3] = '\0';
  local_8.Value[4] = '\0';
  local_8.Value[5] = '\x05';
  local_10 = 0;
  BVar1 = AllocateAndInitializeSid(&local_8,'\x02',0x20,0x220,0,0,0,0,0,0,&local_c);
  if (BVar1 == 0) {
    return 0;
  }
  BVar1 = CheckTokenMembership((HANDLE)0x0,local_c,&local_10);
  if (BVar1 == 0) {
    local_10 = 0;
  }
  FreeSid(local_c);
  return local_10;
}
```

**Límite de la conclusión:** Retornar cero puede corresponder a fallo de consulta o a un resultado negativo; no asumas que todos los ceros significan lo mismo.

En tu ficha: entradas → condición → llamadas → retorno → evidencia faltante. [Volver a la guía](README.md).


<a id="f-00401b50"></a>

## 00401b50 — Solicitud mediante ShellExecuteExA

Nombre en la exportación: `FUN_00401b50-00401b50`.

**Qué mirar:** Identifica campos de SHELLEXECUTEINFOA y la referencia al verbo runas. Sigue param_1 y param_2 hasta sus campos.

```c
bool __cdecl FUN_00401b50(LPCSTR param_1,LPCSTR param_2,int param_3)

{
  BOOL BVar1;
  int iVar2;
  HWND *ppHVar3;
  SHELLEXECUTEINFOA local_3c;

  ppHVar3 = (HWND *)&local_3c.fMask;
  for (iVar2 = 0xe; iVar2 != 0; iVar2 = iVar2 + -1) {
    *ppHVar3 = (HWND)0x0;
    ppHVar3 = ppHVar3 + 1;
  }
  local_3c.fMask = 0;
  local_3c.lpDirectory = (LPCSTR)0x0;
  local_3c.lpFile = param_1;
  local_3c.nShow = -(uint)(param_3 != 0) & 5;
  local_3c.cbSize = 0x3c;
  local_3c.lpParameters = param_2;
  local_3c.lpVerb = s_runas_0041fdac;
  BVar1 = ShellExecuteExA(&local_3c);
  return (bool)('\x01' - (BVar1 != 1));
}
```

**Límite de la conclusión:** La presencia de runas no demuestra elevación concedida ni que una operación contra recuperación terminara.

En tu ficha: entradas → condición → llamadas → retorno → evidencia faltante. [Volver a la guía](README.md).


<a id="f-00401a90"></a>

## 00401a90 — Creación y espera de proceso

Nombre en la exportación: `FUN_00401a90-00401a90`.

**Qué mirar:** Sigue CreateProcessA, la condición de espera, el tratamiento del resultado y los handles cerrados.

```c
undefined4 __cdecl FUN_00401a90(LPSTR param_1,DWORD param_2,LPDWORD param_3)

{
  BOOL BVar1;
  DWORD DVar2;
  int iVar3;
  LPSTR *ppCVar4;
  _PROCESS_INFORMATION local_54;
  _STARTUPINFOA local_44;

  local_44.cb = 0x44;
  ppCVar4 = &local_44.lpReserved;
  for (iVar3 = 0x10; iVar3 != 0; iVar3 = iVar3 + -1) {
    *ppCVar4 = (LPSTR)0x0;
    ppCVar4 = ppCVar4 + 1;
  }
  local_54.hThread = (HANDLE)0x0;
  local_54.dwProcessId = 0;
  local_54.dwThreadId = 0;
  local_54.hProcess = (HANDLE)0x0;
  local_44.dwFlags = 1;
  local_44.wShowWindow = 0;
  BVar1 = CreateProcessA((LPCSTR)0x0,param_1,(LPSECURITY_ATTRIBUTES)0x0,(LPSECURITY_ATTRIBUTES)0x0,0
                         ,0x8000000,(LPVOID)0x0,(LPCSTR)0x0,&local_44,&local_54);
  if (BVar1 == 0) {
    return 0;
  }
  if (param_2 != 0) {
    DVar2 = WaitForSingleObject(local_54.hProcess,param_2);
    if (DVar2 != 0) {
      TerminateProcess(local_54.hProcess,0xffffffff);
    }
    if (param_3 != (LPDWORD)0x0) {
      GetExitCodeProcess(local_54.hProcess,param_3);
    }
  }
  CloseHandle(local_54.hProcess);
  CloseHandle(local_54.hThread);
  return 1;
}
```

**Límite de la conclusión:** El retorno 1 del auxiliar no demuestra éxito del objetivo externo. Este auxiliar no sustituye la decompilación ausente del bloque llamador.

En tu ficha: entradas → condición → llamadas → retorno → evidencia faltante. [Volver a la guía](README.md).
