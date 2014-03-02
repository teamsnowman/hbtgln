import urllib
import urllib2
import json
import xmltodict

class SportsData:
	def __init__(self, apiKey):
		self.apiKey = apiKey
		self.ROOT_URL = "http://api.sportsdatallc.org/mlb-t4/"

	def _request(self, url, data):
		encodedData = urllib.urlencode({
			'api_key': self.apiKey,})
		url = url + data + ".xml"
		request = urllib2.Request(
			"%s?%s" % (url, encodedData),
			headers = {},
		)

		response = urllib2.urlopen(request).read()
		rv =  xmltodict.parse(response.decode("UTF-8-sig"))

		return rv

	def getLeagueSchedule(self, year):
		return self._request(self.ROOT_URL+"schedule/", str(year))

	def getEventStats(self, eventId):
		return self._request(self.ROOT_URL+"statistics/", eventId)

	def getPlayerStatistics(self, year):
		return self._request(self.ROOT_URL+"seasontd/players/", str(year))

