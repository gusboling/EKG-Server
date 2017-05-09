# Python Modules
import json
import time
import random

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

            # Google emails have a bunch of junk data appended to them. This splits the body
            #   after the first word of google-text, and only keeps the first part, which contains
            #   all of our data.
            parsed_body = str(plaintext.split('YOUR')[0])

            ''' DEBUGGING LOGS '''
            #logging.info("Received a message from: " + mail_message.sender)
            #logging.info("Length (Plain Text): %d.", len(plaintext))
            #logging.info("Body (Plain Text): %s", str(plaintext))
            ''' /DEBUGGING LOGS '''

            rand_list = []
            for i in range(0,7):
                rand_list.append(random.randint(0,9))

            patient_ID = str(rand_list[0]) + str(rand_list[1]) + str(rand_list[2]) + "-" + str(rand_list[3]) + str(rand_list[4]) + str(rand_list[5]) + str(rand_list[6])

            now = time.strftime("%c")
            newEntry = models.Packet(source=str(mail_message.sender), body=parsed_body, date=str(now), patientName="Patient #"+patient_ID)
            newKey = newEntry.put()


app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)
