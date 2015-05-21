from flask import Flask, render_template, json, jsonify, request, abort
from database import db_session, engine, init_db
from sqlalchemy.sql import text
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
    con.execute(users.delete())
    con.execute(users.insert(), name='admin', email='admin@localhost', password='password1')
    con.execute(users.insert(), name='anna', email='anna@localhost', password='letmein1')
    return "ok"

@app.route("/auth", methods=["POST"])
def auth():
    # Lowercase passwords so password check is case insensitive
    username = request.values["username"].lower()
    password = request.values["password"].lower()
    # username = request.values["username"]
    # password = request.values["password"]

    # rows = engine.execute("select id from users where name = '%s' and password = '%s'" % (username, password)).first()
    rows = User.query.filter(User.name == username).filter(User.password == password).first()
    if rows:
        return jsonify(status='ok', username=username)
    else:
        response = jsonify({'code': 404,'message': 'Username or password is incorrect'})
        response.status_code = 404
        return response

# Instead of returning username, return a hashed token.
# The UserAPI is the only part of the system that can turn username into a token, and only will with the password
# So an attacker needs the password to do anything on behalf of the user with other services
# (Or to snoop the token, we could use a nonce, or time based token to counter that if we wanted)

# @app.route("/auth", methods=["POST"])
# def auth():
#     username = request.values["username"]
#     password = request.values["password"]
#     rows = engine.execute("select id from users where name = '%s' and password = '%s'" % (username, password)).fetchall()
#     if len(rows) == 1:
#         return jsonify(status='ok', username=hashlib.sha256(SECRET_KEY+str(rows[0][0])).hexdigest())
#     else:
#         response = jsonify({'code': 404,'message': 'Username or password is incorrect'})
#         response.status_code = 404
#         return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
