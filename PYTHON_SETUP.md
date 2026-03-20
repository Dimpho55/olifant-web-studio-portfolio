# Python Setup Guide for Website Automation Suite

## Problem
The automation suite requires Python 3.7+ but `python` command is not properly configured in your system PATH.

## Solution

### Option 1: Install Python from python.org (Recommended)

1. Go to https://python.org/downloads
2. Download Python 3.11 or 3.12
3. **IMPORTANT**: During installation, check the box: "Add Python to PATH"
4. Complete the installation
5. Restart your terminal/PowerShell
6. Verify installation:
   ```powershell
   python --version
   ```

### Option 2: Fix Microsoft Store Python Stub

If Python is installed but the Microsoft Store shim is blocking it:

1. Open Settings > Apps > Advanced app settings
2. Find "python.exe" and "python3.exe" 
3. Click on each and select "Manage app execution aliases"
4. Turn OFF the toggles for python and python3
5. Restart PowerShell
6. Test:
   ```powershell
   python --version
   ```

### Option 3: Use VS Code Python Extension

1. Install the Python extension in VS Code (ms-python.python)
2. Open the project folder in VS Code
3. Click the Python version in the bottom status bar
4. Select "Create Environment" and choose venv
5. VS Code will create and activate a virtual environment automatically

### Option 4: Use Python Full Installation Path

If Python is installed but PATH isn't configured, find it manually:

1. Check these common locations:
   - `C:\Users\[YourUsername]\AppData\Local\Programs\Python\Python311\python.exe`
   - `C:\Program Files\Python311\python.exe`
   - `C:\Program Files (x86)\Python311\python.exe`

2. Once found, add to your PowerShell profile:
   ```powershell
   $env:Path += ";C:\Program Files\Python311"
   ```

## After Installation

Once Python is properly installed and in PATH:

```powershell
# Install project dependencies
pip install -r requirements.txt

# Test the automation suite
python automate.py --help
```

## Troubleshooting

**Error: "Python was not found; run without arguments to install from the Microsoft Store"**
- This means the Microsoft Store Python stub is installed but no actual Python is
- Solution: Install Python from python.org as shown above

**Error: "ModuleNotFoundError: No module named 'requests'"**
- Dependencies not installed
- Solution: Run `pip install -r requirements.txt`

**Error: "No module named 'config'"**
- config.py file is missing or in wrong location
- Solution: Ensure config.py exists in the root directory

## Verify Setup

Once installed, verify everything works:

```powershell
# Test Python
python --version

# Test pip
pip --version

# Install requirements
pip install -r requirements.txt

# Test the automation script
python automate.py --help

# Run a test scan
python automate.py audit
```

If all commands run without errors, your setup is complete!

## Next Steps

See `automation_README.md` for full usage documentation.

## Support

For Python installation issues, see: https://docs.python.org/3/using/windows.html
