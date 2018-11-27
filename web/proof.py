from flask import Flask, abort, request
import json

app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/', methods = ['GET'])
def main():
    return str(request.remote_addr)



if __name__ == '__main__':
    app.run()