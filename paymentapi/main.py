from flask import Flask, jsonify, request, json
from database import db_session, init_db, engine
from models import BankAccount, Payment, accounts, payments

app = Flask(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/setup")
def setup():
    init_db()
    con = engine.connect()
    con.execute(accounts.delete())
    con.execute(payments.delete())


@app.route("/account", methods=["POST"])
def create_account():
    userid = request.values["userid"]
    sortcode = request.values["sortcode"]
    number = request.values["accountnumber"]
    acct = BankAccount(user=userid, sortcode=sortcode, number=number)
    db_session.add(acct)
    db_session.commit()
    return jsonify(created='ok',sortcode=acct.sortcode, number=acct.number, user=acct.user, id=acct.id)

@app.route("/account/<userid>")
def get_account(userid):
    #u = accounts.select(BankAccount.user == userid).execute().first()
    u = BankAccount.query.filter(BankAccount.user == userid).first()
    if u:
        return jsonify(sortcode=u.sortcode, number=u.number, id=u.id)
    else:
        r = jsonify(statuscode=404, reason='No such user')
        r.status_code=404
        return r

@app.route("/account/<userid>", methods=["POST"])
def update_account(userid):
    u = BankAccount.query.filter(BankAccount.user == userid).first()
    if u:
        u.sortcode = request.values["sortcode"]
        u.number = request.values["accountnumber"]
        db_session.commit()
        return jsonify(updated='ok', sortcode=u.sortcode, number=u.number, id=u.id)
    else:
        r = jsonify(statuscode=404, reason='No such user')
        r.status_code=404
        return r

@app.route("/payment", methods=["POST"])
def create_payment():
    userid = request.values["userid"]
    amount = request.values["amount"]
    account = BankAccount.query.filter(BankAccount.user==userid).one()
    payment = Payment(account=account.id, amount=amount)
    db_session.add(payment)
    db_session.commit()
    return jsonify(sortcode=account.sortcode, number=account.number, id=payment.id, amount=amount)

@app.route("/payments")
def list_payments():
    payments = [
        {'account':p.account, 'amount':p.amount, 'account_number':a.number, 'account_sortcode':a.sortcode}
        for p,a in db_session().query(Payment, BankAccount).filter(Payment.account == BankAccount.id).all()]
    return jsonify(payments=payments)


if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=8080, debug=True)
