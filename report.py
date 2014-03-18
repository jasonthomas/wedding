#!/bin/env python
from data import Data
import sys


def report():
    data = Data()
    codes = data.getallkeys()
    for code in codes:
        invite = data.getvalue(code)
        if 'actual_guests' in invite:
            print '%s: %s %s attending: %s guests: %s' % (code, invite['firstname'],
                                                          invite['lastname'], invite['attending'],
                                                          invite['actual_guests'])


if __name__ == "__main__":
    report()
