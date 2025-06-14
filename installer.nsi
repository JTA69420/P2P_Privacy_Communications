; P2P Privacy Communications Installer
; NSIS Script for creating Windows installer/uninstaller

!define APP_NAME "P2P Privacy Communications"
!define APP_VERSION "1.0.0"
!define APP_PUBLISHER "P2P Communications Team"
!define APP_URL "https://github.com/p2p-privacy-comm"
!define APP_EXE "main.py"
!define PYTHON_EXE "python.exe"
!define UNINSTALL_EXE "Uninstall.exe"

; Compression
SetCompressor lzma

; General
Name "${APP_NAME}"
OutFile "P2P_Privacy_Communications_Installer.exe"
InstallDir "$PROGRAMFILES\${APP_NAME}"
InstallDirRegKey HKLM "Software\${APP_NAME}" "Install_Dir"
RequestExecutionLevel admin

; Version information
VIProductVersion "1.0.0.0"
VIAddVersionKey "ProductName" "${APP_NAME}"
VIAddVersionKey "ProductVersion" "${APP_VERSION}"
VIAddVersionKey "CompanyName" "${APP_PUBLISHER}"
VIAddVersionKey "FileDescription" "${APP_NAME} Installer"
VIAddVersionKey "FileVersion" "${APP_VERSION}"
VIAddVersionKey "LegalCopyright" "© 2025 ${APP_PUBLISHER}"

; Interface Settings
!include "MUI2.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Welcome page
!insertmacro MUI_PAGE_WELCOME

; License page
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"

; Components page
!insertmacro MUI_PAGE_COMPONENTS

; Directory page
!insertmacro MUI_PAGE_DIRECTORY

; Instfiles page
!insertmacro MUI_PAGE_INSTFILES

; Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\P2P_Launcher.exe"
!define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\README.md"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Languages
!insertmacro MUI_LANGUAGE "English"

; Sections

Section "Core Application" SEC01
  SectionIn RO
  
  ; Set output path to the installation directory
  SetOutPath "$INSTDIR"
  
  ; Check for Python installation
  nsExec::ExecToLog 'python --version'
  Pop $0
  ${If} $0 != 0
    MessageBox MB_YESNO "Python is not installed or not found in PATH. Do you want to continue anyway?$\n$\nNote: You will need Python 3.7+ to run this application." IDYES continue IDNO abort
    abort:
    Abort
    continue:
  ${EndIf}
  
  ; Copy application files
  File "main.py"
  File "requirements.txt"
  File "README.md"
  File "setup.py"
  File "run.bat"
  File "run.ps1"
  
  ; Create launcher executable
  File "P2P_Launcher.exe"
  
  ; Write the installation path into the registry
  WriteRegStr HKLM "SOFTWARE\${APP_NAME}" "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" '"$INSTDIR\${UNINSTALL_EXE}"'
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayIcon" "$INSTDIR\P2P_Launcher.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "URLInfoAbout" "${APP_URL}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoRepair" 1
  
  ; Create uninstaller
  WriteUninstaller "${UNINSTALL_EXE}"
  
SectionEnd

Section "Python Dependencies" SEC02
  
  SetOutPath "$INSTDIR"
  
  ; Install Python dependencies
  DetailPrint "Installing Python dependencies..."
  nsExec::ExecToLog 'python -m pip install -r "$INSTDIR\requirements.txt"'
  Pop $0
  ${If} $0 != 0
    MessageBox MB_OK "Warning: Failed to install some Python dependencies. You may need to install them manually using:$\npip install -r requirements.txt"
  ${Else}
    DetailPrint "Python dependencies installed successfully."
  ${EndIf}
  
SectionEnd

Section "Desktop Shortcut" SEC03
  
  ; Create desktop shortcut
  CreateShortcut "$DESKTOP\P2P Privacy Communications.lnk" "$INSTDIR\P2P_Launcher.exe" "" "$INSTDIR\P2P_Launcher.exe" 0
  
SectionEnd

Section "Start Menu Shortcuts" SEC04
  
  ; Create start menu shortcuts
  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\P2P Privacy Communications.lnk" "$INSTDIR\P2P_Launcher.exe" "" "$INSTDIR\P2P_Launcher.exe" 0
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\README.lnk" "$INSTDIR\README.md"
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" "$INSTDIR\${UNINSTALL_EXE}" "" "$INSTDIR\${UNINSTALL_EXE}" 0
  
SectionEnd

; Section descriptions
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC01} "Core application files required to run P2P Privacy Communications."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC02} "Automatically install required Python packages (cryptography, pyaudio)."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC03} "Create a desktop shortcut for easy access."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC04} "Create Start Menu shortcuts and program group."
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
  DeleteRegKey HKLM "SOFTWARE\${APP_NAME}"
  
  ; Remove files and uninstaller
  Delete "$INSTDIR\main.py"
  Delete "$INSTDIR\requirements.txt"
  Delete "$INSTDIR\README.md"
  Delete "$INSTDIR\setup.py"
  Delete "$INSTDIR\run.bat"
  Delete "$INSTDIR\run.ps1"
  Delete "$INSTDIR\P2P_Launcher.exe"
  Delete "$INSTDIR\${UNINSTALL_EXE}"
  
  ; Remove shortcuts
  Delete "$DESKTOP\P2P Privacy Communications.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\*.*"
  
  ; Remove directories
  RMDir "$SMPROGRAMS\${APP_NAME}"
  RMDir "$INSTDIR"
  
SectionEnd

