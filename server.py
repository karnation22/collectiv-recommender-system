import os, os.path

import cherrypy
import simplejson
import thousand_students

class WebRoot(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')

@cherrypy.expose
class UserDataWebService(object):  
    def POST(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        body = simplejson.loads(rawbody)
        #assume rec_items is black-box function in recommender system backend...
        list_data = thousand_students.rec_items(body)
        # do_something_with(body)
        cherrypy.session['rec_data'] = list_data
        return "%r" % (list_data,)

@cherrypy.expose
class WorldDataWebService(object):
    def GET(self):
      return "%r" % (cherrypy.session['rec_data'],)

    def POST(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        body = simplejson.loads(rawbody)
        # do_something_with(body)
        return "%r" % (body,)

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/userdata': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
        },
        '/worlddata': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    webapp = WebRoot()
    webapp.userdata = UserDataWebService()
    webapp.worlddata = WorldDataWebService()
    cherrypy.quickstart(webapp, '/', conf)