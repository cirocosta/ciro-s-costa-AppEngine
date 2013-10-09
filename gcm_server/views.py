import webapp2
import httplib, urllib
import json
import os

from google.appengine.api import users
from google.appengine.ext.webapp import template
from models import Device, signupDevice

BROWSER_API_KEY = 'AIzaSyBfqxohffOdrR_p6ERZUGsaTOD_A0Wlg3U'


class IndexGcmServer(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        devices = [x.nome for x in Device.query()]
        template_values = {"devices":devices}
        self.response.out.write(template.render(path,template_values))

class SignupDevice(webapp2.RequestHandler):
    def post(self):
        device_name = self.request.get('param0','null')
        device_regid = self.request.get('param1','null')
        if device_name != 'null' and device_regid != 'null':
            signupDevice(device_name,device_regid)
            self.response.write("Device object successfully created!")
        else:
            self.response.write("Error creating the device object on server")

class IndexGcmSendMessage(webapp2.RequestHandler):
    def post(self):
        conteudo = self.request.get('conteudo')
        self.response.write(sendJsonToAndroid(conteudo))

def sendJsonToAndroid(conteudo,send_to=False):
    import urllib2

    registration_ids = list()   #list of strings
    if not send_to:
        qry = Device.query()
        for device in qry:
            registration_ids.append(device.registration_id)
    else:
        registration_ids.append(send_to)
    headers = {"Content-type":"application/json",\
        "Authorization":"key=" + BROWSER_API_KEY}
    url = 'https://android.googleapis.com/gcm/send'
    conteudo = {"conteudo":conteudo}
    data = json.dumps({"registration_ids":registration_ids,"data":conteudo})
    req = urllib2.Request(url,data,headers)
    f = urllib2.urlopen(req)
    response = json.loads(f.read())
    return response
