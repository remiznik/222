class SymbolTable(object):

    def __init__(self):
        self._symbols = OrderedDict()

    def __str__(self):
        s = 'Symbols: {symbols}'.format(symbols = [value for value in self._symbols.values()])
        return s
    
    __repr__ = __str__

    def define(self, symbol):
        print('Define: %s' % symbol)
        self._symbols[symbol.name] = symbol
    
    def lookup(self, name):
        print('Lookup: %s' % name)
        symbol = self._symbols.get(name)
        return symbol

