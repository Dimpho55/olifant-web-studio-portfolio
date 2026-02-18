"""
Backup Manager Module - Handles backup and restore operations
"""

from pathlib import Path
from typing import Dict, List
from datetime import datetime
import shutil
import os

class BackupManager:
    def __init__(self, config):
        self.config = config
        self.config.BACKUP_DIR.mkdir(exist_ok=True)
    
    def create(self, sites: List[str] = None) -> Dict:
        """Create a backup of specified sites"""
        if sites is None:
            sites = self.config.SITES
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_name = f"backup_{timestamp}.zip"
        backup_path = self.config.BACKUP_DIR / backup_name
        
        try:
            # Create a temporary directory for backup contents
            temp_dir = self.config.BACKUP_DIR / f"temp_{timestamp}"
            temp_dir.mkdir(exist_ok=True)
            
            # Copy sites to temp directory
            for site in sites:
                if site in self.config.SITE_PATHS:
                    site_path = self.config.SITE_PATHS[site]
                    dest = temp_dir / site
                    
                    if site == 'main':
                        # For main site, copy specific files and folders
                        for item in site_path.iterdir():
                            if item.is_file() and item.suffix in ['.html', '.css', '.js']:
                                shutil.copy2(item, dest / item.name)
                            elif item.is_dir() and item.name not in ['modules', 'backups', 'logs', '.git']:
                                shutil.copytree(item, dest / item.name)
                    else:
                        # For subdirectories, copy everything except git and logs
                        shutil.copytree(
                            site_path, 
                            dest,
                            ignore=shutil.ignore_patterns('.git', 'logs', 'backups', '__pycache__')
                        )
            
            # Create zip archive
            shutil.make_archive(
                str(backup_path.with_suffix('')),  # Remove .zip as make_archive adds it
                'zip',
                temp_dir
            )
            
            # Clean up temp directory
            shutil.rmtree(temp_dir)
            
            # Get backup file size
            size_bytes = backup_path.stat().st_size
            size_mb = size_bytes / (1024 * 1024)
            
            # Cleanup old backups
            self._cleanup_old_backups()
            
            return {
                'success': True,
                'backup': backup_name,
                'path': str(backup_path),
                'timestamp': timestamp,
                'size_mb': round(size_mb, 2)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_backups(self) -> List[Dict]:
        """List all available backups"""
        backups = []
        
        for backup_file in sorted(self.config.BACKUP_DIR.glob("backup_*.zip"), reverse=True):
            try:
                size_bytes = backup_file.stat().st_size
                size_mb = size_bytes / (1024 * 1024)
                timestamp = backup_file.stem.replace("backup_", "")
                
                backups.append({
                    'file': backup_file.name,
                    'timestamp': timestamp,
                    'size_mb': round(size_mb, 2),
                    'path': str(backup_file),
                    'created': datetime.fromtimestamp(backup_file.stat().st_mtime)
                })
            except:
                pass
        
        return backups
    
    def restore(self, timestamp: str) -> Dict:
        """Restore from a backup"""
        backup_file = self.config.BACKUP_DIR / f"backup_{timestamp}.zip"
        
        if not backup_file.exists():
            return {
                'success': False,
                'error': f"Backup file not found: {backup_file.name}"
            }
        
        try:
            # Create restore temp directory
            restore_temp = self.config.BACKUP_DIR / f"restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            restore_temp.mkdir(exist_ok=True)
            
            # Extract backup
            shutil.unpack_archive(str(backup_file), str(restore_temp))
            
            # Restore sites
            for site_name in self.config.SITES:
                source = restore_temp / site_name
                target = self.config.SITE_PATHS[site_name]
                
                if source.exists():
                    # Backup current version first
                    if target.exists():
                        backup_current = target.parent / f"{target.name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                        if target.is_dir():
                            shutil.copytree(target, backup_current)
                    
                    # Restore
                    if target.exists():
                        shutil.rmtree(target)
                    
                    shutil.copytree(source, target)
            
            # Clean up temp directory
            shutil.rmtree(restore_temp)
            
            return {
                'success': True,
                'message': f"Successfully restored from backup {timestamp}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _cleanup_old_backups(self):
        """Keep only the most recent N backups"""
        backups = sorted(
            self.config.BACKUP_DIR.glob("backup_*.zip"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        # Delete old backups
        for old_backup in backups[self.config.BACKUP_RETENTION:]:
            try:
                old_backup.unlink()
            except:
                pass
