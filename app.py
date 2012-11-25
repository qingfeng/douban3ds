from flask import Flask
from flask import request
from flask import render_template as st

from douban_client import DoubanClient

import os

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']

SCOPE = 'douban_basic_common,shuo_basic_r,shuo_basic_w'

client = DoubanClient(API_KEY, API_SECRET, '/back', SCOPE)

app = Flask(__name__)

@app.route('/login/')
def login():
    auth_url = client.authorize_url
    return st('login.html', **locals())

@app.route('/back')
def back():
    code = request.args.get('code', '')
    error = request.args.get('error', '')
    if code:
        return st('index.html', **locals())
    elif error:
        return error
    else:
        return 'Unkonw Error'

@app.route('/new', methods=['POST'])
def new():
    code = request.form.get('code')
    image = request.files.get('image')
    client.auth_with_code(code)
    client.miniblog.new(text, image=image)
    return "Upload OK"

if __name__ == '__main__':
    port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)
