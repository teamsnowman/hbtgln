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
		awayTeam = event["statistics"]["visitor"]["@name"]
		homeTeam = event["statistics"]["home"]["@name"]

		if homeTeam == team or awayTeam == team:
			return (homeTeam, awayTeam, gameDate)