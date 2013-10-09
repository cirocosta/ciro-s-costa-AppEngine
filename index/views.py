# -*- coding: utf-8 -*-
import webapp2

class Index(webapp2.RequestHandler):
	def get(self):
		self.response.write("<b>Se está vendo, está funcionando!</b>")