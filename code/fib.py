class Fib:
    def __init__(self):
        self.table = []
    
    def add(self, prefix, listNextHops):
        for [name, nextHops] in self.table:
            if name == prefix:
                nextHops = listNextHops
                return
        self.table.append([prefix, listNextHops])
    
    def print(self):
        print(self.table)