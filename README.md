# WannaCry en el NHS · Laboratorio y Peritaje Forense con NIST CSF 2.0

Repositorio pericial para el estudio del caso **WannaCry en el National Health Service (NHS)** del Reino Unido (12 de mayo de 2017), desarrollado para la materia de **Informática Forense**. Integra análisis documental oficial (NAO y DHSC 2018), ingeniería inversa estática con Ghidra 12.2, correlación de artefactos de Windows y un mapeo retrospectivo riguroso a **NIST CSF 2.0** (NIST CSWP 29) y su perfil **NIST IR 8374 Rev. 1** (versión final de junio de 2026).

---

## Organización del Proyecto (Equipo de 8 · 2 Expositores)

El proyecto está diseñado para un equipo de **8 estudiantes** con roles periciales definidos y una defensa oral estructurada para **dos expositores principales**:

- **Expositor 1 (Perito Coordinador):** Contexto histórico del NHS, marco legal, cadena de custodia y funciones de prevención de NIST CSF 2.0 (**Govern**, **Identify**, **Protect**).
- **Expositor 2 (Perito Técnico):** Estación de laboratorio aislada, análisis estático en Ghidra 12.2, correlación de evidencias (logs, memoria, disco) y funciones de respuesta (**Detect**, **Respond**, **Recover**).
- **Integrantes 3 al 8 (Especialistas Técnicos):** Respaldo técnico en la matriz RACI, redacción del informe y defensa temática en la ronda de preguntas del tribunal.

---

## Documentación y Entregables Académicos

| Documento | Descripción y Uso | Enlace |
|---|---|:---:|
| **Informe Forense Maestro** | Documento formal definitivo de la materia con citas APA 7 y análisis pericial exhaustivo. | [docs/informe-forense.md](docs/informe-forense.md) |
| **Organización del Equipo de 8** | Matriz RACI, asignación de los 8 roles periciales y bitácora de trabajo colaborativo. | [docs/roles-equipo-8.md](docs/roles-equipo-8.md) |
| **Guion de Exposición (2 Expositores)** | Diálogo estructurado minuto a minuto (24 min de ponencia + 6 min de preguntas) con transiciones. | [docs/guion-exposicion.md](docs/guion-exposicion.md) |
| **Diapositivas de Defensa Oral** | Presentación completa proyectable (compatible con Marp y Markdown) con diagramas y tablas. | [docs/diapositivas.md](docs/diapositivas.md) |
| **Banco de Preguntas del Tribunal** | 20 preguntas difíciles con respuestas fundamentadas en código, comandos y auditorías oficiales. | [docs/preguntas-defensa.md](docs/preguntas-defensa.md) |
| **Matriz NIST CSF 2.0** | CSV detallado con las 6 funciones mapeadas a fuentes históricas, evidencias y roles. | [docs/matriz-nist.csv](docs/matriz-nist.csv) |
| **Guía del Laboratorio Aislado** | Arquitectura de la VM Windows 10, instalación de herramientas por ISO y snapshots. | [docs/laboratorio.md](docs/laboratorio.md) |
| **Metodología Pericial** | Protocolo de Ghidra, Volatility 3, adquisición de RAM con WinPmem y cadena de custodia. | [docs/metodologia.md](docs/metodologia.md) |
| **Caso Histórico NHS** | Auditoría de cifras certificadas (NAO 2018), desmitificación del phishing y precisión de 80 trusts. | [docs/caso-nhs.md](docs/caso-nhs.md) |
| **Fuentes Oficiales y PDFs** | Cinco documentos oficiales primarios (NAO, NHS/DHSC, NIST CSWP 29, IR 8374r1, SP 800-61r3). | [fuentes/README.md](fuentes/README.md) |

---

## Estación de Laboratorio Forense Aislada

La máquina virtual `forense-nhs-win10` (Windows 10 x64, 4 GiB RAM, 64 GiB disco dinámico) opera sobre VirtualBox 7.2 gestionada mediante Vagrant 2.4.9 con aislamiento estricto:

```bash
cd /home/leonidas/SSD500/Develoment/forense_nist_nhs

# Iniciar la estación virtual de trabajo
./lab up

# Verificar aislamiento en tiempo real (8 NICs desactivadas, sin carpetas compartidas)
python3 scripts/check_isolation.py
```

* **Política de Seguridad:** 8 adaptadores de red en modo `none`, comunicador `none_communicator`, portapapeles y Drag & Drop inhabilitados.
* **DVD de Herramientas (`local/herramientas.iso`):** Medio óptico virtual de solo lectura con Ghidra 12.2, OpenJDK 25, Volatility 3, WinPmem RC2 y Sysinternals Suite.

---

## Verificación Automatizada del Proyecto

Para comprobar la integridad del repositorio, la configuración de Vagrant y el aislamiento:

```bash
# 1. Validar sintaxis del laboratorio y comunicador 'none'
./lab validate

# 2. Ejecutar la suite de pruebas unitarias de aislamiento
python3 -m unittest discover -s tests -v

# 3. Comprobar aislamiento del hipervisor
python3 scripts/check_isolation.py

# 4. Validar integridad criptográfica de descargas y herramientas
sha256sum -c config/SHA256SUMS
```

---

## Base Documental y Normativa

- **NIST CSF 2.0 (2024):** *The NIST Cybersecurity Framework 2.0* (NIST CSWP 29). [DOI oficial](https://doi.org/10.6028/NIST.CSWP.29).
- **NIST IR 8374 Rev. 1 (Final, junio 2026):** *Ransomware Risk Management: A CSF 2.0 Community Profile*. [DOI oficial](https://doi.org/10.6028/NIST.IR.8374r1).
- **National Audit Office (NAO, 2018):** *Investigation: WannaCry cyber attack and the NHS* (Report HC 414).
- **Department of Health and Social Care (DHSC, 2018):** *Lessons learned review of the WannaCry ransomware cyber attack*.
- **NIST SP 800-61 Rev. 3 (2025):** *Incident Response Recommendations and Considerations for Cybersecurity Risk Management*.
