@echo off
REM Flujo completo de release (Fase 15 del roadmap de instalador):
REM   pruebas -> ejecutable -> instalador -> release\TECLAZO_RD_Setup_vX.X.X.exe
REM
REM No genera nada si los tests fallan.

cd /d "%~dp0\.."

echo === 1/3: Corriendo las pruebas ===
python -m pytest -q
if errorlevel 1 (
    echo.
    echo Los tests fallaron. No se genera ningun build hasta que pasen.
    exit /b 1
)

echo.
echo === 2/3: Generando el ejecutable ===
call tools\build_exe.bat
if errorlevel 1 exit /b 1

echo.
echo === 3/3: Generando el instalador ===
set "ISCC="
for %%P in (
    "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
    "%ProgramFiles%\Inno Setup 6\ISCC.exe"
    "%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"
) do (
    if exist %%~P set "ISCC=%%~P"
)
if not defined ISCC (
    echo.
    echo No se encontro Inno Setup ^(ISCC.exe^).
    echo Instalalo con: winget install --id JRSoftware.InnoSetup -e
    echo o descargalo de https://jrsoftware.org/isinfo.php
    exit /b 1
)

"%ISCC%" installer\teclazo_rd.iss
if errorlevel 1 exit /b 1

echo.
echo Listo. Instalador generado en release\
dir /b release\*.exe
