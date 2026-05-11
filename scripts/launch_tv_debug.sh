#!/usr/bin/env bash
# Finance-Claude — Launch TradingView Desktop with CDP enabled
# Mac/Linux equivalent (TradingView Desktop is Windows-only;
# this script is provided for reference / WSL users)

CDP_PORT=9222

echo "[Finance-Claude] Checking CDP on port $CDP_PORT..."

if lsof -i ":$CDP_PORT" &>/dev/null; then
    echo "[OK] CDP already listening on port $CDP_PORT — ready."
    exit 0
fi

echo ""
echo "TradingView Desktop is Windows-only."
echo "If you are using WSL, launch TradingView from Windows first:"
echo ""
echo '  Start-Process "$env:LOCALAPPDATA\Programs\TradingView\TradingView.exe" -ArgumentList "--remote-debugging-port=9222"'
echo ""
echo "Then return here and run /scan to verify the MCP connection."
