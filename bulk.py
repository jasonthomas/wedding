#!/bin/env python
from data import Data
import sys
import csv


def add(filename):
    user = Data()
    with open(filename) as fp:
        reader = csv.reader(fp)
        for row in reader:
            name = row[0]
            firstname = row[1]
            lastname = row[2]
            middlename = row[3]
            guests = row[4]
            code = user.add(firstname, lastname,
                            guests, middlename=middlename, name=name)
            print code


if __name__ == "__main__":
    filename = sys.argv[1]
    add(filename)
