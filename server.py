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
graphs={}
@app.route('/graph', methods=['GET', 'POST'])
def graph():
	if request.method == 'POST':
		hshs=request.json
		if 'graphs' in hshs.keys():
			for hsh in hshs['graphs']:
				try:
					if(hsh['none']==None or hsh['none']==0):
						return "fail"
					if(hsh['2greedy']==None):
						return "fail"
					if(hsh['greedy']==None):
						return "fail"
					if(hsh['2aprox']==None):
						return "fail"
					counter['nodes']+=hsh['nodes']
					counter['edges']+=hsh['edges']
					counter['requests']+=1
					tmp={}
					if hsh['nodes'] not in graphs.keys():
						graphs[hsh['nodes']]={}
					if hsh['edges'] not in graphs[hsh['nodes']].keys():
						graphs[hsh['nodes']][hsh['edges']]={'graph':{},'mxmnone':0,'mxm2aprox':0,'mxmgreedy':0,'mxm2greedy':0,'cntnone':0,'cnt2aprox':0,'cntgreedy':0,'cnt2greedy':0}
					for otim in ['none','2aprox','greedy','2greedy']:
						tmp['mxm'+otim]=float(hsh[otim])/float(hsh['none'])
						counter['cnt'+otim]+=int(hsh[otim])
						graphs[hsh['nodes']][hsh['edges']]['cnt'+otim]+=int(hsh[otim])
						if(tmp['mxm'+otim]>counter['mxm'+otim]):
							counter['mxm'+otim]=tmp['mxm'+otim]
							counter['graphs'][otim]=hsh['graph']
						if(tmp['mxm'+otim]>graphs[hsh['nodes']][hsh['edges']]['mxm'+otim]):
							graphs[hsh['nodes']][hsh['edges']]['mxm'+otim]=tmp['mxm'+otim]
							graphs[hsh['nodes']][hsh['edges']]['graph']=hsh['graph']
				except:
					return "fail"
		else:
			hsh=hshs
			try:
				if(hsh['none']==None or hsh['none']==0):
					return "fail"
				if(hsh['2greedy']==None):
					return "fail"
				if(hsh['greedy']==None):
					return "fail"
				if(hsh['2aprox']==None):
					return "fail"
				counter['nodes']+=hsh['nodes']
				counter['edges']+=hsh['edges']
				counter['requests']+=1
				tmp={}
				if hsh['nodes'] not in graphs.keys():
					graphs[hsh['nodes']]={}
				if hsh['edges'] not in graphs[hsh['nodes']].keys():
					graphs[hsh['nodes']][hsh['edges']]={'graph':{},'mxmnone':0,'mxm2aprox':0,'mxmgreedy':0,'mxm2greedy':0,'cntnone':0,'cnt2aprox':0,'cntgreedy':0,'cnt2greedy':0}
				for otim in ['none','2aprox','greedy','2greedy']:
					tmp['mxm'+otim]=float(hsh[otim])/float(hsh['none'])
					counter['cnt'+otim]+=int(hsh[otim])
					graphs[hsh['nodes']][hsh['edges']]['cnt'+otim]+=int(hsh[otim])
					if(tmp['mxm'+otim]>counter['mxm'+otim]):
						counter['mxm'+otim]=tmp['mxm'+otim]
						counter['graphs'][otim]=hsh['graph']
					if(tmp['mxm'+otim]>graphs[hsh['nodes']][hsh['edges']]['mxm'+otim]):
						graphs[hsh['nodes']][hsh['edges']]['mxm'+otim]=tmp['mxm'+otim]
						graphs[hsh['nodes']][hsh['edges']]['graph']=hsh['graph']
			except:
				return "fail"
		return "ok"
	else:
		return jsonify({'counter': counter,'batch': batch, 'graphs':graphs})

def magic(nodes,index):
	if(index<nodes):
		return nodes*2
	if(index<2*nodes):
		return nodes*3
	if(index<3*nodes):
		return (nodes*nodes)//5
	return (nodes*nodes)//4

@app.route('/graphindex', methods=['GET', 'POST'])
def graphss():
	batch['count']+=1
	if batch['count']>=4*batch['nodes']:
		batch['count']=0
		batch['nodes']+=1
	batch['edges']=magic(batch['nodes'],batch['count'])
	return jsonify(batch)

@app.route('/resetindex', methods=['GET', 'POST'])
def resetindex():
	batch['count']=0
	batch['nodes']=5
	batch['edges']=10

@app.route('/bumpnodes', methods=['GET', 'POST'])
def bumpnodes():
	batch['nodes']+=5

app.run(host='0.0.0.0',port='5000')
