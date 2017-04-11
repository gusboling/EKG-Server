# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#Basic Python Modules
import os

#Google App Engine Modules
import webapp2
import jinja2
import logging
from google.appengine.ext import ndb

#LongWave Modules
import models

#Global Variables
env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

def standard_template():
    std_dict = {}
    return std_dict

class Login(webapp2.RequestHandler):
    def get(self):
        if (self.request.cookies.get('longWaveAuth') == 'True'):
            self.redirect('/dashboard')
        else:
            template = env.get_template('/html/bootstrap_login.html')
            self.response.out.write(template.render())

    def post(self):
        #Get username and password strings from login form post request
        loginEmail = self.request.get('email')
        loginPassword = self.request.get('password')
        user_profile = models.User.query(models.User.email == loginEmail).get()

        if(user_profile != None) and (loginPassword == user_profile.password):
            self.response.set_cookie('longWaveAuth', 'True', max_age=3600, path='/')
            self.redirect('/dashboard')

        else:
            self.response.delete_cookie('longWaveAuth')
            self.response.out.write("<h2>No Such Username/Password Combination</h2><br><a href=\"/login\">Return to Login</a>")

class Logout(webapp2.RequestHandler):
    def get(self):
        self.response.delete_cookie('longWaveAuth')
        self.redirect('/login')

class CreateUser(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('/html/bootstrap_createuser.html')
        self.response.out.write(template.render(message="What's your admin key?"))

    def post(self):
        new_email = self.request.get('email')
        new_password = self.request.get('password')
        security_key = self.request.get('key')
        template = env.get_template('/html/bootstrap_createuser.html')

        if(security_key == "gusIsAwesome"):
            new_user = models.User(email=new_email, password=new_password)
            user_key = new_user.put()
            self.response.out.write(template.render(message="<span style='color:green'>User Created!</span>"))

        else:
            self.response.out.write(template.render(message="<span style='color:red'>You're not an admin! Bugger off!</span>"))

class Dashboard(webapp2.RequestHandler):
    def get(self):
        if(self.request.cookies.get('longWaveAuth') != 'True'):
            self.redirect('/login')
        else:
            #Get all records, load into template array
            record_query = models.Packet.query()
            record_list = record_query.fetch()

            template_values = standard_template()
            template_values['record_list'] = record_list

            template = env.get_template('/html/bootstrap_dashboard.html')
            self.response.out.write(template.render(template_values))

class RemoveRecord(webapp2.RequestHandler):
    def post(self):
        url_key = self.request.get('url_key')
        record = ndb.Key(urlsafe=url_key).get()
        record.key.delete()
        self.redirect('/dashboard')


app = webapp2.WSGIApplication([
    ('/', Login),
    ('/login', Login),
    ('/logout', Logout),
    ('/dashboard', Dashboard),
    ('/createuser', CreateUser),
    ('/removerecord', RemoveRecord)
], debug=True)
