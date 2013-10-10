import webapp2
import settings

from index.views import Index
from guestbook.guestbook import Guestbook, MainPage
from gcm_server.views import IndexGcmServer, IndexGcmSendMessage, \
	SignupDevice, IndexGcmCriaConversa, IndexGcmCheckChave


application = webapp2.WSGIApplication([
	('/',Index),
    ('/guestbook',MainPage),
    ('/sign',Guestbook),
    ('/gcm_server',IndexGcmServer),
    ('/gcm_server/cria_conversa',IndexGcmCriaConversa),
    ('/gcm_server/valida_chave',IndexGcmCheckChave),
    ('/gcm_server/send_to_device',IndexGcmSendMessage),
    ('/gcm_server/signup_device',SignupDevice),
],debug=settings.DEBUG)