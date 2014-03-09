import redis
import string
import random


class Data:
    def __init__(self, host='localhost'):
        self.conn = redis.Redis(host)

    def getkey(self, key):
        return self.conn.hkeys(key)

    def getvalue(self, key):
        return self.conn.hgetall(key)

    def genrandom(self, length=5):
        unique = False
        while not unique:
            val = ''.join(random.sample(string.digits, length))
            if not self.getkey(val):
                unique = True
        return val

    def add(self, firstname, lastname, guests,
            attending=None, middlename=None):
        name = self.genrandom()
        try:
            self.conn.hset(name, 'invitecode', name)
            self.conn.hset(name, 'firstname', firstname)
            self.conn.hset(name, 'lastname', lastname)
            self.conn.hset(name, 'middlename', middlename)
            self.conn.hset(name, 'guests', guests)
            self.conn.hset(name, 'attending', attending)
        except:
            print "error"

        return name

    def update(self, name, attending, actual_guests):
        try:
            self.conn.hset(name, 'attending', attending)
            self.conn.hset(name, 'actual_guests', actual_guests)
        except:
            print "error"
