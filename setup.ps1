# Website Automation Suite - Windows Setup Script
# Run this script to automatically set up the Python environment and install dependencies
# 
# Usage: .\setup.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Olifant Web Studio - Automation Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator (recommended but not required)
$currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Note: Running as administrator is recommended but not required" -ForegroundColor Yellow
}

# Check Python installation
Write-Host "Step 1: Checking Python installation..." -ForegroundColor Yellow
$pythonExe = $null

# Try finding python in PATH
try {
    $pythonExe = (Get-Command python -ErrorAction SilentlyContinue).Source
    if ($pythonExe) {
        & $pythonExe --version 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Python found at: $pythonExe" -ForegroundColor Green
        } else {
            $pythonExe = $null
        }
    }
} catch {}

# If not found, check common installation paths
if (-not $pythonExe) {
    Write-Host "Python not found in PATH. Checking common installation paths..." -ForegroundColor Yellow
    
    $commonPaths = @(
        "C:\Python312\python.exe",
        "C:\Python311\python.exe",
        "C:\Program Files\Python312\python.exe",
        "C:\Program Files\Python311\python.exe",
        "C:\Program Files (x86)\Python312\python.exe",
        "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python312\python.exe",
        "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python311\python.exe"
    )
    
    foreach ($path in $commonPaths) {
        if (Test-Path $path) {
            $pythonExe = $path
            Write-Host "✓ Python found at: $pythonExe" -ForegroundColor Green
            break
        }
    }
}

# If still not found, guide user to install
if (-not $pythonExe) {
    Write-Host ""
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "To fix this:" -ForegroundColor Yellow
    Write-Host "1. Download Python from: https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "2. Run the installer and CHECK 'Add Python to PATH'" -ForegroundColor White
    Write-Host "3. Restart PowerShell" -ForegroundColor White
    Write-Host "4. Run this script again" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to open Python downloads page in browser"
    Start-Process "https://www.python.org/downloads/"
    exit 1
}

# Verify Python version
Write-Host "Step 2: Verifying Python version..." -ForegroundColor Yellow
$versionOutput = & $pythonExe --version 2>&1
if ($versionOutput -match "Python (\d+\.\d+)") {
    $version = [version]$matches[1]
    if ($version -lt [version]"3.7") {
        Write-Host "ERROR: Python 3.7+ is required, but found $versionOutput" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Python version: $versionOutput" -ForegroundColor Green
}

# Setup virtual environment
Write-Host ""
Write-Host "Step 3: Setting up virtual environment..." -ForegroundColor Yellow

$venvPath = ".\venv"
if (Test-Path $venvPath) {
    Write-Host "Virtual environment already exists" -ForegroundColor Cyan
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor White
    & $pythonExe -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Step 4: Activating virtual environment..." -ForegroundColor Yellow

$activateScript = ".\venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    # Check execution policy
    $policy = Get-ExecutionPolicy -Scope CurrentUser
    if ($policy -eq "Restricted") {
        Write-Host "Setting execution policy to allow scripts..." -ForegroundColor Yellow
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    }
    
    & $activateScript
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "WARNING: Could not find activation script" -ForegroundColor Yellow
}

# Upgrade pip
Write-Host ""
Write-Host "Step 5: Upgrading pip..." -ForegroundColor Yellow
& python -m pip install --quiet --upgrade pip
Write-Host "✓ Pip upgraded" -ForegroundColor Green

# Install requirements
Write-Host ""
Write-Host "Step 6: Installing project dependencies..." -ForegroundColor Yellow

if (Test-Path "requirements.txt") {
    Write-Host "Found requirements.txt, installing packages..." -ForegroundColor White
    & pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "ERROR: requirements.txt not found" -ForegroundColor Red
    exit 1
}

# Verify installation
Write-Host ""
Write-Host "Step 7: Verifying installation..." -ForegroundColor Yellow

$testResult = python -c "
import sys
try:
    from config import Config
    from modules import LinkChecker, ImageValidator, PerformanceMonitor, BackupManager, FileSync
    print('OK')
except Exception as e:
    print(f'ERROR: {e}')
    sys.exit(1)
" 2>&1

if ($testResult -contains "OK") {
    Write-Host "✓ All modules imported successfully" -ForegroundColor Green
} else {
    Write-Host "WARNING: Module verification had warnings" -ForegroundColor Yellow
    Write-Host $testResult
}

# Test the CLI
Write-Host ""
Write-Host "Step 8: Testing CLI..." -ForegroundColor Yellow
& python automate.py --help > $null 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ CLI is working correctly" -ForegroundColor Green
} else {
    Write-Host "WARNING: CLI test had issues" -ForegroundColor Yellow
}

# Done!
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Quick test - Run a full audit:" -ForegroundColor White
Write-Host "   python automate.py audit" -ForegroundColor Gray
Write-Host ""
Write-Host "2. View help for all commands:" -ForegroundColor White
Write-Host "   python automate.py --help" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Common commands:" -ForegroundColor White
Write-Host "   python automate.py check-links  # Find broken links" -ForegroundColor Gray
Write-Host "   python automate.py backup       # Create backup" -ForegroundColor Gray
Write-Host "   python automate.py analyze-performance  # Check performance" -ForegroundColor Gray
Write-Host ""

Write-Host "Documentation:" -ForegroundColor Cyan
Write-Host "  • QUICK_START.md         - Quick reference guide" -ForegroundColor Gray
Write-Host "  • automation_README.md   - Full documentation" -ForegroundColor Gray
Write-Host ""

Write-Host "Your virtual environment is active!" -ForegroundColor Green
Write-Host "To deactivate, type: deactivate" -ForegroundColor Gray
Write-Host ""
