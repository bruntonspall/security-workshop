from flask import Flask, render_template, request, session, url_for, redirect, flash
import requests
app = Flask(__name__)
app.secret_key = '12345678'

@app.route("/")
def hello():
    session['username'] = None
    return render_template('index.html')

@app.route("/login", methods=["POST"])
def login():
    username = request.values['username']
    password = request.values['password']
    payload = {'username':username, 'password':password}
    r = requests.post('http://userapi:8080/auth', params=payload)
    if r.status_code == 200:
        session['username'] = r.json()['username']
        return redirect('/claim')
    else:
        flash('Username/Password incorrect')
        return redirect('/')

@app.route("/claim")
def claim():
    username = session['username']
    r = requests.get('http://paymentapi:8080/account/%s' % (username))
    if r.status_code != 200:
        return render_template('claim.html', create=True)
    else:
        details = r.json()
        app.logger.info("details %s" % details)
        return render_template('claim.html', create=False, sortcode=details['sortcode'], account=details['number'])

@app.route("/claim", methods=["POST"])
def make_claim():
    username = session['username']
    requests.post('http://paymentapi:8080/payment', params={'userid':username, 'amount':"100"})
    flash("A payment of $100 has been queued for your account")
    return redirect('/claim')

@app.route("/update", methods=["POST"])
def update():
    username = session['username']
    sortcode = request.values['sortcode']
    account = request.values['account']
    r = requests.get('http://paymentapi:8080/account/%s' % (username))
    if r.status_code != 200:
        r = requests.post('http://paymentapi:8080/account',
            params={'userid':username, 'sortcode':sortcode, 'accountnumber':account})
        return redirect('/claim')
    else:
        details = r.json()
        r = requests.post('http://paymentapi:8080/account/%s' % (username),
            params={'sortcode':sortcode, 'accountnumber':account})
        return redirect('/claim')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
