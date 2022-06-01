class Fib:
    def __init__(self):
        self.table = {}
    
    def addKeyValue(self, prefix, listNextHops):
        self.table[prefix] = listNextHops
        """ wantToAdd = {prefix, listNextHops}
        for key, value in wantToAdd.items():
            if key in self.table:
                self.table[key] = [self.table[key], value]
            else:
                self.table[key] = value """
        