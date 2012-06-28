import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext import db
class Index(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = ("text/html")
        template_values = {
        }

        path = 'note/index.html'
        self.response.out.write(template.render(path, template_values))
        
class Save(webapp2.RequestHandler):
    def get(self):
        self.post()
        
    def post(self):
        title = self.request.POST["title"]
        content = self.request.POST["content"]
        q = NoteModel.all()
        q.filter("title = ", title)
        for s in q:
            s.delete()
        t = NoteModel(title = title, text= content)
        t.put()
        self.response.headers['Content-Type'] = ("text/html")
        self.response.write("ok")
        
class View(webapp2.RequestHandler):
    def get(self):
        title = self.request.path.split("/")[-1]
        
        q = NoteModel.all()
        q.filter("title = ", title)
        re = q.fetch(1)
        if len(re) > 0:
            self.response.headers['Content-Type'] = ("text/html")
            self.response.write('<html><head><title>%s</title></head><body>%s</body></html>' % (re[0].title, re[0].text));
            return
        self.response.set_status(404)
        
        
class Show(webapp2.RequestHandler):
    def get(self):
        title = self.request.path.split("/")[-1]
        
        q = NoteModel.all()
        q.filter("title = ", title)
        re = q.fetch(1)
        data = {}
        data["title"] = title
        if len(re) > 0:
            data["title"] = re[0].title
            data["content"] = re[0].text
        
        self.response.headers['Content-Type'] = ("text/html")
        path = 'note/index.html'
        self.response.out.write(template.render(path, data))        


class NoteModel(db.Model):
    title = db.StringProperty(required=True)
    text = db.StringProperty(multiline=True)
