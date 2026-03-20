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
            metrics['html_size'] += f.stat().st_size / (1024 * 1024)  # MB
        
        for f in css_files:
            metrics['css_size'] += f.stat().st_size / (1024 * 1024)
        
        for f in js_files:
            metrics['js_size'] += f.stat().st_size / (1024 * 1024)
        
        for f in image_files:
            metrics['image_size'] += f.stat().st_size / (1024 * 1024)
        
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
            except Exception:
                pass
        
        return total
    
    def _estimate_load_time(self, metrics: Dict) -> int:
        """Estimate page load time based on file sizes"""
        # Very rough estimate: 1MB ≈ 500ms (assuming 2Mbps connection)
        base_time = int(metrics['total_size'] * 500)
        
        # Add overhead for number of requests
        request_overhead = (metrics['html_count'] + metrics['css_count'] + 
                           metrics['js_count'] + metrics['image_count']) * 50
        
        return base_time + request_overhead
    
    def _generate_recommendations(self, metrics: Dict) -> list:
        """Generate performance recommendations"""
        recommendations = []
        
        if metrics['load_time'] > 3000:
            recommendations.append({
                'severity': 'warning',
                'message': f"⚠️ Slow load time ({metrics['load_time']}ms). Consider optimizing images and minifying CSS/JS."
            })
        
        if metrics['image_size'] > 10:
            recommendations.append({
                'severity': 'warning',
                'message': f"🖼️ Large images ({metrics['image_size']:.2f}MB). Use WebP or compress images."
            })
        
        if metrics['dom_count'] > 1500:
            recommendations.append({
                'severity': 'warning',
                'message': f"📊 High DOM complexity ({metrics['dom_count']} elements). Simplify HTML structure."
            })
        
        if metrics['css_count'] > 5:
            recommendations.append({
                'severity': 'info',
                'message': f"📋 Multiple CSS files ({metrics['css_count']}). Consider consolidating."
            })
        
        if metrics['js_count'] > 5:
            recommendations.append({
                'severity': 'info',
                'message': f"✨ Multiple JS files ({metrics['js_count']}). Consider bundling."
            })
        
        if not recommendations:
            recommendations.append({
                'severity': 'success',
                'message': "✅ Performance looks good!"
            })
        
        return recommendations
