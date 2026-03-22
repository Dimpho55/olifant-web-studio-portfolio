class ImageValidator:
    def __init__(self, config):
        self.config = config

    def validate(self, site):
        # Minimal stub: return no missing images
        return {'missing': [], 'total': 0, 'no_alt': []}
