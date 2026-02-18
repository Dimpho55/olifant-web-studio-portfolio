"""
Image Validator Module - Validates images in HTML files
"""

from pathlib import Path
from typing import Dict, List
from bs4 import BeautifulSoup

class ImageValidator:
    def __init__(self, config):
        self.config = config
    
    def validate(self, site: str) -> Dict:
        """Validate all images in a website"""
        site_path = self.config.SITE_PATHS[site]
        results = {
            'site': site,
            'total': 0,
            'valid': [],
            'missing': [],
            'no_alt': [],
            'large_files': []
        }
        
        images = self._extract_images(site_path)
        results['total'] = len(images)
        
        for img in images:
            status = self._check_image(img, site_path)
            
            if status['type'] == 'missing':
                results['missing'].append(status)
            elif status['type'] == 'no_alt':
                results['no_alt'].append(status)
            elif status['type'] == 'large':
                results['large_files'].append(status)
            else:
                results['valid'].append(status)
        
        return results
    
    def _extract_images(self, path: Path) -> List[Dict]:
        """Extract all images from HTML files"""
        images = []
        html_files = list(path.glob('**/*.html'))
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f, 'html.parser')
                    
                    for img in soup.find_all('img'):
                        src = img.get('src')
                        alt = img.get('alt', '')
                        
                        if src:
                            images.append({
                                'src': src,
                                'alt': alt,
                                'file': str(html_file),
                                'line': img.sourceline or 'unknown'
                            })
            except Exception as e:
                pass
        
        return images
    
    def _check_image(self, img: Dict, site_path: Path) -> Dict:
        """Check if an image file exists and is valid"""
        src = img['src']
        alt = img['alt']
        
        # Skip data URIs and external URLs for now
        if src.startswith('data:') or src.startswith('http'):
            return {'type': 'valid', **img, 'size_mb': 0}
        
        # Handle paths
        if src.startswith('/'):
            src = '.' + src
        
        # Resolve the path
        try:
            full_path = (site_path / src).resolve()
            exists = full_path.exists()
        except:
            exists = False
        
        if not exists:
            return {'type': 'missing', **img, 'error': 'File not found'}
        
        # Check file size
        try:
            size_bytes = full_path.stat().st_size
            size_mb = size_bytes / (1024 * 1024)
            
            if size_mb > 5:  # Warn about large images
                return {
                    'type': 'large',
                    **img,
                    'size_mb': round(size_mb, 2),
                    'warning': f'Large image: {round(size_mb, 2)}MB'
                }
        except:
            pass
        
        # Check alt text
        if not alt or alt.strip() == '':
            return {'type': 'no_alt', **img, 'warning': 'Missing alt text (accessibility issue)'}
        
        return {'type': 'valid', **img, 'size_mb': round(size_mb, 2) if size_mb else 0}
