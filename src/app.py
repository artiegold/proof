from flask import Flask, abort, request, render_template
import json

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'

@app.route('/', methods=['GET'])
def main():
    return render_template('template.html', basename="shrug.jpg")

@app.route('/testip/<ip_address>', methods=['GET'])
def test_ip(ip_address):
    basename = ip_address
    return render_template('template.html', basename=basename)

if __name__ == '__main__':
    app.run()
