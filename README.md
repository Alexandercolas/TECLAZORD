# TECLAZO RD

"De tecla en tecla, se aprende."

Videojuego local de entrenamiento de mecanografia, 100% offline (sin
internet, servidores ni cuentas). Ver `TECLAZO_RD_Documento_Maestro.docx`
para el diseño completo.

Estado actual: **Niveles 1-20 jugables** (los 10 del documento maestro
mas 10 adicionales de una extension personalizada de ingenieria en
sistemas en ingles, seccion propia mas abajo) mas **10 modos de juego
adicionales** (Practica libre, Modo Errores, Modo Examen, Modo Numpad,
Modo Versus, Contrarreloj, Supervivencia, Leaderboard, Estadisticas,
Logros), con desbloqueo progresivo, teclado visual, XP, sonido, efectos
y configuracion (Fases 1-6 del documento maestro completas, mas la
seccion 16 de modos de juego y la seccion 27 de expansiones).

## Requisitos

- Python 3.10+

## Instalacion

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecutar el juego

```bash
python main.py
```

Controles: escribe el texto que aparece en pantalla (`ENTER` para saltos
de linea en el Nivel 8). `ESC` para volver al menu/seleccion de nivel,
`BACKSPACE` para corregir. En el menu: `E` Mis Estadisticas, `L` Logros,
`P` Entrenamiento personalizado (Modo Errores: genera ejercicios con las
teclas que mas fallas, una vez que hayas jugado algunos niveles), `R`
Leaderboard local (mejor WPM por nombre), `X` Modo Examen (un texto largo
y continuo de 60s, con certificado al final), `N` Modo Numpad dedicado
(solo cuentan las teclas fisicas del teclado numerico, no la fila
superior), `V` Modo Versus (duelo local por turnos: cada jugador escribe
el mismo texto por separado y se compara el resultado), `F` Practica
libre (elige categoria: letras, numeros, simbolos, numpad, codigo u
oficina), `T` Contrarreloj (maxima velocidad en 30/60/120s, ejercicios
mezclados que se reciclan si terminas antes de tiempo), `S` Supervivencia
(el texto no para; si tu precision cae de 80% es GAME OVER), `A` Modo
Aleatorio (elige al azar entre un nivel desbloqueado o cualquier modo
especial), `C` Configuracion (sonido on/off, volumen, cambiar tu nombre
para el leaderboard).

## Niveles 11-20: extension de ingenieria en sistemas (fuera del documento maestro)

A pedido del usuario, mas alla de los 10 niveles originales. Cambia de
formato: las frases **caen de arriba hacia abajo** en vez de quedarse
quietas, y si una frase llega al piso sin completarse cuenta como error
y pasa a la siguiente (el nivel sigue, no es GAME OVER instantaneo).
Al completar una frase entera sin ningun error, suena un "chasquido"
distinto del clic de cada tecla.

- Contenido mayormente en ingles, tematica de informatica / ingenieria
  en sistemas, con dificultad progresiva por nivel:

  | Nivel | Tema |
  |---|---|
  | 11 | IT Basics (vocabulario suelto) |
  | 12 | Networking |
  | 13 | Programming Basics |
  | 14 | Databases |
  | 15 | Web Development |
  | 16 | Cybersecurity |
  | 17 | Operating Systems |
  | 18 | Cloud and DevOps |
  | 19 | Algorithms and Data Structures |
  | 20 | Systems Engineer Final Challenge (oraciones completas, mezcla todo) |

- La velocidad de caida es proporcional al largo de cada frase (no un
  tiempo fijo), y se acelera progresivamente del Nivel 11 al 20.
- Se desbloquean igual que los niveles 1-10 (puntuacion minima en el
  nivel anterior).
- Pendiente, si se pide despues: mas idiomas de codigo (JavaScript,
  SQL, HTML) ademas de la sintaxis tipo Python ya usada en el Nivel 8.

## Compartirlo con otros (ejecutable de Windows)

Para que alguien lo juegue sin instalar Python ni nada:

```bash
tools\build_exe.bat
```

Genera `dist\TeclazoRD\TeclazoRD.exe`. **Comprime toda la carpeta**
`dist\TeclazoRD` (no solo el .exe) y comparte el .zip — el ejecutable
necesita los archivos de al lado (assets de sonido, dependencias de
Python empaquetadas) para funcionar.

El progreso de cada persona **no** se guarda junto al `.exe` — se
guarda en `%LOCALAPPDATA%\TeclazoRD\` (ver seccion de arquitectura mas
abajo). Esto es a proposito: si algun dia el juego se instala en
`C:\Program Files\`, esa carpeta normalmente no se puede escribir sin
permisos de administrador, y ahi es exactamente donde NO debe vivir el
progreso del jugador.

## Arquitectura: rutas y datos del jugador

`core/paths.py` es el unico lugar que decide donde viven las cosas — el
resto del codigo nunca asume su propio directorio de trabajo (ni para
cargar assets, ni para guardar progreso):

- **Corriendo desde codigo fuente** (`python main.py`): igual que
  siempre, todo se guarda en `data/` dentro del proyecto.
- **Empaquetado** (`.exe` generado con PyInstaller): el progreso se
  guarda en `%LOCALAPPDATA%\TeclazoRD\` (Windows) o
  `~/.local/share/TeclazoRD` (otros SO) — nunca junto al `.exe` ni
  dentro de la carpeta de instalacion. Los assets (sonidos) se resuelven
  contra la carpeta del propio ejecutable, no contra el directorio
  desde el que se lo haya lanzado (un acceso directo con un "Iniciar
  en" distinto no rompe nada).

Esto es preparacion explicita para una futura instalacion en
`C:\Program Files\`, donde escribir junto al programa normalmente
requiere permisos de administrador — y es justo donde el progreso del
jugador NO debe vivir, para que una actualizacion o reinstalacion no lo
borre.

## Ejecutar las pruebas

```bash
pytest
```

## Estructura del proyecto

```
main.py            Punto de entrada
config/settings.py Configuracion (colores, ventana, formula de puntuacion)
core/paths.py       Resuelve rutas de assets y datos (ver seccion de arquitectura)
core/               Motor: timer, entrada de texto, puntuacion, progreso
levels/             Definicion de cada nivel (ejercicios, tiempo limite)
systems/            Persistencia en JSON
ui/                 Pantallas (menu, partida, resultados)
data/               Progreso del jugador SOLO en modo desarrollo (ver arquitectura)
tests/              Pruebas de la logica pura (sin Pygame)
assets/sounds/      Efectos de sonido (.wav, generados con tools/generate_sounds.py)
tools/              Herramientas de desarrollo (no se ejecutan en el juego)
```

Los sonidos son sintetizados por codigo (sin bancos de sonido externos,
para mantener el proyecto 100% local). Para regenerarlos o ajustarlos:

```bash
python tools/generate_sounds.py
```

## Progreso segun el plan de fases

- [x] Fase 1: ventana, entrada de teclado, texto, temporizador, WPM, precision, errores
- [x] Fase 2: Niveles 1-3, seleccion de nivel, sistema de progreso, guardado, pantalla de resultados
- [x] Fase 3: Niveles 4-6 (numeros, oficina, simbolos), teclado visual con resaltado de tecla
- [x] Fase 4: Niveles 7-10 (trabajo, codigo, avanzado, final), records por nivel (WPM/precision/tiempo/combo), pantalla de estadisticas, sistema de XP
- [x] Fase 5: sistema de logros (6 logros, pantalla dedicada), entrenamiento inteligente (deteccion de teclas mas falladas + generacion dinamica de ejercicios en el Modo Errores)
- [x] Fase 6: efectos de sonido tipo accion/militar (clic al escribir, error, victoria, derrota, logro, navegacion), transiciones con fundido entre pantallas, destello al fallar una tecla, popup animado de combo, pantalla de Configuracion (sonido on/off, volumen)
- [x] Expansion (seccion 27): Leaderboard local por nombre (mejor WPM), Modo Examen (prueba unica de 60s con certificado)
- [x] Modo Numpad dedicado (seccion 17): detecta teclas fisicas del Numpad (K_KP_*) via core/keymap.py, penaliza usar la fila superior
- [x] Modo Versus - 2 jugadores en un solo teclado (seccion 27): duelo por turnos (no simultaneo), mismo texto para ambos, pantalla de resultado con ganador, alimenta el leaderboard local
- [x] Modos de juego completos (seccion 16): Practica libre (6 categorias, reutiliza contenido de niveles), Contrarreloj (30/60/120s, ejercicios mezclados que se reciclan), Supervivencia (sin limite de tiempo fijo, termina en GAME OVER si la precision cae de 80%)
- [x] Modo Aleatorio: elige al azar entre un nivel desbloqueado o cualquier modo especial (reutiliza los metodos existentes, sin logica nueva)
- [x] Orden aleatorio de ejercicios en Practica Libre y Modo Numpad (decision del usuario: la campana de 10 niveles mantiene su orden fijo a proposito, para no romper la rampa de dificultad "empezar facil, terminar dificil" que pide el documento dentro de cada nivel)
- [ ] Fuera de alcance por ahora: temas visuales alternativos (el usuario confirmo que el esquema amarillo/negro actual esta bien), Modo oficina y Modo programacion multi-lenguaje como modos separados (ya cubiertos por las categorias existentes de Practica Libre y por el Nivel 8/5/7, pero sin JavaScript/SQL/HTML como pide la seccion 27)

## Roadmap de instalador (aparte del documento maestro)

Preparacion para convertir TECLAZO RD en una aplicacion instalable de
Windows de verdad (no solo un `.exe` en una carpeta):

- [x] Fase 1 (rutas/assets/CWD) + Fase 6 (datos del jugador separados
  del programa): `core/paths.py`, ver seccion de arquitectura arriba
- [x] Fase 4 (PyInstaller -> `.exe`): `tools/build_exe.bat`
- [ ] Fase 2: reorganizar todo bajo una carpeta `app/` (reestructuracion
  grande, no bloquea nada de lo demas — pendiente de decidir si vale la pena)
- [ ] Fase 3: icono oficial (`.ico`) para el exe/ventana/accesos directos
- [ ] Fase 7-10: instalador real (asistente, Program Files, acceso
  directo, entrada en Menu Inicio, desinstalador con opcion de
  conservar datos)
- [ ] Fase 11-12: metadata de Windows en el exe (version, editor,
  descripcion) y numero de version (`v0.1.0` etc.)
- [ ] Fase 14-16: prueba de que una actualizacion no borra el progreso,
  build automatico (tests -> build -> instalador), carpeta `release/`

Decision explicita: no se construye el instalador todavia. Se
resolvieron primero las decisiones de arquitectura (Fase 1 y 6) porque
son caras de cambiar despues; el resto se retoma cuando se pida.
