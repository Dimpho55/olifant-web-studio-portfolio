// Website Maintenance Tool - AI-Powered Scanning & Monitoring
// Dimpho Olifant - Olifant Web Studio

const MaintenanceTool = {
    startTime: Date.now(),
    results: {
        links: { total: 0, broken: [], ok: [] },
        images: { total: 0, broken: [], ok: [] },
        performance: {},
        recommendations: []
    },
    
    log: function(message, type = 'info') {
        const container = document.getElementById('logs-container');
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;
        const timestamp = new Date().toLocaleTimeString();
        
        let icon = '📝';
        if (type === 'success') icon = '✅';
        else if (type === 'warning') icon = '⚠️';
        else if (type === 'error') icon = '❌';
        else if (type === 'info') icon = 'ℹ️';
        
        entry.textContent = `[${timestamp}] ${icon} ${message}`;
        container.appendChild(entry);
        container.scrollTop = container.scrollHeight;
    },
    
    scanLinks: async function() {
        this.log('🔗 Starting link integrity scan...', 'info');
        const links = document.querySelectorAll('a[href]');
        this.results.links.total = links.length;
        
        const brokenLinks = [];
        const validLinks = new Set();
        
        for (const link of links) {
            const href = link.getAttribute('href');
            
            // Skip anchor links and external links for now
            if (href.startsWith('#') || href.startsWith('http')) {
                validLinks.add(href);
                continue;
            }
            
            // Check internal links
            try {
                const response = await fetch(href, { method: 'HEAD' });
                if (response.ok) {
                    validLinks.add(href);
                } else {
                    brokenLinks.push({ url: href, status: response.status });
                    this.log(`❌ Broken link: ${href} (${response.status})`, 'error');
                }
            } catch (e) {
                brokenLinks.push({ url: href, status: 'UNREACHABLE' });
                this.log(`⚠️ Could not reach: ${href}`, 'warning');
            }
        }
        
        this.results.links.broken = brokenLinks;
        this.results.links.ok = Array.from(validLinks);
        
        // Update UI
        document.getElementById('link-count').textContent = this.results.links.total;
        const linkStatus = document.getElementById('link-status');
        const linkIssues = document.getElementById('link-issues');
        
        if (brokenLinks.length === 0) {
            linkStatus.textContent = 'PASS';
            linkStatus.className = 'status-badge pass';
            linkIssues.innerHTML = '<li>✅ All links are healthy!</li>';
            this.log('✅ Link scan complete: All links OK', 'success');
        } else {
            linkStatus.textContent = `${brokenLinks.length} ISSUES`;
            linkStatus.className = 'status-badge fail';
            linkIssues.innerHTML = brokenLinks.map(link => 
                `<li><span class="issue-icon">🔗</span> ${link.url} (${link.status})</li>`
            ).join('');
            this.log(`⚠️ Link scan complete: ${brokenLinks.length} broken links found`, 'warning');
        }
    },
    
    scanImages: async function() {
        this.log('🖼️ Starting image resource scan...', 'info');
        const images = document.querySelectorAll('img');
        this.results.images.total = images.length;
        
        const brokenImages = [];
        let loadedCount = 0;
        
        for (const img of images) {
            const src = img.getAttribute('src');
            if (img.complete && img.naturalHeight !== 0) {
                loadedCount++;
            } else if (img.complete && img.naturalHeight === 0) {
                brokenImages.push({
                    src: src,
                    alt: img.getAttribute('alt') || 'No alt text'
                });
                this.log(`❌ Broken image: ${src}`, 'error');
            }
        }
        
        this.results.images.broken = brokenImages;
        this.results.images.ok = loadedCount;
        
        // Update UI
        document.getElementById('image-count').textContent = loadedCount;
        const imageStatus = document.getElementById('image-status');
        const imageIssues = document.getElementById('image-issues');
        
        if (brokenImages.length === 0) {
            imageStatus.textContent = 'PASS';
            imageStatus.className = 'status-badge pass';
            imageIssues.innerHTML = `<li>✅ All ${loadedCount} images loaded successfully!</li>`;
            this.log('✅ Image scan complete: All images OK', 'success');
        } else {
            imageStatus.textContent = `${brokenImages.length} BROKEN`;
            imageStatus.className = 'status-badge fail';
            imageIssues.innerHTML = brokenImages.map(img => 
                `<li><span class="issue-icon">🖼️</span> ${img.src}<br/><small>Alt: ${img.alt}</small></li>`
            ).join('');
            this.log(`⚠️ Image scan complete: ${brokenImages.length} broken images found`, 'warning');
        }
    },
    
    scanPerformance: function() {
        this.log('⚡ Starting performance analysis...', 'info');
        
        // Page load time
        const loadTime = Date.now() - this.startTime;
        document.getElementById('load-time').textContent = loadTime + 'ms';
        
        // DOM elements
        const domCount = document.querySelectorAll('*').length;
        document.getElementById('dom-count').textContent = domCount;
        
        // Memory usage (if available)
        let memoryUsage = 'N/A';
        if (performance.memory) {
            memoryUsage = (performance.memory.usedJSHeapSize / 1048576).toFixed(2) + 'MB';
        }
        document.getElementById('memory-usage').textContent = memoryUsage;
        
        this.results.performance = {
            loadTime: loadTime,
            domCount: domCount,
            memoryUsage: memoryUsage,
            timestamp: new Date().toLocaleString()
        };
        
        this.log(`✅ Performance scan complete: Load time ${loadTime}ms, ${domCount} DOM elements`, 'success');
    },
    
    generateRecommendations: function() {
        const recommendations = [];
        
        // Link recommendations
        if (this.results.links.broken.length > 0) {
            recommendations.push({
                icon: '🔗',
                title: 'Fix Broken Links',
                description: `There are ${this.results.links.broken.length} broken links. Update them to maintain good SEO.`
            });
        }
        
        // Image recommendations
        if (this.results.images.broken.length > 0) {
            recommendations.push({
                icon: '🖼️',
                title: 'Replace Missing Images',
                description: `${this.results.images.broken.length} images are broken. Replace or remove them.`
            });
        }
        
        // Performance recommendations
        if (this.results.performance.loadTime > 3000) {
            recommendations.push({
                icon: '⚡',
                title: 'Optimize Page Load Time',
                description: `Page load time is ${this.results.performance.loadTime}ms. Consider optimizing images and assets.`
            });
        }
        
        if (this.results.performance.domCount > 1000) {
            recommendations.push({
                icon: '📊',
                title: 'Reduce DOM Complexity',
                description: `Page has ${this.results.performance.domCount} DOM elements. Consider simplifying structure.`
            });
        }
        
        // Mobile responsiveness
        const isMobile = window.innerWidth <= 768;
        if (!isMobile) {
            recommendations.push({
                icon: '📱',
                title: 'Test Mobile Responsiveness',
                description: 'Test your site on mobile devices to ensure responsive design is working properly.'
            });
        }
        
        // SEO recommendations
        recommendations.push({
            icon: '🔍',
            title: 'SEO Best Practices',
            description: 'Ensure all pages have meta descriptions, proper heading hierarchy, and alt text on images.'
        });
        
        // Security recommendations
        recommendations.push({
            icon: '🔒',
            title: 'Security Check',
            description: 'Review SSL certificate, HTTPS status, and security headers regularly.'
        });
        
        this.results.recommendations = recommendations;
        this.displayRecommendations(recommendations);
    },
    
    displayRecommendations: function(recommendations) {
        const container = document.getElementById('recommendations');
        if (recommendations.length === 0) {
            container.innerHTML = '<li>✅ No recommendations at this time. Site looks good!</li>';
            return;
        }
        
        container.innerHTML = recommendations.map(rec => 
            `<li><strong>${rec.icon} ${rec.title}</strong><br/><small>${rec.description}</small></li>`
        ).join('');
    },
    
    runFullScan: async function() {
        this.log('🚀 Running full website scan...', 'info');
        
        document.querySelectorAll('.scan-button').forEach(btn => btn.disabled = true);
        
        await this.scanLinks();
        await this.scanImages();
        this.scanPerformance();
        this.generateRecommendations();
        
        document.querySelectorAll('.scan-button').forEach(btn => btn.disabled = false);
        
        this.log('🎉 Full scan complete!', 'success');
    }
};

// Global functions for HTML onclick handlers
function scanLinks() {
    MaintenanceTool.scanLinks();
}

function scanImages() {
    MaintenanceTool.scanImages();
}

function scanPerformance() {
    MaintenanceTool.scanPerformance();
}

function runFullScan() {
    MaintenanceTool.runFullScan();
}

// Auto-run full scan on page load
document.addEventListener('DOMContentLoaded', () => {
    MaintenanceTool.log('🔧 Website Maintenance Tool loaded successfully', 'info');
    MaintenanceTool.log('Run "Full Scan" to check all systems', 'info');
});
