# Website Automation Suite

A comprehensive Python command-line tool for automating maintenance, scanning, and deployment tasks across the Olifant Web Studio portfolio (main site, REGCORP, and Newlysly).

## Features

- **Link Checking**: Scan all HTML files for broken internal and external links
- **Image Validation**: Check for missing images, invalid alt text, and large files
- **Performance Analysis**: Analyze page load times, DOM complexity, and file sizes
- **Backup & Restore**: Create timestamped zip backups and restore from archives
- **File Synchronization**: Sync websites to remote servers (FTP/SFTP support ready)
- **Full Audits**: Run comprehensive scans across all metrics in one command
- **Report Generation**: Generate HTML reports of scan results
- **Logging**: All operations logged with timestamps to `logs/` directory

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Navigate to the project directory:
```bash
cd "c:\Users\user\Olifant Web Studio"
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Commands

All commands follow the pattern:
```bash
python automate.py {command} [options]
```

### Available Commands

#### 1. Full Audit (Recommended)
Runs all scans (links, images, performance) on all sites:
```bash
python automate.py audit
```

#### 2. Check Links
Scan all HTML files for broken and external links:
```bash
# All sites
python automate.py check-links

# Specific sites
python automate.py check-links --sites newlysly
python automate.py check-links --sites main regcorp

# With external link checks
python automate.py check-links --include-external
```

Output includes:
- Valid links
- Broken links (with file locations)
- External links
- Anchor links

#### 3. Check Images
Validate all image tags in HTML files:
```bash
# All sites
python automate.py check-images

# Specific site
python automate.py check-images --sites newlysly
```

Output includes:
- Valid images (with alt text)
- Missing image files
- Images missing alt text (accessibility check)
- File size analysis

#### 4. Analyze Performance
Analyze page load times and performance metrics:
```bash
# All sites
python automate.py analyze-performance

# Specific site
python automate.py analyze-performance --sites main
```

Output includes:
- Estimated load time (in milliseconds)
- HTML/CSS/JS/Image file counts
- Total file sizes (in MB)
- DOM element count
- Optimization recommendations

#### 5. Backup Websites
Create a timestamped zip backup of all websites:
```bash
python automate.py backup
```

Backups are stored in the `backups/` directory with names like:
- `backup_2024-01-15_14-30-45.zip`

#### 6. List Backups
View all existing backups:
```bash
python automate.py backup --list
```

Shows:
- Backup timestamp
- File size
- Full path

#### 7. Restore from Backup
Restore websites from a backup archive:
```bash
python automate.py restore {timestamp}
```

Example:
```bash
python automate.py restore 2024-01-15_14-30-45
```

#### 8. Sync Files
Synchronize websites to remote server (currently demo mode):
```bash
python automate.py sync --remote-host example.com --remote-user admin
```

#### 9. Generate Report
Create an HTML report of the last audit results:
```bash
python automate.py report
```

Reports are saved to `reports/` directory.

### Command Examples

**Scenario 1: Daily Maintenance**
```bash
# Check everything on all sites
python automate.py audit

# Or check just Newlysly for e-commerce issues
python automate.py check-images --sites newlysly
python automate.py analyze-performance --sites newlysly
```

**Scenario 2: Before Deployment**
```bash
# Full audit
python automate.py audit

# Create backup
python automate.py backup

# Check for broken links before going live
python automate.py check-links
```

**Scenario 3: Disaster Recovery**
```bash
# List available backups
python automate.py backup --list

# Restore from specific backup
python automate.py restore 2024-01-15_14-30-45
```

## Configuration

Edit `config.py` to customize:

- **Site Paths**: Modify `SITE_PATHS` to point to your websites
- **Backup Retention**: Change `BACKUP_RETENTION` (default: 10 backups kept)
- **Performance Thresholds**: Adjust `LOAD_TIME_WARNING`, `DOM_COUNT_WARNING`, etc.
- **Remote Server**: Set `REMOTE_ENABLED`, `REMOTE_HOST`, `REMOTE_USER`, `REMOTE_PATH`
- **Notifications**: Configure email settings for alerts

## Output Locations

- **Logs**: `logs/{command}_{timestamp}.log`
- **Backups**: `backups/backup_{timestamp}.zip`
- **Reports**: `reports/report_{timestamp}.html`

## Modules

The automation suite uses a modular architecture:

- **automate.py**: Main CLI orchestrator with command routing
- **modules/link_checker.py**: Validates internal and external links using BeautifulSoup
- **modules/image_validator.py**: Checks images, alt text, and file sizes
- **modules/performance_monitor.py**: Analyzes load times and recommends optimizations
- **modules/backup_manager.py**: Creates and restores zip backups
- **modules/file_sync.py**: Handles file synchronization to remote servers

## Exit Codes

- `0`: Success
- `1`: Error during operation
- `2`: Invalid arguments

## Troubleshooting

**Issue**: `No module named 'requests'`
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: Broken links reported for valid local files
- **Solution**: Check that relative paths in HTML are correct from the site root

**Issue**: Backup restore fails
- **Solution**: Ensure backup zip file exists in `backups/` directory and timestamp is correct

## Examples of Output

### Audit Result
```
========== AUDIT RESULTS ==========
Site: main
  Links: 45 valid, 2 broken, 12 external
  Images: 28 valid, 1 missing, 2 no alt text
  Performance: 1250ms estimated load time (GOOD)

Site: newlysly
  Links: 32 valid, 0 broken, 5 external
  Images: 18 valid, 0 missing, 0 no alt text
  Performance: 980ms estimated load time (EXCELLENT)

Site: regcorp
  Links: 18 valid, 0 broken, 3 external
  Images: 12 valid, 0 missing, 0 no alt text
  Performance: 650ms estimated load time (EXCELLENT)

RECOMMENDATIONS:
- main: Add alt text to 2 images for accessibility
- main: Fix broken links: contact.html:42, portfolio.html:15
```

## Advanced Usage

### Scheduling Automation

**Windows Task Scheduler** (example):
1. Open Task Scheduler
2. Create Basic Task: "Daily Website Audit"
3. Set trigger to daily at 2:00 AM
4. Set action to: `C:\Python\python.exe`
5. Add arguments: `C:\path\to\automate.py audit`
6. Set start in: `C:\Users\user\Olifant Web Studio`

**Linux/Mac Cron** (example):
```bash
# Edit crontab
crontab -e

# Add line to run daily at 2 AM
0 2 * * * cd /path/to/website && /usr/bin/python3 automate.py audit
```

## Support

For issues or feature requests, check:
1. That Python 3.7+ is installed: `python --version`
2. That requirements are installed: `pip list | grep requests`
3. That site paths in `config.py` are correct
4. Check logs in `logs/` directory for detailed error messages

## License

Part of the Olifant Web Studio automation ecosystem.
Developed by Dimpho Olifant.
