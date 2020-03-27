class Config:
    items = None

    def __init__(self):
        self.items = dict()

    def parse_defaults(self, lines):
        for line in lines:
            if not line.startswith('//') and len(line) > 0:
                key, _, value = line.partition(' ')
                if key and value:
                    self.items[key.strip()] = value.strip()

    def set(self, item, value):
        self.items[item] = value

    def generate(self):
        return '\n'.join('{} {}'.format(k, v) for k, v in self.items.items())
