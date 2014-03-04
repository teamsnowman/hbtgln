import os
from SportsData import *

def getLatestGame(team):
	s = SportsData(os.environ["api_key"])
	r = s.getLeagueSchedule(2013)
	r = r["calendars"]["event"]
	games = {}
	for game in r:
		games[game["scheduled_start"]] = game["@id"]

	for gameDate in sorted(games.keys(), reverse=True):
		gameId = games[gameDate]
		event = s.getEventStats(gameId)
		boxScore = s.getBoxScore(gameId)
		scores=[range(int(boxScore["boxscore"]["final"]["@inning"])),range(int(boxScore["boxscore"]["final"]["@inning"]))]
		boxScore = boxScore["boxscore"]["visitor"]
		awayTeam = event["statistics"]["visitor"]["@name"]
		homeTeam = event["statistics"]["home"]["@name"]
		if homeTeam == team or awayTeam == team:
			print "Home Team: ",homeTeam, "Away Team ", awayTeam
			return (homeTeam, awayTeam, gameDate, boxScore)

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
