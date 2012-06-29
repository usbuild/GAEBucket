import webapp2
import note.index
import disk.index
import blog.index
import index

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
             ]
app = webapp2.WSGIApplication(url_mapping, debug=True)
