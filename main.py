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
import sampleData

#Global Variables
env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Comment:
    def __init__(self, author, text):
        self.author = author
        self.text = text

def standard_template():
    std_dict = {}
    return std_dict

def parseBody(bodyText):
    bodyArray = bodyText.split(",")
    dataArray = []

    for numstr in bodyArray:
        #logging.info(numstr)
        dataArray.append(float(numstr))

    return dataArray

def getCommentTuples(raw_comments):
    commentObjList = []

    for comment_string in raw_comments:
        if comment_string.find(":") != -1:
            author = comment_string.split(":")[0]
            comment = comment_string.split(":")[1]
            commentObjList.append(Comment(author, comment))
        else:
            commentObjList.append(Comment("Anonymous", comment_string))

        for comment in commentObjList:
            if comment.author == "Anonymous":
                commentObjList.remove(comment)

    return commentObjList

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
            self.response.set_cookie('longWaveUser', loginEmail, max_age=3600, path='/')
            self.redirect('/regionalDashboard')

        else:
            self.response.delete_cookie('longWaveAuth')
            self.response.out.write("<h2>Invalid Username/Password Combination</h2><br><a href=\"/login\">Return to Login</a>")

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

class RegionalDashboard(webapp2.RequestHandler):
    def get(self):
        if(self.request.cookies.get('longWaveAuth') != 'True'):
            self.redirect('/login')
        else:
            template_values = standard_template()
            template = env.get_template('/html/bootstrap_community.html')
            self.response.out.write(template.render(template_values))

class CommunityDashboard(webapp2.RequestHandler):
    def get(self):
        if(self.request.cookies.get('longWaveAuth') != 'True'):
            self.redirect('/login')
        else:
            community = self.request.get('community')
            logging.info(community)

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

class RemoveComment(webapp2.RequestHandler):
    def get(self):
        url_key = self.request.get('url_key')
        comment_text = self.request.get('comment_text')
        record = ndb.Key(urlsafe=url_key).get()
        old_comments = record.doctorFeedback

        if comment_text in old_comments:
            old_comments.remove(comment_text)

        record.doctorFeedback = old_comments
        record.put()
        self.redirect('/viewData?url_key=' + url_key)

class ViewData(webapp2.RequestHandler):
    def get(self):
        if(self.request.cookies.get('longWaveAuth') != 'True'):
            self.redirect('/login')

        else:
            url_key = self.request.get('url_key')
            record = ndb.Key(urlsafe=url_key).get()

            template_values = standard_template()

            template_values["sample"] = parseBody(record.body)
            template_values["patientName"] = record.patientName
            template_values["readingDate"] =  record.date
            template_values["urlsafe"] = record.key.urlsafe()
            template_values["afib_flag"] = record.afib_flag

            template_values["comment_list"] = getCommentTuples(list(record.doctorFeedback))

            template = env.get_template('/html/view_data.html')
            self.response.out.write(template.render(template_values))

class SendFeedback(webapp2.RequestHandler):
    def post(self):
        url_key = self.request.get('url_key')
        new_comment = self.request.get('new_comment')

        if len(self.request.get('afib_flag')) > 0:
            afib_flag = True
        else:
            afib_flag = False

        author = self.request.cookies.get('longWaveUser')

        record = ndb.Key(urlsafe=url_key).get()
        record.doctorFeedback.append(author + ":" + new_comment)
        record.afib_flag = afib_flag
        record.put()

        self.redirect('/viewData?url_key=' + url_key)

app = webapp2.WSGIApplication([
    ('/', Login),
    ('/login', Login),
    ('/logout', Logout),
    ('/regionalDashboard', RegionalDashboard),
    ('/dashboard', CommunityDashboard),
    ('/createuser', CreateUser),
    ('/removerecord', RemoveRecord),
    ('/removecomment', RemoveComment),
    ('/sendFeedback', SendFeedback),
    ('/viewData', ViewData)
], debug=True)
