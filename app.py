from flask import Flask, render_template, url_for, request, jsonify, after_this_request, make_response, session
from werkzeug.utils import secure_filename
import pandas as pd
import os
import csv
import json 
from rivia import Rivia
import webbrowser
from threading import Timer
import speech_recognition as sr
from gtts import gTTS 
import regex as re
import requests
import numpy as np
from bs4 import BeautifulSoup
import csv
import wget
import urllib
import re

app = Flask(__name__) 

app.config['UPLOAD_FOLDER'] = 'data/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv','tsv'}
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
RECORDED_FILES_PATH = 'static/audio/'
app.secret_key = 'kzquekZZui'

current_file = 'data/output.tsv'
# app = Flask(__name__, static_folder='static')


def allowed_file(filename):
	return '.' in filename and \
 		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def compute_results(question, rivia):
	result,typefile = rivia.rivia_predict(question)
	print(typefile)
	if typefile == 'table':
		print(result["logical_form"][0])
		ans = rivia.correct_answer(result['answer'])
	else:
		print(result["best_span_str"])
		ans = result["best_span_str"]
	return ans


# def check_name():

# 	#open the file


# @app.before_first_request(load_func())	  
@app.route('/')
def index():
	return render_template('homepage.html')

@app.route('/home') 
def home():
	checked = "checked"
	if "language" in session.keys():
		if session['language'] == "hi-IN":
			checked = ''
		else:
			checked = "checked"
	return render_template("index.html", value=checked)

# @app.route('/getdata', methods=['GET', 'POST'])
# def getdata():
# 	@after_this_request
# 	def add_header(response):
# 		response.headers['Access-Control-Allow-Origin'] = '*'
# 		return response

# 	df = pd.read_csv('data/cases.csv')
# 	print (df.shape)
# 	ans = df.to_html(bold_rows=True,classes="table table-hover thead-light table-striped")
# 	resp = {"ans":ans}

# 	return jsonify(resp)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
	if request.method == 'POST':
		rivia = Rivia()
		extention = ''

		if request.get_json() is not None:
			print ("OOPS")
			data = request.get_json()
			fname = data['sampledata']
			print (fname)
			# print ()
			extention = fname.split('.')[1]
			print (extention,"Extension")
			path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
			# resp = {"ans":}	

		else:
			print ("Check if table there: ")
			print ("table" in request.files.keys())
			print (request.get_json())

			f = request.files['table']
			if f and allowed_file(f.filename):
				
				path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
				f.save(path)
				extention = f.filename.rsplit('.', 1)[1].lower()
				print (extention,"Extension")
		
		if extention in ['csv', 'tsv', 'db']:
			print ('Table loaded')
			rivia.type = 'table'
		elif extention in ['txt']:
			print ('Passage loaded')
			rivia.type = 'passage'		
		rivia.process_file(path,rivia.type)
		
		if rivia.type == 'table':
			df = pd.read_csv(path)
			print (df.shape)
			ans = df.to_html(bold_rows=True,classes="table table-hover thead-light table-striped")
		else:
			f = open(path,'r+').read()
			ans = "<h4 style=\"margin-left:50px;margin-right:50px\">"+f+"</h4>"

		resp = {"ans":ans}
		session["type"] = rivia.type
	
	# else:
	# 	resp = {"ans":"Out of format"}
		# print (resp)
		return jsonify(resp)
	else:
		return 'GETTTTT OUT'

@app.route('/getanswer', methods=['GET', 'POST'])
def getanswer():
	rivia = None
	if "type" in session.keys():
		rivia = Rivia(session["type"])

	print (rivia)	
	print ('Got another request')
	req = request.get_json()
	print(req)
	# reply = answer(req['query'])
	
	
	# reply = {"answer":ans}
	ans = compute_results(req['query'], rivia)
	res = make_response(jsonify(ans), 200)
	# print (answer())
	return res

@app.route('/uploadwiki', methods=['POST', 'GET'])
def uploadwiki():
	rivia = Rivia()
	url = 'https://en.wikipedia.org/wiki/COVID-19_pandemic_by_country_and_territory#covid19-container'
	r = requests.get(url)

	soup = BeautifulSoup(r.content, 'html.parser')

	rows = soup.select('#thetable tr')

	#header-----
	header1 = rows[0].select('th')
	header = ['#','Country','Cases','Deaths','Recovery']
	# for i in range(0,len(header1)-1):
	# 	x = header1[i].text.strip()
	# 	header.append(x[:-3])

	#data-----
	data = []
	for x in range(2,len(rows)):
		row = [x-1]
		
		rr = rows[x].select('th a,th i a')
		for ir in rr:
			z = str(ir.string)
			if z[0] != '[' and z != 'None':
				row.append(z)
			
		rrdata = rows[x].select('td')
		for i in range(0,len(rrdata)-1):
			ii = rrdata[i].text.strip()
			if ii == 'No data':
				ii = 'NA'
			else:
				ii = ii.replace(',', '')#removing comma from number input
			row.append(ii)
		data.append(row)

	for x in data:
		if len(x) == 4:
			del data[data.index(x)]
	finalheader = np.vstack((header,data[0]))
	for x in data:
		if data.index(x) == 0:
			del data[data.index(x)]
	data = np.array(data)
	print(finalheader.shape)
	print(data.shape)
	# print(finaldata)
	data = data[:222]
	# print(data)

	with open('data/wikitable.csv', 'w+', newline='') as myfile:
		wr = csv.writer(myfile)
		wr.writerows(finalheader)
	with open('data/wikitable.csv', 'a+', newline='') as myfile:
		wr = csv.writer(myfile)
		wr.writerows(data)

	path = 'data/wikitable.csv'	
	print ('Table loaded')
	rivia.type = 'table'	
	rivia.process_file(path,rivia.type)
	session["type"] = rivia.type

@app.route('/wikiqa')
def wikiqa():
	return render_template('wikiqa.html')

@app.route('/uploadpassage', methods=['POST', 'GET'])
def uploadpassage():
	if request.method == 'POST':
		rivia = Rivia()
		print ('Got another request')
		req = request.get_json()
		print(req)
		
		topic =req['site']
		url = 'https://en.wikipedia.org/wiki/'+topic
		res = requests.get(url)
		res.raise_for_status()

		wiki = BeautifulSoup(res.text,'html.parser')
		index=0
		string = ''
		for i in wiki.select('p'):
			string += (i.getText())
			index+=1
			if index == 4:
				break

		replaced = re.sub(r'\[[0-9]+\]', '', string)
		lines = replaced.split('\n')
		final = str()
		for l in lines:
			if l != '':
				final=final+l+" "

		wikipassage = 'data/wikipassage.txt'
		with open(wikipassage, "w", encoding="utf-8") as fread:
			fread.write(final)

		rivia.type = 'passage'
		rivia.process_file(wikipassage,'passage')
		# f = open(passage,'r+').read()
		ans = "<h4 style=\"margin-left:50px;margin-right:50px\">"+replaced+"</h4>"
		resp = {"ans":ans}
		session["type"] = rivia.type
		return jsonify(resp)

@app.route('/passage')
def passage():
	return render_template('passage.html')

@app.route('/audio')
def audio():
	return render_template("audio.html")

@app.route('/speech', methods = ['POST', 'PUT', 'GET'])
def speech():
	if request.method == 'GET':
		print ("Request MEthod: "+str(s))
		return "Wrong Method"
	if request.method == 'POST':

		print ("In post")
		# try:
		# 	os.system('rm -rf static/audio/')
		# 	os.system('mkdir static/audio')
		# except Exception as e:
		# 	print (e)
		rivia = None
		if "type" in session.keys():
			rivia = Rivia(session["type"])
		f = request.files['audio_data']
		print (f)
		path = os.path.join(RECORDED_FILES_PATH, secure_filename(f.filename))
		f.save(path)
		# f.save(secure_filename(f.filename))

		regex = re.compile(r'[0-9]')
		message_number = regex.findall(secure_filename(f.filename))[0]


		print ("Got the file.")

		r=sr.Recognizer() 
		file=sr.AudioFile(path)

		with file as source:
		   audio = r.record(source)
		#  Speech recognition using Google Speech Recognition
		try:
			if "language" in session.keys():
				current_language = session['language']
			else:
				current_language = 'en-IN'
			print (current_language)
			recog = r.recognize_google(audio, language = current_language)

			query = None
			if (current_language == "hi-IN"):
				print("You said: " + recog)
				query = recog
				translated = rivia.translate_en(query)	
				print (f"which is translated to english as : {translated}")
				query = str(translated)
			else:
				print("You said: " + recog)
				query = recog
			# for testing purposes, we're just using the default API key
			# to use another API key, use r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")
			# instead of `r.recognize_google(audio)`` 

			
			print ("query to compute: ",query)
			answer = compute_results(query, rivia)
			print ("Answer",answer)
			print (type(answer))
			# i = 0
			path = "static/audio/answer_{}.mp3".format(message_number)
			response_path = "../" + path

			ans = {"query" : query,"path":response_path, "textres":answer, "status":"OK"}
			if current_language == "hi-IN":
				print (os.path.isfile(path))
				if os.path.isfile(path):
					os.remove(path)
					print ("File removed")

				random_str = rivia.generate_random()
				translated_path = 'static/audio/translated/answer_{}.mp3'.format(random_str)
				ans['path'] = "../"+ translated_path
				translated_text = rivia.translate_hi(answer)
				print (f"translated answer: {translated_text}")
				hi_speech = urllib.parse.quote_plus(str(translated_text))
				link = "http://ivrapi.indiantts.co.in/tts?type=indiantts&text={}&api_key=cb893c70-46af-11e8-9cf4-3bfbf17df6fd&user_id=37962&action=play&numeric=hcurrency&lang=hi_mohita".format(hi_speech).replace(' ','%20')
				print (link)
				wget.download(link, translated_path)
			else:
				myobj = gTTS(text=str(answer), lang='en', slow=False)
				myobj.save(path) 
			
			res = json.dumps(ans)

		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
			ans = {"query":"Sorry, I don't quite understand what you said.", "status":"NOT OK"}
			res = json.dumps(ans)


		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e)) 
			ans = {"query":"Sorry, We can't process your speech at this moment. Kindly use text input.", "status":"NOT OK"}
			res = json.dumps(ans)

		
		return res
	else:
		return "No method"

@app.route('/updatelangauge',methods=['POST','GET'])
def updatelangauge():
	if request.method == 'POST':
		data = request.get_json()
		print (data)
		print (session.keys())
		# if "language" in session.keys():
		session["language"] = data['language']
		response = {"status":"success"}
		print (session)
		return json.dumps(response)
	else:
		return json.dumps({"status":"error"})

def open_browser():
	path = '/usr/bin/google-chrome %s --incognito'
	webbrowser.get(path).open_new('http://127.0.0.1:5000')

if __name__ == '__main__':
	Timer(1, open_browser).start();
	app.run(debug=True) 