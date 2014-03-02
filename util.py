import os
from SportsData import *

def getLatestGame(team):
	return ("Red Sox","Cardinals","2013-10-30")
	s = SportsData(os.environ["api_key"])
	r = s.getLeagueSchedule(2013)
	r = r["calendars"]["event"]
	games = {}
	for game in r:
		games[game["scheduled_start"]] = game["@id"]

	for gameDate in sorted(games.keys(), reverse=True):
		gameId = games[gameDate]
		event = s.getEventStats(gameId)
		awayTeam = event["statistics"]["visitor"]["@name"]
		homeTeam = event["statistics"]["home"]["@name"]

		if homeTeam == team or awayTeam == team:
			return (homeTeam, awayTeam, gameDate)
	
