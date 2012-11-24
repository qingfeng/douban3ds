from flask import Flask
from flask import render_template as st

from douban_client import DoubanClient

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
    return 'Back'


if __name__ == '__main__':
    port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)


#print 'Go to the following link in your browser:'
#code = raw_input('Enter the verification code:')
#client.auth_with_code(code)

#client.auth_with_token(token)

#new miniblog: client.miniblog.new(text)
