### Estación existente incorporada el 20 de noviembre

El usuario confirmó disponer de una VM llamada «Windows 10» y autorizó usar una
copia aislada. La original estaba apagada, con un adaptador NAT, otro puente y
comparticiones globales del perfil habitual. Se realizó una clonación completa,
sin arrancar la original, hacia `local/vms/forense-nhs-win10-copia/`.

La copia se registró en el perfil VirtualBox e IPC privados del proyecto. Antes
del primer arranque se desactivaron los ocho adaptadores, portapapeles,
transferencia de archivos por portapapeles, arrastrar/soltar, USB y VRDE. Se retiró
la ISO de instalación de la copia y se conectó el DVD de herramientas ya existente.
Se creó el snapshot `aislada-antes-de-practica` antes de arrancar.

Se observó el escritorio y se abrió winver: **Windows 10 Pro, versión 1903,
compilación 18362.356**. Las capturas originales quedan en el expediente local,
fuera de Git. Este resultado acredita un sistema instalado en la copia; no una
instalación nueva realizada por el equipo ni una evaluación de sus parches,
licencia, limpieza o herramientas. No se ejecutó WannaCry.

| Objeto | Estado y uso |
|---|---|
| Windows 10, registro habitual | Original conservada; no utilizarla directamente para el caso |
| forense-nhs-win10-copia | Copia aislada con Windows observado; estación para lectura y ejercicios benignos |
| forense-nhs-win10 | VM vacía anterior, conservada y administrada con `./lab` |
| DVD de herramientas | Imagen anterior de 57 archivos; no incorpora automáticamente esta entrega |
| DVD de lectura de esta edición | `local/entrega-nist-lectura.iso`, medio separado con los documentos nuevos |

La copia conserva 4 CPU y 4 GiB de RAM del origen. Se comprobó su estado
apagado tras solicitar el cierre normal desde Windows; los registros permanecen
locales y la síntesis se incluye en `docs/verificacion.md`.
Las herramientas descargadas todavía requieren validación dentro de ese Windows.
El arranque del sistema no sustituye esa prueba.

Para comprobar y abrir la copia desde el anfitrión:

```bash
python3 scripts/check_isolation.py forense-nhs-win10-copia
./scripts/vbox-lab.sh showvminfo forense-nhs-win10-copia
./scripts/vbox-lab.sh startvm forense-nhs-win10-copia --type gui
```

El tercer comando inicia la copia: usarlo solo tras una comprobación correcta.
En el Explorador de Windows, abrir «Este equipo» y el DVD con etiqueta
`NHS_ESTUDIO`; contiene los dos PDF y Word. La letra de unidad puede variar.
La imagen se preparó y comprobó en el anfitrión y se conectó a la copia; no se
declara comprobada la apertura de los informes dentro del invitado.
Para abrir el administrador del registro aislado se puede utilizar
`./scripts/vbox-lab.sh --gui`. `./lab status` sigue consultando la VM vacía
anterior; no debe confundirse su estado con el de la copia. La copia no se adoptó
en los metadatos de Vagrant ni se cambió el significado de la box inicial.

La verificación posterior a esta preparación dio **18 pruebas correctas**, validó
el Vagrantfile y aprobó el aislamiento real tanto de la VM vacía como de la copia.
Esta comprobación evalúa configuración del hipervisor; no certifica ausencia de
escapes o contaminación previa. No se habilitaron comunicaciones para instalar
herramientas ni se distribuyeron discos o datos personales.

### Actualización: práctica benigna realizada

Se ejecutaron comprobaciones de hash, restauración de un texto ficticio y
apertura/cierre de Bloc de notas. La sección 11.4 registra resultados y el
desfase aproximado de cinco horas entre relojes. Se validó el uso de PowerShell
y herramientas integradas, no los paquetes descargados. La copia se apagó al
finalizar y se comprobó el aislamiento; las pruebas del laboratorio son ahora
19, al añadir el control de transferencias por portapapeles. No hubo detonación.
