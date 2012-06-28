import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext import db
class Index(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = ("text/html")
        template_values = {
        }
        path = 'index.html'
        self.response.out.write(template.render(path, template_values))