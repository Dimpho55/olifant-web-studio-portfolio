from pathlib import Path

class BackupManager:
    def __init__(self, config):
        self.config = config

    def create(self, site):
        # Create an empty marker backup file to simulate backup
        backup_dir = Path(self.config.BACKUP_DIR)
        backup_dir.mkdir(exist_ok=True)
        path = backup_dir / f"backup_{site}.zip"
        path.write_bytes(b"")
        return str(path)

    def restore(self, backup):
        # Stub: do nothing
        return True
