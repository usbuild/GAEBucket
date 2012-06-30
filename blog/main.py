import web
import index
urls = (
    '/blog/?', index.index
)
app = web.application(urls, globals()).wsgifunc()