def rotate(l, n):
    return l[-n:] + l[:-n]

def left_pad(s, n, v='0'):
    if len(s) >= n:
        return s
    return "".join([v for _ in range(n-len(s))]) + s

class LFSR:
    def __init__(self, c, initial=None):
        self.c = c
        if not initial:
            self.state = [1 for _ in range(len(self.c))]
        else:
            self.state = initial
        assert len(self.state) == len(self.c)

    def step(self):
        total = sum(map(lambda x: x[0] * x[1], zip(self.c, self.state))) % 2
        new_state = rotate(self.state, 1)
        new_state[0] = total
        self.state = new_state
        return total

periods = set()
for n in range(2**5):
    binary = left_pad(bin(n)[2:], 5)
    initial = [int(c) for c in binary]
    assert len(initial) == 5
    cycle = initial[:]
    lfsr = LFSR([0, 0, 0, 1, 1], initial)
    for steps in range(60):
        cycle.append(lfsr.step())
        if lfsr.state == initial:
            #print(f"Period: {steps+1}, Cycle: {cycle}")
            periods.add(steps+1)
            break
print(sorted(periods))
