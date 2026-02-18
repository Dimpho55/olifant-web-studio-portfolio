"""
Configuration file for Website Automation Suite
"""

from pathlib import Path

class Config:
    # Base paths
    BASE_DIR = Path(".")
    
    # Site configurations
    SITES = ['main', 'newlysly', 'regcorp']
    
    SITE_PATHS = {
        'main': BASE_DIR,  # Main Olifant Web Studio is in root
        'newlysly': BASE_DIR / 'newlysly',
        'regcorp': BASE_DIR / 'regcorp'
    }
    
    # Backup settings
    BACKUP_DIR = Path("backups")
    BACKUP_RETENTION = 10  # Keep last 10 backups
    
    # Logging
    LOG_DIR = Path("logs")
    LOG_LEVEL = "INFO"
    
    # Reports
    REPORT_DIR = Path("reports")
    
    # Performance thresholds
    LOAD_TIME_WARNING = 3000  # ms
    DOM_COUNT_WARNING = 1500
    IMAGE_SIZE_WARNING = 10  # MB
    
    # Remote configuration (if using remote deployment)
    REMOTE_ENABLED = False
    REMOTE_HOST = "example.com"
    REMOTE_USER = "user"
    REMOTE_PATH = "/var/www/html"
    REMOTE_PORT = 22
    
    # Notification settings
    NOTIFY_EMAIL = "admin@olifantwebstudio.co.za"
    NOTIFY_ON_ERROR = True
    NOTIFY_ON_SUCCESS = False
    
    # Scan settings
    INCLUDE_EXTERNAL_LINKS = False
    LINK_TIMEOUT = 5  # seconds
    
    def __init__(self):
        # Create necessary directories
        self.BACKUP_DIR.mkdir(exist_ok=True)
        self.LOG_DIR.mkdir(exist_ok=True)
        self.REPORT_DIR.mkdir(exist_ok=True)
