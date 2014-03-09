#!/bin/env python
import redis
import sys
import csv

db = redis.Redis('localhost')


def genrandom(length=6):
    unique = False
    while not unique:
        key = ''.join(random.sample(string.digits, length))
        if not getkey(key):
            unique = True

    return key


def add(filename):
    with open(filename) as fp:
        reader = csv.reader(fp)
        for row in reader:
            # if the length is 4 that means there is a middle name defined
            if len(row) == 4:
                return True
            else


def addvalue(firstname, lastname, guests, attending=True, middlename=None):
    name = genrandom()
    db.hset(name, 'firstname', firstname)
    db.hset(name, 'lastname', lastname)
    db.hset(name, 'middlename', middlename)
    db.hset(name, 'guests', guests)
    db.hset(name, 'attending', attending)


def getkey(name):
    return db.hkeys(name)


if __name__ == "__main__":
    filename = sys.argv[1]
    add(filename)
