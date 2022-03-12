import datetime, os;

ts = datetime.datetime.now().timestamp()
pid = os.getpid()
x = ts * pid

def LCG(a, c, m):
    """ Linear Congruential Generator """
    global x
    while True:
        x = (a * x + c) % m
        yield x

def PRNG(min, max):
    """ Pseudo Random Generator """
    a = 2005
    c = 0
    m = 2 ** 64
    new_LCG = LCG(a, c, m)
    choice = ((max) - min) * (next(new_LCG) / (2 ** 64 - 1)) + min
    return choice
