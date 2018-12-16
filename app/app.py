from flask import Flask, abort, request, render_template
import json
import db_interface
import move_rules
import get_image
import model
import config

db = db_interface.db_interface(config.get_dsn(config.CONFIG))
im  = get_image.get_image(db.get_rules(), db.get_campaigns())
mover = move_rules.move_rules(db, im)

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
    return render_template('picture.html', basename=basename)

@app.route('/testip/<ip_address>', methods=['GET'])
def test_ip(ip_address):
    basename = get_basename(ip_address)
    return render_template('picture.html', basename=basename)

@app.route('/rules', methods=['GET'])
def show_rules():
    rules = db.get_rules()
    return render_template(
        'table.html', 
        title="Rules",
        headers=('Rule ID', 'Type', 'Target', 'Campaign ID'),
        rows=((rule.id, rule.field, rule.target, rule.campaign_id) for rule in rules)
    )

@app.route('/rule/move/<rule_id>/after/<target>', methods=['GET', 'PUT'])
def move_rule_after(rule_id, target):
    mover.move_rule_after(rule_id, target)
    rules = db.get_rules()
    return render_template(
        'table.html', 
        title="Rules",
        headers=('Rule ID', 'Type', 'Target', 'Campaign ID'),
        rows=((rule.id, rule.field, rule.target, rule.campaign_id) for rule in rules)
    )
    

@app.route('/rule/move/<rule_id>/before/<target>', methods=['GET', 'PUT'])
def move_rule_before(rule_id, target):
    mover.move_rule_before(rule_id, target)
    rules = db.get_rules()
    return render_template(
        'table.html', 
        title="Rules",
        headers=('Rule ID', 'Type', 'Target', 'Campaign ID'),
        rows=((rule.id, rule.field, rule.target, rule.campaign_id) for rule in rules)
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"))
