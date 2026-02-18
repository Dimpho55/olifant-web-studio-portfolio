"""
Link Checker Module - Scans for broken links across websites
"""

import requests
from pathlib import Path
from typing import Dict, List
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

class LinkChecker:
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Olifant-Site-Automation/1.0'})
    
    def scan(self, site: str) -> Dict:
        """Scan website for broken links"""
        site_path = self.config.SITE_PATHS[site]
        results = {
            'site': site,
            'total': 0,
            'broken': [],
            'external': [],
            'valid': [],
            'anchors': []
        }
        
        links = self._extract_links(site_path)
        results['total'] = len(links)
        
        for link in links:
            status = self._check_link(link, site_path)
            
            if status['type'] == 'broken':
                results['broken'].append(status)
            elif status['type'] == 'external':
                results['external'].append(status)
            elif status['type'] == 'anchor':
                results['anchors'].append(status)
            else:
                results['valid'].append(status)
        
        return results
    
    def _extract_links(self, path: Path) -> List[str]:
        """Extract all links from HTML files"""
        links = set()
        html_files = list(path.glob('**/*.html'))
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f, 'html.parser')
                    
                    for tag in soup.find_all(['a', 'script', 'link', 'img']):
                        href = tag.get('href') or tag.get('src')
                        if href and href.strip():
                            links.add(href)
            except Exception as e:
                pass
        
        return list(links)
    
    def _check_link(self, url: str, site_path: Path) -> Dict:
        """Check if a link is valid"""
        # Skip anchors
        if url.startswith('#'):
            return {'url': url, 'type': 'anchor', 'status': 200}
        
        # Skip javascript
        if url.startswith('javascript:'):
            return {'url': url, 'type': 'javascript', 'status': 200}
        
        # Skip mailto
        if url.startswith('mailto:'):
            return {'url': url, 'type': 'mailto', 'status': 200}
        
        # External links
        if url.startswith('http'):
            try:
                response = self.session.head(url, timeout=self.config.LINK_TIMEOUT, allow_redirects=True)
                return {
                    'url': url,
                    'type': 'external' if response.status_code < 400 else 'broken',
                    'status': response.status_code,
                    'valid': response.status_code < 400
                }
            except Exception as e:
                return {'url': url, 'type': 'broken', 'status': 'ERROR', 'error': str(e), 'valid': False}
        
        # Internal links
        if url.startswith('/'):
            url = '.' + url
        
        # Handle relative paths
        full_path = (site_path / url).resolve()
        
        # Check if file exists
        try:
            exists = full_path.exists()
        except:
            exists = False
        
        return {
            'url': url,
            'type': 'valid' if exists else 'broken',
            'status': 200 if exists else 404,
            'exists': exists
        }
