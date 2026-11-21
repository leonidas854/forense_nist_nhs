# Suplemento: intento controlado bloqueado por protección de Windows

**Fecha:** 21 de noviembre de 2026. **Alcance:** intento de apertura de una
muestra conocida en un clon enlazado desechable. No es una detonación efectiva,
una captura del NHS ni una prueba de que el código de WannaCry se ejecutara.

## Pregunta y resultado

Se intentó determinar si la muestra 24d004… podía abrirse en una copia aislada
de Windows 10 y registrar su actividad de red. Windows PowerShell devolvió al
invocar el archivo: «No se pudo completar la operación porque el archivo
contiene un virus o software potencialmente no deseado». El mensaje es
compatible con un bloqueo antimalware de Windows, pero no se consultó el registro
de Defender para identificar motor, firma o evento. No se desactivó Defender,
no se creó una exclusión, no se elevó el proceso y no se intentó eludir el
bloqueo.

El resultado observado permite afirmar **bloqueo de apertura**. No permite
afirmar cifrado, creación de servicio, persistencia, escaneo de SMB, propagación
ni ejecución de otra carga. No se obtuvo evidencia de que el proceso malicioso
se iniciara. La lectura/hash desde Windows también recibió un error de
protección; el SHA-256 se
comprobó de forma independiente en el anfitrión antes de preparar el medio.

## Procedencia e identificación

La página de Malware-Traffic-Analysis.net identifica el hash de la muestra y
describe la captura de tráfico asociada como procedente de una LAN de prueba de
terceros. El paquete se descargó desde el enlace de archivo que ofrece esa
entrada. La misma página no relaciona el tráfico con el NHS.

| Objeto | Identificación observada |
|---|---|
| ZIP obtenido de la fuente | SHA-256 `966d59fa4b372b82ba75681be548ccf8340ec225e1b8199e47a277316d73653e` |
| EXE extraído | 3.723.264 bytes; SHA-256 `24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c` |
| ISO óptico preparado para el clon | SHA-256 `cf5f5a66bfe006ea9d8edd897c1aa87941257cba77ff646ffa2b4373f0dff4c7` |
| PCAP de nictrace | SHA-256 `66fc0bc2fd656f6cef3409451671d86dde2cb691de256473d82019ba6a4836f8` |

Fuente: Szili, D. (2017, 18 de mayo), *PCAP of WannaCry spreading using
EternalBlue*, publicado en Malware-Traffic-Analysis.net. La página informa el
hash `24d004…` para la muestra y la describe como el binario lanzado en su
entorno de prueba. [Entrada y metadatos](https://www.malware-traffic-analysis.net/2017/05/18/index2.html).

## Entorno y aislamiento

- Se utilizó `forense-nhs-wcry-prueba-20261121`, clon enlazado de
  `forense-nhs-win10-copia`, tomado desde su snapshot `antes-practica-benigna-20261120`.
- La VM original «Windows 10» y la copia base permanecieron apagadas. Tras la
  prueba se verificó que la copia base conserva sus ocho NIC en `none`, sin
  comparticiones, portapapeles, USB ni VRDE.
- El clon tuvo una sola NIC en una red interna VirtualBox con nombre único.
  Las otras siete NIC estaban desactivadas. No hubo NAT, puente, host-only,
  gateway ni DNS; no se conectó otro invitado al segmento.
- Windows mostró interfaz Ethernet con IPv4 `169.254.106.134`, sin puerta de
  enlace predeterminada ni DNS.
- El EXE se ofreció desde un ISO óptico. Las carpetas compartidas, USB,
  portapapeles, transferencia por portapapeles, drag-and-drop y VRDE estuvieron
  desactivados. `nictrace` registró el adaptador virtual.
- El primer intento mediante ruta larga no creó un proceso: la imagen ISO
  expuso el nombre del archivo truncado en el invitado. El intento con el
  manejador de Windows sobre el EXE visible produjo el mensaje de bloqueo de
  Defender. No se desactivó la protección.
- Se apagó el invitado, se preservó el expediente local y se eliminó únicamente
  el clon desechable. La VM original y la copia base no se alteraron.

## Lectura de la captura

TShark (Wireshark) 4.7.4 informó 100 paquetes Ethernet, 15.146 bytes y una
duración de 449,225006 segundos. Los filtros reproducidos sobre el PCAP dieron:

| Filtro | Tramas |
|---|---:|
| `tcp` | 0 |
| `tcp.port == 445` | 0 |
| `dns` | 0 |
| Disector `smb` | 4 |
| `udp.port == 138` | 4 |

Las cuatro tramas que Wireshark etiqueta `smb` corresponden a anuncios NetBIOS
por datagramas UDP/138; no son sesiones SMB sobre TCP/445 ni evidencia de
explotación. El resto del tráfico observado consiste en DHCP, IPv6 y protocolos
de descubrimiento local de Windows. Dado que Defender bloqueó la apertura y no
se obtuvo evidencia de proceso, estos paquetes no se atribuyen a WannaCry.

VirtualBox guardó los tiempos absolutos del PCAP en 1969. Esa marca de tiempo es
inválida para cronología forense. La duración y el orden de tramas pueden
describirse con esta limitación, pero no se usa la hora absoluta ni se intenta
corregirla retrospectivamente. La captura tampoco puede probar propagación: no
había un segundo sistema en la red interna.

Los comandos de revisión usados en el anfitrión fueron:

```bash
capinfos local/wannacry-detonacion/capturas/wannacry-live.pcap
tshark -r local/wannacry-detonacion/capturas/wannacry-live.pcap -Y tcp -T fields -e frame.number
tshark -r local/wannacry-detonacion/capturas/wannacry-live.pcap -Y 'tcp.port == 445' -T fields -e frame.number
tshark -r local/wannacry-detonacion/capturas/wannacry-live.pcap -Y dns -T fields -e frame.number
```

## Interpretación forense y NIST

Conforme a la lógica de SP 800-86, se registraron la fuente, los hashes, el
entorno, la acción intentada, el error observado, la captura y los límites de
la conclusión. La adquisición de la muestra desde un portal público no
establece cadena de custodia previa ni procedencia hospitalaria. Se preservan
separadas la observación de laboratorio, el PCAP externo y los hechos históricos
del NHS.

Como mapeo retrospectivo y limitado, el aislamiento de red se relaciona con
CSF 2.0 `PR.IR-01`; la lectura del evento y de la captura se relaciona con
`RS.AN-03`. Estos códigos sirven para organizar el análisis académico, no para
declarar cumplimiento, efectividad general de controles ni resultados del NHS.

Para explicar el comportamiento que no pudo observarse localmente, se recurre a
las funciones estáticas de Ghidra y a la captura externa de terceros asociada
por su fuente al mismo hash. Cada afirmación sobre ejecución, cifrado, servicio,
kill switch o escaneo de SMB debe seguir etiquetada como estática o externa; no
como resultado de esta VM.

## Ubicación de los registros

Los archivos originales y capturas permanecen en `local/wannacry-detonacion/`,
excluido de Git: ZIP, EXE, ISO, PCAP, capturas de pantalla y salida de TShark.
Los hashes de las capturas están en `local/wannacry-detonacion/resultado-analisis.txt`.
No se agregan muestras, PCAP, discos ni capturas del invitado al repositorio.
