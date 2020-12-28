!include "MUI2.nsh"
!include "x64.nsh"

SetCompressor /SOLID /FINAL lzma

Name "GTA Eenzaam"
OutFile "gta-eenzaam.exe"
Unicode True

InstallDir "$LOCALAPPDATA\GTA Eenzaam"

;Get installation folder from registry if available
InstallDirRegKey HKCU "Software\GTA Eenzaam" ""

;Request application privileges for Windows Vista
RequestExecutionLevel user

!define MUI_ABORTWARNING

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

Section

SetOutPath "$INSTDIR"

File /r dist\*

;Store installation folder
WriteRegStr HKCU "Software\GTA Eenzaam" "" $INSTDIR

CreateShortcut "$SMPROGRAMS\GTA Eenzaam.lnk" "$INSTDIR\gta-eenzaam.exe"

SectionEnd