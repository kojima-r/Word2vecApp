# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, jsonify, json, Response
from vec import  load_word2vec, find_vector_index, nearest_words
import json
import random
app = Flask(__name__)

words,vectors,words_x,words_index=load_word2vec(filename="vector5.bin")
"""
fp = open('va_list.json', 'r')
va_list = list(json.load(fp))
fp.close
"""


def jsonp(data, callback="function"):
	return Response(
		"%s(%s);" %(callback, json.dumps(data, ensure_ascii=False)),
		mimetype="text/javascript")


@app.route('/')
def index():
	title = "ようこそ"
	print(request.args)
	result={"title":title,"name":"aaa"}
	return jsonify(ResultSet=result)

@app.route('/nn', methods=['GET', 'POST'])
def get_nearest_words():
	search_word=request.args["word"]
	index=find_vector_index(search_word,words_x,words_index)
	v=vectors[index]
	output_words=nearest_words(v,words,vectors,K=10)
	result={"words":output_words}
	callback = request.args.get("callback")
	if callback:
		return jsonp(result, callback)
	return jsonify(ResultSet=result)


@app.route('/analogy_words', methods=['GET', 'POST'])
def get_analogy_words():
	word1=request.args["word1"]
	index1=find_vector_index(word1,words_x,words_index)
	v1=vectors[index1]
	#
	word2=request.args["word2"]
	index2=find_vector_index(word2,words_x,words_index)
	v2=vectors[index2]
	#
	word3=request.args["word3"]
	index3=find_vector_index(word3,words_x,words_index)
	v3=vectors[index3]
	#
	v=v3+v2-v1
	output_words=nearest_words(v,words,vectors,K=10)
	result={"words":output_words}
	callback = request.args.get("callback")
	if callback:
		return jsonp(result, callback)
	return jsonify(ResultSet=result)

if __name__ == '__main__':
	app.debug = False
	print("...start")
	app.run(host='0.0.0.0',port=5001)

