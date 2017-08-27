from flask import Flask, request, url_for
from os import environ
import calendar
import datetime

from leaderboard import *
from compare import *
from suggest import *
from heroes import *

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/leaderboard')
def leaderboard():
    try:
        playerlist = getPlayerlist()
    except ValueError:
        return "Error : Invalid player given, please provide Steam32 account id"
    days = getTimeRange()
    result = Leaderboard.leaderboard(playerlist, days)
    return str(result)

@app.route('/compare')
def compare():
    try:
        playerlist = getPlayerlist()
    except ValueError:
        return "Error : Invalid player given, please provide Steam32 account id"
    attribute = request.args.get("attr")
    result = Compare.compare(playerlist, attribute)
    return str(result)

@app.route('/suggest')
def suggest():
    try:
        playerlist = getPlayerlist()
    except ValueError:
        return "Error : Invalid player given, please provide Steam32 account id"
    result = Suggest.suggest(playerlist)
    return str(result)

@app.route('/heroes')
def heroes():
    Heroes.initialise()
    return str(Heroes.heroes)

@app.route('/', methods=["GET", "POST"])
def index():
    displayText = "\n".join([
    "To get the leaderbaord, use url {leaderboard};".format(leaderboard=url_for('leaderboard', _external=True)),
    "To compare players, use url {compare};".format(compare=url_for('compare', _external=True)),
    "To suggest hero for a player, use url {suggest}".format(suggest=url_for('suggest', _external=True))
    ])
    return displayText

def getPlayerlist():
    try:
        playerlist = [int(value) for value in request.args.getlist("player")]
    except ValueError:
        raise
    return playerlist

def getTimeRange():
    days = 7 # default to 7 days
    if len(request.args.getlist("time")) > 1:
        raise Exception("More than one time range has been specified. Please don't specify more than one time range.")
    elif request.args.get("time") == "last_day":
        days = 1
    elif request.args.get("time") == "last_week":
        days = 7
    elif request.args.get("time") == "last_month":
        days = getDaysInLastMonth()
    elif request.args.get("time") == "last_year":
        days = 366 if calendar.isleap(datetime.today().year - 1) else 365
    return days

def getDaysInLastMonth():
    daysInLastMonth = [None, 31, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30]
    today = datetime.today()
    if calendar.isleap(today.year):
        daysInLastMonth[3] += 1
    return daysInLastMonth[today.month]

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
