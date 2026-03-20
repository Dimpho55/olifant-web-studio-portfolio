"""
Image Validator Module - Validates images across websites
"""

from pathlib import Path
from typing import Dict, List
from bs4 import BeautifulSoup
import os

class ImageValidator:
    def __init__(self, config):
        self.config = config
    
    def validate(self, site: str) -> Dict:
        """Validate all images in a website"""
        site_path = self.config.SITE_PATHS[site]
        results = {
            'site': site,
            'total': 0,
            'missing': [],
            'valid': [],
            'no_alt': []
        }
        
        images = self._extract_images(site_path)
        results['total'] = len(images)
        
        for img in images:
            validation = self._validate_image(site_path, img)
            
            if validation['status'] == 'missing':
                results['missing'].append(validation)
            elif validation['status'] == 'no_alt':
                results['no_alt'].append(validation)
            else:
                results['valid'].append(validation)
        
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
                                'file': str(html_file.relative_to(path))
                            })
            except Exception as e:
                pass
        
        return images
    
    def _validate_image(self, site_path: Path, img: Dict) -> Dict:
        """Validate a single image"""
        src = img['src']
        
        # Skip external URLs
        if src.startswith('http'):
            return {
                'path': src,
                'file': img['file'],
                'status': 'external',
                'alt': img['alt']
            }
        
        # Skip data URIs
        if src.startswith('data:'):
            return {
                'path': src,
                'file': img['file'],
                'status': 'data_uri',
                'alt': img['alt']
            }
        
        # Check local file
        img_path = site_path / src.lstrip('/')
        exists = img_path.exists()
        
        # Check alt text
        has_alt = bool(img['alt'].strip())
        
        if not exists:
            return {
                'path': src,
                'file': img['file'],
                'status': 'missing',
                'alt': img['alt'],
                'error': f'File not found: {img_path}'
            }
        
        if not has_alt:
            return {
                'path': src,
                'file': img['file'],
                'status': 'no_alt',
                'alt': img['alt']
            }
        
        return {
            'path': src,
            'file': img['file'],
            'status': 'valid',
            'alt': img['alt'],
            'size': os.path.getsize(img_path)
        }
