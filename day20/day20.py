import copy

class Module:
    low_sent = 0
    high_sent = 0
    def __init__(self, name, edges):
        self.name = name
        self.edges = edges
        self.state = False
        self.type = ''

    def receive(self, origin, pulse): pass

class FlipFlop(Module):
    def __init__(self, name, edges):
        super().__init__(name, edges)
        self.type = 'F'

    def receive(self, origin, pulse):
        if not pulse:
            self.state = not self.state
            if self.state: Module.high_sent += len(self.edges)
            else: Module.low_sent += len(self.edges)
            return [(self.state, self.name, edge) for edge in self.edges]
        return []

class Conjunction(Module):
    def __init__(self, name, edges):
        super().__init__(name, edges)
        self.type = 'C'
        self.state = {}

    def add_incoming(self, name): self.state[name] = False

    def receive(self, origin, pulse):
        if origin in self.state.keys(): self.state[origin] = pulse
        for mem in self.state.values():
            if not mem:
                Module.high_sent += len(self.edges)
                return [(True, self.name, edge) for edge in self.edges]
        Module.low_sent += len(self.edges)
        return [(False, self.name, edge) for edge in self.edges]


def day20(filename, part):
    with open(filename) as f: lines = [line.strip() for line in f.readlines()]
    modules = {}
    signals = []
    # initialize starting state
    for line in lines:
        module, dest_str = line.split(' -> ')
        dests = [dest.strip() for dest in dest_str.split(', ')]
        if module == 'broadcaster':
            for dest in dests: signals.append((False, None, dest)) # broadcast Low to dest
            continue
        name = module[1:]
        if module[0] == '%': modules[name] = FlipFlop(name, dests)
        if module[0] == '&': modules[name] = Conjunction(name, dests)
    # initialize incoming
    for module in modules.values():
        for dest in module.edges:
            if dest in modules.keys() and modules[dest].type == 'C': modules[dest].add_incoming(module.name)
    presses = 0
    sn_history = []
    #sn_history.append(copy.deepcopy(modules['sn'].state))
    while True:
        presses += 1
        inputs = copy.deepcopy(signals)
        Module.low_sent += len(inputs) + 1
        while inputs:
            outputs = []
            for pulse, origin, dest in inputs:
                if dest in modules.keys(): outputs += modules[dest].receive(origin, pulse)
                elif dest == 'rx' and not pulse and part == 2: return presses
            inputs = outputs
        if part == 1 and presses >= 1000:
            return Module.high_sent * Module.low_sent

print(day20('input', 1))
print(day20('testinput', 2))

# Experimenting with part 2 reveals that the graph structure encodes 4 binary numbers. At this point, the puzzle is
# a math problem, not a coding problem.
