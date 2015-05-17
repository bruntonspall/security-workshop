from sqlalchemy import Table, Column, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import mapper
from database import metadata, db_session

class BankAccount(object):
    query = db_session.query_property()

    def __init__(self, id=None, user=None, sortcode=None, number=None):
        self.id = id
        self.user = user
        self.sortcode = sortcode
        self.number = number

    def __repr__(self):
        return '<Acct %s %s>' % (self.sortcode, self.number)

accounts = Table('account', metadata,
    Column('id', Integer, primary_key=True),
    Column('user', String(128)),
    Column('sortcode', String(6)),
    Column('number', String(8)),
    UniqueConstraint('sortcode', 'number', name='sortcode_acct')
)
mapper(BankAccount, accounts)

class Payment(object):
    query = db_session.query_property()

    def __init__(self, id=None, account=None, amount=None):
        self.id = id
        self.account = account
        self.amount = amount

    def __repr__(self):
        return '<Payment %r to %r>' % (self.amount, self.account)

payments = Table('payment', metadata,
    Column('id', Integer, primary_key=True),
    Column('account', ForeignKey('account.id')),
    Column('amount', Integer)
    )
mapper(Payment, payments)
