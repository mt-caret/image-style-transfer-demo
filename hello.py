from flask import Flask
app = Flask(__name__)

@app.route("/echo")
def hello():
	return "Hello, World!"
