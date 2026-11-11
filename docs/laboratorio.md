# Laboratorio Windows 10 con Vagrant y VirtualBox

## Estado y diseño

Se parte de una box **vacía**, creada localmente: no es una distribución de
Windows preinstalada. Vagrant controla el ciclo de vida; la consola de VirtualBox
permite instalar Windows sin WinRM ni SSH. La ISO encontrada se registra solo
en `local/settings.json`, excluido de Git. No se necesita compartir la licencia.

La ISO detectada corresponde a Windows 10 x64, versión 1903, español.
Esto no reproduce automáticamente los sistemas del NHS ni acredita
vulnerabilidad a MS17-010. Es una estación inicial para practicar forense.

```text
Anfitrión Linux
  └─ Vagrant / VirtualBox
       └─ forense-nhs-win10
            ├─ Windows 10 propio, disco dinámico 64 GiB
            ├─ DVD instalador (ISO local)
            ├─ DVD herramientas (solo lectura)
            └─ 8 adaptadores de red deshabilitados
```

## Primera instalación

1. Ejecuta `./lab up` y abre la consola de `forense-nhs-win10` en VirtualBox.
2. Completa el instalador: selecciona la edición correspondiente a tu licencia,
   instalación personalizada y el disco vacío de 64 GiB de **esta VM**.
3. Crea una cuenta local, sin añadir cuentas de trabajo ni datos personales.
   Introduce la clave solo dentro del instalador si corresponde.
4. Cuando Windows termine, copia los archivos del DVD `NHS_TOOLS` a
   `C:\Forense\Herramientas`. La letra de unidad puede variar.
5. Descomprime Ghidra, el JDK, Sysinternals y FLOSS. Usa una ruta corta sin espacios
   innecesarios. Conserva los archivos de licencia incluidos.
6. Define `JAVA_HOME` con la carpeta extraída del JDK 25 y abre `ghidraRun.bat`.
   En Ghidra puedes indicar el JDK cuando lo solicite. No requiere Internet.
7. Instala Wireshark desde el DVD si vas a revisar PCAP. La captura en vivo requiere
   su controlador Npcap y su instalación dentro del invitado; aún no se validó.
8. Abre Process Monitor, Process Explorer y Autoruns para comprobar que funcionan.
   Configura Sysmon únicamente dentro de esta VM si vas a registrar actividad:

   ```powershell
   # PowerShell como administrador; ajusta la ruta donde descomprimiste la suite.
   C:\Forense\Herramientas\Sysinternals\Sysmon64.exe -accepteula -i C:\Forense\Herramientas\sysmon-lab.xml
   ```

9. Apaga Windows desde Inicio. Ejecuta:

   ```bash
   ./lab snapshot save limpio-herramientas
   python3 scripts/check_isolation.py
   ```

No se ha probado todavía la compatibilidad de cada herramienta dentro de esta
edición antigua de Windows. WinPmem incluido es una **versión candidata (RC2)**:
prueba primero la adquisición de RAM en una sesión limpia y registra fallos de
controlador. Descargarlo no significa que se haya validado una captura.

## Comandos de uso

```bash
./lab status
./lab up
./lab suspend
./lab resume
./lab snapshot list
python3 scripts/check_isolation.py
```

Usa `./lab` en lugar de `vagrant`: activa `none_communicator`, función
experimental incluida en Vagrant 2.4.9. No instala plugins de terceros.
El comunicador `none` no ejecuta comandos dentro de Windows: no hay
aprovisionamiento remoto, `ssh` ni apagado ordenado por ese canal. Apaga desde
Windows. `./lab halt --force` equivale a cortar la energía y puede perder evidencia.

En su log, Vagrant muestra inicialmente `Adapter 1: nat`, pero la personalización
`pre-boot` lo deshabilita antes de encender el invitado. Comprueba siempre el
estado real con el verificador, especialmente después de cambiar la configuración.
La reanudación de una VM guardada conserva su configuración previa.

Una snapshot sirve para volver a una práctica limpia; **no sustituye** la
adquisición forense ni la cadena de custodia. Antes de restaurarla, preserva las
evidencias fuera del disco que vas a revertir.

## Reconstrucción en otro equipo Linux

Necesitas Git, Python 3, Ruby/Vagrant 2.4.9 y VirtualBox 7.2 compatibles, unos
40 GiB libres para crecer y una ISO Windows 10 x64 propia.

```bash
git clone https://github.com/leonidas854/forense_nist_nhs.git
cd forense_nist_nhs
bash scripts/download.sh
export WIN10_ISO='/ruta/a/Windows10.iso'
bash scripts/create-base.sh
bash scripts/build-tools-iso.sh
./lab up
python3 scripts/check_isolation.py
```

Mantén `WIN10_ISO` exportada durante esa sesión o guarda la ruta en
`local/settings.json` con la forma `{"windows_iso":"/ruta/a/Windows10.iso"}`.
La box queda registrada como `nhs/windows10-installer` y no contiene el sistema.
`create-base.sh` rehúsa sobrescribir una VM base existente. Si falla a mitad,
inspecciona la VM y los archivos antes de repetir; no borres discos con datos.

`download.sh` descarga versiones fijadas y verifica los hashes. Si una URL
mutable (como Sysinternals Suite) cambió, falla la comparación: revisa la nueva
publicación y actualiza deliberadamente el manifiesto, sin omitir la verificación.

La ISO de herramientas se vuelve a montar al arrancar con `./lab up` cuando la
VM está apagada. Para sacar evidencias, utiliza un disco de evidencias dedicado
y desconéctalo con la VM apagada; trabaja sobre una copia montada en solo lectura
en una estación de análisis. No habilites carpetas compartidas como atajo.

Para reconstruir el entorno local de Volatility después de clonar:

```bash
python3 -m venv local/analysis-env
local/analysis-env/bin/python -m pip install -r config/volatility-requirements.txt
local/analysis-env/bin/python descargas/volatility3/vol.py --help
```

Para revisar las afirmaciones documentales con SISIFO, si está instalado:

```bash
bash scripts/extract-sources.sh
sisifo verificar
```

## Alcance pendiente

- Instalación/activación de Windows y validación de herramientas en el invitado.
- Selección y adquisición documentada de muestra o dataset; no se descargó malware.
- Para MalwareBazaar, la API exige una Auth-Key, que no se ha proporcionado para
  este trabajo. No guardes claves en Git. [Documentación oficial](https://bazaar.abuse.ch/api/).
- Un dataset puede exigir cuenta o aceptar condiciones de acceso. No se presenta
  la documentación histórica como si fuera un volcado del NHS.
- FTK Imager no forma parte de la descarga realizada. Se usa WinPmem como opción
  de adquisición de RAM; la adquisición de disco necesita su propio procedimiento.
- El laboratorio actual sin red sirve para análisis estático y artefactos locales;
  un ejercicio de tráfico entre VMs requiere otra topología documentada y revisada.

Referencias técnicas: [personalización VirtualBox en Vagrant](https://developer.hashicorp.com/vagrant/docs/providers/virtualbox/configuration),
[creación de boxes](https://developer.hashicorp.com/vagrant/docs/boxes/base),
[comunicador none de Vagrant](https://github.com/hashicorp/vagrant/blob/v2.4.9/plugins/communicators/none/plugin.rb).
