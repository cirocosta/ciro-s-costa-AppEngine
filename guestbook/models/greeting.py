from google.appengine.ext import ndb

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

class Greeting(ndb.Model):
    """ Models an individual Guestbook entry with author, content and date """
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """ Constructs a Datastore key for a Guestbook entity with a guestbook_name """
    return ndb.Key('Guestbook',guestbook_name)

