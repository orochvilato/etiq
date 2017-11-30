from flask import Flask,redirect,request
import json
import requests
import xmltodict

app = Flask(__name__)
#cas = CAS(app, '/test')
app.config['CAS_SERVER'] = 'https://www-test.sante-martinique.fr/ideosso'
app.config['CAS_SERVICE'] = 'http://172.25.10.72:5000'

@app.route('/')
def route_root():
    st = request.args.get('ticket')
    r = requests.get('%s/serviceValidate' % app.config['CAS_SERVER'],params=dict(service=app.config['CAS_SERVICE'],ticket=st))
    return json.dumps(xmltodict.parse(r.content))
@app.route('/login')
def login():
    return redirect('%s/login?service=%s' % (app.config['CAS_SERVER'],app.config['CAS_SERVICE']))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
nsmap={'wsse':'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd'}
from lxml import etree
from zeep import Client
from zeep.wsse.username import UsernameToken
client = Client('https://www-test.sante-martinique.fr/ideodirectory.services/IdeoDirectoryManagerSecure?wsdl',wsse=UsernameToken(username='', password='',use_digest=True))
#node = client.create_message(client.service, 'getPersonneInfos')
#usernametoken = node.xpath('//wsse:UsernameToken',namespaces=nsmap)[0]
#usernametoken.set('{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wsswssecurity-utility-1.0.xsd}Id','Id')
gur_type=client.get_type('{com.sqli.sante.ideoldap.remoting}GetUserRequest')
gur = gur_type(idCompte="test")
print client.service.getUserInfos(gur)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
