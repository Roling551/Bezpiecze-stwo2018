from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/user/<username>/<password>')
def user(username, password):
	f = open("password.txt", "w")
	f.write(username+"\n"+password) 
	return "pwr"


if __name__ == "__main__":
	app.run(port=80, ssl_context=('certA.crt', 'privkeyA.pem'))
