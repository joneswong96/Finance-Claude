@echo off
:: Finance-Claude — Launch TradingView Desktop with CDP enabled
:: Required for chart-analyst and signal-tracker MCP tools

set CDP_PORT=9222
set TV_EXE=C:\Program Files\WindowsApps\TradingView.Desktop_3.1.0.7818_x64__n534cwy3pjxzj\TradingView.exe

echo [Finance-Claude] Checking for TradingView...

if not exist "%TV_EXE%" (
    echo ERROR: TradingView not found at %TV_EXE%
    echo Please update TV_EXE path in this script to match your installation.
    pause
    exit /b 1
)

:: Check if TradingView is already running with CDP
netstat -an 2>nul | find ":%CDP_PORT% " >nul
if %errorlevel% == 0 (
    echo [OK] CDP already listening on port %CDP_PORT% — TradingView is ready.
    goto :done
)

echo [Finance-Claude] Launching TradingView with CDP on port %CDP_PORT%...
start "" "%TV_EXE%" --remote-debugging-port=%CDP_PORT%

:: Wait up to 15 seconds for CDP to come up
set /a tries=0
:wait_loop
timeout /t 1 /nobreak >nul
netstat -an 2>nul | find ":%CDP_PORT% " >nul
if %errorlevel% == 0 goto :cdp_ready
set /a tries+=1
if %tries% lss 15 goto :wait_loop

echo ERROR: TradingView started but CDP not detected on port %CDP_PORT% after 15s.
echo Make sure TradingView is fully loaded before retrying.
pause
exit /b 1

:cdp_ready
echo [OK] TradingView running with CDP on port %CDP_PORT%.

:done
echo.
echo [Finance-Claude] You can now start Claude Code.
echo     chart-analyst and signal-tracker will connect automatically via .mcp.json
echo.
pause
