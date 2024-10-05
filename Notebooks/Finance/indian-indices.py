class Index:
    def __init__(self, moniker, name, data):
        self.moniker = moniker
        self.name = name
        self.data = data

    def __repr__(self):
        return f'Index({self.name}, {self.data})'

    def __str__(self):
        return f'{self.name}'
