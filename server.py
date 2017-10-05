from flask import Flask,request,jsonify

from OpenSSL import SSL
import ssl
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('server.crt', 'server.key')

app = Flask("Server")
counter = {}
counter['cntnone']=0
counter['cnt2aprox']=0
counter['cntgreedy']=0
counter['cnt2greedy']=0
counter['requests']=0
counter['nodes']=0
counter['edges']=0
counter['mxmnone']=0
counter['mxm2aprox']=0
counter['mxmgreedy']=0
counter['mxm2greedy']=0
counter['graphs']={}
@app.route('/graph', methods=['GET', 'POST'])
def graph():
	if request.method == 'POST':
		hsh=request.form
		try:
			counter['nodes']+=hsh['nodes']
			counter['edges']+=hsh['edges']
			counter['requests']+=1
			if(hsh['none']==None or hsh['none']==0):
				return "fail"
			if(hsh['2greedy']==None):
				return "fail"
			if(hsh['greedy']==None):
				return "fail"
			if(hsh['2aprox']==None):
				return "fail"
			tmp={}
			for otim in ['none','2aprox','greedy','2greedy']:
				tmp['mxm'+otim]=float(hsh[otim])/float(hsh['none'])
				counter['cnt'+otim]+=int(hsh[otim])
				if(tmp['mxm'+otim]>counter['mxm'+otim]):
					counter['mxm'+otim]=tmp['mxm'+otim]
					counter['graphs'][otim]=hsh['graph']
			return "ok"
		except:
			return "fail"
	else:
		return jsonify(counter)
app.run(host='0.0.0.0',port='5000',
        debug = False, ssl_context=context)
