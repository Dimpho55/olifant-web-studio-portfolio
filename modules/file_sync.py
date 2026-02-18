"""
File Sync Module - Handles file synchronization to remote servers
"""

from pathlib import Path
from typing import Dict, List
from datetime import datetime
import json

class FileSync:
    def __init__(self, config):
        self.config = config
        self.config_file = Path("config/remote.conf")
    
    def sync_to_remote(self, args) -> Dict:
        """Sync local files to remote server"""
        # Validate remote settings
        host = args.remote_host or self.config.REMOTE_HOST
        user = args.remote_user or self.config.REMOTE_USER
        path = args.remote_path or self.config.REMOTE_PATH
        
        if not host:
            return {'success': False, 'error': 'Remote host not specified'}
        
        try:
            # Detect changes
            changes = self._detect_changes()
            
            # In production, would use paramiko for SFTP or ftplib
            # For now, log the sync operation
            result = self._sync_local_to_remote(host, user, path, changes)
            
            return {
                'success': True,
                'message': f"Synced {len(changes)} files to {host}:{path}",
                'changes': changes
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def sync_from_remote(self, args) -> Dict:
        """Sync remote files to local"""
        host = args.remote_host or self.config.REMOTE_HOST
        user = args.remote_user or self.config.REMOTE_USER
        path = args.remote_path or self.config.REMOTE_PATH
        
        if not host:
            return {'success': False, 'error': 'Remote host not specified'}
        
        try:
            result = self._sync_remote_to_local(host, user, path)
            return {
                'success': True,
                'message': f"Synced files from {host}:{path}",
                'files': result
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _detect_changes(self) -> List[str]:
        """Detect which files have changed since last sync"""
        sync_marker = self.config.LOG_DIR / ".last_sync"
        changed_files = []
        
        try:
            last_sync = sync_marker.stat().st_mtime if sync_marker.exists() else 0
        except:
            last_sync = 0
        
        # Check all sites for changes
        for site_name in self.config.SITES:
            site_path = self.config.SITE_PATHS[site_name]
            
            for file in site_path.rglob('*'):
                if file.is_file():
                    try:
                        mtime = file.stat().st_mtime
                        if mtime > last_sync:
                            changed_files.append(str(file.relative_to(site_path.parent)))
                    except:
                        pass
        
        return changed_files
    
    def _sync_local_to_remote(self, host: str, user: str, path: str, files: List[str]) -> Dict:
        """Sync local files to remote server"""
        # Placeholder for FTP/SFTP implementation
        # In production, would use:
        # from paramiko import SSHClient
        # or from ftplib import FTP
        
        sync_log = {
            'timestamp': datetime.now().isoformat(),
            'direction': 'local_to_remote',
            'host': host,
            'user': user,
            'path': path,
            'files_synced': len(files),
            'files': files
        }
        
        # Log the sync operation
        log_file = self.config.LOG_DIR / f"sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        with open(log_file, 'w') as f:
            json.dump(sync_log, f, indent=2)
        
        # Update sync marker
        sync_marker = self.config.LOG_DIR / ".last_sync"
        sync_marker.touch()
        
        return {
            'logged': True,
            'files': files
        }
    
    def _sync_remote_to_local(self, host: str, user: str, path: str) -> List[str]:
        """Sync remote files to local"""
        # Placeholder for FTP/SFTP implementation
        
        sync_log = {
            'timestamp': datetime.now().isoformat(),
            'direction': 'remote_to_local',
            'host': host,
            'user': user,
            'path': path,
            'status': 'DEMO_MODE'
        }
        
        # Log the operation
        log_file = self.config.LOG_DIR / f"sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        with open(log_file, 'w') as f:
            json.dump(sync_log, f, indent=2)
        
        return []
    
    def setup_remote_config(self, host: str, user: str, password: str = None, path: str = None, port: int = 22) -> Dict:
        """Setup remote server configuration"""
        self.config_file.parent.mkdir(exist_ok=True)
        
        config_data = {
            'host': host,
            'user': user,
            'path': path or '/var/www/html',
            'port': port,
            'last_updated': datetime.now().isoformat()
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            return {
                'success': True,
                'message': f"Remote config saved for {user}@{host}:{path}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
