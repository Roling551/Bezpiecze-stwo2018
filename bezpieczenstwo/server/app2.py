from flask import Flask
from flask import request
app = Flask(__name__)
import _mysql


if __name__ == "__main__":
	db=_mysql.connect(host="localhost",user='root',port=3306,db="bezpieczenstwo")
	print("test")