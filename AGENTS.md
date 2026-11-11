# Contexto del proyecto

- Lee `BRIEF.md` y `docs/verificacion.md` antes de continuar.
- Responde y documenta en español. Es un caso de informática forense sobre
  WannaCry en el NHS con mapeo retrospectivo a NIST CSF 2.0.
- No confundas documentación histórica, hipótesis y observaciones de laboratorio.
- Preserva `config/descargas.lock.json` y hashes; no actualices versiones sin
  documentar procedencia. No modifiques PDFs originales.
- Usa `./lab` para Vagrant. La box inicial contiene hardware vacío, no Windows instalado.
- No habilites redes ni comparticiones por solucionar problemas de comunicación.
- Nunca agregues discos, claves, muestras o evidencias reales a Git. El carácter
  privado del repositorio no cambia esta regla.
- Comprueba `python3 -m unittest discover -s tests -v`, `./lab validate` y el
  estado real con `python3 scripts/check_isolation.py` tras cambiar el laboratorio.
- No declares ejecutada una captura, instalado Windows o validada una herramienta
  dentro del invitado sin evidencia de esa comprobación.
