from flask import Flask
from flask import request, redirect
from flask import render_template as st

from douban_client import DoubanClient
from douban_client.api.error import DoubanError

from cStringIO import StringIO
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

def hash_name(names):
    return " ".join("#%s#" % name for name in names if name)

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
    comment = request.form.get('comment', '')
    hash1 = request.form.get('hash[new1]', '')
    hash2 = request.form.get('hash[new2]', '')
    hash3 = request.form.get('hash[new3]', '')

    if image:
        fname = '/tmp/1.jpg'
        image.save(fname)
        hash_text = hash_name([hash1, hash2, hash3])
        text = "%s %s" % (comment, hash_text)
        text = text.encode("utf-8")
        try:
            client.auth_with_code(code)
            client.miniblog.new(text, image=open(fname))
        except DoubanError:
            return redirect('/login')
        return "Upload OK"
    else:
        return "Error"

if __name__ == '__main__':
    port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)
