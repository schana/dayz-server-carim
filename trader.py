class Config:
    def __init__(self):
        self.traders = list()

    def generate(self):
        result = '<CurrencyName> #tm_ruble\n'
        result += '\n'.join('<Currency> MoneyRuble{i}, {i}'.format(i=i) for i in (1, 5, 10, 25, 50, 100))
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
        self.items.sort(key=lambda i: (i.buy, i.name))
        result = '<Category> {}\n'.format(self.name) + '\n'.join(i.generate() for i in self.items)
        return result


class Item:
    def __init__(self, name, quantity, buy, sell):
        self.name = name
        self.quantity = quantity
        self.buy = buy
        self.sell = sell

    def generate(self):
        return ','.join(str(s) for s in (self.name, self.quantity, self.buy, self.sell))


class Weapon(Item):
    def __init__(self, name, buy, sell):
        super().__init__(name, 'W', buy, sell)


class Magazine(Item):
    def __init__(self, name, buy, sell):
        super().__init__(name, 'M', buy, sell)


class Steak(Item):
    def __init__(self, name, buy, sell):
        super().__init__(name, 'S', buy, sell)


class Singular(Item):
    def __init__(self, name, buy, sell):
        super().__init__(name, '*', buy, sell)


class Vehicle(Item):
    def __init__(self, name, buy, sell):
        super().__init__(name, 'V', buy, sell)

'''
// Item Classname, Quantity, Buyvalue, Sellvalue

* means max value
V means Vehicle
VNK means Vehicle without Key
K means Key Duplication

Buyvalue -1 means it can not be bought
Sellvalue -1 means it can not be sold
'''






