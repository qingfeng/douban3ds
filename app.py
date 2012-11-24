from flask import Flask
from flask import render_template as st

app = Flask(__name__)

@app.route('/login/')
def login():
    return st('login.html', **locals())


if __name__ == '__main__':
    port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)

'''
from douban_client import DoubanClient

API_KEY = 'your api key'
API_SECRET = 'your api secret'

SCOPE = 'douban_basic_common,shuo_basic_r,shuo_basic_w'

client = DoubanClient(API_KEY, API_SECRET, your_redirect_uri, SCOPE)

print 'Go to the following link in your browser:'
print client.authorize_url
code = raw_input('Enter the verification code:')
client.auth_with_code(code)

client.auth_with_token(token)

new miniblog client.miniblog.new(text)
'''
