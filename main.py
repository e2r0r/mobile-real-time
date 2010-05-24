import cgi
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Position(db.Model):
  time = db.TimeProperty(auto_now_add=True)
  device = db.StringProperty()
  geo = db.GeoPtProperty()

class Upload(webapp.RequestHandler):
  def post(self):
    position = Position()
    position.geo = db.GeoPt(float(self.request.get('lat')),float(self.request.get('lng')))
    position.device = self.request.get('device')
    position.put()

class MainPage(webapp.RequestHandler):
  def get(self):
    mobi = self.request.get('mobile')
    if mobi:
        positions = db.GqlQuery("SELECT * FROM Position where device = '%s' ORDER BY time DESC"%mobi)
        start = str(positions[0].geo)
        glist = []
        for pos in positions:
          glist.append("new GLatLng(%s)"%pos.geo)
        geolist = ','.join(glist)
        template_values = {
        'start': start,
        'geolist': geolist,
        }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
    else:  
      self.response.out.write('<html><body>')
    # Write the submission form and the footer of the page
      self.response.out.write("""<form action="/" method="get"><div>Mobile ID:<input type="text" name="mobile" value="test"></div><div><input type="submit" value="Look"></div>
</form></body></html>""")


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/up', Upload)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
