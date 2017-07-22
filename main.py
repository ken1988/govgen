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
import models

class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), './templates/index.html')
        self.response.out.write(template.render(path, template_values))

'''------------------------------------------
ユーザ管理用クラス
------------------------------------------'''
class User(webapp2.RequestHandler):
    def get(self):

        if client_id == '':
            template_values = {}

        else:
            disp_mail = self.request.cookies.get('email', '')
            template_values = {'login':1,
                               'email':disp_mail}

        path = os.path.join(os.path.dirname(__file__), './templates/header_menu.html')
        header_html = template.render(path,template_values)

        template_values = {'header':header_html}
        path = os.path.join(os.path.dirname(__file__), './templates/User_registration.html')
        self.response.out.write(template.render(path, template_values))
        return

    def post(self):
        uid = self.request.get('userID')
        passstr = self.request.get('password')
        country = self.request.get('countryName')

        #パスワードハッシュ値生成
        password = Signin().make_hashkey(passstr)

        #メールアドレスハッシュ値生成
        user_key = Signin().make_hashkey(uid)

        new_user = models.user(id = user_key)
        new_user.email = uid
        new_user.password = password
        new_user.countryName = country

        new_user.put()

        self.redirect('/')
        return
class Mypage(webapp2.RequestHandler):
    def get(self):
        user_key = self.request.cookies.get('hash', '')
        if user_key == '':
            self.redirect('/')

        pr_user = models.user().get_by_id(user_key)

        template_values = {'country':pr_user.countryName}
        path = os.path.join(os.path.dirname(__file__), './templates/mypage.html')
        self.response.out.write(template.render(path, template_values))

        return

    def post(self):
        return

class Signin(webapp2.RequestHandler):
    def get(self):
        #cookieを破棄する
        self.response.delete_cookie('clid')
        self.response.delete_cookie('hash')
        self.redirect('/')
        return

    def post(self):
        #Postがあった場合の処理
        uid = self.request.get("userID")
        password = self.request.get('password')

        #ユーザーキー生成
        user_key = self.make_hashkey(uid)

        #パスワードハッシュ値生成
        passwd = self.make_hashkey(password)

        pr_user = models.user().get_by_id(user_key)
        if pr_user:
            if pr_user.password == passwd:
                client_id = str(uuid.uuid4())
                max_age = 60*120
                pr_list = {'clid':client_id,'hash':user_key}
                self.put_cookie(pr_list,max_age)
                self.redirect('/Mypage')

                return
            else:
                ermsg = "パスワードが異なる"
        else:
            ermsg = "ユーザIDが存在しない"

        template_values = {'ermsg':ermsg}
        path = os.path.join(os.path.dirname(__file__), './templates/index.html')
        self.response.out.write(template.render(path, template_values))
        return

    def make_hashkey(self,base):
        #ユーザーキー生成
        h = hashlib.md5()
        h.update(base)
        hash_key = h.hexdigest()

        return hash_key


    def put_cookie(self,param_list,max_age):
        for key,value in param_list.iteritems():
            keys = key.encode('utf_8')
            values = value.encode('utf_8')
            myCookie = Cookie.SimpleCookie(os.environ.get( 'HTTP_COOKIE', '' ))
            myCookie[keys] = values
            myCookie[keys]["path"] = "/"
            myCookie[keys]["max-age"] = max_age
            self.response.headers.add_header('Set-Cookie', myCookie.output(header=""))
        return


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/User', User),
                               ('/Mypage', Mypage),
                               ('/Signin', Signin)
                               ], debug=True)
