# CinePulse Start Script (PowerShell)
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host "  CinePulse: Movie Analytics & Recommendation System (PES University)" -ForegroundColor Yellow
Write-Host "====================================================================" -ForegroundColor Cyan

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "`n[1/3] Initializing Relational Database & Triggers..." -ForegroundColor Green
python "$projectRoot\build_database_and_test.py"

Write-Host "`n[2/3] Launching Python REST API & Vector Engine (Port 5000)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python '$projectRoot\backend\server.py'"

Start-Sleep -Seconds 2

Write-Host "`n[3/3] Launching Next.js Frontend Server (Port 3000)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$projectRoot\frontend'; npm run start"

Start-Sleep -Seconds 3

Write-Host "`nOpening http://localhost:3000 in your browser..." -ForegroundColor Cyan
Start-Process "http://localhost:3000"
Write-Host "CinePulse is running successfully!" -ForegroundColor Green
