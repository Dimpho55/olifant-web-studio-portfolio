# Website Automation Suite - Quick Start Setup Script
# Run this script to automatically set up the Python environment and install dependencies

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Olifant Web Studio - Automation Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonCheck = &powershell -Command "python --version 2>&1" -ErrorAction SilentlyContinue
if ($pythonCheck -like "*not found*" -or $pythonCheck -like "*is not recognized*") {
    Write-Host "ERROR: Python is not properly installed or not in PATH" -ForegroundColor Red
    Write-Host "Please see PYTHON_SETUP.md for installation instructions" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Quick fix options:" -ForegroundColor Cyan
    Write-Host "1. Install Python from https://python.org/downloads" -ForegroundColor White
    Write-Host "   - Use version 3.11 or higher" -ForegroundColor White
    Write-Host "   - Check 'Add Python to PATH' during installation" -ForegroundColor White
    Write-Host "2. If installed, disable Microsoft Store Python shim:" -ForegroundColor White
    Write-Host "   Settings > Apps > Advanced app settings > Manage app execution aliases" -ForegroundColor White
    exit 1
}

Write-Host "✓ Python found: $pythonCheck" -ForegroundColor Green
Write-Host ""

# Create virtual environment (optional but recommended)
Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

Write-Host ""
Write-Host "Installing project dependencies..." -ForegroundColor Yellow
pip install -q -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green

Write-Host ""
Write-Host "Verifying installation..." -ForegroundColor Yellow
$testRun = python -c "from config import Config; from modules import LinkChecker, ImageValidator, PerformanceMonitor, BackupManager, FileSync; print('OK')" 2>&1
if ($testRun -like "*OK*") {
    Write-Host "✓ All modules imported successfully" -ForegroundColor Green
} else {
    Write-Host "WARNING: Some modules failed to import" -ForegroundColor Yellow
    Write-Host $testRun -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Quick start commands:" -ForegroundColor Cyan
Write-Host "  python automate.py --help      # Show all commands" -ForegroundColor White
Write-Host "  python automate.py audit       # Run full system audit" -ForegroundColor White
Write-Host "  python automate.py check-links # Check for broken links" -ForegroundColor White
Write-Host ""
Write-Host "For detailed usage, see: automation_README.md" -ForegroundColor Cyan
Write-Host ""
