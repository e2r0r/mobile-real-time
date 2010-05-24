import positioning
import time
import httplib, urllib
print "Init Program"
print ""
print "Default Module:"
print positioning.default_module()
print ""
positioning.select_module(positioning.default_module())
print "Detailed Module Info:"
print ""
print positioning.module_info(positioning.default_module())
print "GPS Data:"
print ""
positioning.set_requestors([{"type":"service","format":"application","data":"test_app"}])
while 1:
    data = positioning.position(course=1,satellites=1)
    la,lo = data['position']['latitude'],data['position']['longitude']
    gps_coords = urllib.urlencode({'device': 'N6730C', 'lat':str(la),'lng':str(lo)})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection("mobile-real-map.appspot.com:80")
    conn.request("POST", "/up", gps_coords, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    print "here is %s \n"%str(la)
    time.sleep(30)
