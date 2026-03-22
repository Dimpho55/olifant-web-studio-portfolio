class PerformanceMonitor:
    def __init__(self, config):
        self.config = config

    def analyze(self, site):
        # Minimal stub: return conservative sample metrics
        return {
            'load_time': 800,
            'dom_count': 450,
            'total_size': 1.8,
            'css_count': 2,
            'js_count': 3
        }
