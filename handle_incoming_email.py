# Python Modules
import json
import time

# Google App Engine Modules
import logging
import webapp2
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

# Project Specific Modules
import models

class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        plaintext_bodies = mail_message.bodies('text/plain')

        for content_type, body in plaintext_bodies:
            plaintext = body.decode()

            ''' DEBUGGING LOGS '''
            logging.info("Received a message from: " + mail_message.sender)
            logging.info("Length (Plain Text): %d.", len(plaintext))
            logging.info("Body (Plain Text): %s", str(plaintext))
            ''' /DEBUGGING LOGS '''

            now = time.strftime("%c")
            newEntry = models.Packet(source=str(mail_message.sender), body=str(plaintext), date=str(now))
            newKey = newEntry.put()





app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)
