from allennlp.models.archival import load_archive
from allennlp.predictors import Predictor
from allennlp_rc.predictors.reading_comprehension import ReadingComprehensionPredictor
from allennlp_semparse.predictors.wikitables_parser import WikiTablesParserPredictor
from allennlp_semparse.models.wikitables.wikitables_erm_semantic_parser import WikiTablesErmSemanticParser
import pytest
import spacy
from allennlp.common.testing import AllenNlpTestCase
from allennlp_hub import pretrained
import pandas as pd
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process
import csv
from textblob import TextBlob
from textblob.exceptions import NotTranslated
import wget
import random
import math


class Rivia:

	def __init__(self, type=None, language="en-IN"):
		self.type = type
		self.language = language

	def what(self):
		print ("Rivia is a AI based Chatbot")

	def say_hello(self, name):
		print (f"Hello {name}")

	def correct_answer(self, temp_answer):
		# temp_answer = result['answer']
		# print (type(temp_answer))
		if type(temp_answer) is list:
			df = pd.read_table('data/final_output.txt','\t',encoding='ISO-8859-1')
			types = dict(df.dtypes)

			checks = []
			for key, value in types.items():
				if (value == 'object'):
					checks.append(key)

			threshold = 50
			final_answer = []

			for answer in temp_answer:
				if type(answer) is str:
					match = {}

					for check in checks:
						for index, row in df.iterrows(): 
							if process.extractOne(answer,[row[check]])[1] > threshold:
								match[row[check]] = process.extractOne(answer,[row[check]])[1]

					max_val = 0
					max_key = ''
					for key in match.keys():
						if match[key]>max_val:
							max_val = match[key]
							max_key = key
					
					final_answer.append(max_key)
					
			ans = ', '.join(final_answer)
			print (f"The final answer is {ans}")
		else:
			ans = temp_answer

		return ans

	def rivia_predict(self, question):
		if self.type == 'table':

			archive = load_archive("model/wikitables-model-2020.02.10.tar.gz")
			predictor = Predictor.from_archive(archive, 'wikitables-parser')

			with open('data/final_output.txt','r') as f:
				table = f.read()

			data = {
			  "table": table,
			  "question": question
			}
			print(data['question'])
			result = predictor.predict_json(data)
			print(result["answer"])
			return result, self.type
		
		elif self.type == 'passage':
			archive = load_archive("model/bidaf-model.tar.gz")
			bidaf = Predictor.from_archive(archive, "reading-comprehension")

			with open("data/output.txt","r",encoding="utf-8") as f:
				passage = f.read()

			data = {
			  "passage": passage,
			  "question": question
			}
			result = bidaf.predict_json(data)
			print(result["best_span_str"])
			return result, self.type
		else:
			return None

	def process_file(self, path,filetype):
		self.type=filetype
		if self.type == 'table':
			csv.writer(open("data/output.txt", 'w+',newline='\n'), delimiter='\t').writerows(csv.reader(open(path)))	
		
		else:
			file = open("data/output.txt", "w+",newline='\n')
			with open(path,"r",encoding="utf-8") as f:
				x = f.read()
			file.write(x)

		with open("data/output.txt","r",encoding="utf-8") as f:
			d = f.read()
		
		fd=open("data/final_output.txt","w+",newline='\n')
		if self.type == 'table':
			m=d.split("\n")
			s="\n".join(m[:-1])
			for i in range(len(s)):
				fd.write(s[i])
		else:
			fd.write(d)
		fd.close()

	def translate_en(self, original_text):
		source = TextBlob(original_text)
		return source.translate(to='en')

	def translate_hi(self, original_text):
		try:
			source = TextBlob(original_text)
			return source.translate(to='hi')
		except NotTranslated:
			return original_text
		except Exception as e:
			return original_text
	def generate_random(self):
		digits = [i for i in range(0, 10)]

		random_str = ""

		for i in range(6):
			index = math.floor(random.random() * 10)

			random_str += str(digits[index])

		## displaying the random string
		print(random_str)
		return random_str

	def __repr__(self):
		return {"type":self.type} 

	def __str__(self):
		return f'The File type is {self.type}'

