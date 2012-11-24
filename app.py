import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

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
