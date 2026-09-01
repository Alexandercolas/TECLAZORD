; Script de Inno Setup para el instalador de TECLAZO RD (Fases 7-10 del
; roadmap de instalador). Se compila con:
;
;     ISCC installer\teclazo_rd.iss
;
; (o via tools\build_app.bat, que hace todo el flujo completo).
;
; Requiere que ya exista dist\TeclazoRD\ (generado con tools\build_exe.bat).

#define MyAppName "TECLAZO RD"
#define MyAppVersion "1.0.1"
#define MyAppPublisher "TECLAZO RD"
#define MyAppURL "https://github.com/Alexandercolas/TECLAZORD"
#define MyAppExeName "TeclazoRD.exe"

[Setup]
; No cambiar este AppId una vez publicada la primera version: es lo que
; permite que un instalador v1.1.0 reconozca y actualice la v1.0.0 en
; vez de instalarse como programa aparte.
AppId={{EC8AC00B-79F9-48C5-AA5E-D170CA3111C5}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\TECLAZO RD
DefaultGroupName=TECLAZO RD
DisableProgramGroupPage=yes
OutputDir=..\release
OutputBaseFilename=TECLAZO_RD_Setup_v{#MyAppVersion}
SetupIconFile=..\assets\icon\teclazo_rd.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
; Deja elegir "instalar para todos" (necesita admin) o "solo para mi"
; (sin admin) en vez de forzar uno de los dos.
PrivilegesRequiredOverridesAllowed=dialog
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Accesos directos:"; Flags: checkedonce

[Files]
Source: "..\dist\TeclazoRD\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\TECLAZO RD"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,TECLAZO RD}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\TECLAZO RD"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,TECLAZO RD}"; Flags: nowait postinstall skipifsilent

[Code]
// Fase 10: al desinstalar, preguntar explicitamente si conservar o
// borrar el progreso del jugador (vive en %LOCALAPPDATA%\TeclazoRD,
// separado de la carpeta de instalacion - ver core/paths.py).
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  DataDir: String;
  Response: Integer;
begin
  if CurUninstallStep = usUninstall then
  begin
    DataDir := ExpandConstant('{localappdata}\TeclazoRD');
    // En desinstalacion silenciosa (/VERYSILENT, usada por ejemplo al
    // actualizar) no hay nadie para responder el MsgBox: por defecto se
    // CONSERVAN los datos. Solo se pregunta -y solo se puede borrar- en
    // una desinstalacion interactiva normal.
    if DirExists(DataDir) and not UninstallSilent() then
    begin
      Response := MsgBox(
        '¿Deseas conservar tus estadisticas y progreso de TECLAZO RD?' + #13#10 + #13#10 +
        'Si eliges "No", se eliminaran permanentemente.',
        mbConfirmation, MB_YESNO);
      if Response = IDNO then
        DelTree(DataDir, True, True, True);
    end;
  end;
end;
