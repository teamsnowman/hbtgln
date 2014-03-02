from flask import Flask, request, jsonify, render_template
import random
import datetime
from SportsData import *
from FanGraphs import *
import os
import collections
import math
from util import *

app = Flask(__name__, static_url_path='/static')
@app.route("/")
def index():
	return app.send_static_file('templates/index.html')

@app.route("/display-tips")
def tips():
	homeTeam, awayTeam, date = getLatestGame("Red Sox")
	print homeTeam
	f = FanGraphs(os.environ["kimono_api_key"])

	data = f.getData(date.split("T")[0], homeTeam, 2013)
	data = data["results"]["collection1"]

	sortedData = sorted(data, key=lambda k: math.fabs(float(k['wpa'])))

	topPlays = sortedData[-5:]
	tips = []
	for cosa in topPlays:
		tips.append(cosa['wpa'] + ":" + cosa['play'].rstrip(".") + " in " + cosa['inning'] + "<br>")
	
	return render_template('displaytips.html', 
		homeTeam = homeTeam,
		awayTeam = awayTeam,
		date = date,
		tips = tips,
		homeTeamScore=range(9),
		awayTeamScore=range(9),)

if __name__ == '__main__':
	app.debug = True
	app.run(threaded = True)




