"""
Olifant Web Studio - Website Automation Suite
Main CLI orchestrator for all website maintenance and deployment tasks
Created by Dimpho Olifant - February 2024
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
import json

# Import custom modules
from modules.link_checker import LinkChecker
from modules.image_validator import ImageValidator
from modules.performance_monitor import PerformanceMonitor
from modules.backup_manager import BackupManager
from modules.file_sync import FileSync
from config import Config

class WebsiteAutomation:
    def __init__(self):
        self.config = Config()
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_file = Path("logs") / f"automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.log_file.parent.mkdir(exist_ok=True)
        
    def log(self, message, level="INFO"):
        """Log messages to file and console"""
        log_msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{level}] {message}"
        print(log_msg)
        with open(self.log_file, 'a') as f:
            f.write(log_msg + '\n')
    
    def scan_links(self, args):
        """Scan all websites for broken links"""
        self.log("🔗 Starting link integrity scan", "INFO")
        checker = LinkChecker(self.config)
        
        sites = args.sites if args.sites else self.config.SITES
        results = {}
        
        for site in sites:
            self.log(f"Scanning {site} for broken links...", "INFO")
            site_results = checker.scan(site)
            results[site] = site_results
            
            if site_results['broken']:
                self.log(f"❌ Found {len(site_results['broken'])} broken links in {site}", "WARNING")
                for link in site_results['broken']:
                    self.log(f"   - {link['url']}", "WARNING")
            else:
                self.log(f"✓ All links valid in {site}", "INFO")
            
            self.log(f"  Valid: {len(site_results['valid'])}, Broken: {len(site_results['broken'])}, External: {len(site_results['external'])}", "INFO")
        
        return results
    
    def scan_images(self, args):
        """Scan all websites for image issues"""
        self.log("🖼️  Starting image validation scan", "INFO")
        validator = ImageValidator(self.config)
        
        sites = args.sites if args.sites else self.config.SITES
        results = {}
        
        for site in sites:
            self.log(f"Validating images in {site}...", "INFO")
            image_results = validator.validate(site)
            results[site] = image_results
            
            if image_results['missing']:
                self.log(f"❌ Found {len(image_results['missing'])} missing images in {site}", "WARNING")
            if image_results['no_alt']:
                self.log(f"⚠️  Found {len(image_results['no_alt'])} images without alt text in {site}", "WARNING")
            
            self.log(f"  Valid: {len(image_results['valid'])}, Missing: {len(image_results['missing'])}, No alt: {len(image_results['no_alt'])}", "INFO")
        
        return results
    
    def analyze_performance(self, args):
        """Analyze website performance"""
        self.log("⚡ Starting performance analysis", "INFO")
        monitor = PerformanceMonitor(self.config)
        
        sites = args.sites if args.sites else self.config.SITES
        results = {}
        
        for site in sites:
            self.log(f"Analyzing performance for {site}...", "INFO")
            metrics = monitor.analyze(site)
            results[site] = metrics
            
            status = "🟢 GOOD" if metrics['load_time'] < 2000 else "🟡 OK" if metrics['load_time'] < 3000 else "🔴 SLOW"
            self.log(f"  {status} Load time: {metrics['load_time']}ms", "INFO")
            self.log(f"  Files: HTML({metrics['html_count']}) CSS({metrics['css_count']}) JS({metrics['js_count']}) IMG({metrics['image_count']})", "INFO")
            self.log(f"  Size: {metrics['total_size']:.2f}MB (HTML: {metrics['html_size']:.2f}MB, CSS: {metrics['css_size']:.2f}MB, JS: {metrics['js_size']:.2f}MB, Images: {metrics['image_size']:.2f}MB)", "INFO")
            
            for rec in metrics['recommendations']:
                self.log(f"  [{rec['severity']}] {rec['message']}", "INFO")
        
        return results
    
    def create_backup(self, args):
        """Create backup of websites"""
        self.log("💾 Creating backup", "INFO")
        manager = BackupManager(self.config)
        
        result = manager.create(args.sites if args.sites else None)
        
        if result['success']:
            self.log(f"✓ Backup created: {result['backup']} ({result['size_mb']}MB)", "INFO")
        else:
            self.log(f"❌ Backup failed: {result['error']}", "ERROR")
        
        return result
    
    def list_backups(self, args):
        """List all backups"""
        self.log("📋 Listing backups", "INFO")
        manager = BackupManager(self.config)
        
        backups = manager.list_backups()
        
        if not backups:
            self.log("No backups found", "INFO")
            return []
        
        for backup in backups:
            self.log(f"  {backup['timestamp']} ({backup['size_mb']}MB) - {backup['file']}", "INFO")
        
        return backups
    
    def restore_backup(self, args):
        """Restore from backup"""
        self.log(f"♻️  Restoring from backup: {args.timestamp}", "INFO")
        manager = BackupManager(self.config)
        
        result = manager.restore(args.timestamp)
        
        if result['success']:
            self.log(f"✓ {result['message']}", "INFO")
        else:
            self.log(f"❌ Restore failed: {result['error']}", "ERROR")
        
        return result
    
    def sync_files(self, args):
        """Sync files to remote server"""
        self.log("🔄 Starting file sync", "INFO")
        syncer = FileSync(self.config)
        
        if args.direction == 'push':
            result = syncer.sync_to_remote(args)
        else:
            result = syncer.sync_from_remote(args)
        
        if result.get('success'):
            self.log(f"✓ {result['message']}", "INFO")
        else:
            self.log(f"❌ Sync failed: {result.get('error', 'Unknown error')}", "ERROR")
        
        return result
    
    def run_full_audit(self, args):
        """Run complete audit of all websites"""
        self.log("🔍 Starting full system audit", "INFO")
        self.log("=" * 50, "INFO")
        
        audit_results = {
            'timestamp': datetime.now().isoformat(),
            'sites': {}
        }
        
        # Get sites to audit
        sites = args.sites if args.sites else self.config.SITES
        
        for site in sites:
            self.log(f"\n📌 Auditing {site.upper()}", "INFO")
            self.log("-" * 50, "INFO")
            
            # Create args object for each test
            class Args:
                pass
            
            scan_args = Args()
            scan_args.sites = [site]
            
            # Run tests
            link_results = self.scan_links(scan_args)
            image_results = self.scan_images(scan_args)
            perf_results = self.analyze_performance(scan_args)
            
            audit_results['sites'][site] = {
                'links': link_results.get(site, {}),
                'images': image_results.get(site, {}),
                'performance': perf_results.get(site, {})
            }
        
        self.log("\n" + "=" * 50, "INFO")
        self.log("✓ Audit complete", "INFO")
        
        return audit_results
    
    def generate_report(self, args):
        """Generate HTML report of last scan"""
        self.log("📄 Generating report", "INFO")
        
        report_dir = self.config.REPORT_DIR
        report_dir.mkdir(exist_ok=True)
        
        report_file = report_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Olifant Web Studio - Audit Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }
        .site { background: white; margin: 20px 0; padding: 20px; border-radius: 5px; border-left: 4px solid #3498db; }
        .section { margin: 15px 0; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
        .metric { background: #ecf0f1; padding: 15px; border-radius: 5px; }
        .metric-value { font-size: 24px; font-weight: bold; color: #2c3e50; }
        .metric-label { color: #7f8c8d; font-size: 12px; }
        .warning { color: #e74c3c; }
        .success { color: #27ae60; }
        .info { background: #e8f4f8; padding: 10px; margin: 10px 0; border-radius: 3px; border-left: 3px solid #3498db; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Olifant Web Studio - System Audit Report</h1>
        <p>Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
    </div>
    
    <div class="site">
        <h2>Audit Summary</h2>
        <p>This report contains the results of a full system audit of all websites.</p>
        <p>Check the logs directory for detailed scan results.</p>
        <div class="info">
            <strong>Note:</strong> Run 'python automate.py audit' for latest results.
        </div>
    </div>
    
    <footer style="text-align: center; color: #7f8c8d; margin-top: 40px; border-top: 1px solid #ecf0f1; padding-top: 20px;">
        <p>Olifant Web Studio Automation Suite | Developed by Dimpho Olifant</p>
    </footer>
</body>
</html>
        """
        
        with open(report_file, 'w') as f:
            f.write(html_content)
        
        self.log(f"✓ Report generated: {report_file}", "INFO")
        return {'file': str(report_file)}

def main():
    parser = argparse.ArgumentParser(
        description='Olifant Web Studio - Website Automation Suite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python automate.py audit                      # Full system audit
  python automate.py check-links                # Scan all sites for broken links
  python automate.py check-images --sites main  # Check images on main site only
  python automate.py analyze-performance        # Analyze all sites
  python automate.py backup                     # Create backup
  python automate.py backup --list              # List backups
  python automate.py restore timestamp          # Restore from backup
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Audit command
    audit_parser = subparsers.add_parser('audit', help='Run full system audit')
    audit_parser.add_argument('--sites', nargs='+', help='Specific sites to audit', metavar='SITE')
    
    # Link check command
    links_parser = subparsers.add_parser('check-links', help='Check for broken links')
    links_parser.add_argument('--sites', nargs='+', help='Specific sites to check', metavar='SITE')
    links_parser.add_argument('--include-external', action='store_true', help='Include external links')
    
    # Image check command
    images_parser = subparsers.add_parser('check-images', help='Validate images')
    images_parser.add_argument('--sites', nargs='+', help='Specific sites to check', metavar='SITE')
    
    # Performance analysis command
    perf_parser = subparsers.add_parser('analyze-performance', help='Analyze performance')
    perf_parser.add_argument('--sites', nargs='+', help='Specific sites to analyze', metavar='SITE')
    
    # Backup commands
    backup_parser = subparsers.add_parser('backup', help='Backup operations')
    backup_parser.add_argument('--list', action='store_true', help='List backups')
    backup_parser.add_argument('--sites', nargs='+', help='Specific sites to backup', metavar='SITE')
    
    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore from backup')
    restore_parser.add_argument('timestamp', help='Backup timestamp (YYYY-MM-DD_HH-MM-SS)')
    
    # Sync command
    sync_parser = subparsers.add_parser('sync', help='Sync files to remote')
    sync_parser.add_argument('--remote-host', help='Remote server hostname', default=None)
    sync_parser.add_argument('--remote-user', help='Remote server username', default=None)
    sync_parser.add_argument('--remote-path', help='Remote server path', default=None)
    sync_parser.add_argument('--direction', choices=['push', 'pull'], default='push', help='Sync direction')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate HTML report')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        automation = WebsiteAutomation()
        
        if args.command == 'audit':
            automation.run_full_audit(args)
        elif args.command == 'check-links':
            automation.scan_links(args)
        elif args.command == 'check-images':
            automation.scan_images(args)
        elif args.command == 'analyze-performance':
            automation.analyze_performance(args)
        elif args.command == 'backup':
            if args.list:
                automation.list_backups(args)
            else:
                automation.create_backup(args)
        elif args.command == 'restore':
            automation.restore_backup(args)
        elif args.command == 'sync':
            automation.sync_files(args)
        elif args.command == 'report':
            automation.generate_report(args)
        else:
            parser.print_help()
            return 1
        
        return 0
    
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
