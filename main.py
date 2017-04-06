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

#LongWave Modules
import models

#Global Variables
env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Login(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('/html/bootstrap_login.html')
        self.response.out.write(template.render())

    def post(self):
        #Get username and password strings from login form post request
        loginEmail = self.request.get('email')
        loginPassword = self.request.get('password')

        #query_result = userAccount.query(userAccount.user_id_local == google_user.user_id()).fetch()
        user_profile = models.User.query(models.User.email == loginEmail).get()

        if(user_profile != None):
            self.response.out.write("I Found Something!")

        else:
            self.response.out.write("<h2>Invalid Username/Password Combination</h2><br><a href=\"/login\">Return to Login</a>")

            ''' # Used to initially create login credentials in the datastore.
            new_user = models.User(email=loginEmail, password=loginPassword)
            user_key = newUser.put()
            self.response.out.write("Key: " + user_key.urlsafe())
            '''


class Dashboard(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('/html/bootstrap_dashboard.html')
        self.response.out.write(template.render())


app = webapp2.WSGIApplication([
    ('/', Login),
    ('/login', Login),
    ('/dashboard', Dashboard)
], debug=True)
