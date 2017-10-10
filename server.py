from flask import Flask,request,jsonify
from random import shuffle
import json

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
batch={}
batch['edges']=10
batch['nodes']=5
batch['count']=0

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
			#graphs.append(hsh)
			dumpname='abcdefghijklmnopqrstuvwxyz'
			dumpname=list(dumpname)
			shuffle(dumpname)
			dumpname=''.join(dumpname)
			with open('GrafosVC.github.io/dump/'+dumpname+'.json', 'w+') as outfile:
				json.dump(hsh, outfile)
			with open('GrafosVC.github.io/dump/'+dumpname+'.json', 'rb') as outfile:
				s3.upload_fileobj(outfile, "grafosvc", "dump")
			return "ok"
		except:
			return "fail"
	else:
		return jsonify({'stats': counter,'batch': batch})

def magic(nodes,index):
	if(index<5):
		return nodes*2
	if(index<10):
		return nodes*3
	if(index<15):
		return (nodes*nodes)//5
	return (nodes*nodes)//4

@app.route('/graphindex', methods=['GET', 'POST'])
def graphss():
	batch['count']+=1
	if batch['count']==20:
		batch['count']=0
		batch['nodes']+=1
	batch['edges']=magic(batch['nodes'],batch['count'])
	return jsonify(batch)
app.run(host='0.0.0.0',port='5000')
