; 🍭 Fililico - Inno Setup Script
; Configuration pour l'installateur Windows

#define MyAppName "Fililico"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Marill Dev"
#define MyAppURL "https://github.com/marill-dev/fililico"
#define MyAppExeName "Fililico.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
AppId={{E3F8A1B2-4C5D-6E7F-8901-ABCDEF123456}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; Output settings
OutputDir=..\build\installers
OutputBaseFilename=Fililico-{#MyAppVersion}-Setup
SetupIconFile=..\assets\images\logo.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
; Branding
WizardSmallImageFile=..\assets\images\logo.bmp
; Requirements
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "contextmenu"; Description: "Ajouter au menu contextuel (clic droit)"; GroupDescription: "Intégration système:"

[Files]
Source: "..\dist\Fililico.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\web\*"; DestDir: "{app}\web"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
; Menu contextuel pour tous les fichiers images et PDF
Root: HKCU; Subkey: "*\shell\Fililico"; ValueType: string; ValueName: ""; ValueData: "🍭 Ajouter un filigrane"; Tasks: contextmenu
Root: HKCU; Subkey: "*\shell\Fililico"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\{#MyAppExeName}"; Tasks: contextmenu
Root: HKCU; Subkey: "*\shell\Fililico\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""; Tasks: contextmenu

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    // Nettoyer les clés de registre
    RegDeleteKeyIncludingSubkeys(HKEY_CURRENT_USER, '*\shell\Fililico');
  end;
end;
