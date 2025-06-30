import sqlite3
import time

conobj=sqlite3.connect(database='bank.sqlite')
curobj=conobj.cursor()

table_accounts='''create table if not exists accounts(
accounts_acno integer primary key autoincrement,
accounts_name text,
accounts_pass text,
accounts_email text,
accounts_mob text,
accounts_sex text,
accounts_opendate text,
accounts_bal float,
accounts_address text,
accounts_pan text,
accounts_passport text)'''

table_statements='''create table if not exists statements(
statements_txnid integer primary key,
statements_date text,
statements_acno integer,
statements_amt float,
statements_amt_type text,
statements_pbal float,
statements_upbal float,
statements_transfer text,
foreign key(statements_acno) references accounts(accounts_acno)
)'''

try:
    conobj.execute("PRAGMA foreign_keys = ON")
    curobj.execute(table_accounts)
    curobj.execute(table_statements)
except Exception as e:
    print(e)
conobj.close()

class Accounts():
    def __init__(self,acno,name,passw,email,mob,sex,opendate,bal,address,pan,passport):
        self.uacno=acno
        self.uname=name
        self.upass=passw
        self.uemail=email
        self.umob=mob
        self.usex=sex
        self.uacnopendate=opendate
        self.ubal=bal
        self.uadd=address
        self.upan=pan
        self.upassport=passport
    
    def update_att(self,acno,email,mob,address,pan,passport):
        conobj=sqlite3.connect(database='bank.sqlite')
        conobj.execute("PRAGMA foreign_keys = ON")
        curobj=conobj.cursor()
        query='update accounts set accounts_email=?,accounts_mob=?,accounts_address=?,accounts_pan=?,accounts_passport=? where accounts_acno=?'
        curobj.execute(query,(email,mob,address,pan,passport,acno))
        conobj.commit()
        curobj.execute('select * from accounts where accounts_acno=?',(acno,))
        tup_updated_udata=curobj.fetchone()
        conobj.close()

        self.uemail=tup_updated_udata[3]
        self.umob=tup_updated_udata[4]
        self.uadd=tup_updated_udata[8]
        self.upan=tup_updated_udata[9]
        self.upassport=tup_updated_udata[10]

    def update_pass(self,passw,acno):
        conobj=sqlite3.connect(database='bank.sqlite')
        conobj.execute("PRAGMA foreign_keys = ON")
        curobj=conobj.cursor()
        query='update accounts set accounts_pass=? where accounts_acno=?'
        curobj.execute(query,(passw,acno))
        conobj.commit()
        conobj.close()

        self.upass=passw

    def deposit(self,dep_amt,acno):
        conobj=sqlite3.connect(database='bank.sqlite')
        conobj.execute("PRAGMA foreign_keys = ON")
        curobj=conobj.cursor()
        query='update accounts set accounts_bal=accounts_bal+? where accounts_acno=?'
        curobj.execute(query,(dep_amt,acno))
        conobj.commit()
        curobj.execute('select accounts_bal from accounts where accounts_acno=?',(acno,))
        row=curobj.fetchone()
        conobj.close()

        self.ubal=row[0]
    
    def withdraw(self,wd_amt,acno):
        conobj=sqlite3.connect(database='bank.sqlite')
        conobj.execute("PRAGMA foreign_keys = ON")
        curobj=conobj.cursor()
        query='update accounts set accounts_bal=accounts_bal-? where accounts_acno=?'
        curobj.execute(query,(wd_amt,acno))
        conobj.commit()
        curobj.execute('select accounts_bal from accounts where accounts_acno=?',(acno,))
        row=curobj.fetchone()
        conobj.close()

        self.ubal=row[0]

    def transfer(self,amt,acno,to_acno):
        conobj=sqlite3.connect(database='bank.sqlite')
        conobj.execute("PRAGMA foreign_keys = ON")
        curobj=conobj.cursor()
        query='update accounts set accounts_bal=accounts_bal-? where accounts_acno=?'
        curobj.execute(query,(amt,acno))
        curobj.execute('select accounts_bal from accounts where accounts_acno=?',(acno,))
        row=curobj.fetchone()
        curobj.execute('select accounts_bal from accounts where accounts_acno=?',(to_acno,))
        to_acn_pbal=curobj.fetchone()[0]
        query='update accounts set accounts_bal=accounts_bal+? where accounts_acno=?'
        curobj.execute(query,(amt,to_acno))
        curobj.execute('select accounts_bal from accounts where accounts_acno=?',(to_acno,))
        to_acn_upbal=curobj.fetchone()[0]
        conobj.commit()
        conobj.close()

        self.ubal=row[0]
        return to_acn_pbal,to_acn_upbal
    
    def acnos(self):
        conobj=sqlite3.connect('bank.sqlite')
        conobj.execute("PRAGMA foreign_keys = ON")
        curobj=conobj.cursor()
        curobj.execute('select accounts_acno from accounts')
        tup_acnos=curobj.fetchall()
        conobj.close()
        if tup_acnos:
            acnos_li=list(tup[0] for tup in tup_acnos)
            return acnos_li

def udetails(uacno,upass):
    conobj=sqlite3.connect('bank.sqlite')
    conobj.execute("PRAGMA foreign_keys = ON")
    curobj=conobj.cursor()
    curobj.execute('select * from accounts where accounts_acno=? and accounts_pass=?',(uacno,upass))
    tup_udetails=curobj.fetchone()
    conobj.close()
    if tup_udetails:
        return Accounts(*tup_udetails)
    else:
        return None

def stmts(amt_type,acno,amt,pbal,upbal,transfer=None):
    txn_id=int(time.time()*1000)
    conobj=sqlite3.connect(database='bank.sqlite')
    conobj.execute("PRAGMA foreign_keys = ON")
    curobj=conobj.cursor()
    query='insert into statements values(?,?,?,?,?,?,?,?)'
    if amt_type=='credit':
        at='CR'
    else:
        at='DR'
    curobj.execute(query,(txn_id,time.strftime('%d-%m-%Y, %r'),acno,amt,at,pbal,upbal,transfer))
    conobj.commit()
    conobj.close()

def ustmts(acno):
    conobj=sqlite3.connect('bank.sqlite')
    conobj.execute("PRAGMA foreign_keys = ON")
    curobj=conobj.cursor()
    query='''SELECT statements_txnid,statements_date,statements_amt,
statements_amt_type,statements_pbal,statements_upbal,statements_transfer
from statements where statements_acno=? order by statements_txnid desc'''
    curobj.execute(query,(acno,))
    rows=curobj.fetchall()
    conobj.close()

    return rows