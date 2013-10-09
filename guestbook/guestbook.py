import cgi
import urllib
import webapp2
import os
import settings

from models.greeting import Greeting
from models.greeting import guestbook_key

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template


DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')
        guestbook_name = self.request.get('guestbook_name',\
            DEFAULT_GUESTBOOK_NAME)

        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'


        template_values = {
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
        }

        sign_query_params = urllib.urlencode({'guestbook_name':guestbook_name})
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, template_values))


class Guestbook(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name',\
            DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting_author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))
