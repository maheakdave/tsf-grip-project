from flask import Flask, redirect, url_for, render_template, request
import psycopg2 as psy
import os
# flask app instance
app = Flask(__name__)

#Connect to cloud db
def get_db_connection():
 try:
        conn = psy.connect(os.environ.get('DBURL'))
 except Exception as e:
        print("Exception while connecting to RenderDB")
        print(e)
        exit(1)

 print(">>>> Successfully connected to RenderDB!")
 return conn

#home page
@app.route('/')
def home():  
 return render_template("index.html")

#transaction page
@app.route('/view and transact', methods = ['GET','POST'])
def transact():
 ac = 0
 conn = get_db_connection()
 cur = conn.cursor()
 cur.execute('SELECT * FROM passbook;')
 d_table = cur.fetchall()
 print(d_table[0][0])
 if request.method == 'POST':
   user = request.form['user']
   if user == '':
     return redirect('/view and transact')
   try:
    amount = int(request.form['amount'])
    s_q = """SELECT BALANCE FROM passbook WHERE NAME LIKE %s"""
    s_u = """UPDATE passbook SET BALANCE = %s WHERE NAME LIKE %s"""
    cur.execute(s_q, (user,))
    user_b = cur.fetchall()
    check, = user_b[0]
    ac = amount + check
    cur.execute(s_u, (ac,user))
    cur.execute('SELECT * FROM passbook;')
    d_table = cur.fetchall()
    return render_template("transaction_page_update.html",d_table = d_table,user = user,amount = amount)
   except:
     return redirect('/view and transact')
 cur.close()
 conn.close()
 return render_template("transaction_page.html",d_table = d_table)

# run app
if __name__ == '__main__':
 app.run(host = '0.0.0.0',debug = True)
