import webapp2

from guestbook.guestbook import Guestbook, MainPage
import settings

application = webapp2.WSGIApplication([
    ('/guestbook',MainPage),
    ('/sign',Guestbook),
],debug=settings.DEBUG)