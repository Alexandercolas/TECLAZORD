"""Resuelve rutas de la aplicacion sin asumir un directorio de trabajo
concreto (Fase 1 del roadmap de instalador: el juego no debe asumir que
corre desde la carpeta del proyecto).

Separa dos conceptos distintos:
- "base dir": donde viven el codigo y los assets empaquetados (de solo
  lectura una vez instalado - ej. dentro de Program Files).
- "user data dir": donde el JUGADOR guarda su progreso (debe ser
  escribible sin permisos de administrador, y sobrevivir a una
  reinstalacion o actualizacion - Fase 6).
"""
import os
import sys

APP_NAME = "TeclazoRD"


def is_frozen():
    """True cuando corre empaquetado (PyInstaller), no como 'python main.py'."""
    return getattr(sys, "frozen", False)


def get_base_dir():
    """Carpeta del ejecutable empaquetado, o la raiz del proyecto si se
    corre desde codigo fuente."""
    if is_frozen():
        return os.path.dirname(sys.executable)
    # Este archivo vive en <raiz_del_proyecto>/core/paths.py
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_asset_path(*parts):
    return os.path.join(get_base_dir(), "assets", *parts)


def get_user_data_dir():
    """Carpeta de datos del jugador, separada de los archivos del programa.

    - Empaquetado (instalado): %LOCALAPPDATA%\\TeclazoRD (Windows) o
      ~/.local/share/TeclazoRD (otros SO), para no depender de permisos
      de escritura dentro de la carpeta de instalacion.
    - Corriendo desde codigo fuente: la carpeta data/ del proyecto, como
      hasta ahora, para no complicar el flujo de desarrollo/pruebas.
    """
    if not is_frozen():
        return os.path.join(get_base_dir(), "data")

    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    else:
        base = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
    return os.path.join(base, APP_NAME)


def get_user_data_path(filename):
    directory = get_user_data_dir()
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, filename)
