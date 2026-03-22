from pathlib import Path

class LinkChecker:
    def __init__(self, config):
        self.config = config

    def scan(self, site):
        # Minimal stub: scan local HTML files for simple link count
        site_path = self.config.SITE_PATHS.get(site)
        total = 0
        broken = []
        return {'broken': broken, 'total': total, 'external': 0}
