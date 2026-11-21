# Windows 10 existente: copia aislada para el estudio

Comprobación del 20/11/2026, hora de Bolivia. El usuario identificó la VM
«Windows 10» y autorizó una copia aislada. Se realizó una clonación **completa**,
no un clon enlazado; se conservó la original apagada. Su configuración consultada
antes y después coincide. No se inició ni instaló software en la original.

## Qué quedó preparado

- Nombre: `forense-nhs-win10-copia`, en el registro VirtualBox e IPC privados.
- Carpeta: `local/vms/forense-nhs-win10-copia/`, excluida de Git.
- 4 CPU, 4096 MiB de RAM; disco clonado localmente.
- Ocho NIC en `none`; sin carpetas compartidas, portapapeles, transferencia por
  portapapeles, arrastrar/soltar, USB o VRDE.
- ISO de instalación desconectada; DVD de herramientas anterior conectado.
- DVD independiente `local/entrega-nist-lectura.iso`, etiqueta `NHS_ESTUDIO`,
  conectado para consultar los nuevos PDF y Word desde «Este equipo».
- Snapshot `aislada-antes-de-practica`, tomado antes de arrancar la copia.
- Escritorio y winver observados: Windows 10 Pro, versión 1903, build 18362.356.
- Cierre comprobado: apagada tras solicitar apagado normal desde Windows.

No se evaluaron la limpieza previa, todos los parches, la activación/licencia ni
la compatibilidad de cada herramienta con esta versión. No se ejecutaron muestras.
Las capturas y logs permanecen en `local/revision-informe-2026-11-20/vm/`;
no se publican datos personales ni discos de la máquina del usuario.

## Abrir la copia correcta

```bash
python3 scripts/check_isolation.py forense-nhs-win10-copia
./scripts/vbox-lab.sh showvminfo forense-nhs-win10-copia
./scripts/vbox-lab.sh startvm forense-nhs-win10-copia --type gui
```

Comprobar el primer resultado antes de arrancar. Para abrir el administrador
aislado: `./scripts/vbox-lab.sh --gui`. No usar la VM original del perfil normal,
que conserva NAT, puente y comparticiones globales.

La VM `forense-nhs-win10` anterior sigue vacía y se administra con `./lab`.
`./lab status` consulta esa VM, **no la copia**. La box inicial continúa siendo
hardware vacío; no se sustituyeron sus discos, identidad ni metadatos Vagrant.
No se empaqueta ni se publica la copia del Windows existente.

## Verificación efectuada

Se ejecutaron las 18 pruebas unitarias, `./lab validate`,
`python3 scripts/check_isolation.py` y la misma comprobación indicando el nombre
de la copia. Todos dieron resultado correcto. El control real evalúa aislamiento
de configuración; no certifica ausencia de escapes del hipervisor.

La copia puede usarse para lectura y los ejercicios benignos descritos en la
[parte práctica](../entrega_nist/PARTE_PRACTICA_NIST_GHIDRA.pdf). La instalación y
validación de herramientas en el invitado siguen pendientes. La imagen de
herramientas existente no contiene automáticamente los documentos nuevos.
