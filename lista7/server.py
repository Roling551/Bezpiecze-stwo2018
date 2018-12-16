from flask import Flask, session, render_template, request, redirect, g, url_for
from itsdangerous import URLSafeTimedSerializer
import MySQLdb
import os

import string
import random
import smtplib

app = Flask(__name__)
app.secret_key = os.urandom(24)
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

def send_mail(msg, receiver):
	print(msg)
	#server = smtplib.SMTP('smtp.gmail.com', 25)
	#server.set_debuglevel(1)
	#server.ehlo()
	#server.starttls()
	#server.ehlo()
	#server.connect('smtp.gmail.com', 587)
	#server.login("roling95@gmail.com", "password")
	#server.sendmail("roling95@gmail.com", receiver, msg)
	#server.close()

def id_generator(size=20, chars=string.ascii_letters	 + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

@app.route('/', methods=["GET", "POST"])
def index():
	#token = ts.dumps('email', salt='email-confirm-key')
	#confirm_url = url_for('confirm_email',email='email',token=token,_external=True)
	return '<script>alert("test")</script>'

@app.route('/log_in', methods=["GET", "POST"])
def log_in():
	if request.method == 'POST':
		c1 = db.cursor()
		c1.execute("""SELECT password = PASSWORD(%s) FROM users WHERE login = %s""",[request.form['password'],request.form['login']])
		if c1.fetchone()[0]==1:
			session['user'] = request.form['login']
			return redirect(url_for('get_session'))
	return render_template('log_in.html')
	
@app.route('/create_account', methods=["GET", "POST"])
def create_account():
	if request.method == 'POST':
		c1 = db.cursor()
		c1.execute("""SELECT * FROM users WHERE login = %s""",[request.form['login']])
		if c1.fetchone():
			return render_template('create_account.html',error="login already taken")
		c2 = db.cursor()
		c2.execute("""SELECT * FROM users WHERE email = %s""",[request.form['email']])
		if c2.fetchone():
			return render_template('create_account.html',error="email already taken")
		random_salt = id_generator()
		token = ts.dumps(request.form['email'], salt=random_salt)
		confirm_url = url_for('confirm_email',email=request.form['email'],token=token,_external=True)
		print(confirm_url)
		c=db.cursor()
		c.execute("""INSERT INTO users(login, email, password,confirmed_salt,confirmed_sent) VALUES (%s,%s,PASSWORD(%s),%s,FALSE)""",[request.form['login'],request.form['email'],request.form['password'],random_salt])
		db.commit()
		return 'test'
	return render_template('create_account.html')


	
@app.route('/confirm/<token>')
def confirm_email(token):
	#try:
	c1 = db.cursor()
	c1.execute("""SELECT confirmed_salt FROM users WHERE email = %s""",[request.args.get('email')])
	random_salt=c1.fetchone()[0]
	email = ts.loads(token, salt=random_salt, max_age=86400)
	if email == request.args.get('email'):
		c2 = db.cursor()
		c2.execute("""UPDATE users SET confirmed=TRUE WHERE email=%s""",[email])
		db.commit()
	return email
@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']
	
@app.route('/get_session')
def get_session():
    if 'user' in session:
        return session['user']

    return 'Not logged in!'

@app.route('/make_transfer', methods=["GET", "POST"])
def make_transfer():
	if not('user' in session):
		return redirect(url_for('log_in'))
	if request.method == 'POST':
		c1 = db.cursor()
		c1.execute("""SELECT id FROM users WHERE login=%s""",[session['user']])
		sender_id = c1.fetchone()[0]
		c2 = db.cursor()
		c2.execute("""SELECT id FROM users WHERE login=%s""",[request.form['receiver']])
		receiver_id = c2.fetchone()[0]
		c3 = db.cursor()
		c3.execute("""INSERT INTO transfers(title, amount, sender, receiver) VALUES (%s,%s,%s,%s)""",[request.form['title'],request.form['amount'],sender_id,receiver_id])
		db.commit()
		return str(receiver_id)
	return render_template('make_transfer.html')

@app.route('/view_transfer', methods=["GET", "POST"])
def view_transfer():
	if not('user' in session):
		return redirect(url_for('log_in'))
	if request.method == 'POST':
		return request.args.get('title')
		
	c1 = db.cursor()
	c1.execute("""SELECT id FROM users WHERE login=%s""",[session['user']])
	user_id = c1.fetchone()[0]
	c2 = db.cursor()
	c2.execute("""SELECT isAdmin FROM users WHERE login=%s""",[session['user']])
	isAdmin_= c2.fetchone()[0]
	title_ = request.args.get('title')


	c3 = db.cursor()
	c3.execute("""SELECT transfers.title, sender.login, receiver.login, transfers.amount, transfers.description, transfers.confirmed, transfers.realised FROM transfers INNER JOIN users AS sender ON transfers.sender = sender.id INNER JOIN users AS receiver ON transfers.receiver = receiver.id WHERE (sender.id = %s OR receiver.id = %s) AND transfers.title = %s""",[user_id,user_id,title_])
	return render_template('view_transfer.html',data = c3.fetchone(),isAdmin = isAdmin_, curUser = session['user'])

@app.route('/view_transfer_b', methods=["GET", "POST"])
def view_transfer_b():
	if not('user' in session):
		return redirect(url_for('log_in'))
	if request.method == 'POST':
		return request.args.get('title')
		
	c1 = db.cursor()
	c1.execute("""SELECT id FROM users WHERE login=%s""",[session['user']])
	user_id = c1.fetchone()[0]
	c2 = db.cursor()
	c2.execute("""SELECT isAdmin FROM users WHERE login=%s""",[session['user']])
	isAdmin_= c2.fetchone()[0]
	title_ = request.args.get('title')


	c3 = db.cursor()
	query_ = """SELECT transfers.title, sender.login, receiver.login, transfers.amount, transfers.description, transfers.confirmed, transfers.realised FROM transfers INNER JOIN users AS sender ON transfers.sender = sender.id INNER JOIN users AS receiver ON transfers.receiver = receiver.id WHERE (sender.id = %s OR receiver.id = %s) AND transfers.title = '"""+title_+"""'"""
	print(query_)
	c3.execute(query_,[[user_id,user_id]])
	db.commit()
	return render_template('view_transfer.html',data = c3.fetchone(),isAdmin = isAdmin_, curUser = session['user'])
@app.route('/execute_many_example', methods=["GET", "POST"])
def execute_many_example():
	c1 = db.cursor()
	c1.execute("""INSERT INTO users(login, password, email) VALUES ("user2","pass","mail2@gmail.com");; INSERT INTO users(login, password, email) VALUES ("user3","pass","mail3@gmail.com");""",[])
	c1.fetchall()
	db.commit()
	return "test2"
	
@app.route('/confirm_transfer', methods=["POST"])
def confirm_transfer():
	if not('user' in session):
		return redirect(url_for('log_in'))
	c1 = db.cursor()
	c1.execute("""SELECT id FROM users WHERE login=%s""",[session['user']])
	user_id = c1.fetchone()[0]
	c2 = db.cursor()
	title_ = request.args.get('title')
	c2.execute("""SELECT sender FROM transfers WHERE title=%s""",[title_])
	sender_id = c2.fetchone()[0]
	if user_id != sender_id:
		return "Wrong user"
	c3 = db.cursor()
	c3.execute("""UPDATE transfers SET confirmed = true WHERE title = %s""",[title_])
	db.commit()
	return "Confirmed"
	
@app.route('/realise_transfer', methods=["GET", "POST"])
def realise_transfer():
	if not('user' in session):
		return redirect(url_for('log_in'))
	c4 = db.cursor()
	c4.execute("""SELECT isAdmin FROM users WHERE login=%s""",[session['user']])
	isAdmin_= c4.fetchone()[0]
	if isAdmin_ != 1:
		return "User is not admin"
	title_ = request.args.get('title')
	c3 = db.cursor()
	c3.execute("""UPDATE transfers SET realised = true WHERE title = %s""",[title_])
	db.commit()
	return "Realised"
	
@app.route('/transfers_list', methods=["GET", "POST"])
def transfers_list():
	if not('user' in session):
		return redirect(url_for('log_in'))
	c1 = db.cursor()
	c1.execute("""SELECT id FROM users WHERE login=%s""",[session['user']])
	user_id = c1.fetchone()[0]
	c2 = db.cursor()
	c2.execute("""SELECT transfers.title, sender.login, receiver.login, transfers.amount, transfers.description FROM transfers INNER JOIN users AS sender ON transfers.sender = sender.id INNER JOIN users AS receiver ON transfers.receiver = receiver.id WHERE sender.id = %s OR receiver.id = %s""",[user_id,user_id])
	return render_template('transfers_list.html',data = c2.fetchall())


@app.route('/transfers_list_b', methods=["GET", "POST"])
def transfers_list_b():
	if not('user' in session):
		return redirect(url_for('log_in'))
	c1 = db.cursor()
	c1.execute("""SELECT id FROM users WHERE login=%s""",[session['user']])
	user_id = c1.fetchone()[0]
	c2 = db.cursor()
	c2.execute("""SELECT transfers.title, sender.login, receiver.login, transfers.amount, transfers.description FROM transfers INNER JOIN users AS sender ON transfers.sender = sender.id INNER JOIN users AS receiver ON transfers.receiver = receiver.id WHERE sender.id = %s OR receiver.id = %s""",[user_id,user_id])
	transfers = c2.fetchall()
	table = "<table>"
	table = table + "<tr>"
	table = table + "<th>Firstname</th>"
	table = table + "<th>Lastname</th>"
	table = table + "<th>Age</th>"
	table = table + "</tr>"
	for transfer in transfers:
	
		table = table + "<tr>"
		for column in transfer:
		
			table = table + "<td>"
			table = table + str(column)
			table = table + "</td>"
		
		table = table + "</tr>"
	
	table = table + "</table>"
	return table
	
@app.route('/post_test', methods=["GET", "POST"])
def post_test():
	if request.method == 'POST':
		return request.form['key']
	else:
		return "get"

@app.route('/list_test')
def list_test():
	data = [1,2,3]
	return render_template('list_test.html',data = data)

@app.route('/redirect_test', methods=["GET", "POST"])
def redirect_test():
	return redirect(url_for('log_in'))
	
@app.route('/js_test', methods=["GET", "POST"])
def js_test():
	return render_template('js_test.html')
	
if __name__ == "__main__":
	db=MySQLdb.connect(host="localhost",user='root',port=3306,db="bezpieczenstwo")
	app.run(port=1234)