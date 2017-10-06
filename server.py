from flask import Flask,request,jsonify
from random import shuffle

app = Flask("Server",static_url_path='',static_folder="GrafosVC.github.io/")
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
graphs=[]
@app.route('/graph', methods=['GET', 'POST'])
def graph():
	if request.method == 'POST':
		hsh=request.json
		try:
			print(hsh)
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
			graphs.append(hsh)
			print("a")
			dumpname='abcdefghijklmnopqrstuvwxyz'
			dumpname=list(dumpname)
			print("b")
			shuffle(dumpname)
			dumpname=''.join(dumpname)
			print("d")
			with open('GrafosVC.github.io/dump/'+dumpname+'.json', 'w+') as outfile:
				json.dump(hsh, outfile)
			return "ok"
		except:
			print("here2")
			return "fail"
	else:
		return jsonify(counter)

@app.route('/graphs', methods=['GET', 'POST'])
def graphss():
	return jsonify(graphs)
app.run(host='0.0.0.0',port='5000')
