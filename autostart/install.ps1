# Installs auto-start-at-login for the FRIDAY / JARVIS Dashboard Mirror.
#   Run:  powershell -ExecutionPolicy Bypass -File .\autostart\install.ps1
$startup = [Environment]::GetFolderPath('Startup')
$src     = Join-Path $PSScriptRoot 'FridayJarvisDashboard.vbs'
$dst     = Join-Path $startup 'FridayJarvisDashboard.vbs'
Copy-Item $src $dst -Force
Write-Host "Installed: $dst (starts http://127.0.0.1:9100 at every login)" -ForegroundColor Green
Write-Host "Start now without rebooting:  wscript `"$dst`""
