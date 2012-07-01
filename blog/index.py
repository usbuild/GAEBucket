# -*- coding:UTF-8 -*-
from google.appengine.ext import db
import json
from datetime import datetime
from base import BaseHandler, AppConfig


class Index(BaseHandler):
    def get(self):
        data = {}
        data["articles"] = []
        data['view_url'] = AppConfig.baseurl + "article/"
        q = BlogData.all()
        q.order("-date")
        q.fetch(10)
        for s in q:
            data["articles"].append({
                                     "id":s.key().id(),
                                     "title":s.title,
                                     "author":s.author,
                                     "date":s.date,
                                     "tags":s.tags,
                                     "catalog":s.catalog,
            })
        self.render_response("index.html", **data)
class LoginPage(BaseHandler):
    def get(self):
        data = {
                "submit_url":AppConfig.baseurl + "login/login",
        }
        self.response.write(self.jinja2.render_template("login.html", **data))

class LoginHander(BaseHandler):
    def post(self):
        username = self.request.POST['username']
        password = self.request.POST['password']
        if username == u"usbuild" and password == u"123":
            self.session['username'] = username
            self.response.write(json.dumps({"success":1}))
        else:
            self.response.write(json.dumps({"success":0}))
            
class NewPost(BaseHandler):
    def get(self):
        username = self.session.get("username")
        if username:
            context = {
                       "username" : username,
                       "post_url" : AppConfig.baseurl + "post",
                       "view_url" : AppConfig.baseurl + "article/",
                       }
            self.render_response("newpost.html", **context)
        else:
            self.response.write("you haven't logged!")
class Post(BaseHandler):
    def post(self):
        username = self.session.get("username")
        result = {}
        if username:
            article = {}
            tags = self.request.POST['tags'].strip().split(",")
            catalog = self.request.POST['catalog'].strip().split(",")
            title = self.request.POST['title'].strip()
            article['author'] = username if username else "null"
            article['content'] = self.request.POST['content']
            article['date'] = datetime.now()
            article['title'] = title if len(title) > 0 else "no title"
            article['tags'] = tags if len(tags[0].strip()) > 0 else ['默认标签']
            article['catalog'] = catalog if len(catalog[0].strip()) > 0 else ['默认分类']
            
            q = BlogData(**article)
            q.put()
            result["error"] = 0
            result["article_id"] = q.key().id()
            self.response.write(json.dumps(result))
        else:
            result["error"] = 1
            result["message"] = "您没有登录"
            self.response.write(json.dumps(result))  
class View(BaseHandler):
    def get(self):
        context = {}
        q = BlogData.get_by_id(int(self.request.path.split("/")[-1]))
        
        if q is not None :
            context['article'] = q
            context['article'].datestring = context['article'].date.strftime("%d/%m/%y %H:%M")
            self.render_response("view.html", **context)
        else:
            self.response.set_status(404)

class BlogData(db.Model):
    title = db.StringProperty()
    author = db.StringProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty()
    tags = db.StringListProperty()
    catalog = db.StringListProperty()
