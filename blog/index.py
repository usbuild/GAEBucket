# -*- coding:UTF-8 -*-
from google.appengine.ext import db
import json
from datetime import datetime
from base import BaseHandler, AppConfig

context = {
           'base_url': AppConfig.baseurl,
           'view_url':AppConfig.baseurl + "article/",
           "login_url":AppConfig.baseurl + "login/login",
           "manage_url" : AppConfig.baseurl + "manage",
           "post_page" : AppConfig.baseurl + "newpost",
           "post_url" : AppConfig.baseurl + "post",
           "edit_page" : AppConfig.baseurl + "edit/",
           "delete_url" : AppConfig.baseurl + "delete/",
           }

class Index(BaseHandler):
    def get(self):
        context["articles"] = []
        q = BlogData.all()
        q.order("-date")
        q.fetch(10)
        for s in q:
            context["articles"].append({
                                     "id":s.key().id(),
                                     "title":s.title,
                                     "author":s.author,
                                     "date":s.date,
                                     "tags":s.tags,
                                     "catalog":s.catalog,
            })
        self.render_response("index.html", **context)
class LoginPage(BaseHandler):
    def get(self):
        self.response.write(self.jinja2.render_template("login.html", **context))

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
            context['username'] = username
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
            
            if self.request.POST.has_key("id") :
                id = self.request.POST['id']
                q = BlogData.get_by_id(int(id))
                if q is not None:
                    q.content = article['content']
                    q.title = article['title']
                    q.tags = article['tags']
                    q.catalog = article['catalog']
                    q.save()
                    result['error'] = 0
                    result['article_id'] = id
                else:
                    result['error'] = 1
            else:
                q = BlogData(**article)
                q.put()
                result["error"] = 0
                result["article_id"] = q.key().id()
        else:
            result["error"] = 1
            result["message"] = "您没有登录"
        self.response.write(json.dumps(result))  
class Manage(BaseHandler):
    def get(self):
        username = self.session.get("username")
        if username:
            context['username'] = username
            context['articles'] = []
            q = BlogData.all()
            q.order("-date")
            for s in q:
                context['articles'].append({
                                            "id":s.key().id(),
                                            "title":s.title,
                                            "author":s.author,
                                            "date":s.date,
                                            "tags":s.tags,
                                            "catalog":s.catalog,
                                            })
            
            
            self.render_response("manage.html", **context)
        else:
            self.response.write("you haven't logged!")
class Edit(BaseHandler):
    def get(self):
        username = self.session.get("username")
        id = int(self.request.path.split("/")[-1])
        q = BlogData.get_by_id(id)
        if username:
            context['username'] = username
            context['article'] = q
            context['article_id'] = id
            self.render_response("edit.html", **context)
        else:
            self.response.write("you haven't logged!")
    
class View(BaseHandler):
    def get(self):
        q = BlogData.get_by_id(int(self.request.path.split("/")[-1]))
        
        if q is not None :
            context['article'] = q
            self.render_response("view.html", **context)
        else:
            self.response.set_status(404)
class Delete(BaseHandler):
    def get(self):
        username = self.session.get("username")
        q = BlogData.get_by_id(int(self.request.path.split("/")[-1]))
        result = {}
        if username:
            db.delete(q)
            result['error'] = 0
        else:
            result['error'] = 1
        self.response.write(json.dumps(result))
            
class BlogData(db.Model):
    title = db.StringProperty()
    author = db.StringProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty()
    tags = db.StringListProperty()
    catalog = db.StringListProperty()
