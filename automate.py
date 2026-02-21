"""
Olifant Web Studio - Website Automation Suite
Main CLI orchestrator for all website maintenance and deployment tasks
Created by Dimpho Olifant - February 2026
"""

import argparse
import sys
import os
from pathlib import Path
from datetime import datetime
import json
import shutil

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
        log_msg = f"[{self.timestamp}] [{level}] {message}"
        print(log_msg)
        with open(self.log_file, 'a') as f:
            f.write(log_msg + '\n')
    
    def scan_links(self, args):
        """Scan all websites for broken links"""
        self.log("🔗 Starting link integrity scan", "INFO")
        checker = LinkChecker(self.config)
        
        for site in args.sites or self.config.SITES:
            self.log(f"Scanning {site} for broken links...", "INFO")
            results = checker.scan(site)
            
            if results['broken']:
                self.log(f"❌ Found {len(results['broken'])} broken links in {site}", "WARNING")
                for link in results['broken']:
                    self.log(f"   - {link['url']} (Status: {link['status']})", "WARNING")
            else:
                self.log(f"✅ All links OK in {site} ({results['total']} links checked)", "SUCCESS")
        
        self.log("✅ Link scan complete", "SUCCESS")
    
    def scan_images(self, args):
        """Validate all images across websites"""
        self.log("🖼️ Starting image validation scan", "INFO")
        validator = ImageValidator(self.config)
        
        for site in args.sites or self.config.SITES:
            self.log(f"Validating images in {site}...", "INFO")
            results = validator.validate(site)
            
            if results['missing']:
                self.log(f"❌ Found {len(results['missing'])} missing/broken images in {site}", "WARNING")
                for img in results['missing']:
                    self.log(f"   - {img['path']} in {img['file']}", "WARNING")
            else:
                self.log(f"✅ All images OK in {site} ({results['total']} images checked)", "SUCCESS")
        
        self.log("✅ Image validation complete", "SUCCESS")
    
    def analyze_performance(self, args):
        """Analyze website performance metrics"""
        self.log("⚡ Starting performance analysis", "INFO")
        monitor = PerformanceMonitor(self.config)
        
        for site in args.sites or self.config.SITES:
            self.log(f"Analyzing performance for {site}...", "INFO")
            metrics = monitor.analyze(site)
            
            self.log(f"   📊 Page Load Time: {metrics['load_time']}ms", "INFO")
            self.log(f"   📄 DOM Elements: {metrics['dom_count']}", "INFO")
            self.log(f"   📁 Total File Size: {metrics['total_size']}MB", "INFO")
            self.log(f"   🎨 CSS Files: {metrics['css_count']}", "INFO")
            self.log(f"   ✨ JS Files: {metrics['js_count']}", "INFO")
            
            # Generate recommendations
            if metrics['load_time'] > 3000:
                self.log(f"   ⚠️ RECOMMENDATION: Optimize page load time (currently {metrics['load_time']}ms)", "WARNING")
            if metrics['dom_count'] > 1000:
                self.log(f"   ⚠️ RECOMMENDATION: Reduce DOM complexity ({metrics['dom_count']} elements)", "WARNING")
        
        self.log("✅ Performance analysis complete", "SUCCESS")
    
    def create_backup(self, args):
        """Create website backups"""
        self.log("💾 Starting backup process", "INFO")
        backup = BackupManager(self.config)
        
        for site in args.sites or self.config.SITES:
            self.log(f"Backing up {site}...", "INFO")
            backup_path = backup.create(site)
            self.log(f"✅ Backup created: {backup_path}", "SUCCESS")
    
    def restore_backup(self, args):
        """Restore from backup"""
        if not args.backup:
            self.log("❌ Backup path required (--backup)", "ERROR")
            return
        
        self.log(f"🔄 Restoring from backup: {args.backup}", "INFO")
        backup = BackupManager(self.config)
        backup.restore(args.backup)
        self.log("✅ Restore complete", "SUCCESS")
    
    def sync_files(self, args):
        """Sync files between local and remote"""
        self.log("🔄 Starting file synchronization", "INFO")
        sync = FileSync(self.config)
        
        direction = args.direction or "local_to_remote"
        for site in args.sites or self.config.SITES:
            self.log(f"Syncing {site} ({direction})...", "INFO")
            sync.sync(site, direction)
            self.log(f"✅ {site} synced", "SUCCESS")
    
    def run_full_audit(self, args):
        """Run comprehensive website audit"""
        self.log("🔍 Starting comprehensive website audit", "INFO")
        self.log("=" * 60, "INFO")
        
        # Run all scans
        self.scan_links(args)
        print()
        self.scan_images(args)
        print()
        self.analyze_performance(args)
        
        self.log("=" * 60, "INFO")
        self.log("🎉 Full audit complete! Check logs for details.", "SUCCESS")
    
    def generate_report(self, args):
        """Generate comprehensive HTML report"""
        self.log("📋 Generating website audit report", "INFO")
        
        report_data = {
            'timestamp': self.timestamp,
            'sites': {},
        }
        
        checker = LinkChecker(self.config)
        validator = ImageValidator(self.config)
        monitor = PerformanceMonitor(self.config)
        
        for site in args.sites or self.config.SITES:
            report_data['sites'][site] = {
                'links': checker.scan(site),
                'images': validator.validate(site),
                'performance': monitor.analyze(site),
            }
        
        report_file = Path("reports") / f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        self.log(f"✅ Report generated: {report_file}", "SUCCESS")

def main():
    parser = argparse.ArgumentParser(
        description='Olifant Web Studio - Website Automation Suite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python automate.py audit                              # Run full audit
  python automate.py check-links                        # Check all links
  python automate.py check-images --sites newlysly      # Check images on Newlysly
  python automate.py analyze-performance                # Analyze performance
  python automate.py backup                             # Create backups
  python automate.py restore --backup path/to/backup    # Restore from backup
  python automate.py sync --direction local_to_remote   # Sync files
  python automate.py report                             # Generate audit report
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Common argument
    def add_sites_arg(subparser):
        subparser.add_argument(
            '--sites',
            nargs='+',
            choices=['main', 'newlysly', 'regcorp'],
            help='Websites to process (default: all)'
        )
    
    # Audit command
    audit = subparsers.add_parser('audit', help='Run comprehensive website audit')
    add_sites_arg(audit)
    
    # Link checker
    links = subparsers.add_parser('check-links', help='Check for broken links')
    add_sites_arg(links)
    
    # Image validator
    images = subparsers.add_parser('check-images', help='Validate images')
    add_sites_arg(images)
    
    # Performance analyzer
    perf = subparsers.add_parser('analyze-performance', help='Analyze performance metrics')
    add_sites_arg(perf)
    
    # Backup
    backup = subparsers.add_parser('backup', help='Create website backups')
    add_sites_arg(backup)
    
    # Restore
    restore = subparsers.add_parser('restore', help='Restore from backup')
    restore.add_argument('--backup', required=True, help='Path to backup file')
    
    # Sync
    sync = subparsers.add_parser('sync', help='Sync files between local and remote')
    add_sites_arg(sync)
    sync.add_argument(
        '--direction',
        choices=['local_to_remote', 'remote_to_local'],
        help='Sync direction (default: local_to_remote)'
    )
    
    # Report
    report = subparsers.add_parser('report', help='Generate audit report')
    add_sites_arg(report)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    automation = WebsiteAutomation()
    
    # Route commands
    if args.command == 'audit':
        automation.run_full_audit(args)
    elif args.command == 'check-links':
        automation.scan_links(args)
    elif args.command == 'check-images':
        automation.scan_images(args)
    elif args.command == 'analyze-performance':
        automation.analyze_performance(args)
    elif args.command == 'backup':
        automation.create_backup(args)
    elif args.command == 'restore':
        automation.restore_backup(args)
    elif args.command == 'sync':
        automation.sync_files(args)
    elif args.command == 'report':
        automation.generate_report(args)

if __name__ == '__main__':
    main()
