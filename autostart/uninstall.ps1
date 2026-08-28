# Disables auto-start by removing the Startup launcher. Nothing else is touched.
$dst = Join-Path ([Environment]::GetFolderPath('Startup')) 'FridayJarvisDashboard.vbs'
if (Test-Path $dst) { Remove-Item $dst -Force; Write-Host "Auto-start disabled." -ForegroundColor Yellow }
else { Write-Host "No auto-start launcher found." }
