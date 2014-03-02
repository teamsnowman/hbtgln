from flask import Flask, request, jsonify, render_template
import random
import datetime
from SportsData import *
from FanGraphs import *
import os
import collections
import math
from util import *
from tip_templates import *
import re

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/display-tips", methods=["POST"])
def tips():
	if request.method == 'POST':	
		homeTeam, awayTeam, date = getLatestGame(request.form['team'])
	else:
		homeTeam, awayTeam, date = getLatestGame("Red Sox")

	print "GOT IT"
	f = FanGraphs(os.environ["kimono_api_key"])

	data = f.getData(date.split("T")[0], homeTeam, 2013)
	print "GOT IT"
	data = data["results"]["collection1"]

	sortedData = sorted(data, key=lambda k: math.fabs(float(k['wpa'])))

	topPlays = sortedData[-5:]
	tips = []
	for play in topPlays:
		tip = ""
		if float(play['wpa']) > 0: 
			tip = random.choice(team_templates).format(pos_team = homeTeam, neg_team = awayTeam, inning = play['inning'])
		else:
			tip = random.choice(team_templates).format(pos_team = homeTeam, neg_team = awayTeam, inning = play['inning'])

		formattedPlay = play['play'].rstrip(".")
		
		#remove parenthesis 
		#(from http://stackoverflow.com/questions/8713118/remove-content-inside-parenthesis-as-well-as-the-parenthesis-themselves-from-a-p)
		# regEx = re.compile(r'([^\(]*)\([^\)]*\) *(.*)')
		# m = regEx.match(formattedPlay)
		# while m:
		# 	text = m.group(1) + m.group(2)
		# 	m = regEx.match(formattedPlay)

		tip += ": "+play['play'].rstrip(".")
		tips.append(tip)
		#tips.append(cosa['wpa'] + ":" + cosa['play'].rstrip(".") + " in " + cosa['inning'] +)

	return render_template('displaytips.html', 
		homeTeam = homeTeam,
		awayTeam = awayTeam,
		homeAbbrev = abbrevDict[homeTeam],
		awayAbbrev = abbrevDict[awayTeam],
		date = date,
		tips = tips,
		homeTeamScore=range(9),
		awayTeamScore=range(9),)

if __name__ == '__main__':
	app.debug = True
	app.run(threaded = True)
