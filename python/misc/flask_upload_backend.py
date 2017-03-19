from flask import Flask
from flask import request
from flask import make_response

import json

app = Flask(__name__)


@app.route('/login', methods = ['GET'])
def login():
	return 200

@app.route('/uploadavatar', methods = ['POST'])
def uploadavatar():
	'''
	content = json.dumps({
		'name': request.form[u'file_name'], 
		'content_type': request.form[u'file_content_type'], 
		'md5': request.form[u'file_md5'], 
		'path': request.form[u'file_path'], 
		'size': request.form[u'file_size'],
		'type': request.form[u'type']
	})
	resp = make_response(content)
	resp.headers['Content-Type'] = 'text/json'
	return content
	'''
	return jsonify({
		'name': request.form[u'file_name'], 
		'content_type': request.form[u'file_content_type'], 
		'md5': request.form[u'file_md5'], 
		'path': request.form[u'file_path'], 
		'size': request.form[u'file_size'],
		'type': request.form[u'type']
	})

@app.route('/uploadlifephoto', methods = ['POST'])
def uploadlifephoto():
	return jsonify({'state:success'});

if __name__ == '__main__':
	app.run(debug = True, host = '127.0.0.1', port = 5444)