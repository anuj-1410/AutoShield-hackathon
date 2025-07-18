# AutoShield Startup Script
# This script starts both the backend and frontend services

param(
    [switch]$Backend,
    [switch]$Frontend,
    [switch]$All
)

function Start-Backend {
    Write-Host "Starting AutoShield Backend..." -ForegroundColor Green
    Write-Host "Backend will be available at: http://localhost:8000" -ForegroundColor Yellow
    Write-Host "API Documentation: http://localhost:8000/api/docs" -ForegroundColor Yellow
    
    Set-Location backend/app
    python main_simple.py
}

function Start-Frontend {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Green
    Set-Location frontend
    npm install
    
    Write-Host "Starting AutoShield Frontend..." -ForegroundColor Green
    Write-Host "Frontend will be available at: http://localhost:3000" -ForegroundColor Yellow
    
    npm run dev
}

function Start-Both {
    Write-Host "AutoShield Full Stack Startup" -ForegroundColor Cyan
    Write-Host "=" * 50 -ForegroundColor Cyan
    
    # Start backend in background
    Write-Host "Starting backend..." -ForegroundColor Green
    Start-Job -Name "AutoShield-Backend" -ScriptBlock {
        Set-Location $using:PWD
        Set-Location backend/app
        python main_simple.py
    }
    
    # Wait a bit for backend to start
    Start-Sleep -Seconds 3
    
    # Start frontend
    Write-Host "Starting frontend..." -ForegroundColor Green
    Start-Frontend
}

function Show-Help {
    Write-Host "AutoShield Startup Script" -ForegroundColor Cyan
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\start-autoshield.ps1 -Backend    # Start only backend"
    Write-Host "  .\start-autoshield.ps1 -Frontend   # Start only frontend"
    Write-Host "  .\start-autoshield.ps1 -All        # Start both services"
    Write-Host ""
    Write-Host "Services will be available at:" -ForegroundColor Yellow
    Write-Host "  Frontend: http://localhost:3000"
    Write-Host "  Backend:  http://localhost:8000"
    Write-Host "  API Docs: http://localhost:8000/api/docs"
}

# Main logic
if ($Backend) {
    Start-Backend
} elseif ($Frontend) {
    Start-Frontend
} elseif ($All) {
    Start-Both
} else {
    Show-Help
}
