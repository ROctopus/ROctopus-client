; makewinstaller.nsi
;
; This script is based on example1.nsi, but it remember the directory, 
; has uninstall support and (optionally) installs start menu shortcuts.
;
; It will install example2.nsi into a directory that the user selects,

;--------------------------------

; The name of the installer
Name "rocto-client"

; The file to write
OutFile "..\dist\rocto-setup.exe"

; The default installation directory
InstallDir $PROGRAMFILES\rocto-client

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\NSIS_rocto-client" "Install_Dir"

; Request application privileges for Windows Vista
RequestExecutionLevel admin

;--------------------------------

; Pages

Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

; The stuff to install
Section "rocto-client (required)"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File ..\dist\rocto-client.exe
  
  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\NSIS_rocto-client "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\rocto-client" "DisplayName" "NSIS rocto-client"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\rocto-client" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\rocto-client" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\rocto-client" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\rocto-client"
  CreateShortcut "$SMPROGRAMS\rocto-client\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortcut "$SMPROGRAMS\rocto-client\rocto-client.lnk" "$INSTDIR\rocto-client.exe" "" "$INSTDIR\rocto-client.nsi" 0
  
SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\rocto-client"
  DeleteRegKey HKLM SOFTWARE\NSIS_rocto-client

  ; Remove files and uninstaller
  Delete $INSTDIR\rocto-client.exe
  Delete $INSTDIR\uninstall.exe

  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\rocto-client\*.*"

  ; Remove directories used
  RMDir "$SMPROGRAMS\rocto-client"
  RMDir "$INSTDIR"

SectionEnd
