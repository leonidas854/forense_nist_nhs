# Materiales del análisis y preparación local

**Para repartir el trabajo y leer el código desde el repositorio:**
[paquetes P1–P4](../equipo/README.md). Incluyen 16 funciones transcritas en
cuadernos Markdown, con guías, fragmentos de Listing y ejercicios. Esta edición
didáctica es publicable; los archivos originales de evidencia permanecen locales.

Preparación del 15/11/2026. Windows **no se instala todavía**, por indicación
expresa del usuario. La ISO propia encontrada se identificó localmente; no se
configura para arranque ni se publica. Configuración y comprobaciones finales
del entorno se registran en `local/preparacion/`.

## Qué contiene Git y qué se conserva localmente

| En el repositorio | Fuera de Git, en este equipo |
|---|---|
| Plan, guías y cuadernos de código para cuatro personas | Muestras originales y derivados |
| Informe, matriz y seis PDFs de fuentes públicas | Proyecto Ghidra y respuestas MCP |
| Scripts y edición didáctica de funciones seleccionadas | Exportaciones originales MCP/C y evidencias |
| Manifiestos con URL, versión y SHA-256 | Paquetes de herramientas en descargas/ |
| Configuración Vagrant y verificadores | ISO Windows, ISO herramientas, box y discos |

El AGENTS.md prohíbe incorporar muestras, claves, evidencias reales o discos a
Git, aunque el repositorio sea privado. Clonar no entrega esos materiales.
Los datos previos de laboratorio sin respaldo no se reutilizan como evidencia.

## Descargas reproducibles

```bash
bash scripts/download.sh
sha256sum -c config/SHA256SUMS
```

Se mantienen las versiones fijadas y los hashes originales. La descarga incluye
Ghidra PUBLIC para Windows, JDK 25, Sysinternals, FLOSS, Wireshark y WinPmem RC2;
Volatility 3 queda en `descargas/volatility3` con el commit fijado. Es opcional
para este alcance estático: no se declara preparado su entorno Python dentro
de Windows ni una captura de RAM. La procedencia del Ghidra DEV del anfitrión
está separada en `config/ghidra-mcp-host.lock.json`.

Si una URL mutable cambia y falla el hash, detener esa descarga y documentar
la nueva procedencia en un manifiesto complementario. No alterar silenciosamente
`config/descargas.lock.json` ni los PDFs.

## DVD local de herramientas y lectura

```bash
bash scripts/build-tools-iso.sh
```

Genera `local/herramientas.iso`, sin autorun, con:

- los seis paquetes Windows fijados;
- los seis PDFs públicos y sus manifiestos;
- guías vigentes, plan, informe y matriz;
- exportaciones de texto disponibles de Ghidra, sin muestras ejecutables;
- `INVENTARIO.json` con tamaño y SHA-256 de cada archivo.

Las herramientas se encuentran en `descargas/` dentro del DVD, las guías en
`docs/` y las lecturas en `local/decompilados-ghidra/`. Los ejecutables que
incluye el DVD son herramientas oficiales verificadas; no se incluye WannaCry.
El SHA-256 del DVD queda junto a él. Leer o instalar herramientas en el invitado
sigue siendo una comprobación pendiente; descargar no equivale a instalar.

Para regenerar una exportación seleccionada cuando Ghidra/MCP esté abierto:

```bash
local/ghidra/herramientas/pyghidra-mcp/.venv/bin/python scripts/exportar-decompilados.py
```

Crea una carpeta fechada bajo `local/exportaciones-ghidra/` con 16 funciones,
respuestas originales y hashes; identifica programas por SHA-256. El DVD toma
la colección de lectura conservada en `local/decompilados-ghidra/` y el suplemento
PlayGame de `local/ec1383-detalle/`, no sobrescribe esas exportaciones previas.

## Registro VirtualBox separado del usuario

Se encontraron comparticiones globales en el perfil habitual de VirtualBox.
El laboratorio utiliza su propio registro en `local/virtualbox/` y un identificador
IPC exclusivo del proyecto. Se mantienen intactas las comparticiones y VMs ajenas.
Ambos parámetros importan: cambiar solo VBOX_USER_HOME puede reutilizar un
servidor VBoxSVC ya abierto con otro perfil.

Usar siempre estos accesos para el laboratorio:

```bash
./lab status
./scripts/vbox-lab.sh list vms
./scripts/vbox-lab.sh --gui
python3 scripts/check_isolation.py
```

La GUI habitual puede no mostrar estas VMs: abrir la del proyecto con el comando
anterior. No cambiar a NAT ni añadir comparticiones para solucionar la visibilidad.
El registro separado evita heredar configuración, no constituye una barrera
adicional frente a vulnerabilidades del hipervisor.

Referencia: [Oracle, archivos de configuración](https://docs.oracle.com/en/virtualization/virtualbox/7.1/user/TechnicalBackground.html).

La base y la box contienen hardware vacío, no Windows. La configuración prevista
es 2 CPU, 4096 MiB y disco dinámico de 64 GiB, con ocho NIC deshabilitadas, sin
comparticiones, portapapeles, arrastrar/soltar, USB ni VRDE. La VM de trabajo quedó
apagada, con el DVD conectado y sin medio Windows en SATA 1. Se comprobó el
arranque de hardware vacío y se apagó; no se inició el instalador. Debe permanecer
apagada mientras la instalación esté aplazada. Los discos están en `local/vms/`.

Cuando el usuario decida instalar Windows, registrar la ruta propia en
`local/settings.json` con `windows_iso`, y seguir [laboratorio.md](laboratorio.md).
Por ahora ese campo está ausente. No ejecutar `create-base.sh` sobre una base
ya creada; el script rechaza esa situación para preservar sus discos.

## Comprobaciones

```bash
python3 -m unittest discover -s tests -v
./lab validate
python3 scripts/check_isolation.py
python3 scripts/verificar_caso_nist.py
```

Los primeros verifican código/configuración; el tercero inspecciona el estado
real de la VM en el perfil del proyecto; el último comprueba integridad y
referencias NIST. Ninguno acredita instalación de Windows, ejecución de malware
ni recuperación hospitalaria.
