from flask import Flask, render_template, redirect, request, url_for
import requests
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        r = requests.get("https://api.opendota.com/api/players/70388657/matches")
        print(r.status_code)
        return str(r.json())
    

if __name__ == "__main__":
	app.run()