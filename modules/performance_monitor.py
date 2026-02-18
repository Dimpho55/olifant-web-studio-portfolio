"""
Performance Monitor Module - Analyzes website performance metrics
"""

from pathlib import Path
from typing import Dict
from bs4 import BeautifulSoup
import os

class PerformanceMonitor:
    def __init__(self, config):
        self.config = config
    
    def analyze(self, site: str) -> Dict:
        """Analyze website performance metrics"""
        site_path = self.config.SITE_PATHS[site]
        
        metrics = {
            'site': site,
            'load_time': 0,
            'dom_count': 0,
            'total_size': 0.0,
            'html_size': 0.0,
            'css_size': 0.0,
            'js_size': 0.0,
            'image_size': 0.0,
            'html_count': 0,
            'css_count': 0,
            'js_count': 0,
            'image_count': 0,
            'recommendations': []
        }
        
        # Count and measure files
        html_files = list(site_path.glob('**/*.html'))
        css_files = list(site_path.glob('**/*.css'))
        js_files = list(site_path.glob('**/*.js'))
        image_files = list(site_path.glob('**/*.{png,jpg,jpeg,gif,svg,webp}'))
        
        metrics['html_count'] = len(html_files)
        metrics['css_count'] = len(css_files)
        metrics['js_count'] = len(js_files)
        metrics['image_count'] = len(image_files)
        
        # Calculate sizes
        for f in html_files:
            try:
                metrics['html_size'] += f.stat().st_size / (1024 * 1024)  # MB
            except:
                pass
        
        for f in css_files:
            try:
                metrics['css_size'] += f.stat().st_size / (1024 * 1024)
            except:
                pass
        
        for f in js_files:
            try:
                metrics['js_size'] += f.stat().st_size / (1024 * 1024)
            except:
                pass
        
        for f in image_files:
            try:
                metrics['image_size'] += f.stat().st_size / (1024 * 1024)
            except:
                pass
        
        metrics['total_size'] = round(
            metrics['html_size'] + metrics['css_size'] + 
            metrics['js_size'] + metrics['image_size'], 2
        )
        
        # Estimate DOM count
        metrics['dom_count'] = self._count_dom_elements(html_files)
        
        # Estimate load time (rough calculation)
        metrics['load_time'] = self._estimate_load_time(metrics)
        
        # Generate recommendations
        metrics['recommendations'] = self._generate_recommendations(metrics)
        
        return metrics
    
    def _count_dom_elements(self, html_files: list) -> int:
        """Count total DOM elements across all HTML files"""
        total = 0
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f, 'html.parser')
                    total += len(soup.find_all())
            except:
                pass
        
        return total
    
    def _estimate_load_time(self, metrics: Dict) -> int:
        """Estimate page load time in milliseconds"""
        # Simple formula: base time + file size + request overhead
        base_time = 200  # ms
        size_time = int(metrics['total_size'] * 500)  # 500ms per MB
        request_time = (metrics['html_count'] + metrics['css_count'] + 
                       metrics['js_count'] + metrics['image_count']) * 50  # 50ms per request
        
        return base_time + size_time + request_time
    
    def _generate_recommendations(self, metrics: Dict) -> list:
        """Generate performance recommendations"""
        recommendations = []
        
        # Load time recommendations
        if metrics['load_time'] > self.config.LOAD_TIME_WARNING:
            recommendations.append({
                'severity': 'HIGH',
                'message': f"Load time is {metrics['load_time']}ms (warning: {self.config.LOAD_TIME_WARNING}ms)",
                'suggestions': [
                    'Minify CSS and JavaScript files',
                    'Compress and optimize images (use WebP format)',
                    'Enable browser caching',
                    'Consider lazy loading for images'
                ]
            })
        
        # DOM complexity
        if metrics['dom_count'] > self.config.DOM_COUNT_WARNING:
            recommendations.append({
                'severity': 'MEDIUM',
                'message': f"DOM has {metrics['dom_count']} elements (warning: {self.config.DOM_COUNT_WARNING})",
                'suggestions': [
                    'Simplify HTML structure',
                    'Remove unnecessary nested divs',
                    'Consider virtual scrolling for dynamic content'
                ]
            })
        
        # Image size
        if metrics['image_size'] > self.config.IMAGE_SIZE_WARNING:
            recommendations.append({
                'severity': 'MEDIUM',
                'message': f"Total image size is {metrics['image_size']:.2f}MB",
                'suggestions': [
                    'Use modern image formats (WebP, AVIF)',
                    'Compress images using TinyPNG or similar',
                    'Use responsive images (srcset)',
                    'Consider using SVG for icons'
                ]
            })
        
        # CSS files
        if metrics['css_count'] > 3:
            recommendations.append({
                'severity': 'LOW',
                'message': f"Found {metrics['css_count']} CSS files",
                'suggestions': [
                    'Consolidate CSS files to reduce requests',
                    'Remove unused CSS rules'
                ]
            })
        
        # JS files
        if metrics['js_count'] > 5:
            recommendations.append({
                'severity': 'LOW',
                'message': f"Found {metrics['js_count']} JavaScript files",
                'suggestions': [
                    'Consolidate or split strategically',
                    'Use code splitting for large applications',
                    'Defer non-critical JavaScript'
                ]
            })
        
        if not recommendations:
            recommendations.append({
                'severity': 'INFO',
                'message': 'Performance is good!',
                'suggestions': ['Continue monitoring for regressions']
            })
        
        return recommendations
