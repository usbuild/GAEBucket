from web.contrib.template import render_jinja
render = render_jinja(
        'blog/templates',
        encoding = 'utf-8',                         # Encoding.
    )
class index:
    def GET(self):
        data = {}
        return render.index(data)