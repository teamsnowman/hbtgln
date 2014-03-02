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
	return app.send_static_file('templates/index.html')

@app.route("/display-tips")
def tips():
	homeTeam, awayTeam, date = getLatestGame("Red Sox")

	f = FanGraphs(os.environ["kimono_api_key"])

	data = f.getData(date.split("T")[0], homeTeam, 2013)
	data = data["results"]["collection1"]

	sortedData = sorted(data, key=lambda k: math.fabs(float(k['wpa'])))

	topPlays = sortedData[-1:]
	tips = []
	for cosa in topPlays:
		tips.append(cosa['wpa'] + ":" + cosa['play'].rstrip(".") + " in " + cosa['inning'] + "<br>")
	abbrevDict = {
		"Red Sox":"bos",
		"Yankees":"nya",
		"Rays":"tba",
		"Orioles":"bal",
		"Blue Jays":"tor",
		"Tigers":"det",
		"Indians":"cle",
		"Royals":"kca",
		"Twins":"min",
		"White Sox":"cha",
		"Athletics":"oak",
		"Rangers":"tex",
		"Angels":"ana",
		"Mariners":"sea",
		"Astros":"hou",
		"Braves":"atl",
		"Nationals":"was",
		"Phillies":"phi",
		"Mets":"nyn",
		"Marlins":"mia",
		"Pirates":"pit",
		"Cardinals":"sln",
		"Reds":"cin",
		"Cubs":"chn",
		"Brewers":"mil",
		"Dodgers":"lan",
		"Diamondbacks":"ari",
		"Rockies":"col",
		"Giants":"sfn",
		"Padres":"sdn",
	}
	for play in topPlays:
		tip = ""
		if float(play['wpa']) > 0: 
			tip = random.choice(team_templates) % (homeTeam, play['inning'])
		else:
			tip = random.choice(team_templates) % (awayTeam, play['inning'])

		formattedPlay = play['play'].rstrip(".")
		
		#remove parenthesis 
		#(from http://stackoverflow.com/questions/8713118/remove-content-inside-parenthesis-as-well-as-the-parenthesis-themselves-from-a-p)
		regEx = re.compile(r'([^\(]*)\([^\)]*\) *(.*)')
		m = regEx.match(formattedPlay)
		while m:
			text = m.group(1) + m.group(2)
			m = regEx.match(formattedPlay)

		tip += play['play'].rstrip(".")
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




