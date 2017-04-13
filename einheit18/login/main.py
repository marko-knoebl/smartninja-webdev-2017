#!/usr/bin/env python
import os
import jinja2
import webapp2

from google.appengine.api import users

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
        user = users.get_current_user()

        if user:
            logout_url = users.create_logout_url('/')
            params = {'logged_in': True,
                      'logout_url': logout_url,
                      'user': user}
            return self.render_template('hello.html', params)

        else:
            login_url = users.create_login_url('/')
            params = {'logged_in': False, 'login_url': login_url}

        return self.render_template("hello.html", params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
