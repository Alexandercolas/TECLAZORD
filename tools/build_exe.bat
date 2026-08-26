@echo off
REM Genera un ejecutable independiente de Windows en dist\TeclazoRD\.
REM No requiere que quien lo reciba tenga Python instalado.
REM
REM --contents-directory . pone los assets junto al .exe en vez de
REM dentro de una subcarpeta _internal (asi el codigo, que usa rutas
REM relativas como "assets/sounds/..." y "data/...", no necesita cambios).

cd /d "%~dp0\.."

python -m pip install --quiet pyinstaller
if errorlevel 1 goto :error

python -m PyInstaller --name TeclazoRD --onedir --windowed --contents-directory . --add-data "assets;assets" --noconfirm main.py
if errorlevel 1 goto :error

echo.
echo Listo. El ejecutable esta en dist\TeclazoRD\TeclazoRD.exe
echo Para compartirlo, comprime toda la carpeta dist\TeclazoRD (no solo el .exe).
goto :eof

:error
echo.
echo La build fallo. Revisa el mensaje de error de arriba.
exit /b 1
