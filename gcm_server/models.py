from google.appengine.ext import ndb

class Device(ndb.Model):
    nome = ndb.StringProperty()
    registration_id = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

def signupDevice(nome,regid):
    device = Device(nome=nome,registration_id=regid)
    device.put()