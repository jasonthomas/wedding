import string
import random
from data import Data


def genrandom(length=6):
    a = Data()
    unique = False
    while not unique:
        val = ''.join(random.sample(string.digits, length))
        if not a.getkey(val):
            unique = True
        return val

print genrandom()
