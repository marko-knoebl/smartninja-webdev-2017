#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("home.html")

class AboutHandler(BaseHandler):
    def get(self):
        return self.render_template("about.html")

class QuizHandler(BaseHandler):
    def get(self):
        import random
        country = random.choice(['Austria', 'Germany', 'Italy', 'France'])
        return self.render_template("quiz.html", {'country': country})

    def post(self):
        capital = self.request.get('capital')
        self.write('Input:' + capital)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/about', AboutHandler),
    webapp2.Route('/aboutme', AboutHandler),
    webapp2.Route('/quiz', QuizHandler),
], debug=True)
