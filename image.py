import glob
import base64
import xmlrpclib
user = 'admin'
pwd = 'admin'
dbname = 'DrishtiNew'
model = 'hr.employee'
ip = '192.168.1.238:8069'
sock = xmlrpclib.ServerProxy('http://'+ip+'/xmlrpc/common')
uid = sock.login(dbname ,user ,pwd)
sock = xmlrpclib.ServerProxy('http://192.168.1.238:8069/xmlrpc/object')
image_list = glob.glob("/home/drishti/ERP/HRimage/*.*")
for filename in image_list:
    imagename = filename[30:]
    print "imagename",imagename
    f = open(filename , 'rb')
    img = base64.encodestring(f.read())
    emp_code = [s for k in imagename.split() for s in k.split(".") if s.isdigit()]
    for code in emp_code:
        
        results = sock.execute(dbname, uid, pwd, model, 'search', [('identification_id1','like',code)])
        print "results",results
        sock.execute(dbname, uid, pwd, model, 'write', results,{'image_medium': img})
    

