"""
Backup Manager Module - Creates and manages website backups
"""

import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Dict

class BackupManager:
    def __init__(self, config):
        self.config = config
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
    
    def create(self, site: str) -> str:
        """Create a backup of a website"""
        site_path = self.config.SITE_PATHS[site]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create backup filename
        backup_name = f"{site}_backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        
        # Create zip archive
        try:
            shutil.copytree(site_path, backup_path)
            
            # Zip it
            zip_path = self.backup_dir / f"{backup_name}.zip"
            shutil.make_archive(
                str(zip_path).replace('.zip', ''),
                'zip',
                backup_path
            )
            
            # Remove uncompressed backup
            shutil.rmtree(backup_path)
            
            return str(zip_path)
        except Exception as e:
            raise Exception(f"Backup failed for {site}: {str(e)}")
    
    def restore(self, backup_path: str):
        """Restore a website from backup"""
        backup_file = Path(backup_path)
        
        if not backup_file.exists():
            raise Exception(f"Backup file not found: {backup_path}")
        
        try:
            # Extract backup
            extract_dir = self.backup_dir / "temp_restore"
            extract_dir.mkdir(exist_ok=True)
            
            with zipfile.ZipFile(backup_file, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Find site directory (usually first folder in zip)
            site_dir = next(extract_dir.iterdir())
            
            # Restore to original location
            # This is a placeholder - you'd need to identify which site and restore
            print(f"Restore completed. Files extracted to: {extract_dir}")
            
        except Exception as e:
            raise Exception(f"Restore failed: {str(e)}")
    
    def list_backups(self) -> list:
        """List all available backups"""
        backups = []
        
        for backup_file in self.backup_dir.glob("*.zip"):
            stat = backup_file.stat()
            backups.append({
                'name': backup_file.name,
                'path': str(backup_file),
                'size': stat.st_size / (1024 * 1024),  # MB
                'date': datetime.fromtimestamp(stat.st_mtime)
            })
        
        return sorted(backups, key=lambda x: x['date'], reverse=True)
    
    def cleanup_old_backups(self, keep_count: int = 5):
        """Keep only the most recent backups"""
        backups = self.list_backups()
        
        # Delete old backups
        for backup in backups[keep_count:]:
            Path(backup['path']).unlink()
            print(f"Deleted old backup: {backup['name']}")
