from google.appengine.ext import ndb

class Pessoa(ndb.Model):
    nome = ndb.StringProperty()
    user_id = ndb.StringProperty(default='0')
    data_registro = ndb.DateTimeProperty(auto_now_add=True)

class Device(ndb.Model):
    nome = ndb.StringProperty()
    registration_id = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    dono = ndb.KeyProperty(kind=Pessoa,required=True)

class Mensagem(ndb.Model):
    mensagem = ndb.StringProperty()
    device = ndb.KeyProperty(kind=Device,required=True)
    data_envio = ndb.DateTimeProperty(auto_now_add=True)

class Conversa(ndb.Model):
    nome = ndb.StringProperty()
    chave = ndb.StringProperty()
    owner = ndb.KeyProperty(kind=Pessoa,required=True)
    not_allowed = ndb.KeyProperty(kind=Pessoa,repeated=True)
    ativa = ndb.BooleanProperty(required=True)
    data_criacao = ndb.DateTimeProperty(auto_now_add=True)

# ----  Metodos e objetos convenientes

class ModelPessoa():
    def __init__(self,user_id):
        self.user_id = user_id
        self.iterator = None

    def pessoaExiste(self):
        query = Pessoa.query(Pessoa.user_id == self.user_id)
        self.iterator = query.__iter__()
        if self.iterator.has_next():
            return True
        else:
            return False

    def getPessoa(self):
        if self.pessoaExiste():
            return self.iterator.next()
        else:
            return False

class ModelConversa():
    def __init__(self,key):
        self.key = key

    def getConversa():
        return

def criaConversa():

    return

def deletaConversa():
    return

def modificaConversa():
    return

def addToConversa():
    return

def removeFromConversa():
    return

def statusConversa(atividade):
    #ativa ou desativa uma conversa
    return

def enviaMensagem():
    return

def alteraDevice():
    return

def signupDevice(nome,regid):
    device = Device(nome=nome,registration_id=regid)
    device.put()