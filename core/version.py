"""Fuente unica de verdad para el numero de version (Fase 12 del roadmap
de instalador). Se usa en el menu, en el .exe (tools/version_info.txt) y
en el instalador (installer/teclazo_rd.iss) - si se cambia aqui, hay que
actualizar esos dos archivos tambien (no se generan automaticamente).

Esquema: v0.x.x desarrollo, v0.5.x beta, v1.0.0 primera version estable.
20 niveles + 10 modos de juego + persistencia + sonido/efectos ya
cumplen ese criterio, por eso arranca en 1.0.0 en vez de 0.1.0.
"""
VERSION = "1.0.1"
