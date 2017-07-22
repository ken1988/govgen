'''
Created on 2017/07/19

@author: ken
'''
from google.appengine.ext import ndb
import logging

class user(ndb.Model):
    email        = ndb.StringProperty()
    password     = ndb.StringProperty()
    countryName  = ndb.StringProperty()