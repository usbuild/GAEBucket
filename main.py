import webapp2
import note.index
import disk.index
import blog.index
import index
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'aslghasffa-sdfgasghasfs',
}
config['webapp2_extras.jinja2'] = {
    'template_path': 'blog/templates',
    'environment_args':{
        'autoescape': False,
    },
}
url_mapping = [
             ('/?', index.Index),
             ('/note/?', note.index.Index),
             ('/note/save', note.index.Save),
             ('/note/view/[^/]+', note.index.View),
             ('/note/[^/]+', note.index.Show),
             ('/disk/?', disk.index.MainHandler),
             ('/disk/upload', disk.index.UploadHandler),
             ('/disk/delete', disk.index.DeleteHandler),
             ('/disk/content/([^/]+)?', disk.index.ServeHandler),
             ('/blog/?', blog.index.Index),
             ('/blog/login/?', blog.index.LoginPage),
             ('/blog/login/login', blog.index.LoginHander),
             ('/blog/newpost/?', blog.index.NewPost),
             ('/blog/edit/\d+?', blog.index.Edit),
             ('/blog/delete/\d+?', blog.index.Delete),
             ('/blog/manage/?', blog.index.Manage),
             ('/blog/post', blog.index.Post),
             ('/blog/article/\d+', blog.index.View),
             ]
app = webapp2.WSGIApplication(url_mapping, debug=True, config=config)
