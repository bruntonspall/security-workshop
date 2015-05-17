from flask import Flask, render_template, json, jsonify, request, abort
from database import db_session, engine, init_db
from models import User, users
import hashlib

app = Flask(__name__)
SECRET_KEY="123456"

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/setup")
def setup():
    init_db()
    con = engine.connect()
    con.execute(users.insert(), name='admin', email='admin@localhost', password='123456')
    con.execute(users.insert(), name='anna', email='anna@localhost', password='12345678')
    return "ok"

@app.route("/user/<user>")
def index(user):
    u = engine.execute("select * from users where id = '%s'" % (user)).first()
    #u = User.query.filter(User.name == 'admin').first()
    return jsonify(name=u.name, email=u.email, id=u.id)

@app.route("/auth", methods=["POST"])
def auth():
    username = request.values["username"]
    password = request.values["password"]
    rows = engine.execute("select id from users where name = '%s' and password = '%s'" % (username, password)).fetchall()
    if len(rows) == 1:
        return jsonify({'status':'ok'})
    else:
        response = jsonify({'code': 404,'message': 'Username or password is incorrect'})
        response.status_code = 404
        return response

@app.route("/auth2", methods=["POST"])
def auth2():
    username = request.values["username"]
    password = request.values["password"]
    rows = engine.execute("select id from users where name = '%s' and password = '%s'" % (username, password)).fetchall()
    if len(rows) == 1:
        return jsonify(token=hashlib.sha256(SECRET_KEY+str(rows[0][0])).hexdigest())
    else:
        response = jsonify({'code': 404,'message': 'Username or password is incorrect'})
        response.status_code = 404
        return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
