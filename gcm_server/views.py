import webapp2
import httplib, urllib
import json
import os
import urllib2

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

from models import Device, Pessoa, Conversa, Mensagem
from models import signupDevice, ModelPessoa

BROWSER_API_KEY = 'AIzaSyBfqxohffOdrR_p6ERZUGsaTOD_A0Wlg3U'

class IndexGcmServer(webapp2.RequestHandler):
    def get(self):
        logged = False
        devices = [x.nome for x in Device.query()]
        user = users.get_current_user()
        conversas = False

        plus_btn_url = ''
        if user:
            logged = True
            plus_btn_url = users.create_logout_url('/gcm_server')
            model_pessoa = ModelPessoa(user.user_id())
            pessoa = model_pessoa.getPessoa()
            if pessoa != False:
                conversas = \
                    Conversa.query(Conversa.owner == pessoa.key).__iter__()
                if not conversas.has_next():
                    conversas = False
            else:
                pessoa = Pessoa(nome=user.nickname(),user_id=user.user_id())
                pessoa.put()
        else:
            plus_btn_url = users.create_login_url('/gcm_server')

        path = os.path.join(os.path.dirname(__file__), \
            'templates/index.html')
        template_values = {
            "devices":devices,
            "logged":logged,
            "plus_btn_url":plus_btn_url,
            "user":user,
            "conversas":conversas
        }
        self.response.out.write(template.render(path,template_values))

class IndexGcmCriaConversa(webapp2.RequestHandler):
    def post(self):
        nome = self.request.get('nome')
        chave = self.request.get('chave')
        user_id = self.request.get('user_id')

        print 'nome: ' + nome
        print 'chave: ' + chave
        print 'user_id: ' + user_id

        owner = ModelPessoa(users.get_current_user().user_id())
        owner = owner.getPessoa()

        if not owner:
            self.response.write("Erro: Nao foi encontrada pessoa")
            print 'ERRO, PESSOA NAO ENCONTRADA'
            return

        conversa = Conversa(nome=nome,chave=chave, owner=owner.key,\
            ativa=True)
        conversa.put()
        print 'CONVERSA CRIADA!'
        self.response.write("Success! conversa criada")


class IndexGcmCheckChave(webapp2.RequestHandler):
    def post(self):
        chave = self.request.get('chave')
        key_conversa = self.request.get('key_conversa')

        print chave
        print key_conversa

        conversa = ndb.Key(urlsafe=key_conversa).get()
        if conversa:
            if chave == conversa.chave:
                self.response.write("success")
            else:
                print 'CHAVE ERRADA'
                self.response.write("error")
        else:
            print 'CONVERSA NAO ENCONTRADA'
            self.response.write("error")



class SignupDevice(webapp2.RequestHandler):
    def post(self):
        device_name = self.request.get('param0','null')
        device_regid = self.request.get('param1','null')
        pessoa_uid = self.request.get('param2','null')
        if device_name != 'null' and device_regid != 'null':
            signupDevice(device_name,device_regid)
            self.response.write("Device object successfully created!")
        else:
            self.response.write("Error creating the device \
                object on server")

class IndexGcmSendMessage(webapp2.RequestHandler):
    def post(self):
        conteudo = self.request.get('conteudo')
        self.response.write(sendJsonToAndroid(conteudo))

def sendJsonToAndroid(conteudo,send_to=False):

    registration_ids = list()   #list of strings
    if not send_to:
        qry = Device.query()
        for device in qry:
            registration_ids.append(device.registration_id)
    else:
        registration_ids.append(send_to)
    headers = {
        "Content-type":"application/json",
        "Authorization":"key=" + BROWSER_API_KEY
        }
    url = 'https://android.googleapis.com/gcm/send'
    conteudo = {"conteudo":conteudo}
    data = json.dumps({
        "registration_ids":registration_ids,
        "data":conteudo
        })
    req = urllib2.Request(url,data,headers)
    f = urllib2.urlopen(req)
    response = json.loads(f.read())
    return response