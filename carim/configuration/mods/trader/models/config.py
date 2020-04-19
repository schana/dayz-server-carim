class Config:
    def __init__(self):
        self.traders = list()

    def generate(self):
        result = '<CurrencyName> #tm_ruble\n'
        result += '\n'.join('<Currency> MoneyRuble{i}, {i}'.format(i=i) for i in (1, 10, 100))
        result += '\n'
        result += '\n'.join(t.generate() for t in self.traders)
        result += '\n<FileEnd>'
        return result


class Trader:
    def __init__(self, name):
        self.name = name
        self.categories = list()

    def generate(self):
        result = '<Trader> {}\n'.format(self.name)
        result += '\n'.join(c.generate() for c in self.categories)
        return result


class Category:
    def __init__(self, name):
        self.name = name
        self.items = list()

    def generate(self):
        self.items.sort(key=lambda i: (i.name, i.buy))
        result = '<Category> {}\n'.format(self.name) + '\n'.join(i.generate() for i in self.items)
        return result

    def __contains__(self, item):
        return item in self.items


class Item:
    def __init__(self, name, buy, sell, quantity):
        self.name = name
        self.quantity = quantity
        self.buy = buy
        self.sell = sell

    def generate(self):
        return ','.join(str(s) for s in (self.name, self.quantity, self.buy, self.sell))

    def __eq__(self, other):
        if isinstance(other, Item):
            return other.name == self.name
        return False


class Weapon(Item):
    def __init__(self, name, buy, sell, quantity='W'):
        super().__init__(name, buy, sell, quantity)


class Magazine(Item):
    def __init__(self, name, buy, sell, quantity='M'):
        super().__init__(name, buy, sell, quantity)


class Steak(Item):
    def __init__(self, name, buy, sell, quantity='S'):
        super().__init__(name, buy, sell, quantity)


class Singular(Item):
    def __init__(self, name, buy, sell, quantity='*'):
        super().__init__(name, buy, sell, quantity)


class Vehicle(Item):
    def __init__(self, name, buy, sell, quantity='V'):
        super().__init__(name, buy, sell, quantity)


'''
// Item Classname, Quantity, Buyvalue, Sellvalue

* means max value
V means Vehicle
VNK means Vehicle without Key
K means Key Duplication

Buyvalue -1 means it can not be bought
Sellvalue -1 means it can not be sold
'''
