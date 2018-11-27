from flask import Flask, abort, request, render_template
import json

app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/', methods = ['GET'])
def main():
    return render_template('template.html', basename="shrug.jpg")

if __name__ == '__main__':
    app.run()