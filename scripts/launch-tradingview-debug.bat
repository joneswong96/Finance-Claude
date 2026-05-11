@echo off
REM Launch TradingView Desktop with Chrome DevTools Protocol enabled
REM Required for tradesdontlie/tradingview-mcp to connect

echo Starting TradingView with CDP on port 9222...

REM Microsoft Store version (confirmed working path)
set "TV_PATH=C:\Program Files\WindowsApps\TradingView.Desktop_3.1.0.7818_x64__n534cwy3pjxzj\TradingView.exe"

if exist "%TV_PATH%" (
    start "" "%TV_PATH%" --remote-debugging-port=9222
    echo [OK] TradingView launched (Microsoft Store version)
    goto :done
)

REM Fallback: search for any TradingView in WindowsApps
for /d %%i in ("C:\Program Files\WindowsApps\TradingView*") do (
    if exist "%%i\TradingView.exe" (
        start "" "%%i\TradingView.exe" --remote-debugging-port=9222
        echo [OK] TradingView launched from WindowsApps
        goto :done
    )
)

REM Other common locations
if exist "%LOCALAPPDATA%\TradingView\TradingView.exe" (
    start "" "%LOCALAPPDATA%\TradingView\TradingView.exe" --remote-debugging-port=9222
    echo [OK] TradingView launched from LocalAppData
    goto :done
)

echo [ERROR] TradingView not found. Update TV_PATH in this script.
pause
exit /b 1

:done
echo.
echo TradingView is running with CDP on localhost:9222
echo You can now use tv_health_check in Claude Code.
timeout /t 5
