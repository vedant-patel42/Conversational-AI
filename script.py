from allennlp.models.archival import load_archive
from allennlp.predictors import Predictor
from allennlp_rc.predictors.reading_comprehension import ReadingComprehensionPredictor
from allennlp_semparse.predictors.wikitables_parser import WikiTablesParserPredictor
from allennlp_semparse.models.wikitables.wikitables_erm_semantic_parser import WikiTablesErmSemanticParser
import pytest
import spacy
from allennlp.common.testing import AllenNlpTestCase
from allennlp_hub import pretrained
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process
import pandas as pd
from rivia import Rivia
from gtts import gTTS 

r = Rivia('table')
r.what()
r.say_hello('Megh')

# last_line = []
# with open('data/output.txt', 'r') as f:
# 	lines = f.read().splitlines()
# 	last_line = lines[:-1]
# 	print ('.'.join(last_line))
# ans = '.'.join(last_line)
# with open('data/final_output.txt', 'w+') as f:
# 	f.write(ans)

# fd=open("data/output.txt","r")
# d=fd.read()
# fd.close()
# m=d.split("\n")
# s="\n".join(m[:-1])
# fd=open("data/final_output.txt","w+")
# for i in range(len(s)):
#     fd.write(s[i])
# fd.close()
# question = "Which country have more than 5000 deaths?"
# result = r.rivia_predict(question)
# print(result["logical_form"][0])

# ans = r.correct_answer(result['answer'])

myobj = gTTS(text="Hello, How are you?", lang='en', slow=False)
myobj.save("static/welcome.mp3") 
# print (final_answer)
# reply = {'answer':result['answer']}
# print (type(jsonify(reply)))
# fd=open("file.txt","r")
# d=fd.read()
# fd.close()
# m=d.split("\n")
# s="\n".join(m[:-1])
# fd=open("file.txt","w+")
# for i in range(len(s)):
# 	fd.write(s[i])
# fd.close()


# query = 'united_states'
# choices = ['United States']
   
# Get a list of matches ordered by score, default limit to 5 
# print (process.extractOne(query, choices)) 
   
# If we want only the top one 
# print (process.extractOne(query, choices) )