# Website Automation Suite - Complete Documentation

A comprehensive Python command-line tool for automating maintenance, scanning, and deployment tasks across the Olifant Web Studio portfolio (main site, REGCORP, and Newlysly).

## Features

- **Link Checking**: Scan HTML files for broken internal and external links
- **Image Validation**: Check for missing images, invalid alt text, and file sizes
- **Performance Analysis**: Analyze page load times, DOM complexity, and file sizes
- **Backup & Restore**: Create timestamped zip backups and restore from archives
- **File Synchronization**: Sync websites to remote servers
- **Full Audits**: Run comprehensive scans in one command
- **Logging**: All operations logged with timestamps

## Prerequisites

- Python 3.7+
- Windows, macOS, or Linux
- pip (Python package manager)

## Installation

### 1. Download and Install Python

Visit [python.org](https://www.python.org/downloads/) and download Python 3.11+

**Important**: During installation, check "Add Python to PATH"

### 2. Install Project Dependencies

```powershell
cd "c:\Users\user\Olifant Web Studio"
pip install -r requirements.txt
```

This installs:
- `requests` (HTTP client for link checking)
- `beautifulsoup4` (HTML parsing)

### 3. Verify Installation

```powershell
python automate.py --help
```

You should see the help menu with all available commands.

## Usage

All commands follow this pattern:
```
python automate.py {command} [options]
```

### 1. Full System Audit

Run all scans on all sites:
```powershell
python automate.py audit
```

This command:
- Checks all links in HTML files
- Validates all images
- Analyzes performance metrics
- Generates recommendations

### 2. Link Integrity Checking

**Check all sites:**
```powershell
python automate.py check-links
```

**Check specific sites:**
```powershell
python automate.py check-links --sites main newlysly
python automate.py check-links --sites regcorp
```

**Include external links:**
```powershell
python automate.py check-links --include-external
```

**What it does:**
- Scans all `.html` files
- Extracts links from `<a>`, `<script>`, `<link>`, `<img>` tags
- Validates internal file paths
- Checks HTTP status codes for external links
- Reports broken links with file locations

**Output shows:**
- Total links found
- Valid links ✓
- Broken links ❌
- External links →
- Anchor links #

### 3. Image Validation

**Check all sites:**
```powershell
python automate.py check-images
```

**Check specific site:**
```powershell
python automate.py check-images --sites newlysly
```

**What it does:**
- Finds all `<img>` tags in HTML files
- Verifies image files exist on disk
- Checks for missing alt text (accessibility)
- Analyzes file sizes
- Identifies large images (>5MB)

**Output shows:**
- Valid images with alt text ✓
- Missing image files ❌
- Images without alt text ⚠️
- Large files warning

### 4. Performance Analysis

**Analyze all sites:**
```powershell
python automate.py analyze-performance
```

**Analyze specific site:**
```powershell
python automate.py analyze-performance --sites main
```

**What it does:**
- Counts HTML, CSS, JavaScript, and image files
- Calculates total file sizes
- Counts DOM elements
- Estimates page load time
- Generates optimization recommendations

**Output shows:**
- Estimated load time (🟢 GOOD, 🟡 OK, 🔴 SLOW)
- File counts by type
- Total size breakdown
- DOM element count
- Specific recommendations for optimization

### 5. Backup & Restore

**Create a backup:**
```powershell
python automate.py backup
```

**Create backup of specific sites:**
```powershell
python automate.py backup --sites main newlysly
```

**List existing backups:**
```powershell
python automate.py backup --list
```

Shows:
- Backup filename
- Timestamp
- File size
- Full path

**Restore from backup:**
```powershell
python automate.py restore 2024-01-15_14-30-45
```

Replace the timestamp with the one from the backup list.

**Example workflow:**
```powershell
# Create backup before making changes
python automate.py backup

# Make changes...

# If something goes wrong, restore
python automate.py backup --list
python automate.py restore 2024-01-15_14-30-45
```

### 6. File Synchronization

**Sync to remote server:**
```powershell
python automate.py sync --remote-host example.com --remote-user admin
```

**Sync from remote:**
```powershell
python automate.py sync --direction pull --remote-host example.com --remote-user admin
```

**Currently**: Logs sync operations (placeholder for FTP/SFTP)

### 7. Generate Report

Create an HTML report:
```powershell
python automate.py report
```

Report is saved to `reports/` folder.

## Configuration

Edit `config.py` to customize:

```python
# Site paths
SITE_PATHS = {
    'main': BASE_DIR,
    'newlysly': BASE_DIR / 'newlysly',
    'regcorp': BASE_DIR / 'regcorp'
}

# Backup settings
BACKUP_RETENTION = 10  # Keep last 10 backups

# Performance thresholds
LOAD_TIME_WARNING = 3000  # milliseconds
DOM_COUNT_WARNING = 1500

# Remote server (for sync)
REMOTE_ENABLED = False
REMOTE_HOST = "example.com"
REMOTE_USER = "admin"
```

## Output Files

### Logs (`logs/` folder)
```
logs/
├── automation_20240115_143045.log
├── automation_20240115_152030.log
└── sync_20240115_160000.log
```

Each log file contains timestamped entries of what the tool did.

### Backups (`backups/` folder)
```
backups/
├── backup_2024-01-15_14-30-45.zip
├── backup_2024-01-15_15-20-30.zip
└── backup_2024-01-15_16-00-00.zip
```

Zip archives contain your website files at that point in time.

### Reports (`reports/` folder)
```
reports/
└── report_20240115_143045.html
```

HTML report of scan results.

## Example Workflows

### Daily Maintenance
```powershell
# Run every morning
python automate.py audit

# Check specific site
python automate.py check-images --sites newlysly
```

### Before Deployment
```powershell
# Create backup
python automate.py backup

# Full audit
python automate.py audit

# If all good, deploy
# If issues, review logs in `logs/` folder
```

### Disaster Recovery
```powershell
# List backups
python automate.py backup --list

# Restore from specific backup
python automate.py restore 2024-01-15_14-30-45

# Verify restoration
python automate.py audit
```

### Regular Monitoring
```powershell
# Weekly performance check
python automate.py analyze-performance

# Identify slow sites
# Edit config.py to optimize thresholds
# Run recommendations from output
```

## Log File Analysis

Log files contain detailed information about what happened:

```
[2024-01-15 14:30:45] [INFO] 🔍 Starting full system audit
[2024-01-15 14:30:45] [INFO] 📌 Auditing MAIN
[2024-01-15 14:30:46] [INFO] 🔗 Starting link integrity scan
[2024-01-15 14:30:47] [INFO] ✓ All links valid in main
[2024-01-15 14:30:48] [INFO] 🖼️  Starting image validation scan
[2024-01-15 14:30:49] [WARNING] ⚠️  Found 2 images without alt text in main
```

## Performance Thresholds

The tool evaluates performance based on these defaults:

- **Load Time**: < 2000ms = 🟢 GOOD, < 3000ms = 🟡 OK, > 3000ms = 🔴 SLOW
- **DOM Elements**: Warning at > 1500 elements
- **Image Size**: Warning at > 5MB per file
- **CSS Files**: Warning at > 3 files
- **JS Files**: Warning at > 5 files

Adjust these in `config.py` to match your needs.

## Advanced Features

### Module System

The tool uses separate modules for each function:

- `config.py` - Configuration and settings
- `modules/link_checker.py` - Link validation
- `modules/image_validator.py` - Image checking
- `modules/performance_monitor.py` - Performance analysis
- `modules/backup_manager.py` - Backup/restore
- `modules/file_sync.py` - File synchronization

You can modify individual modules without affecting others.

### Adding Custom Scans

To add a new scan type:

1. Create a new file in `modules/`
2. Implement a class with `__init__(self, config)` and `scan(self, site)` methods
3. Import in `automate.py`
4. Add command in `main()` function

## Troubleshooting

### Python Not Found
```
Error: Python was not found; run without arguments to install from Microsoft Store
```

**Solution:**
1. Install Python from [python.org](https://python.org)
2. Check "Add Python to PATH"
3. Restart PowerShell
4. Run: `python --version`

### ModuleNotFoundError
```
ModuleNotFoundError: No module named 'requests'
```

**Solution:**
```powershell
pip install -r requirements.txt
```

### File Not Found Errors

If you get "file not found" errors for valid files:

1. Check that relative paths in HTML are correct
2. Verify `config.py` has correct site paths
3. Check that files actually exist on disk

### Backup Restore Fails

Check:
1. Backup file exists in `backups/` folder
2. Timestamp in restore command matches backup filename
3. Enough disk space to restore

## Performance Tips

1. **First Run**: Takes longer (creates directories, logs)
2. **Large Sites**: Big image collections may take time to analyze
3. **External Link Checks**: Much slower (makes HTTP requests)
4. **Backups**: Large sites create large zip files

To speed up:
- Don't include external links unless needed
- Target specific sites with `--sites` flag
- Run during off-peak hours

## Support & Documentation

- **Quick Start**: See [QUICK_START.md](QUICK_START.md)
- **Python Setup**: See [PYTHON_SETUP.md](PYTHON_SETUP.md)
- **Config Reference**: See [config.py](config.py)

## Exit Codes

- `0` = Success
- `1` = Error occurred (check logs)
- `2` = Invalid arguments

## By the Numbers

After full audit, you get:
- Total files scanned
- Total links checked
- Total images validated
- Performance metrics for each site
- Actionable recommendations

## Examples of Output

**Successful Audit:**
```
[INFO] ✓ Audit complete
[INFO]   Valid: 45, Broken: 0, External: 12
[INFO]   ✓ All links valid in main
[INFO]   Valid: 28, Missing: 0, No alt: 2
[INFO]   🟢 GOOD Load time: 1250ms
[INFO]   [INFO] Performance is good!
```

**Issues Found:**
```
[WARNING] ❌ Found 2 broken links in main
[WARNING]    - /missing-page.html (Status: 404)
[WARNING]    - /old-product.html (Status: 404)
[WARNING] ⚠️  Found 2 images without alt text in main
[INFO]   [HIGH] Load time is 3500ms
[INFO]     - Minify CSS and JavaScript files
[INFO]     - Compress and optimize images
```

## Security Notes

- Backups are stored locally in `backups/` folder
- Remote sync credentials are stored in `config/remote.conf` (add to .gitignore)
- Log files contain operation details (may include error messages)
- External link checks make HTTP requests (may be logged by remote servers)

## License

Part of the Olifant Web Studio ecosystem.
Developed by Dimpho Olifant.

## Version History

- **v1.0** (January 2024): Initial release
  - Link checking
  - Image validation
  - Performance analysis
  - Backup/restore
  - File sync (placeholder)
