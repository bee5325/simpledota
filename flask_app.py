from flask import Flask, render_template, redirect, request, url_for
from os import environ
#from flask_sqlalchemy import SQLAlchemy
from leaderboard import *
from compare import *
from suggest import *

app = Flask(__name__)
app.config["DEBUG"] = True

Simpledota.Initialise()

'''
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="bee5325",
    password="i am learning web api",
    hostname="bee5325.mysql.pythonanywhere-services.com",
    databasename="bee5325$comments"
    )
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
'''

@app.route('/leaderboard')
def leaderboard():
    playerlist = getPlayerlist()
    days = getTimeRange()
    result = Leaderboard.leaderboard(playerlist, days)
    return "LEADER : " + str(result)

@app.route('/compare')
def compare():
    playerlist = getPlayerlist()
    attribute = request.args.get("attr")
    result = Compare.compare(playerlist, attribute)
    return "COMPARE : " + str(result)

@app.route('/suggest')
def suggest():
    playerlist = getPlayerlist()
    result = Suggest.suggest(playerlist)
    return "SUGGEST : " + str(result)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return "This is the home page"
        #match = api.get_match_details(match_id=1000193456)
        #return str(match['radiant_win'])
        #return render_template("main_page.html", comments=Comment.query.all())

    #comment = Comment(content=request.form["contents"])
    #db.session.add(comment)
    #db.session.commit()
    return redirect(url_for('index'))

def getPlayerlist():
    playerlist = [int(value) for value in request.args.getlist("player")]
    return playerlist

def getTimeRange():
    if not request.args.get("time"):
        days = 7 # default to 7 days
    if len(request.args.getlist("time")) > 1:
        raise Exception("More than one time range has been specified. Please don't specify more than one time range.")
    elif request.args.get("time") == "today":
        days = 1
    elif request.args.get("time") == "this_week":
        days = 7
    elif request.args.get("time") == "this_month":
        days = 30
    return days

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
