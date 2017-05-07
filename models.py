from google.appengine.ext import ndb

'''
CLASS:  Packet
DESCRIPTION: An NDB model which stores an individual email-packet's worth of
data.
'''
class Packet(ndb.Model):
    source = ndb.StringProperty() #Email or Phone number this packet originated from
    date = ndb.StringProperty() #Timestamp for when message was recieved

    body = ndb.StringProperty() #The raw body of the text message

    patientName = ndb.StringProperty()
    doctorFeedback = ndb.StringProperty(repeated=True)


'''
CLASS:  User
DESCRIPTION: An NDB model which stores an individual user's information.
'''
class User(ndb.Model):
    email = ndb.StringProperty()
    password = ndb.StringProperty() #TODO: Make this a hash
