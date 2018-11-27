from flask import Flask, abort, request, render_template
import json
import db_interface
import get_image

db = db_interface.db_interface('')
im = get_image.get_image(db.get_rules(), db.get_campaigns())

def get_basename(ip_address):
    user = db.get_user(ip_address)
    return im.get_image_basename(user)

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'

@app.route('/', methods=['GET'])
def main():
    ip_address = request.remote_addr
    basename = get_basename(ip_address)
    return render_template('template.html', basename=basename)

@app.route('/testip/<ip_address>', methods=['GET'])
def test_ip(ip_address):
    basename = get_basename(ip_address)
    return render_template('template.html', basename=basename)

if __name__ == '__main__':
    app.run()
