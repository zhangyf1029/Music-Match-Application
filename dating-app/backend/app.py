import time 
from flask import Flask
from flask import render_template, request

app = Flask(__name__)


@app.route('/')
def hello():
    return {'text': "Hello World!"}

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

if __name__ == '__main__':
    app.run()