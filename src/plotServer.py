from flask import Flask, request, render_template
import matplotlib.pyplot as plt
import numpy
import io
import base64
import time
import pandas as pd

app = Flask(__name__)

ageDict = {'(0,10)':0, '(11,15)':0, '(16,25)':0, '(26,35)':1, '(36,45)':0, '(46,60)':1, '(60,100)':0}
genderDict = {'Male':1, 'Female':1}
totalN = 2
avgTime = 35.0

def build_gender_graph():
	img = io.BytesIO()
	plt.pie([float(v) for v in genderDict.values()], labels=[str(k) for k in genderDict.keys()], autopct='%1.2f', startangle=90)
	plt.title('Total Vistors Number: {}'.format(totalN))
	plt.savefig(img, format='png')
	img.seek(0)
	graph_url = base64.b64encode(img.getvalue()).decode()
	plt.close()
	return 'data:image/png;base64,{}'.format(graph_url)

def build_age_graph():
	img = io.BytesIO()
	plt.bar(ageDict.keys(), ageDict.values(), 1.0, color='g')
	plt.title('Age Distribution')
	plt.xlabel('Age Range')
	plt.ylabel('Age Count')
	plt.grid(axis='y', alpha=0.75)
	plt.savefig(img, format='png')
	img.seek(0)
	graph_url = base64.b64encode(img.getvalue()).decode()
	plt.close()
	return 'data:image/png;base64,{}'.format(graph_url)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/peopleInfo', methods=['POST'])
def receivePeopleInfo():
	personId = request.form['personId']
	time = request.form['time']
	age = request.form['age']
	gender = request.form['gender']

	genderDict[gender] = genderDict[gender] + 1
	ageDict[age] = ageDict[age] + 1
	global totalN
	totalN = totalN+1
	global avgTime
	avgTime = round((avgTime + float(time))/2,3)

	return 'received {}'.format(request)

@app.route('/graphs')
def graphs():
    #These coordinates could be stored in DB
    while True:
    	
	    graph1_url = build_gender_graph();
	    graph2_url = build_age_graph();

	    global avgTime
	 
	    return render_template('graph.html',
	    graph1=graph1_url,
	    graph2=graph2_url,
	    avgTime=avgTime)

if __name__ == '__main__':
	app.config["CACHE_TYPE"] = "null"
	app.run(debug=True)