# Python Automation Suite Setup & Usage Guide

## Quick Start

Before using the automation suite, you must install Python and configure it properly.

### Step 1: Install Python

1. Download Python 3.11+ from [python.org](https://www.python.org/downloads/)
2. During installation, **IMPORTANT**: Check "Add Python to PATH"
3. Complete the installation
4. Restart your PowerShell/Terminal

### Step 2: Install Dependencies

```powershell
cd "c:\Users\user\Olifant Web Studio"
pip install -r requirements.txt
```

### Step 3: Test Installation

```powershell
python automate.py --help
```

If this shows the help menu, you're ready to go!

## Command Reference

### Full System Audit
```powershell
python automate.py audit
```
Runs complete scan on all sites (links, images, performance).

### Check Links
```powershell
# All sites
python automate.py check-links

# Specific site(s)
python automate.py check-links --sites main newlysly

# Include external links
python automate.py check-links --include-external
```

### Check Images
```powershell
# All sites
python automate.py check-images

# Specific site
python automate.py check-images --sites newlysly
```

### Analyze Performance
```powershell
# All sites
python automate.py analyze-performance

# Specific site
python automate.py analyze-performance --sites regcorp
```

### Backup Management
```powershell
# Create backup
python automate.py backup

# List backups
python automate.py backup --list

# Restore from backup
python automate.py restore 2024-01-15_14-30-45

# Backup specific sites
python automate.py backup --sites main newlysly
```

### File Synchronization
```powershell
# Sync to remote server
python automate.py sync --remote-host example.com --remote-user admin

# Sync from remote
python automate.py sync --direction pull --remote-host example.com
```

### Generate Report
```powershell
python automate.py report
```

## Output Locations

- **Logs**: `logs/` folder (timestamped files)
- **Backups**: `backups/` folder (zip files)
- **Reports**: `reports/` folder (HTML files)

## Troubleshooting

### "Python not found"
- Install Python from [python.org](https://python.org)
- Ensure "Add Python to PATH" is checked
- Restart PowerShell

### "ModuleNotFoundError: No module named 'requests'"
```powershell
pip install -r requirements.txt
```

### Automation script won't run
- Verify all files exist: config.py, automate.py, modules/ folder
- Check Python path: `python --version`
- Run from correct directory

## Next Steps

See [automation_README.md](automation_README.md) for detailed documentation.
