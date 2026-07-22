@echo off
setlocal enabledelayedexpansion

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

set "scope=Machine"
set "dest=%ProgramFiles%\TagFetch"
echo Running with administrator privileges

:: detect arch
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    echo Your arch: %PROCESSOR_ARCHITECTURE%
    set "file=tagfetch_windows_x86_64.exe"
) else (
    echo Unsupported arch: %PROCESSOR_ARCHITECTURE%
    exit /b 1
)

:: create dest dir
if not exist "%dest%" mkdir "%dest%" 2>nul
if %errorlevel% neq 0 (
    echo Failed to create directory: %dest%
    exit /b 1
)

echo Downloading TagFetch
:: get download url from latest release
for /f "delims=" %%u in ('powershell -command "&{$r=Invoke-RestMethod 'https://api.github.com/repos/elitrycraft/tagfetch/releases/latest'; foreach($a in $r.assets){if($a.name -eq '%file%'){$a.browser_download_url}}}"') do set "url=%%u"

if "%url%"=="" (
    echo Asset %file% not found in latest release
    exit /b 1
)

:: download
echo Downloading %file%...
curl -sfL "%url%" -o "%dest%\tagfetch.exe" 2>nul
if %errorlevel% neq 0 (
    echo Trying PowerShell download...
    powershell -command "Invoke-WebRequest -Uri '%url%' -OutFile '%dest%\tagfetch.exe'" >nul
    if !errorlevel! neq 0 (
        echo Download failed
        exit /b 1
    )
)

echo Adding to PATH
:: add to PATH
for /f "delims=" %%p in ('powershell -command "[Environment]::GetEnvironmentVariable('Path','%scope%')"') do set "curpath=%%p"
echo !curpath! | find /I "%dest%" >nul
if %errorlevel% neq 0 (
    powershell -command "[Environment]::SetEnvironmentVariable('Path',$([Environment]::GetEnvironmentVariable('Path','%scope%')+';%dest%'),'%scope%')"
    echo Added to %scope% PATH
)

echo Installed to %dest%. Restart terminal and run: tagfetch
endlocal
