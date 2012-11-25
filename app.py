from flask import Flask
from flask import request, redirect
from flask import render_template as st

from douban_client import DoubanClient
from douban_client.api.error import DoubanError

import os

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
CALLBACK = os.environ['API_CALLBACK']
SCOPE = 'douban_basic_common,shuo_basic_r,shuo_basic_w'


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/login/')
def login():
    client = DoubanClient(API_KEY, API_SECRET, CALLBACK, SCOPE)
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
    client = DoubanClient(API_KEY, API_SECRET, CALLBACK, SCOPE)
    code = request.form.get('code')
    image = request.files.get('image')
    text = request.form.get('comment', '')
    client.auth_with_code(code)
    if image and allowed_file(image.filename):
        from cStringIO import StringIO
        image.save('/tmp/1.jpg')
        try:
            client.miniblog.new(text, image=open('/tmp/1.jpg'))
        except DoubanError:
            return redirect('/login')
    return "Upload OK"

if __name__ == '__main__':
    port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)
