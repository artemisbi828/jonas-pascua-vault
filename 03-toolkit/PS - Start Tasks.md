
```
# .bat files

start outlook.exe
start onenote.exe
start excel.exe
start winword.exe
:: start ssms.exe

start onenote.exe
```

# More robust version
```shell
@echo off
setlocal

REM --- helpers ---------------------------------------------------------
REM Always use: start "" "full\path\to\app.exe"
REM Add small delays so apps don’t stampede your CPU/disk
set "DELAY_SHORT=1"
set "DELAY_MED=2"

REM --- VS Code (User install) -----------------------------------------
if exist "%LocalAppData%\Programs\Microsoft VS Code\Code.exe" (
  start "" "%LocalAppData%\Programs\Microsoft VS Code\Code.exe"
) else if exist "%ProgramFiles%\Microsoft VS Code\Code.exe" (
  start "" "%ProgramFiles%\Microsoft VS Code\Code.exe"
) else (
  echo [WARN] VS Code not found in standard locations.
)

timeout /t %DELAY_SHORT% /nobreak >nul

REM --- File Explorer ---------------------------------------------------
start "" explorer.exe
timeout /t %DELAY_SHORT% /nobreak >nul

REM --- Microsoft Teams (new Teams typical path; may vary) --------------
if exist "%LocalAppData%\Microsoft\Teams\current\Teams.exe" (
  start "" "%LocalAppData%\Microsoft\Teams\current\Teams.exe"
) else (
  echo [WARN] Teams exe not found at LocalAppData\Microsoft\Teams\current.
)

timeout /t %DELAY_SHORT% /nobreak >nul

REM --- Obsidian --------------------------------------------------------
if exist "%LocalAppData%\Obsidian\Obsidian.exe" (
  start "" "%LocalAppData%\Obsidian\Obsidian.exe"
) else if exist "%ProgramFiles%\Obsidian\Obsidian.exe" (
  start "" "%ProgramFiles%\Obsidian\Obsidian.exe"
) else (
  echo [WARN] Obsidian not found in standard locations.
)

timeout /t %DELAY_SHORT% /nobreak >nul

REM --- Outlook ---------------------------------------------------------
REM "olk.exe" is not a common Outlook executable name on most installs.
REM Classic Outlook is typically OUTLOOK.EXE (Microsoft Office\root\OfficeXX\OUTLOOK.EXE)
REM The New Outlook may be a packaged app (no stable OUTLOOK.EXE).
for %%P in (
  "%ProgramFiles%\Microsoft Office\root\Office16\OUTLOOK.EXE"
  "%ProgramFiles(x86)%\Microsoft Office\root\Office16\OUTLOOK.EXE"
) do (
  if exist "%%~P" start "" "%%~P"
)

timeout /t %DELAY_SHORT% /nobreak >nul

REM --- SSMS ------------------------------------------------------------
REM SSMS path varies by version; this is a common one
for %%P in (
  "%ProgramFiles(x86)%\Microsoft SQL Server Management Studio 20\Common7\IDE\Ssms.exe"
  "%ProgramFiles(x86)%\Microsoft SQL Server Management Studio 19\Common7\IDE\Ssms.exe"
  "%ProgramFiles(x86)%\Microsoft SQL Server Management Studio 18\Common7\IDE\Ssms.exe"
) do (
  if exist "%%~P" start "" "%%~P"
)

timeout /t %DELAY_MED% /nobreak >nul

REM --- Sublime Text ----------------------------------------------------
if exist "%ProgramFiles%\Sublime Text\sublime_text.exe" (
  start "" "%ProgramFiles%\Sublime Text\sublime_text.exe"
) else if exist "%ProgramFiles%\Sublime Text 3\sublime_text.exe" (
  start "" "%ProgramFiles%\Sublime Text 3\sublime_text.exe"
) else (
  echo [WARN] Sublime Text not found in standard locations.
)

REM --- M365 Copilot ----------------------------------------------------
REM If this is a Store/packaged app, launching via exe may not work reliably.
REM If you can launch it via a shortcut, prefer the shortcut approach (Option B).
echo [INFO] Copilot launch depends on how it's installed; see notes below.

endlocal
```