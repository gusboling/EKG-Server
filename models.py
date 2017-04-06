from google.appengine.ext import ndb

'''
CLASS:  Packet
DESCRIPTION: An NDB model which stores an individual email-packet's worth of
data.
'''
class Packet(ndb.Model):
    source = ndb.StringProperty() #Email or Phone number this packet originated from
    sequence = ndb.IntegerProperty() #The
    body = ndb.StringProperty()


'''
CLASS:  User
DESCRIPTION: An NDB model which stores an individual user's information.
'''
class User(ndb.Model):
    email = ndb.StringProperty()
    password = ndb.StringProperty() #TODO: Make this a hash
