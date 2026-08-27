# TECLAZO RD

"De tecla en tecla, se aprende."

Videojuego local de entrenamiento de mecanografia, 100% offline (sin
internet, servidores ni cuentas). Ver `TECLAZO_RD_Documento_Maestro.docx`
para el diseño completo.

Estado actual: **Niveles 1-10 jugables** mas **10 modos de juego adicionales** (Practica libre, Modo Errores, Modo Examen, Modo Numpad, Modo Versus, Contrarreloj, Supervivencia, Leaderboard, Estadisticas, Logros), con desbloqueo progresivo, teclado visual, XP, sonido, efectos y configuracion (Fases 1-6 del documento maestro completas, mas la seccion 16 de modos de juego y la seccion 27 de expansiones).

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

## Compartirlo con otros (ejecutable de Windows)

Para que alguien lo juegue sin instalar Python ni nada:

```bash
tools\build_exe.bat
```

Genera `dist\TeclazoRD\TeclazoRD.exe`. **Comprime toda la carpeta**
`dist\TeclazoRD` (no solo el .exe) y comparte el .zip — el ejecutable
necesita los archivos de al lado (assets de sonido, dependencias de
Python empaquetadas) para funcionar. Cada persona que lo use genera su
propia carpeta `data/` junto al .exe con su progreso, nombre y
estadisticas; no se comparte entre instalaciones.

## Ejecutar las pruebas

```bash
pytest
```

## Estructura del proyecto

```
main.py            Punto de entrada
config/settings.py Configuracion (colores, ventana, formula de puntuacion)
core/               Motor: timer, entrada de texto, puntuacion, progreso
levels/             Definicion de cada nivel (ejercicios, tiempo limite)
systems/            Persistencia en JSON
ui/                 Pantallas (menu, partida, resultados)
data/               Progreso guardado del jugador (JSON, no versionado)
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
- [ ] Fuera de alcance por ahora: temas visuales alternativos (el usuario confirmo que el esquema amarillo/negro actual esta bien), Modo oficina y Modo programacion multi-lenguaje como modos separados (ya cubiertos por las categorias existentes de Practica Libre y por el Nivel 8/5/7, pero sin JavaScript/SQL/HTML como pide la seccion 27)
