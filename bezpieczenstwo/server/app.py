from flask import Flask
from flask import request
app = Flask(__name__)
import _mysql

@app.route('/', methods=['POST'])
def hello_world():
	print(request.method)
	return 'Hello, World!'

@app.route('/post_test', methods=['POST'])
def post_test():
	print("---LOG---")
	#print(request)
	if(request.method == "GET"):
		print("get")
		
	else:
		print(request.form["test"])
		#print("post")
	return 'test'
	
@app.route('/user/<username>/<password>', methods=['GET', 'POST'])
def user(username, password):
	f = open("password.txt", "w")
	f.write(username+"\n"+password) 
	return "pwr"


if __name__ == "__main__":
	db=_mysql.connect(host="localhost",user='root',port=3306,db="bezpieczenstwo")
	app.run(port=1234)
