# -*- coding: utf_8 -*-
'''
Created on 2017/7/18
@author: ken
'''
import webapp2
import os
import uuid
import Cookie
import hashlib
import logging
from datetime import datetime
from datetime import time
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
import json
from inspect import iscode

class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), './templates/index.html')
        self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([('/', MainPage)
                               ], debug=True)
