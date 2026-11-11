# WannaCry en el NHS · Laboratorio de informática forense

Repositorio privado de **leonidas854** para estudiar el caso NHS y organizar
evidencias con NIST CSF 2.0. Incluye fuentes oficiales, Vagrant + VirtualBox,
herramientas descargables y plantillas. **No contiene resultados de una infección
real ni una muestra de WannaCry.**

## Empieza aquí

En el equipo donde se preparó el proyecto, la box local ya está registrada:

```bash
cd /home/leonidas/SSD500/Develoment/forense_nist_nhs
./lab up
python3 scripts/check_isolation.py
```

La VM se llama `forense-nhs-win10`. Tiene 4 GiB de RAM, 2 CPU y disco dinámico
de 64 GiB. Arranca el instalador de tu Windows 10; **todavía debes instalar
Windows y las herramientas dentro del invitado**. `Machine booted and ready`
solo indica que VirtualBox encendió la VM, no que Windows esté instalado.
Si ya está encendida sin ventana, usa **Mostrar** en VirtualBox.

Sigue [la guía del laboratorio](docs/laboratorio.md). Para otro equipo, empieza
por la sección de reconstrucción: la box, ISO, discos y herramientas grandes
son locales y no viajan mediante `git clone`.

## Contenido

| Ruta | Uso |
|---|---|
| [BRIEF.md](BRIEF.md) | Alcance acordado y pendientes del docente |
| [docs/laboratorio.md](docs/laboratorio.md) | Windows, herramientas, snapshots y reconstrucción |
| [docs/caso-nhs.md](docs/caso-nhs.md) | Fuentes, correcciones y límites históricos |
| [docs/metodologia.md](docs/metodologia.md) | Ghidra, evidencias y cadena de custodia |
| [docs/matriz-nist.csv](docs/matriz-nist.csv) | Mapeo inicial de las seis funciones |
| [fuentes/README.md](fuentes/README.md) | Cinco PDF oficiales y ediciones |
| [config/descargas.lock.json](config/descargas.lock.json) | URL, tamaño, fecha y SHA-256 de las descargas |
| [plantillas/](plantillas/) | Bitácora, inventario, hallazgos y timeline vacíos |
| [docs/verificacion.md](docs/verificacion.md) | Comprobaciones realizadas y pendientes |

`descargas/` contiene Ghidra, Java, Sysinternals, Wireshark, FLOSS, WinPmem y
el código de Volatility 3. `local/herramientas.iso` permite transferir herramientas
por DVD de solo lectura. `evidencias/` está excluida de Git para los datos del caso.

## Validación

```bash
./lab validate
python3 -m unittest discover -s tests -v
python3 scripts/check_isolation.py
sha256sum -c config/SHA256SUMS
```

El verificador inspecciona la configuración actual; no garantiza que un
hipervisor sea invulnerable. No se habilita NAT, bridge, host-only, carpetas
compartidas, USB, portapapeles, arrastrar/soltar ni escritorio remoto.

## Base documental

El análisis aplica **retrospectivamente** CSF 2.0 al caso, porque el marco se
publicó después del incidente. Se utiliza la edición final de
[NIST IR 8374 Rev. 1](https://csrc.nist.gov/pubs/ir/8374/r1/final),
[CSF 2.0](https://csrc.nist.gov/pubs/cswp/29/the-nist-cybersecurity-framework-csf-20/final)
y los informes institucionales del NHS/NAO (NIST, 2024; National Audit Office, 2018).
Las herramientas conservan sus
licencias originales; la licencia de Windows y su activación corresponden al usuario.
